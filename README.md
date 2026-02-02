# Data & AI Industry Index

**What's hot, what's growing, what's dying in the data/AI space?**

A multi-source analytics platform that tracks interest, demand, and growth signals across the data engineering and AI ecosystem.

---

## The Problem

The data/AI fields evolve rapidly. New tools emerge monthly, roles shift and rename, technologies rise and fall. But there's no single place to answer:

- Is demand for Snowflake growing faster than Databricks?
- When did "Analytics Engineer" become a real job title?
- Are MLOps roles actually increasing, or is it just hype?
- Which technologies should I learn next?

This project answers those questions with data.

---

## What It Does

1. **Ingests job postings** from Hacker News "Who Is Hiring" (93K posts, 2011-present) and LinkedIn (1.3M jobs)
2. **Extracts skills/technologies** using keyword matching against a curated taxonomy
3. **Tracks GitHub activity** for 81 key data/AI repositories
4. **Aggregates trends** by month, technology, and role
5. **Visualizes insights** via interactive Streamlit dashboard

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Warehouse** | Snowflake |
| **Transformation** | dbt |
| **Orchestration** | Airflow |
| **Visualization** | Streamlit |
| **Language** | Python, SQL |

---

## Data Sources

| Source | Volume | Description |
|--------|--------|-------------|
| **HN Who Is Hiring** | 93K posts | Monthly job postings from Hacker News (2011-present) |
| **LinkedIn Jobs** | 1.3M jobs | January 2024 snapshot from Kaggle |
| **GitHub Repos** | 81 repos | Stars, forks, activity for key data/AI tools |

---

## Project Structure

```
data-ai-industry-index-tracker/
├── dashboard/              # Streamlit app
│   └── app.py
├── dbt/                    # dbt project
│   ├── models/
│   │   ├── staging/        # Source-conformed views
│   │   ├── intermediate/   # Business logic (skill extraction)
│   │   └── marts/          # Analytics-ready facts & dims
│   └── seeds/              # Taxonomy CSVs
├── airflow/dags/           # Airflow DAGs
├── infrastructure/         # Snowflake setup scripts
├── exploration/            # Jupyter notebooks
├── data/raw/               # Raw data files
└── docs/                   # Documentation (see below)
```

---

## Documentation

Detailed documentation lives in the `docs/` folder:

| File | Description |
|------|-------------|
| [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) | Complete schema reference for all tables, columns, and data sources |
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
GitHub API ───────┘                         │                  │                  │
                                            │                  │                  │
                                      (1:1 clean)    (skill extraction)    (facts & dims)
```

---

## Key Tables

| Table | Rows | Description |
|-------|------|-------------|
| `fct_monthly_technology_trends` | 9.8K | Technology mentions aggregated by month |
| `fct_monthly_role_trends` | 2.9K | Role mentions aggregated by month |
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
- **Skill extraction uses keyword matching** - May miss context or have false positives

See the dashboard's "Data Sources & Limitations" section for full details.

---

## Status

🚧 **In Development** - Capstone project for DataExpert.io analytics engineering bootcamp

---

## License

MIT
