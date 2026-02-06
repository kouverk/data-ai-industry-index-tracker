# Architecture

Technical architecture for the Data & AI Industry Index Tracker.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA SOURCES                                   │
├───────────────────┬───────────────────┬───────────────────┬─────────────────┤
│  HN Who Is Hiring │   LinkedIn Jobs   │    GitHub API     │   Claude API    │
│  (HuggingFace)    │   (Kaggle)        │   (REST)          │   (Anthropic)   │
│  93K posts        │   1.3M jobs       │   81 repos        │   LLM extraction│
└─────────┬─────────┴─────────┬─────────┴─────────┬─────────┴────────┬────────┘
          │                   │                   │                  │
          ▼                   ▼                   ▼                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SNOWFLAKE RAW LAYER                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐│
│  │ hn_job_posts │ │linkedin_posts│ │ github_repos │ │raw_llm_skill_extract ││
│  │    93,251    │ │  1,310,929   │ │      81      │ │       9,818          ││
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              dbt MODELS (21)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  STAGING (6 models)                                                         │
│  ├── stg_hn__job_postings           # Clean HN posts with parsed dates      │
│  ├── stg_linkedin__postings         # Clean LinkedIn job listings           │
│  ├── stg_linkedin__skills           # LinkedIn skill associations           │
│  ├── stg_linkedin__summaries        # LinkedIn job summaries                │
│  ├── stg_github__repos              # GitHub repository metadata            │
│  └── stg_llm__skill_extractions     # LLM-extracted skills (10K sample)     │
├─────────────────────────────────────────────────────────────────────────────┤
│  INTERMEDIATE (4 models)                                                    │
│  ├── int_hn__skills_extracted       # Regex skill extraction from HN        │
│  ├── int_hn__roles_extracted        # Regex role extraction from HN         │
│  ├── int_linkedin__skill_counts     # LinkedIn skill aggregation            │
│  └── int_llm__technology_mentions   # Parsed LLM JSON to rows               │
├─────────────────────────────────────────────────────────────────────────────┤
│  MARTS (11 models)                                                          │
│  ├── dim_technologies               # 152 technologies (seed)               │
│  ├── dim_roles                      # 27 roles (seed)                       │
│  ├── dim_databases                  # Database subset (seed)                │
│  ├── fct_monthly_technology_trends  # Tech mentions by month (regex)        │
│  ├── fct_monthly_role_trends        # Role mentions by month                │
│  ├── fct_llm_technology_mentions    # LLM extractions (63K mentions)        │
│  ├── fct_llm_vs_regex_comparison    # Method agreement rates                │
│  ├── fct_linkedin_skill_counts      # LinkedIn skill demand                 │
│  ├── fct_github_repo_stats          # GitHub activity metrics               │
│  ├── fct_technology_cooccurrence    # Tech pairs in same posting            │
│  └── fct_hn_linkedin_comparison     # Cross-platform skill comparison       │
└─────────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          STREAMLIT DASHBOARD                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │  Executive  │ │  Technology │ │    Role     │ │   GitHub/   │            │
│  │   Summary   │ │   Trends    │ │   Trends    │ │  LinkedIn   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                            │
│  │ LLM vs Regex│ │    Data     │ │ Methodology │                            │
│  │  Analysis   │ │  Explorer   │ │    Docs     │                            │
│  └─────────────┘ └─────────────┘ └─────────────┘                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Warehouse** | Snowflake | Data storage, SQL compute |
| **Transformation** | dbt | SQL-based data modeling |
| **Orchestration** | Airflow | Pipeline scheduling |
| **LLM** | Claude API (Anthropic) | Skill extraction, insights |
| **Visualization** | Streamlit + Plotly | Interactive dashboard |
| **Language** | Python, SQL | Extraction scripts, models |

---

## Data Pipeline

### Extraction Layer

All extraction scripts live in `extraction/`. The pattern is:
1. **Fetch** - Pull data from external sources → save to `data/raw/`
2. **Load** - Push raw data to Snowflake raw tables
3. **Transform** - dbt handles all transformations (ELT pattern)

