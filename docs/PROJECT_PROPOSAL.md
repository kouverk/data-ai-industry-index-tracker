# Project Proposal: Data & AI Industry Interest Index

## Executive Summary

This capstone project builds a **multi-source analytics platform** that tracks interest, demand, and growth signals across the data engineering and AI ecosystem. By combining job market data from Hacker News "Who Is Hiring" threads and LinkedIn postings with community engagement metrics from Reddit, this project creates a unified dashboard answering the question:

> **"What's hot, what's growing, what's dying in the data/AI space?"**

The project demonstrates modern data engineering practices including cloud data warehousing (Snowflake), transformation frameworks (dbt), workflow orchestration (Airflow), and dimensional modeling—while producing genuinely novel analysis that doesn't exist anywhere else.

---

## Motivation

### The Problem

The data engineering and AI fields are evolving rapidly. New tools emerge monthly (dbt, Dagster, Iceberg), roles shift and rename (ETL Developer → Data Engineer → Analytics Engineer), and technologies rise and fall (Hadoop → Spark → Snowflake). 

**But there's no single place to answer:**
- Is demand for Snowflake skills growing faster than Databricks?
- When did "Analytics Engineer" become a real job title?
- Are MLOps roles actually increasing, or is it just hype?
- How did ChatGPT's launch affect AI job postings?
- Which technologies should I learn next?

### Why This Matters

| Audience | Value |
|----------|-------|
| **Job Seekers** | Understand which skills are trending up/down to guide learning investments |
| **Bootcamps & Educators** | Data-driven curriculum decisions based on actual market demand |
| **Hiring Managers** | Benchmark job requirements against industry trends |
| **Practitioners** | Track the health and direction of their field |
| **Investors/Analysts** | Gauge technology adoption and market momentum |

### Why Now

The data ecosystem has matured enough that:
1. **Historical data exists**: HN "Who Is Hiring" has 13+ years of job posts (2011-present)
2. **Modern tooling is standardized**: dbt, Snowflake, Airflow are industry standards worth demonstrating
3. **Multiple signals are trackable**: Jobs, Reddit communities, and content ecosystems all produce measurable data
4. **AI boom creates urgency**: The 2023-2025 AI explosion makes tracking these trends more relevant than ever

---

## Why This Project Hasn't Been Done Before

### Existing Solutions and Their Gaps

I conducted a thorough analysis of existing projects in this space. While several tools track pieces of this data, **none combine multiple sources with proper data engineering practices**:

