# Data & AI Industry Index

**What's hot, what's growing, what's dying in the data/AI space?**

A multi-source analytics platform that tracks interest, demand, and growth signals across the data engineering and AI ecosystem. Combines 93K+ job postings, 1.3M LinkedIn jobs, and 81 GitHub repositories with LLM-powered extraction to surface technology and role trends over time.

---

## The Problem

The data/AI fields evolve rapidly. New tools emerge monthly, roles shift and rename, technologies rise and fall. But there's no single place to answer:

- Is demand for Snowflake growing faster than Databricks?
- When did "Analytics Engineer" become a real job title?
- Are MLOps roles actually increasing, or is it just hype?
- Which technologies should I learn next?

This project answers those questions with data.

---

## Key Findings

| Finding | Evidence |
|---------|----------|
| **Snowflake overtook Redshift** | 1.6% vs 0.4% of HN posts in 2024 (crossed in 2022) |
| **PyTorch dominates TensorFlow** | 2.0% vs 0.5% in 2025 (4x lead, flipped in 2022) |
| **OpenAI mentions exploded** | 0.4% (2022) to 2.7% (2025) - the ChatGPT effect |
| **LLM extracts 4x more skills** | 6.4 technologies/post vs 1.5 from regex |
| **PostgreSQL is king** | 14% of HN posts (2024-25) - 6x the next database |
| **2021 was peak hiring** | 10,570 HN posts; 2023-2024 dropped to ~40% of peak |

---

## What It Does

1. **Ingests job postings** from Hacker News "Who Is Hiring" (93K posts, 2011-present) and LinkedIn (1.3M jobs)
2. **Extracts skills/technologies** using keyword matching against a curated taxonomy (152 technologies, 27 roles)
3. **LLM-powered extraction** via Claude Haiku on a 10K post sample for validation and taxonomy discovery
4. **Tracks GitHub activity** for 81 key data/AI repositories
5. **Compares extraction methods** with a dbt model that quantifies LLM vs regex agreement rates
6. **Generates automated insights** with Claude Sonnet producing weekly market summaries
7. **Visualizes everything** via interactive Streamlit dashboard

---

## Dashboard Features

The Streamlit dashboard provides 7 pages of interactive analysis:

| Page | Features |
|------|----------|
| **Executive Summary** | Key metrics, headline findings, trend charts, LLM performance stats |
| **Technology Trends** | Time-series visualization, YoY comparison, technology co-occurrence analysis, top technology pairs |
| **Role Trends** | Role mentions over time, tier filtering, top roles ranking |
| **GitHub & LinkedIn** | Repository stats, LinkedIn skill rankings, HN vs LinkedIn cross-validation comparison |
| **LLM vs Regex** | Agreement rates, method breakdown, LLM time-series trends, side-by-side extraction comparison |
| **Data Explorer** | Browse raw tables, job posting keyword search with preview |
| **Methodology** | Data sources, pipeline architecture, extraction methods, taxonomy, limitations |

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Warehouse** | Snowflake |
| **Transformation** | dbt (21 models, 3 seeds) |
| **Orchestration** | Airflow |
| **LLM** | Claude API (Anthropic) |
| **Visualization** | Streamlit |
| **Language** | Python, SQL |

---

## Data Sources

| Source | Volume | Description |
|--------|--------|-------------|
| **HN Who Is Hiring** | 93K posts | Monthly job postings from Hacker News (2011-present) |
| **LinkedIn Jobs** | 1.3M jobs | January 2024 snapshot from Kaggle |
| **GitHub Repos** | 81 repos | Stars, forks, activity for key data/AI tools |