```
┌─────────────────────────────────────────────────────────────────┐
│                      EXTRACTION SCRIPTS                         │
│                        extraction/                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DATA SOURCE FETCHERS                                           │
│  ├── fetch_hn_data.py           # HuggingFace → data/raw/       │
│  │   └── Downloads 93K HN posts from HuggingFace dataset        │
│  │   └── Saves to data/raw/hn_who_is_hiring.parquet             │
│  │                                                              │
│  ├── fetch_github_data.py       # GitHub API → data/raw/        │
│  │   └── Fetches stats for 81 data/AI repos                     │
│  │   └── Saves to data/raw/github_repo_stats.json               │
│  │                                                              │
│  └── (LinkedIn: manual download from Kaggle → data/raw/linkedin)│
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SNOWFLAKE LOADER                                               │
│  └── load_to_snowflake.py       # data/raw/ → Snowflake         │
│      └── Loads HN, GitHub, LinkedIn to raw_* tables             │
│      └── Full refresh (truncate + insert)                       │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LLM ENRICHMENT                                                 │
│  ├── llm_skill_extraction.py    # Claude Haiku skill extraction │
│  │   └── Processes 10K posts → 63K technology mentions          │
│  │   └── Cost: ~$0.00045/post ($4.50 total)                     │
│  │                                                              │
│  └── generate_weekly_insights.py # Claude Sonnet market reports │
│      └── Queries fct_* tables for trend data                    │
│      └── Generates markdown reports + saves to Snowflake        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Exploration scripts (prototyping, one-time analysis) remain in exploration/
```

### Transformation Layer (dbt)

```
┌─────────────────────────────────────────────────────────────────┐
│                        dbt PROJECT                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  models/                                                        │
│  ├── staging/          # 1:1 source cleaning                    │
│  │   ├── hn/           # HN job postings                        │
│  │   ├── linkedin/     # LinkedIn postings, skills, summaries   │
│  │   ├── github/       # GitHub repo stats                      │
│  │   └── llm/          # LLM skill extractions                  │
│  │                                                              │
│  ├── intermediate/     # Business logic                         │
│  │   └── Regex-based skill/role extraction                      │
│  │   └── Skill counting and aggregation                         │
│  │                                                              │
│  └── marts/            # Analytics-ready models                 │
│      └── Dimensional models (dim_*, fct_*)                      │
│      └── Time-series aggregations                               │
│      └── Cross-source comparisons                               │
│                                                                 │
│  seeds/                # Static reference data                  │
│  ├── technologies.csv  # 152 technologies with categories       │
│  ├── roles.csv         # 27 roles with tiers                    │
│  └── databases.csv     # Database subset for analysis           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Orchestration Layer (Airflow)

```
┌─────────────────────────────────────────────────────────────────┐
│                        AIRFLOW DAGS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  airflow/dags/                                                  │
│  ├── dag_dbt_transform.py      # Daily dbt run                  │
│  │   └── dbt run → dbt test                                     │
│  │                                                              │
│  ├── dag_github_extract.py     # Weekly GitHub fetch            │
│  │   └── fetch_github_data.py → Snowflake                       │
│  │                                                              │
│  └── dag_weekly_insights.py    # Weekly LLM insights            │
│      └── generate_weekly_insights.py                            │
│      └── Outputs: docs/WEEKLY_INSIGHTS_*.md + Snowflake table   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Skill Extraction Methods

### Method 1: Regex (Full Dataset)

```
┌─────────────────────────────────────────────────────────────────┐
│                     REGEX EXTRACTION                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input:  93,251 HN job postings                                 │
│  Method: Pattern matching against 152 technology taxonomy       │
│  Output: ~140K technology mentions                              │
│                                                                 │
│  Strengths:                                                     │
│  ✓ Fast (processes full dataset)                                │
│  ✓ Deterministic                                                │
│  ✓ Zero marginal cost                                           │
│                                                                 │
│  Limitations:                                                   │
│  ✗ Limited to predefined taxonomy                               │
│  ✗ Misses variations/synonyms                                   │
│  ✗ ~1.5 technologies per post average                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Method 2: LLM (10K Sample)

```
┌─────────────────────────────────────────────────────────────────┐
│                      LLM EXTRACTION                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input:  10,000 HN job postings (random sample)                 │
│  Method: Claude Haiku structured extraction                     │
│  Output: 63,013 technology mentions (9,818 successful)          │
│  Cost:   ~$4.50 ($0.00045/post)                                 │
│                                                                 │
│  Strengths:                                                     │
│  ✓ ~6.4 technologies per post (4x regex)                        │
│  ✓ Discovers new technologies not in taxonomy                   │
│  ✓ Handles variations/synonyms                                  │
│  ✓ 4,569 unique technologies extracted                          │
│                                                                 │
│  Limitations:                                                   │
│  ✗ Cost at scale (~$37 for full dataset)                        │
│  ✗ API latency                                                  │
│  ✗ 98.2% success rate (1.8% failures)                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Comparison Model