| Project | What It Does | Tech Stack | Gap |
|---------|--------------|------------|-----|
| **[hntrends.com](https://hntrends.com)** | Tracks tech mentions over time | Web app | No DE pipeline, no dimensional model, single source only |
| **[hnhiring.com](https://hnhiring.com)** | Job index/search | Web app, basic DB | No analytics, no transformations, no trend analysis |
| **[hnjobs](https://github.com/nchelluri/hnjobs)** - "A private Hacker News 'Who is hiring?' thread filter and search tool" | Filter/search tool | Go, localStorage | Frontend only, no pipeline, no persistence |
| **[sojobs](https://github.com/drorm/sojobs)** - "Scans the jobs from the monthly hacker news 'who is hiring' thread and loads them into a database" | DB + search | Postgres, Node | Basic ETL, no dimensional model, no cloud |
| **[hn-whoishiring](https://github.com/gabfl/hn-whoishiring)** - "A FastUI/FastAPI app to manage Hacker News's 'Who is Hiring' postings... uses SQLite for data storage" | Scraper + UI | FastAPI, SQLite | No cloud DW, no dbt, local only |
| **[hn-hiring](https://github.com/nickmancol/hn-hiring)** - "A simple dashboard based on Hacker News' Who is hiring posts... tagging process try to identify common aspects of the post" | Dashboard + tagging | Python, Vue, dc.js | Local only, no cloud pipeline, limited taxonomy |
| **[hn-new-jobs](https://github.com/nemanjam/hn-new-jobs)** - "A website that provides obvious, effortless and deep insights into fresh and recurring job opportunities" | Company tracking | Web app | No dbt/Snowflake, no cross-platform analysis |

### What About LinkedIn Job Analysis?

One existing project uses the same LinkedIn dataset:
- **[job_posting_analytics](https://github.com/mar1-k/job_posting_analytics)** - "A Data Engineering project for visualizing the top skills demanded by roles based on parsing of LinkedIn job postings" (DataTalks.Club Zoomcamp 2024 capstone)

**Gap:** This project analyzes LinkedIn only. No HN comparison, no community metrics, no cross-platform analysis.

### The Unique Contribution

This project is differentiated by:

| Aspect | Existing Projects | This Project |
|--------|-------------------|--------------|
| **Data Sources** | Single source (HN only OR LinkedIn only) | Multiple sources (HN + LinkedIn + Reddit) |
| **Tech Stack** | SQLite, local scripts, basic web apps | Snowflake, dbt, Airflow (industry standard) |
| **Data Modeling** | Flat tables, no dimensional model | Proper dimensional model (facts + dimensions) |
| **Analysis Depth** | Basic counts, simple search | Technology taxonomy, role classification, trend analysis |
| **Cross-Platform** | None | Compare HN startup jobs vs LinkedIn enterprise jobs |
| **Reproducibility** | Ad-hoc scripts | Orchestrated, tested, documented pipeline |

---

## Project Scope

### Phase 1: MVP (Core Deliverable)

**Objective:** Build a working end-to-end pipeline demonstrating data engineering skills with two distinct data sources.

**Data Sources:**
1. **Hacker News "Who Is Hiring"** (2018-present)
   - Source: HuggingFace dataset `brusic/hacker-news-who-is-hiring-posts`
   - Format: Parquet
   - Volume: ~50,000 job postings
   - Refresh: Monthly via HN Firebase API

2. **LinkedIn Jobs Dataset**
   - Source: Kaggle `asaniczka/1-3m-linkedin-jobs-and-skills-2024`
   - Format: CSV
   - Volume: 1.3M job postings + pre-extracted skills
   - Refresh: Static snapshot (January 2024)

**Deliverables:**
- [ ] Extraction scripts for both sources
- [ ] S3 landing zone with raw data
- [ ] Snowflake raw schema loaded
- [ ] dbt project with staging → intermediate → marts layers
- [ ] Skill extraction from unstructured HN text
- [ ] Technology taxonomy (canonical skill names)
- [ ] Role classification logic
- [ ] Monthly trend aggregations
- [ ] Dashboard with core visualizations
- [ ] Airflow DAGs for orchestration
- [ ] Documentation and tests

### Phase 2: Stretch Goals

**Objective:** Add community engagement signals to create a more complete industry health picture.

**Additional Data Source:**
3. **Reddit Subreddit Metrics**
   - Subreddits: r/dataengineering, r/MachineLearning, r/datascience, r/LocalLLaMA
   - Metrics: Subscriber growth, post volume, engagement rates
   - Source: Reddit API + historical archives

**Additional Deliverables:**
- [ ] Reddit extraction pipeline
- [ ] Subreddit growth tracking
- [ ] Discussion topic analysis
- [ ] Cross-platform dashboard views

### Phase 3: Future Enhancements

**Potential additions (not in scope for capstone):**
- Google Trends integration
- YouTube channel growth tracking (if historical data source found)
- Stack Overflow question volume
- Salary trend analysis (from HN posts that include compensation)

---

## Technical Architecture

### Stack Selection

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Warehouse** | Snowflake | Industry standard, free trial, scales well |
| **Transformation** | dbt | Required for bootcamp, demonstrates analytics engineering |
| **Orchestration** | Airflow | Required for bootcamp, industry standard |
| **Storage** | S3 | Landing zone for raw data before warehouse load |
| **Extraction** | Python | Flexible, good library support for APIs |
| **Visualization** | Metabase/Looker/Streamlit | TBD based on preference |

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              EXTRACTION                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐       │
│   │   HuggingFace   │   │     Kaggle      │   │   Reddit API    │       │
│   │   HN Dataset    │   │ LinkedIn Jobs   │   │   (Phase 2)     │       │
│   │   (Parquet)     │   │    (CSV)        │   │    (JSON)       │       │
│   └────────┬────────┘   └────────┬────────┘   └────────┬────────┘       │
│            │                     │                     │                 │
│            ▼                     ▼                     ▼                 │
│   ┌─────────────────────────────────────────────────────────────┐       │
│   │                    Python Extraction Scripts                 │       │
│   │                    (hn_extract.py, linkedin_load.py)         │       │
│   └─────────────────────────────┬───────────────────────────────┘       │
│                                 │                                        │
└─────────────────────────────────┼────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              STORAGE                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────┐       │
│   │                     S3 Landing Zone                          │       │
│   │   s3://bucket/raw/hn_jobs/*.parquet                         │       │
│   │   s3://bucket/raw/linkedin/*.csv                            │       │
│   │   s3://bucket/raw/reddit/*.json                             │       │
│   └─────────────────────────────┬───────────────────────────────┘       │
│                                 │                                        │
│                                 ▼                                        │
│   ┌─────────────────────────────────────────────────────────────┐       │
│   │                 Snowflake RAW Schema                         │       │
│   │   raw.hn_job_postings                                        │       │
│   │   raw.linkedin_postings                                      │       │
│   │   raw.linkedin_skills                                        │       │
│   └─────────────────────────────┬───────────────────────────────┘       │
│                                 │                                        │
└─────────────────────────────────┼────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           TRANSFORMATION                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────┐       │
│   │                      dbt Project                             │       │
│   ├─────────────────────────────────────────────────────────────┤       │
│   │  STAGING (source-conformed)                                  │       │
│   │  ├── stg_hn__job_postings                                    │       │
│   │  ├── stg_linkedin__postings                                  │       │
│   │  └── stg_linkedin__skills                                    │       │
│   ├─────────────────────────────────────────────────────────────┤       │
│   │  INTERMEDIATE (business logic)                               │       │
│   │  ├── int_hn__skills_extracted      ← NLP/regex parsing       │       │
│   │  ├── int_hn__roles_classified      ← Role taxonomy           │       │
│   │  ├── int_all__skills_standardized  ← Canonical names         │       │
│   │  └── int_all__monthly_aggregates   ← Time-series rollup      │       │
│   ├─────────────────────────────────────────────────────────────┤       │
│   │  MARTS (analytics-ready)                                     │       │
│   │  ├── dim_technologies                                        │       │
│   │  ├── dim_roles                                               │       │
│   │  ├── dim_companies                                           │       │
│   │  ├── dim_date                                                │       │
│   │  ├── fct_job_postings                                        │       │
│   │  ├── fct_skill_mentions                                      │       │
│   │  └── fct_monthly_trends                                      │       │
│   └─────────────────────────────┬───────────────────────────────┘       │
│                                 │                                        │
└─────────────────────────────────┼────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────┐       │
│   │                       Dashboard                              │       │
│   │                                                              │       │
│   │   ┌─────────────────┐  ┌─────────────────┐                  │       │
│   │   │  Technology     │  │    Role         │                  │       │
│   │   │  Trends         │  │    Trends       │                  │       │
│   │   └─────────────────┘  └─────────────────┘                  │       │
│   │                                                              │       │
│   │   ┌─────────────────┐  ┌─────────────────┐                  │       │
│   │   │  Platform       │  │  Community      │                  │       │
│   │   │  Comparison     │  │  Growth (Ph 2)  │                  │       │
│   │   └─────────────────┘  └─────────────────┘                  │       │
│   │                                                              │       │
│   └─────────────────────────────────────────────────────────────┘       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Orchestration

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          AIRFLOW DAGS                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   dag_hn_extract (Monthly)                                               │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐            │
│   │  Fetch   │──▶│ Extract  │──▶│ Upload   │──▶│ Trigger  │            │
│   │ Thread ID│   │  Posts   │   │  to S3   │   │ dbt Run  │            │
│   └──────────┘   └──────────┘   └──────────┘   └──────────┘            │
│                                                                          │
│   dag_linkedin_load (One-time)                                           │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐                            │
│   │ Download │──▶│ Upload   │──▶│  Load    │                            │
│   │ Kaggle   │   │  to S3   │   │ Snowflake│                            │
│   └──────────┘   └──────────┘   └──────────┘                            │
│                                                                          │
│   dag_dbt_transform (Triggered)                                          │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐            │
│   │   Run    │──▶│   Run    │──▶│   Run    │──▶│   Run    │            │
│   │ Staging  │   │  Intermd │   │  Marts   │   │  Tests   │            │
│   └──────────┘   └──────────┘   └──────────┘   └──────────┘            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Dimensional Model

### Fact Tables

**fct_job_postings**
- Grain: One row per job posting
- Measures: posting_count (always 1, for aggregation)
- Foreign Keys: date_key, company_key, location_key, role_key, platform_key

**fct_skill_mentions**
- Grain: One row per skill mention per job posting
- Measures: mention_count (always 1, for aggregation)
- Foreign Keys: job_posting_key, technology_key, date_key

**fct_monthly_trends**
- Grain: One row per technology per month
- Measures: job_count, mention_count, pct_of_jobs
- Foreign Keys: technology_key, date_key

### Dimension Tables

**dim_technologies**
- technology_key (surrogate)
- technology_name (canonical name: "Snowflake", "dbt", "Kubernetes")
- technology_category (Warehouse, Orchestration, Language, etc.)
- aliases (array of variations: ["k8s", "kubernetes", "kube"])

**dim_roles**
- role_key (surrogate)
- role_name (canonical: "Data Engineer", "Analytics Engineer")
- role_tier (Core, Adjacent, Overlapping)
- keywords (array for classification)

**dim_companies**
- company_key (surrogate)
- company_name
- is_yc_company (boolean, for HN)
- first_seen_date
- total_postings

**dim_locations**
- location_key (surrogate)
- location_raw (original text)
- city, state, country (parsed)
- is_remote (boolean)

**dim_date**
- date_key (surrogate)
- full_date
- year, quarter, month, week
- month_name, is_weekend

**dim_platform**
- platform_key (surrogate)
- platform_name ("Hacker News", "LinkedIn")
- platform_type ("Job Board", "Social Network")

---

## Analysis Capabilities

### Questions This Dashboard Will Answer

**Technology Trends**
- How fast is [Snowflake/Databricks/dbt/Airflow] growing in job mentions?
- When did [technology] first appear in job postings?
- Is [Hadoop/ETL/on-prem] declining?
- What technologies are most commonly requested together?
- How quickly did "LLM" appear in job requirements after ChatGPT launched?

**Role Evolution**
- Is "Analytics Engineer" growing faster than "Data Engineer"?
- What happened to "Data Scientist" job volume post-2022?
- Are "MLOps Engineer" postings actually increasing?
- How did role titles evolve over time?

**Platform Comparison**
- Do HN startups want different skills than LinkedIn enterprise companies?
- What's the remote work % difference between platforms?
- Are salaries mentioned more often on HN vs LinkedIn?
- Which platform has more AI/ML job focus?

**Market Events**
- How did COVID affect remote data engineering jobs?
- Did the 2022-2023 tech layoffs show up in HN posting volume?
- What was the ChatGPT effect on AI job postings?

**Community Health (Phase 2)**
- Which data/AI subreddit is growing fastest?
- What topics generate the most engagement in r/dataengineering?
- How does Reddit discussion volume correlate with job market activity?

---

## Data Volume Estimates

### Phase 1 MVP

| Table | Estimated Rows | Source |
|-------|----------------|--------|
| `raw.hn_job_postings` | 50,000 | HN 2018-present |
| `raw.linkedin_postings` | 1,300,000 | Kaggle |
| `raw.linkedin_skills` | 5,000,000+ | Kaggle (pre-extracted) |
| `fct_job_postings` | 1,350,000 | Combined HN + LinkedIn |
| `fct_skill_mentions` | 6,000,000+ | ~4-6 skills per job |
| `fct_monthly_trends` | 10,000 | ~100 technologies × 84 months |
| `dim_technologies` | 500+ | Unique technologies tracked |
| `dim_companies` | 50,000+ | Unique companies |
| **Total** | **~13,000,000+** | |

### Requirements Check

| Requirement | Target | Actual | Status |
|-------------|--------|--------|--------|
| Data sources | 2+ | 2 (HN + LinkedIn), 3 with Reddit | ✅ |
| Row count | 1,000,000+ | 13,000,000+ | ✅ |
| Different formats | Required | Parquet, CSV, JSON | ✅ |
| Original analysis | Required | Cross-platform job market analysis | ✅ |

---

## Development Timeline

### Week 1-2: Data Exploration & Prototyping
- [ ] Download and explore HN dataset
- [ ] Download and explore LinkedIn dataset
- [ ] Prototype skill extraction logic in Jupyter
- [ ] Define initial technology taxonomy
- [ ] Validate data quality and volume

### Week 3-4: Pipeline Infrastructure
- [ ] Set up Snowflake account and schemas
- [ ] Set up S3 bucket structure
- [ ] Write extraction scripts
- [ ] Load raw data to Snowflake
- [ ] Set up dbt project structure

### Week 5-6: dbt Transformations
- [ ] Build staging models
- [ ] Build intermediate models (skill extraction, standardization)
- [ ] Build mart models (facts and dimensions)
- [ ] Write dbt tests
- [ ] Document models

### Week 7-8: Orchestration & Dashboard
- [ ] Set up Airflow (local or managed)
- [ ] Create DAGs for extraction and transformation
- [ ] Build dashboard visualizations
- [ ] Add interactivity (filters, drill-downs)
- [ ] Documentation and presentation prep

### Week 9+ (Stretch): Phase 2
- [ ] Add Reddit data source
- [ ] Expand dashboard with community metrics

---

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| HN skill extraction is harder than expected | High | Medium | Start with simple regex, iterate; use pre-extracted LinkedIn skills as validation |
| Snowflake free trial expires | High | Low | Monitor usage; project should complete within trial period |
| LinkedIn dataset too large for local dev | Medium | Medium | Sample during development; full load only for final pipeline |
| Reddit API rate limits block extraction | Medium | Medium | This is Phase 2; can deprioritize if needed |
| Taxonomy too complex to maintain | Medium | Medium | Start with top 50 technologies, expand incrementally |
| Scope creep | High | High | Strict Phase 1 focus; no Phase 2 until MVP complete |

---

## Success Criteria

### Minimum Viable Product (Must Have)
- [ ] Two data sources loaded and transformed (HN + LinkedIn)
- [ ] Working dbt project with staging/intermediate/marts layers
- [ ] At least one Airflow DAG orchestrating the pipeline
- [ ] Dashboard showing technology trends over time
- [ ] Documentation sufficient for another engineer to understand and run

### Target (Should Have)
- [ ] Complete technology taxonomy with 50+ technologies
- [ ] Role classification working
- [ ] Platform comparison visualizations
- [ ] dbt tests passing
- [ ] Incremental loading for HN data

### Stretch (Nice to Have)
- [ ] Reddit data source integrated
- [ ] Community growth metrics
- [ ] Salary trend analysis
- [ ] Interactive dashboard with drill-downs

---

## Appendix A: Data Source Details

### HN "Who Is Hiring" - HuggingFace
```python
from datasets import load_dataset

# Load the pre-built dataset
dataset = load_dataset("brusic/hacker-news-who-is-hiring-posts")

# Each row contains:
# - id: Comment ID
# - by: Username of poster
# - text: Full job posting text (HTML)
# - time: Unix timestamp
# - parent: Thread ID
```

### HN "Who Is Hiring" - BigQuery (Alternative)
```sql
SELECT 
  c.id,
  c.by AS poster,
  c.text AS job_posting,
  TIMESTAMP_SECONDS(c.time) AS posted_at,
  p.title AS thread_title
FROM `bigquery-public-data.hacker_news.full` c
JOIN `bigquery-public-data.hacker_news.full` p ON c.parent = p.id
WHERE p.by = 'whoishiring'
  AND LOWER(p.title) LIKE '%who is hiring%'
  AND c.type = 'comment'
  AND c.dead IS NOT TRUE
  AND c.deleted IS NOT TRUE
  AND EXTRACT(YEAR FROM TIMESTAMP_SECONDS(c.time)) >= 2018
```

### LinkedIn Jobs - Kaggle
```python
import pandas as pd

# Download from Kaggle: asaniczka/1-3m-linkedin-jobs-and-skills-2024
postings = pd.read_csv('linkedin_job_postings.csv')
skills = pd.read_csv('job_skills.csv')  # Pre-extracted skills!
summary = pd.read_csv('job_summary.csv')

# Key fields in postings:
# - job_link: Unique identifier
# - job_title: Role title
# - company: Company name
# - job_location: Location string
# - search_position: Ranking
# - job_level: Seniority

# Key fields in skills:
# - job_link: Foreign key to postings
# - job_skills: Skill name
```

### Reddit API (Phase 2)
```python
import praw

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="data-ai-index/1.0"
)

# Target subreddits
subreddits = [
    "dataengineering",    # ~250K subscribers
    "MachineLearning",    # ~3M subscribers
    "datascience",        # ~1M subscribers
    "LocalLLaMA",         # ~500K subscribers
    "analytics",          # ~100K subscribers
]

# Get current stats (historical not available via API)
for name in subreddits:
    sub = reddit.subreddit(name)
    print(f"{name}: {sub.subscribers} subscribers")
```

---

## Appendix B: Technology Taxonomy (Initial)

### Data Engineering - Orchestration
`Airflow`, `Dagster`, `Prefect`, `Mage`, `Luigi`, `Argo`

### Data Engineering - Transformation
`dbt`, `Spark`, `pandas`, `Polars`, `dask`

### Data Engineering - Warehouses
`Snowflake`, `BigQuery`, `Redshift`, `Databricks`, `Azure Synapse`, `ClickHouse`

### Data Engineering - Streaming
`Kafka`, `Flink`, `Kinesis`, `Spark Streaming`, `Pulsar`

### Data Engineering - Storage
`S3`, `GCS`, `Azure Blob`, `Delta Lake`, `Iceberg`, `Hudi`

### Data Engineering - ETL/ELT Tools
`Fivetran`, `Airbyte`, `Stitch`, `AWS Glue`, `Matillion`

### Analytics - BI Tools
`Tableau`, `Looker`, `Power BI`, `Metabase`, `Superset`, `Mode`

### Machine Learning - Frameworks
`scikit-learn`, `XGBoost`, `LightGBM`, `PyTorch`, `TensorFlow`, `Keras`

### Machine Learning - LLMs
`GPT`, `Claude`, `Llama`, `Mistral`, `Gemini`, `OpenAI API`

### Machine Learning - MLOps
`MLflow`, `Kubeflow`, `Weights & Biases`, `SageMaker`, `Vertex AI`

### Machine Learning - Vector DBs
`Pinecone`, `Weaviate`, `Chroma`, `pgvector`, `Milvus`

### Languages
`Python`, `SQL`, `Scala`, `Java`, `Go`, `Rust`, `R`

### Infrastructure
`Kubernetes`, `Docker`, `Terraform`, `AWS`, `GCP`, `Azure`

---

## Appendix C: Sample Dashboard Mockups

### Panel 1: Technology Trends Over Time
```
[Line Chart]
X-axis: Month (2018-01 to 2025-01)
Y-axis: % of job postings mentioning technology
Lines: Snowflake, Databricks, BigQuery, Redshift

Shows: Snowflake overtaking Redshift around 2021
       Databricks rapid growth 2022-2024
```

### Panel 2: Technology Co-occurrence Heatmap
```
[Heatmap]
Rows/Cols: Top 20 technologies
Color: Frequency of appearing together in same job posting

Shows: dbt + Snowflake high correlation
       Airflow + Python high correlation
       PyTorch + TensorFlow low correlation (substitutes)
```

### Panel 3: Role Evolution
```
[Stacked Area Chart]
X-axis: Month
Y-axis: Number of job postings
Areas: Data Engineer, Analytics Engineer, Data Scientist, ML Engineer

Shows: Analytics Engineer emergence ~2019
       Data Scientist plateau ~2022
```

### Panel 4: Platform Comparison
```
[Grouped Bar Chart]
X-axis: Technology
Y-axis: % of postings
Groups: HN "Who Is Hiring" vs LinkedIn

Shows: HN higher in emerging tech (dbt, Dagster)
       LinkedIn higher in enterprise (Tableau, Azure)
```

---

## References

1. HuggingFace HN Dataset: https://huggingface.co/datasets/brusic/hacker-news-who-is-hiring-posts
2. Kaggle LinkedIn Dataset: https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024
3. BigQuery HN Dataset: https://console.cloud.google.com/bigquery?p=bigquery-public-data&d=hacker_news
4. HN Firebase API: https://github.com/HackerNews/API
5. Reddit API: https://www.reddit.com/dev/api/
6. dbt Documentation: https://docs.getdbt.com/
7. Snowflake Documentation: https://docs.snowflake.com/
8. Airflow Documentation: https://airflow.apache.org/docs/
