# CLAUDE.md - Data & AI Industry Interest Index

## Project Overview

**Project Name:** Data & AI Industry Interest Index  
**Type:** Data Engineering Bootcamp Capstone  
**Goal:** Build a multi-source analytics platform that tracks interest, demand, and growth signals across the data engineering and AI ecosystem.

### The Core Question
> "What's hot, what's growing, what's dying in the data/AI space?"

### Business Value
- Job seekers: Understand which skills are trending up/down
- Bootcamps/educators: Know what to teach
- Hiring managers: Benchmark against market
- Practitioners: Track the health of their field

---

## Project Phases

### Phase 1: MVP (Must Ship)
**Data Sources:**
1. **HN "Who Is Hiring"** - Monthly job postings from Hacker News (2018-present)
   - Source: HuggingFace `brusic/hacker-news-who-is-hiring-posts` (Parquet)
   - Backup: BigQuery `bigquery-public-data.hacker_news.full`
   - Incremental: HN Firebase API for new months
   - ~150K raw job postings total, ~50K+ from 2018 onward

2. **LinkedIn Jobs Dataset** - 1.3M job postings from January 2024
   - Source: Kaggle `asaniczka/1-3m-linkedin-jobs-and-skills-2024`
   - Format: CSV (3 files: job_postings, job_skills, job_summary)
   - Pre-extracted skills included

**Transformations:**
- Skill/technology extraction from unstructured job text (HN)
- Technology taxonomy standardization (map variations to canonical names)
- Role classification (Data Engineer, Analytics Engineer, ML Engineer, etc.)
- Time-series aggregation (monthly granularity)

**Outputs:**
- Dimensional model in Snowflake
- dbt models (staging → intermediate → marts)
- Dashboard showing technology and role trends over time

### Phase 2: Stretch Goals
**Additional Data Sources:**
3. **Reddit Subreddit Growth**
   - Subreddits: r/dataengineering, r/MachineLearning, r/datascience, r/LocalLLaMA, r/analytics
   - Metrics: Subscriber count, posts per month, engagement rates
   - Source: Reddit API + Pushshift archive (if available)

4. **Reddit Post Content**
   - Discussion topics and volume
   - Sentiment analysis on technology mentions

### Phase 3: Future Enhancements
5. **YouTube Channel Stats** (challenging - no historical API data)
6. **Google Trends** (CSV export for key terms)
7. **Stack Overflow question volume** (public data dump)

---

## Technical Stack

### Required (per bootcamp)
- **Orchestration:** Airflow
- **Transformation:** dbt
- **Warehouse:** Snowflake
- **Catalog:** Glue Catalog / Iceberg / PyIceberg
- **Storage:** S3 or GCS (landing zone for raw data)

### Recommended Additions
- **Extraction:** Python scripts (requests, pandas)
- **NLP:** spaCy or regex for skill extraction
- **Visualization:** Metabase, Looker, or Streamlit

---

## Data Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                             │
├─────────────────────┬─────────────────────┬─────────────────────┤
│   HN Who Is Hiring  │   LinkedIn Jobs     │   Reddit (Phase 2)  │
│   (JSON/Parquet)    │   (CSV)             │   (JSON)            │
└─────────┬───────────┴─────────┬───────────┴─────────┬───────────┘
          │                     │                     │
          ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    S3 LANDING ZONE (Raw)                         │