**Data Licensing:**
- **LinkedIn:** [Kaggle dataset](https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024) used under Kaggle terms for academic/research purposes
- **HN:** Public data via [HuggingFace](https://huggingface.co/datasets/brusic/hacker-news-who-is-hiring-posts) and HN Firebase API
- **GitHub:** Public REST API

---

## Project Structure

```
data-ai-industry-index-tracker/
├── dashboard/              # Streamlit app
│   └── app.py
├── dbt/                    # dbt project (21 models)
│   ├── models/
│   │   ├── staging/        # 6 source-conformed views
│   │   │   ├── hn/         # HN job postings
│   │   │   ├── linkedin/   # LinkedIn postings, skills, summaries
│   │   │   ├── github/     # GitHub repo stats
│   │   │   └── llm/        # LLM skill extractions
│   │   ├── intermediate/   # 4 tables (keyword extraction logic)
│   │   └── marts/          # 11 models (facts & dims)
│   └── seeds/              # Taxonomy CSVs (technologies, roles, databases)
├── extraction/             # LLM extraction scripts
│   ├── llm_skill_extraction.py      # Claude Haiku skill extraction (10K posts)
│   └── generate_weekly_insights.py  # Claude Sonnet weekly reports
├── airflow/dags/           # Airflow DAGs
├── exploration/            # Data exploration scripts
├── infrastructure/         # Snowflake setup scripts
├── data/raw/               # Raw data files
└── docs/                   # Documentation
```

---

## Documentation

Detailed documentation lives in the `docs/` folder:

| File | Description |
|------|-------------|
| [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) | Complete schema reference for all tables, columns, and data sources |
| [DATA_QUALITY.md](docs/DATA_QUALITY.md) | Data quality checks (77 dbt tests across 4 sources) |
| [INSIGHTS.md](docs/INSIGHTS.md) | Key findings and observations from the data |
| [GITHUB_REPOS.md](docs/GITHUB_REPOS.md) | Selection criteria and methodology for the 81 tracked repositories |
| [CAPSTONE_FEEDBACK.md](docs/CAPSTONE_FEEDBACK.md) | Instructor feedback on the capstone proposal |
| [CHECKPOINT.md](docs/CHECKPOINT.md) | Project progress checkpoints |

Additional project context:
| File | Description |
|------|-------------|
| [PROJECT_PROPOSAL.md](docs/PROJECT_PROPOSAL.md) | Original detailed project proposal with motivation and scope |
| [CAPSTONE_PROPOSAL.md](docs/CAPSTONE_PROPOSAL.md) | Combined capstone proposal (this project + AI Influence Monitor) |
| [CLAUDE.md](CLAUDE.md) | Context file for Claude Code AI assistant |

---

## Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd data-ai-industry-index-tracker
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your Snowflake credentials

# Run the dashboard
cd dashboard && streamlit run app.py
```

---

## Data Pipeline

```
HuggingFace (HN) ─┐
Kaggle (LinkedIn) ┼──▶ Snowflake Raw ──▶ dbt Staging ──▶ dbt Intermediate ──▶ dbt Marts ──▶ Streamlit
GitHub API ───────┘         │                 │                  │                  │
                            │                 │                  │                  │
                            │           (1:1 clean)    (skill extraction)    (facts & dims)
                            │                                                      │
                            ▼                                                      ▼
                    ┌───────────────┐                                ┌──────────────────────┐
                    │  LLM Layer    │                                │  LLM Comparison      │
                    │  (Claude API) │                                │  fct_llm_vs_regex_   │
                    └───────────────┘                                │  comparison          │
                            │                                       └──────────────────────┘
            ┌───────────────┴───────────────┐
            ▼                               ▼
   LLM Skill Extraction            Weekly Insights
   (10K sample → 63K mentions)     (Automated reports)
```

---

## AI/LLM Components

This project uses Claude (Anthropic API) for two agentic pipeline tasks:

### 1. LLM Skill Extraction
- **What:** Extracts structured technology and role mentions from job postings using Claude Haiku
- **Scale:** 10,000 posts processed, 9,818 successful (98.2%), 63,013 technology mentions extracted
- **Cost:** ~$4.50 total ($0.00045/post)
- **Why:** Captures 4x more technologies per post than regex (6.4 vs 1.5 avg), identifies 4,569 unique technologies vs 152 in the seed taxonomy
- **Output:** `raw_llm_skill_extractions` → `stg_llm__skill_extractions` → `fct_llm_technology_mentions`

### 2. LLM vs Regex Comparison
- **What:** dbt model that joins LLM and regex extractions on overlapping posts to quantify agreement
- **Key finding:** PostgreSQL has highest agreement (66.1%), while React/JavaScript/TypeScript are found only by LLM (not in regex taxonomy)
- **Output:** `fct_llm_vs_regex_comparison`

### 3. Automated Weekly Insights
- **What:** Claude Sonnet analyzes trend data and generates a written market summary
- **Schedule:** Weekly (Airflow task)
- **Output:** `weekly_insights` table + `docs/WEEKLY_INSIGHTS_*.md` files

**Scripts:**
- `extraction/llm_skill_extraction.py` - LLM-powered skill extraction
- `extraction/generate_weekly_insights.py` - Automated insights generator

---

## Key Tables

| Table | Rows | Description |
|-------|------|-------------|
| `fct_monthly_technology_trends` | 9.8K | Technology mentions aggregated by month (regex) |
| `fct_monthly_role_trends` | 2.9K | Role mentions aggregated by month |
| `fct_llm_technology_mentions` | 63K | LLM-extracted technology mentions (10K sample) |
| `fct_llm_vs_regex_comparison` | ~150 | LLM vs regex agreement rates by technology |
| `fct_linkedin_skill_counts` | 3.3M | LinkedIn skill demand |
| `fct_github_repo_stats` | 81 | GitHub repository metrics |
| `dim_technologies` | 152 | Technology master list |
| `dim_roles` | 27 | Role taxonomy |

---

## Who This Is For

| Audience | Value |
|----------|-------|
| **Job Seekers** | See which skills are trending to guide learning |
| **Educators** | Data-driven curriculum decisions |
| **Hiring Managers** | Benchmark against market trends |
| **Practitioners** | Track the health of your field |

---

## Known Limitations

- **HN data skews toward startups** - Enterprise hiring patterns may differ
- **LinkedIn is a single snapshot** - No time series, cross-sectional only
- **Regex extraction is taxonomy-limited** - Only detects 152 curated technologies; LLM extraction covers the gap but at higher cost
- **LLM extraction covers 10K posts** - Sample only; full 93K dataset uses regex for cost efficiency

See the dashboard's "Data Sources & Limitations" section for full details.

---

## Challenges & Solutions

### 1. Unstructured Job Posting Text
**Challenge:** HN "Who Is Hiring" posts are freeform HTML with no consistent structure. Company names, roles, and technologies are embedded in prose.

**Solution:** Two-pronged extraction approach:
- Regex-based keyword matching against a curated 152-technology taxonomy for full dataset coverage
- LLM extraction (Claude Haiku) on a 10K sample for validation and taxonomy discovery
- dbt model `fct_llm_vs_regex_comparison` quantifies method agreement rates

### 2. LLM Extraction Failures
**Challenge:** 182 of 10,000 posts (1.8%) failed LLM extraction due to context length limits or malformed content.

**Solution:**
- Graceful error handling with `is_successful` flag
- Failed extractions logged with null `llm_model` field
- dbt tests configured with `severity: warn` to allow pipeline to continue
- Dashboard filters to successful extractions only

### 3. LinkedIn Single Snapshot
**Challenge:** LinkedIn dataset is a January 2024 snapshot with no historical data, making time-series analysis impossible.

**Solution:**
- Used LinkedIn for cross-platform validation, not trend analysis
- Built `fct_linkedin_skill_counts` to compare skill demand between platforms
- HN data (2011-present) provides the time-series dimension

### 4. Taxonomy Coverage vs. LLM Cost
**Challenge:** Regex taxonomy only covers 152 technologies, but LLM extraction found 4,569 unique technologies. Full LLM processing would cost ~$42 for 93K posts.

**Solution:**
- LLM on 10K sample (~$4.50) to validate approach and discover new technologies
- Regex on full 93K posts for cost-efficient coverage
- LLM finds 4x more technologies per post (6.4 vs 1.5), quantified in comparison model

### 5. Source Data Quality Issues
**Challenge:** LinkedIn has 11 null company names, LLM extractions have 182 null model names (failed runs).

**Solution:**
- dbt tests with `severity: warn` for known source data quirks
- 77 data quality tests total: 74 PASS, 3 WARN, 0 ERROR
- Documented in [DATA_QUALITY.md](docs/DATA_QUALITY.md)

### 6. GitHub Category Classification
**Challenge:** Mapping 81 repositories to technology categories required domain expertise.

**Solution:**
- Created 14 categories: orchestration, transformation, warehouse, streaming, table_format, etl_elt, bi, ml_framework, llm, mlops, vector_db, data_quality, database, infrastructure
- Documented selection criteria in [GITHUB_REPOS.md](docs/GITHUB_REPOS.md)
- dbt `accepted_values` test ensures all repos have valid categories

---

## Status

**Complete** - DataExpert.io analytics engineering capstone project

- [x] Data ingestion (HN, LinkedIn, GitHub)
- [x] dbt models (6 staging + 4 intermediate + 11 marts)
- [x] LLM skill extraction (10K posts, 98.2% success)
- [x] LLM vs regex comparison analysis
- [x] Automated weekly insights
- [x] Airflow DAGs
- [x] Streamlit dashboard
- [ ] Process remaining 83K+ posts with LLM

---

## License

MIT
