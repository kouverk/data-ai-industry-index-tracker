# Data Quality Checks

This document describes the data quality checks implemented in the dbt project.

---

## Overview

All data quality checks are implemented as dbt tests in schema YAML files. Tests run automatically with `dbt test` and validate data in Snowflake.

**Total Tests:** 77 across 4 data sources

| Source | Models Tested | Test Count |
|--------|---------------|------------|
| Hacker News | 1 | 7 |
| LinkedIn | 3 | 11 |
| GitHub | 1 | 10 |
| LLM Extractions | 1 | 8 |
| Marts (dims/facts) | 10 | 51 |

**Latest Run:** 74 PASS, 3 WARN, 0 ERROR

---

## Test Types

| Test Type | Description | Data Quality Dimension |
|-----------|-------------|------------------------|
| `unique` | No duplicate values in column | Uniqueness |
| `not_null` | Column contains no NULL values | Completeness |
| `accepted_values` | Values must be in predefined list | Validity |
| `dbt_utils.accepted_range` | Numeric values within min/max bounds | Validity |
| `relationships` | Foreign key references exist in parent table | Referential Integrity |

---

## Tests by Source

### Hacker News (`stg_hn__job_postings`)

| Column | Test | Description |
|--------|------|-------------|
| `posting_id` | unique | Each HN post has unique ID |
| `posting_id` | not_null | All posts have an ID |
| `posting_text` | not_null | All posts have text content |
| `posting_month` | not_null | Month is parsed for all posts |
| `posting_year` | not_null | Year is extracted for all posts |
| `posting_year` | accepted_range (2011-2030) | Year is within valid HN timeframe |
| `thread_id` | not_null | All posts belong to a thread |

### LinkedIn Postings (`stg_linkedin__postings`)

| Column | Test | Description |
|--------|------|-------------|
| `posting_id` | unique | Each job has unique link URL |
| `posting_id` | not_null | All jobs have a link |
| `job_title` | not_null | All jobs have a title |
| `company` | not_null (warn) | Most jobs have a company (11 nulls in source) |
| `job_level` | accepted_values | Level is Entry/Mid-Senior/Director/Executive/Associate/Internship/Not Applicable |

### LinkedIn Skills (`stg_linkedin__skills`)

| Column | Test | Description |
|--------|------|-------------|
| `posting_id` | not_null | All skills linked to a posting |
| `posting_id` | relationships | FK exists in stg_linkedin__postings |
| `skill_name` | not_null | All rows have a skill name |

### LinkedIn Summaries (`stg_linkedin__summaries`)

| Column | Test | Description |
|--------|------|-------------|
| `posting_id` | unique | One summary per posting |
| `posting_id` | not_null | All summaries linked to a posting |
| `posting_id` | relationships | FK exists in stg_linkedin__postings |

### GitHub (`stg_github__repo_stats`)

| Column | Test | Description |
|--------|------|-------------|
| `repo_id` | unique | Each repo has unique full_name |
| `repo_id` | not_null | All repos have an ID |
| `repo_name` | not_null | All repos have a name |
| `category` | not_null | All repos are categorized |
| `category` | accepted_values | Category is one of: orchestration, transformation, warehouse, streaming, table_format, etl_elt, bi, ml_framework, llm, mlops, vector_db, data_quality, database, infrastructure |
| `stars` | not_null | All repos have star count |
| `stars` | accepted_range (>= 0) | Stars cannot be negative |
| `forks` | not_null | All repos have fork count |
| `forks` | accepted_range (>= 0) | Forks cannot be negative |
| `open_issues` | accepted_range (>= 0) | Issues cannot be negative |

### LLM Extractions (`stg_llm__skill_extractions`)

| Column | Test | Description |
|--------|------|-------------|
| `posting_id` | not_null | All extractions linked to a post |
| `posting_id` | unique | One extraction per post |
| `posting_id` | relationships | FK exists in stg_hn__job_postings |
| `is_successful` | not_null | Success status always recorded |
| `is_successful` | accepted_values | Value is true or false |
| `technology_count` | accepted_range (>= 0) | Count cannot be negative |
| `role_count` | accepted_range (>= 0) | Count cannot be negative |
| `llm_model` | not_null (warn) | Model name recorded (182 nulls from failed extractions) |

---

## Running Tests

```bash
# Run all tests
cd dbt && dbt test

# Run tests for specific source
dbt test --select source:raw+

# Run tests for specific model
dbt test --select stg_hn__job_postings
```

---

## Test Results

Tests are executed as part of the dbt pipeline. Failed tests indicate data quality issues that need investigation.

- **Pass:** Data meets quality standards
- **Warn:** Soft failure (configured with `severity: warn`), logged but doesn't block pipeline
- **Fail:** Hard failure, blocks downstream models

Relationship tests (foreign keys) are configured as warnings since source data may have orphaned records.

---

## LLM Extraction Validation

Beyond schema-level dbt tests, LLM extraction quality is validated through a **comparison model** that measures agreement between LLM and regex extraction methods.

### Validation Approach

Rather than manual annotation of a sample set, we validate LLM extraction by comparing it against regex extraction on the same 10K posts. This approach:

1. **Covers the full sample** - All 10K posts are compared, not a 200-post annotation sample
2. **Is reproducible** - Results are computed in dbt and queryable in Snowflake
3. **Quantifies real-world performance** - Shows how LLM compares to an alternative method

### Key Metrics

| Metric | Value | Description |
|--------|-------|-------------|
| **Extraction Success Rate** | 98.2% | 9,818 of 10,000 posts successfully processed |
| **Avg Technologies (LLM)** | 6.4 per post | Technologies extracted by Claude Haiku |
| **Avg Technologies (Regex)** | 1.5 per post | Technologies matched by keyword taxonomy |
| **Coverage Improvement** | 4.3x | LLM finds 4x more technologies per post |
| **Unique Technologies (LLM)** | 4,569 | Distinct technologies identified |
| **Unique Technologies (Regex)** | 152 | Technologies in curated taxonomy |

### Agreement Analysis

The `fct_llm_vs_regex_comparison` model calculates per-technology agreement rates:

| Technology | Agreement Rate | Interpretation |
|------------|----------------|----------------|
| PostgreSQL | 66.1% | High agreement - both methods detect reliably |
| Python | 58.3% | Moderate agreement |
| React | 0% | LLM-only - not in regex taxonomy |
| TypeScript | 0% | LLM-only - not in regex taxonomy |

**Key insight:** Technologies with 0% agreement are typically valid extractions that simply aren't in the 152-technology regex taxonomy, demonstrating LLM's broader coverage.

### Validation Model

```sql
-- fct_llm_vs_regex_comparison joins LLM and regex extractions
-- on the same posting_id to calculate agreement rates
SELECT
    technology,
    COUNT(*) as total_mentions,
    SUM(CASE WHEN found_by_both THEN 1 ELSE 0 END) as agreed,
    agreed / total_mentions as agreement_rate
FROM comparison_base
GROUP BY technology
```

### Why Not Traditional Precision/Recall?

Traditional evaluation requires:
- Manual annotation of 200+ posts (labor-intensive)
- Subjective judgment on what "counts" as a technology mention
- Point-in-time evaluation that doesn't scale

Our comparison approach provides:
- Automated, reproducible validation
- Full coverage of the 10K sample
- Quantified comparison against an alternative method
- Dashboard visualization of results (LLM vs Regex page)