│   s3://bucket/raw/hn_jobs/                                       │
│   s3://bucket/raw/linkedin_jobs/                                 │
│   s3://bucket/raw/reddit_subreddits/                             │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SNOWFLAKE RAW SCHEMA                          │
│   raw.hn_job_postings                                            │
│   raw.linkedin_postings                                          │
│   raw.linkedin_skills                                            │
│   raw.reddit_subreddit_stats                                     │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    dbt TRANSFORMATIONS                           │
├─────────────────────────────────────────────────────────────────┤
│  STAGING (1:1 with source, light cleaning)                       │
│  ├── stg_hn__job_postings                                        │
│  ├── stg_linkedin__postings                                      │
│  ├── stg_linkedin__skills                                        │
│  └── stg_reddit__subreddit_stats                                 │
├─────────────────────────────────────────────────────────────────┤
│  INTERMEDIATE (business logic, enrichment)                       │
│  ├── int_hn__skills_extracted          # NLP/regex extraction    │
│  ├── int_hn__roles_classified          # Role classification     │
│  ├── int_all__skills_standardized      # Canonical skill names   │
│  ├── int_all__technologies_tagged      # Technology taxonomy     │
│  └── int_all__monthly_aggregates       # Time-series rollup      │
├─────────────────────────────────────────────────────────────────┤
│  MARTS (analytics-ready, dimensional)                            │
│  ├── dim_technologies                  # Master tech list        │
│  ├── dim_roles                         # Role taxonomy           │
│  ├── dim_companies                     # Company dimension       │
│  ├── dim_locations                     # Location dimension      │
│  ├── dim_date                          # Date dimension          │
│  ├── fct_job_postings                  # Grain: 1 row per post   │
│  ├── fct_skill_mentions                # Grain: 1 row per skill  │
│  ├── fct_monthly_trends                # Pre-aggregated trends   │
│  └── fct_subreddit_growth              # Reddit metrics (Ph 2)   │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DASHBOARD                                │
│  • Technology trends over time                                   │
│  • Role demand changes                                           │
│  • Platform comparison (HN vs LinkedIn)                          │
│  • Subreddit growth (Phase 2)                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technology Taxonomy

### Domains to Track

**Data Engineering (Core)**
- Orchestration: Airflow, Dagster, Prefect, Mage
- Transformation: dbt, Spark, pandas
- Warehouses: Snowflake, BigQuery, Redshift, Databricks
- Streaming: Kafka, Flink, Kinesis, Spark Streaming
- Storage: S3, GCS, Delta Lake, Iceberg
- ETL/ELT: Fivetran, Airbyte, Stitch, AWS Glue

**Analytics Engineering**
- BI Tools: Tableau, Looker, Power BI, Metabase, Superset
- Semantic Layer: dbt Metrics, Cube, Looker LookML

**Machine Learning / AI**
- Classical ML: scikit-learn, XGBoost, LightGBM
- Deep Learning: PyTorch, TensorFlow, Keras
- LLMs: GPT, Claude, Llama, Mistral, OpenAI API
- MLOps: MLflow, Kubeflow, Weights & Biases, SageMaker
- Vector DBs: Pinecone, Weaviate, Chroma, pgvector

**Data Science**
- Analysis: pandas, numpy, scipy
- Visualization: matplotlib, plotly, seaborn

**Programming Languages**
- Python, SQL, Scala, Java, Go, Rust

### Role Taxonomy

**Tier 1: Core Data Roles**
- Data Engineer
- Analytics Engineer
- Data Analyst
- Data Scientist
- Data Architect

**Tier 2: Adjacent Roles**
- Machine Learning Engineer
- MLOps Engineer
- Platform Engineer / Data Platform Engineer
- BI Engineer / BI Developer
- ETL Developer
- Database Administrator (DBA)

**Tier 3: Overlapping Roles**
- Backend Engineer (data focus)
- Software Engineer, Data
- AI Engineer
- Site Reliability Engineer (data infra)

### Skill Standardization Examples
```
# Raw mention → Canonical name
"AWS Glue" → "AWS Glue"
"glue" → "AWS Glue" (context-dependent)
"dbt" → "dbt"
"data build tool" → "dbt"
"Snowflake DB" → "Snowflake"
"snowflake" → "Snowflake"
"k8s" → "Kubernetes"
"kubernetes" → "Kubernetes"
"postgres" → "PostgreSQL"
"psql" → "PostgreSQL"
"tf" → "Terraform" OR "TensorFlow" (context-dependent)
```

---

## Key Metrics & Questions

