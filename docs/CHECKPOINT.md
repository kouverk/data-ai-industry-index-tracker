# Project Checkpoint - Phase 1 Complete

**Date:** January 2025
**Status:** Phase 1 Exploration Complete, Ready for Phase 2

---

## What We Built

### Exploration Scripts
| Script | Purpose | Output |
|--------|---------|--------|
| `exploration/01_explore_hn_data.py` | Download & flatten HN dataset | `data/raw/hn_who_is_hiring.parquet` (93K posts) |
| `exploration/02_explore_linkedin_data.py` | Explore LinkedIn dataset | Samples + skill analysis |
| `exploration/03_skill_extraction_prototype.py` | Test role/tech extraction | `data/processed/hn_with_extractions.parquet` |
| `exploration/04_explore_github_data.py` | Fetch GitHub repo stats | `data/raw/github_repo_stats.json` + `.csv` |

### Taxonomy
| File | Contents |
|------|----------|
| `exploration/taxonomy.py` | 27 roles, 171 technologies, 33 databases |

### Documentation
| File | Contents |
|------|----------|
| `docs/DATA_DICTIONARY.md` | Schema definitions for all data sources |
| `docs/INSIGHTS.md` | 13 key findings from exploration |

---

## Key Insights Discovered

1. **HN posting volume** tracks tech hiring cycles (2021 peak, 2023-24 trough)
2. **Snowflake overtook Redshift** around 2021-2022
3. **PyTorch surpassed TensorFlow** around 2021-2022
4. **OpenAI mentions 4x'd** from 2022→2023 (ChatGPT effect)
5. **dbt emerged** around 2020, now ~0.8% of posts
6. **PostgreSQL dominates** at 14.6% (3x next database)
7. **LLM tools dominate GitHub** stars - 4 of top 7 repos
8. **Polars approaching Spark** in GitHub stars (Rust-based pandas alternative)

---

## Data Source Schedule

| Source | Frequency | Notes |
|--------|-----------|-------|
| GitHub Repo Stats | **Daily** | Good for demo, shows fresh data |
| HN "Who Is Hiring" | Monthly | New thread each month |
| LinkedIn Jobs | One-time | Jan 2024 snapshot (no API for refresh) |
| Reddit (Phase 2) | Daily | Subscriber counts, post volume |

---

## Next Steps (Phase 2)

### Infrastructure Setup
1. Set up Snowflake account (free trial)
2. Create schemas: `raw`, `staging`, `intermediate`, `marts`
3. Set up S3 bucket for raw data landing
4. Load raw parquet/CSV files to Snowflake

### dbt Project
1. Initialize dbt project structure
2. Build staging models (1:1 with sources, light cleaning)
3. Build intermediate models (skill extraction in SQL, standardization)
4. Build mart models (dimensional: dim_technologies, fct_monthly_trends)
5. Write tests (unique, not_null, accepted_values)

### Airflow DAGs
1. `dag_github_daily` - Fetch repo stats, upload to S3, load to Snowflake
2. `dag_hn_monthly` - Fetch new thread, extract posts, load to Snowflake
3. `dag_linkedin_load` - One-time load from local files
4. `dag_dbt_transform` - Triggered after data loads, runs dbt

### Dashboard
1. Connect BI tool (Metabase/Superset) to Snowflake
2. Build trend visualizations
3. Add filters and drill-downs

---

## Commands to Verify Data

```bash
# Check HN data exists
ls -la data/raw/hn_who_is_hiring.parquet

# Check GitHub data exists
ls -la data/raw/github_repo_stats.*

# Check processed data exists
ls -la data/processed/hn_with_extractions.parquet

# Quick Python check
python -c "import pandas as pd; print(f'HN rows: {len(pd.read_parquet(\"data/raw/hn_who_is_hiring.parquet\")):,}')"
```

---

## Resume Points

When continuing this project, pick up with:

1. **"Let's set up Snowflake"** - Create account, schemas, and load raw data
2. **"Let's start dbt"** - Initialize project and build staging models
3. **"Let's build the Airflow DAGs"** - Start with dag_github_daily for daily refresh

---

## Files Created During Phase 1

```
data-ai-industry-index-tracker/
├── CLAUDE.md                           # Project context
├── PROJECT_PROPOSAL.md                 # Original proposal
├── requirements.txt                    # Python dependencies
├── docs/
│   ├── DATA_DICTIONARY.md              # Schema documentation
│   ├── INSIGHTS.md                     # 13 key findings
│   └── CHECKPOINT.md                   # This file
├── exploration/
│   ├── taxonomy.py                     # Role/tech/database taxonomies
│   ├── 01_explore_hn_data.py           # HN exploration
│   ├── 02_explore_linkedin_data.py     # LinkedIn exploration
│   ├── 03_skill_extraction_prototype.py # Extraction logic
│   └── 04_explore_github_data.py       # GitHub stats
├── data/
│   ├── raw/
│   │   ├── hn_who_is_hiring.parquet    # 93K HN posts
│   │   ├── hn_sample_100.csv           # Sample for review
│   │   ├── github_repo_stats.json      # 81 repos, full metadata
│   │   ├── github_repo_stats.csv       # Simplified view
│   │   └── linkedin/                   # LinkedIn CSVs (user-provided)
│   │       ├── linkedin_job_postings.csv
│   │       ├── job_skills.csv
│   │       └── job_summary.csv
│   └── processed/
│       └── hn_with_extractions.parquet # HN with extracted roles/techs
├── extraction/                         # (empty, for Phase 2)
├── dbt/                                # (empty, for Phase 2)
└── airflow/dags/                       # (empty, for Phase 2)
```