```
┌─────────────────────────────────────────────────────────────────┐
│                 LLM vs REGEX COMPARISON                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  fct_llm_vs_regex_comparison joins both methods on post_id      │
│                                                                 │
│  Key findings:                                                  │
│  • PostgreSQL: 66.1% agreement (highest)                        │
│  • React/JavaScript/TypeScript: LLM-only (not in regex taxonomy)│
│  • LLM discovers ~30x more unique technologies                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Dashboard Architecture

### Page Structure

| Page | Data Sources | Key Queries |
|------|--------------|-------------|
| **Executive Summary** | All marts | Aggregated metrics, headline stats |
| **Technology Trends** | fct_monthly_technology_trends, fct_technology_cooccurrence | Time-series, co-occurrence pairs |
| **Role Trends** | fct_monthly_role_trends, dim_roles | Time-series by tier |
| **GitHub & LinkedIn** | fct_github_repo_stats, fct_linkedin_skill_counts, fct_hn_linkedin_comparison | Cross-platform comparison |
| **LLM vs Regex** | fct_llm_vs_regex_comparison, fct_llm_technology_mentions | Agreement rates, method breakdown |
| **Data Explorer** | stg_hn__job_postings, all tables | Raw data browse, keyword search |
| **Methodology** | Static content | Documentation, limitations |

### Connection Flow

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│                 │      │                 │      │                 │
│   Streamlit     │──────│   Snowflake     │──────│   dbt Models    │
│   (app.py)      │ SQL  │   Connector     │      │   (marts)       │
│                 │      │                 │      │                 │
└─────────────────┘      └─────────────────┘      └─────────────────┘
        │
        ▼
┌─────────────────┐
│                 │
│   Plotly        │
│   Charts        │
│                 │
└─────────────────┘
```

---

## Data Volumes

| Table | Rows | Description |
|-------|------|-------------|
| stg_hn__job_postings | 93,251 | All HN job posts (2011-present) |
| stg_linkedin__postings | 1,310,929 | LinkedIn jobs (Jan 2024) |
| stg_linkedin__skills | 3,271,917 | LinkedIn skill associations |
| fct_monthly_technology_trends | 9,800 | Monthly tech aggregations |
| fct_monthly_role_trends | 2,900 | Monthly role aggregations |
| fct_llm_technology_mentions | 63,013 | LLM extractions (10K sample) |
| fct_github_repo_stats | 81 | GitHub repo metrics |
| dim_technologies | 152 | Technology taxonomy |
| dim_roles | 27 | Role taxonomy |

---

## Environment Configuration

### Required Environment Variables

```bash
# Snowflake
SNOWFLAKE_ACCOUNT=xxx
SNOWFLAKE_USER=xxx
SNOWFLAKE_PASSWORD=xxx
SNOWFLAKE_DATABASE=KOUVERK_DATA_INDUSTRY
SNOWFLAKE_WAREHOUSE=xxx
SNOWFLAKE_SCHEMA=marts

# Anthropic (for LLM extraction)
ANTHROPIC_API_KEY=xxx
```

### Local Development

```bash
# 1. Fetch data from sources
python extraction/fetch_hn_data.py           # HuggingFace → data/raw/
python extraction/fetch_github_data.py       # GitHub API → data/raw/
# LinkedIn: manually download from Kaggle to data/raw/linkedin/

# 2. Load to Snowflake
python extraction/load_to_snowflake.py       # All sources
python extraction/load_to_snowflake.py hn    # Just HN
python extraction/load_to_snowflake.py github # Just GitHub

# 3. Transform with dbt
cd dbt && dbt run && dbt test

# 4. LLM enrichment (optional)
python extraction/llm_skill_extraction.py    # Claude Haiku extraction
python extraction/generate_weekly_insights.py # Weekly insights

# 5. Run dashboard
cd dashboard && streamlit run app.py
```

---

## Future Enhancements

| Enhancement | Status | Notes |
|-------------|--------|-------|
| Process remaining 83K posts with LLM | Planned | ~$37, 4-6 hours |
| Expand regex taxonomy with LLM discoveries | Planned | Use LLM findings to improve regex |
| Reddit subreddit tracking | Future | API rate limits, no historical data |
| Streamlit Cloud deployment | Planned | Secrets management needed |
| Historical LinkedIn data | Future | Currently single snapshot |