### Technology Trends
- How fast is [technology] growing in job mentions?
- When did [new technology] first appear in job posts?
- Is [old technology] declining?
- What technologies co-occur most frequently?

### Role Trends
- Is "Analytics Engineer" growing faster than "Data Engineer"?
- What happened to "Data Scientist" job volume post-2022?
- Are "MLOps Engineer" postings increasing?

### Platform Comparison
- Do HN startups want different skills than LinkedIn enterprise jobs?
- What's the remote work % difference between platforms?
- Are salaries mentioned more often on HN vs LinkedIn?

### Community Health (Phase 2)
- Which subreddit is growing fastest?
- What topics get the most engagement?
- How did major events (ChatGPT launch, tech layoffs) affect community activity?

---

## Data Source Details

### HN "Who Is Hiring" - HuggingFace Dataset
```python
from datasets import load_dataset
dataset = load_dataset("brusic/hacker-news-who-is-hiring-posts")
```
- Format: Parquet
- Content: All first-level comments from "Who Is Hiring" threads since April 2011
- Fields: id, by, text, time, parent (thread ID)
- Update frequency: Monthly (threads close after 2 weeks)

### HN "Who Is Hiring" - BigQuery (Backup/Validation)
```sql
-- Get all "Who Is Hiring" job posts
SELECT 
  c.id,
  c.by AS poster,
  c.text AS job_posting,
  c.time,
  TIMESTAMP_SECONDS(c.time) AS posted_at,
  p.title AS thread_title
FROM `bigquery-public-data.hacker_news.full` c
JOIN `bigquery-public-data.hacker_news.full` p ON c.parent = p.id
WHERE p.by = 'whoishiring'
  AND LOWER(p.title) LIKE '%who is hiring%'
  AND c.type = 'comment'
  AND c.dead IS NOT TRUE
  AND c.deleted IS NOT TRUE
  AND EXTRACT(YEAR FROM TIMESTAMP_SECONDS(c.time)) >= 2018;
```

### HN Firebase API (Incremental Updates)
```python
import requests

def get_who_is_hiring_posts(story_id):
    """Fetch all job posts from a Who Is Hiring thread."""
    base_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"
    
    # Get the thread
    thread = requests.get(base_url.format(story_id)).json()
    
    # Get all top-level comments (job posts)
    job_posts = []
    for comment_id in thread.get('kids', []):
        comment = requests.get(base_url.format(comment_id)).json()
        if comment and not comment.get('deleted') and not comment.get('dead'):
            job_posts.append(comment)
    
    return job_posts

# Example: January 2026 thread
# Find thread ID from: https://news.ycombinator.com/submitted?id=whoishiring
```

### LinkedIn Jobs - Kaggle Dataset
```python
import pandas as pd

# Download from: https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024
postings = pd.read_csv('linkedin_job_postings.csv')
skills = pd.read_csv('job_skills.csv')
summary = pd.read_csv('job_summary.csv')
```
- Format: CSV
- Size: 1.3M job postings
- Pre-extracted skills: Yes (job_skills.csv)
- Time period: January 2024 snapshot

### Reddit API (Phase 2)
```python
import praw

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="data-ai-index/1.0"
)

# Get subreddit stats
subreddit = reddit.subreddit("dataengineering")
print(f"Subscribers: {subreddit.subscribers}")
print(f"Active users: {subreddit.active_user_count}")

# Note: Historical subscriber data NOT available via API
# Need to scrape over time or use Pushshift archive
```

Target Subreddits:
- r/dataengineering (~250K subscribers)
- r/MachineLearning (~3M subscribers)
- r/datascience (~1M subscribers)
- r/LocalLLaMA (~500K subscribers)
- r/analytics (~100K subscribers)
- r/learnpython (~800K subscribers)
- r/SQL (~200K subscribers)

---

## Row Count Estimates

### Phase 1 (MVP)
| Table | Estimated Rows | Source |
|-------|----------------|--------|
| raw.hn_job_postings | 50,000 | HN 2018+ |
| raw.linkedin_postings | 1,300,000 | Kaggle |
| raw.linkedin_skills | 5,000,000+ | Kaggle (pre-extracted) |
| fct_skill_mentions (HN) | 300,000 | ~6 skills per HN post |
| **Total** | **6,500,000+** | |

### Phase 2 (With Reddit)
| Table | Estimated Rows | Source |
|-------|----------------|--------|
| raw.reddit_posts | 500,000+ | Top subreddits, 3 years |
| fct_subreddit_growth | 2,500 | 7 subreddits × 365 days |
| **Additional Total** | **500,000+** | |

---

## Airflow DAG Structure

```
dag_hn_extract (monthly)
├── task_fetch_latest_thread_id
├── task_extract_job_posts
├── task_upload_to_s3
└── task_trigger_dbt_run

dag_linkedin_load (one-time + optional refresh)
├── task_download_from_kaggle
├── task_upload_to_s3
└── task_load_to_snowflake

dag_reddit_extract (daily) [Phase 2]
├── task_fetch_subreddit_stats
├── task_fetch_recent_posts
├── task_upload_to_s3
└── task_trigger_dbt_run

dag_dbt_transform (triggered after extracts)
├── task_dbt_run_staging
├── task_dbt_run_intermediate
├── task_dbt_run_marts
└── task_dbt_test
```

---

## Development Approach

### Step 1: Get Data Locally First
Before building pipelines, manually download and explore:
1. Download HuggingFace HN dataset
2. Download Kaggle LinkedIn dataset
3. Explore in Jupyter notebook
4. Prototype skill extraction logic
5. Validate data quality and volume

### Step 2: Build dbt Models Locally
1. Set up dbt project structure
2. Build staging models
3. Build intermediate models (skill extraction, standardization)
4. Build mart models
5. Write tests (uniqueness, not null, accepted values)

### Step 3: Deploy to Cloud
1. Set up Snowflake (free trial)
2. Set up S3 bucket
3. Load raw data to S3 → Snowflake
4. Run dbt in cloud environment
5. Set up Airflow (local or managed)

### Step 4: Build Dashboard
1. Connect BI tool to Snowflake
2. Build core visualizations
3. Add interactivity (filters, drill-downs)

---

## File Structure

```
data-ai-interest-index/
├── CLAUDE.md                    # This file
├── README.md                    # Project overview
├── requirements.txt             # Python dependencies
│
├── extraction/                  # Python extraction scripts
│   ├── hn_extract.py           # HN API extraction
│   ├── linkedin_load.py        # Kaggle download + load
│   └── reddit_extract.py       # Reddit API extraction (Phase 2)
│
├── dbt/                        # dbt project
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_hn__job_postings.sql
│   │   │   ├── stg_linkedin__postings.sql
│   │   │   └── stg_linkedin__skills.sql
│   │   ├── intermediate/
│   │   │   ├── int_hn__skills_extracted.sql
│   │   │   ├── int_all__skills_standardized.sql
│   │   │   └── int_all__monthly_aggregates.sql
│   │   └── marts/
│   │       ├── dim_technologies.sql
│   │       ├── dim_roles.sql
│   │       ├── fct_job_postings.sql
│   │       └── fct_monthly_trends.sql
│   ├── seeds/
│   │   ├── skill_mappings.csv   # Raw → canonical skill mapping
│   │   └── role_keywords.csv    # Keywords for role classification
│   └── tests/
│
├── airflow/                     # Airflow DAGs
│   └── dags/
│       ├── dag_hn_extract.py
│       ├── dag_linkedin_load.py
│       └── dag_dbt_transform.py
│
├── notebooks/                   # Exploration notebooks
│   ├── 01_hn_data_exploration.ipynb
│   ├── 02_linkedin_data_exploration.ipynb
│   ├── 03_skill_extraction_prototype.ipynb
│   └── 04_dashboard_mockup.ipynb
│
└── infrastructure/              # IaC (optional)
    ├── terraform/
    └── docker-compose.yml
```

---

## Notes for Claude

### Tone
- Student is direct, uses colorful language, appreciates honesty
- Don't sugarcoat problems or overcomplicates explanations
- Get to the point

### Priorities
1. Working pipeline > perfect architecture
2. Phase 1 MVP first, don't scope creep
3. Validate data quality early (explore before building)
4. Show instructor the dbt skills (staging → intermediate → marts)

### Known Challenges
- HN job text is unstructured, skill extraction requires NLP/regex work
- LinkedIn dataset is a single snapshot (Jan 2024), no time-series
- YouTube historical data is not available via API
- Reddit API rate limits and no historical subscriber data

### Key Decisions Made
- Start with 2018+ data (modern data stack era)
- Don't pre-filter during extraction, filter in dbt
- Taxonomy discovery is part of the analysis, not just pre-defined
- Skip correlation analysis, let dashboard users draw conclusions
- Build narrow first, expand later (The Boner Principle™)

---

## Implementation Status (Complete)

### What Was Built

**Data Pipeline:**
- 93K+ HN job postings (2011-present) loaded to Snowflake
- 1.3M LinkedIn jobs snapshot loaded
- 81 GitHub repos tracked via API
- 10K posts processed through Claude Haiku for LLM skill extraction

**dbt Project (21 models):**
- 6 staging models (hn, linkedin, github, llm)
- 4 intermediate models (technology/role/database extraction)
- 11 mart models (facts + dimensions)
- 3 seed files (technology, role, database mappings)

**LLM Components:**
- `extraction/llm_skill_extraction.py` - Claude Haiku structured extraction
- `extraction/generate_weekly_insights.py` - Claude Sonnet market analysis
- `fct_llm_technology_mentions` - 63K technology mentions from 10K posts
- `fct_llm_vs_regex_comparison` - Agreement analysis between methods

### Dashboard Features (7 Pages)

| Page | Key Features |
|------|--------------|
| **Executive Summary** | Key metrics, headline findings, trend charts |
| **Technology Trends** | Time-series, YoY gainers/decliners, co-occurrence analysis, top technology pairs |
| **Role Trends** | Role mentions over time, tier filtering, top roles |
| **GitHub & LinkedIn** | Repo stats, LinkedIn skills, HN vs LinkedIn cross-validation |
| **LLM vs Regex** | Agreement rates, method comparison, LLM trends over time, side-by-side extraction comparison |
| **Data Explorer** | Table browser, job posting keyword search |
| **Methodology** | Data sources, pipeline, extraction methods, taxonomy, limitations |

### Key Findings (Validated)

| Finding | Evidence |
|---------|----------|
| Snowflake overtook Redshift | 1.6% vs 0.4% in 2024 (crossed in 2022) |
| PyTorch dominates TensorFlow | 2.0% vs 0.5% in 2025 (4x lead, flipped 2022) |
| OpenAI mentions exploded | 0.4% → 2.7% (2022-2025) |
| LLM extracts 4x more skills | 6.4 vs 1.5 technologies/post |
| PostgreSQL is king | 14% of HN posts (6x next database) |
| 2021 was peak hiring | 10,570 posts; 2023-24 ~40% of peak |

### Files Added Beyond Original Plan

```
extraction/
├── llm_skill_extraction.py      # Claude Haiku extraction (10K posts)
└── generate_weekly_insights.py  # Claude Sonnet weekly reports

dbt/models/staging/llm/
└── stg_llm__skill_extractions.sql

dbt/models/marts/
├── fct_llm_technology_mentions.sql
└── fct_llm_vs_regex_comparison.sql

docs/
├── WEEKLY_INSIGHTS_*.md         # Generated weekly reports
└── INSIGHTS.md                  # LLM vs regex analysis section
```

### What's Left

- [ ] Process remaining 83K+ posts with LLM (~$37, 4-6 hours)
- [ ] Expand regex taxonomy with LLM discoveries
- [ ] Deploy dashboard to Streamlit Cloud
