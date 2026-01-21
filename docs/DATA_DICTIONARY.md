# Data Dictionary

This document describes the data sources, exploration scripts, and taxonomy definitions used in the Data & AI Industry Interest Index project.

---

## Data Sources

### 1. Hacker News "Who Is Hiring" (HN)

| Attribute | Value |
|-----------|-------|
| **Source** | HuggingFace `brusic/hacker-news-who-is-hiring-posts` |
| **Format** | Parquet |
| **Coverage** | April 2011 - Present |
| **Row Count** | ~93,000 total posts |
| **Update Frequency** | Monthly |

**Schema (flattened):**

| Column | Type | Description |
|--------|------|-------------|
| `thread_month` | string | Month name and year (e.g., "December 2025") |
| `thread_type` | string | Thread type ("permanent", "freelancer", etc.) |
| `parent_id` | int | HN thread/story ID |
| `id` | int | HN comment ID (unique per post) |
| `by` | string | HN username of poster |
| `text` | string | Job posting text (HTML-encoded) |
| `posted_at` | datetime | Parsed date from thread_month |
| `year` | int | Year extracted from posted_at |
| `year_month` | period | Year-month period |

**Notes:**
- Text is HTML-encoded (e.g., `&#x2F;` for `/`, `&amp;` for `&`)
- No per-comment timestamp; uses thread month for time bucketing
- Skill extraction requires NLP/regex processing

---

### 2. LinkedIn Jobs (Kaggle)

| Attribute | Value |
|-----------|-------|
| **Source** | Kaggle `asaniczka/1-3m-linkedin-jobs-and-skills-2024` |
| **Format** | CSV (3 files) |
| **Coverage** | January 2024 snapshot |
| **Row Count** | 1.3M job postings |

**Files:**

#### `linkedin_job_postings.csv` (1.3M rows)

| Column | Type | Description |
|--------|------|-------------|
| `job_link` | string | Unique job URL (primary key) |
| `last_processed_time` | string | Timestamp of data collection |
| `job_title` | string | Job title |
| `company` | string | Company name |
| `job_location` | string | Location string |
| `first_seen` | string | When job was first observed |
| `search_city` | string | City used in search |
| `search_country` | string | Country used in search |
| `job_level` | string | Seniority level |
| `job_type` | string | Employment type |

#### `job_skills.csv` (1.3M rows)

| Column | Type | Description |
|--------|------|-------------|
| `job_link` | string | Foreign key to job_postings |
| `job_skills` | string | Comma-separated list of skills |

**Note:** Skills are stored as one comma-separated string per job, not normalized. Requires splitting in transformation.

#### `job_summary.csv` (1.3M rows)

| Column | Type | Description |
|--------|------|-------------|
| `job_link` | string | Foreign key to job_postings |
| `job_summary` | string | Full job description text |

---

### 3. GitHub Repository Stats

| Attribute | Value |
|-----------|-------|
| **Source** | GitHub REST API |
| **Format** | JSON/CSV |
| **Coverage** | Current snapshot (daily refresh in pipeline) |
| **Row Count** | 81 repositories tracked |
| **Update Frequency** | Daily |

**Schema:**

| Column | Type | Description |
|--------|------|-------------|
| `repo` | string | Repository identifier (owner/repo) |
| `category` | string | Category from taxonomy (orchestration, transformation, etc.) |
| `stars` | int | Star count (popularity metric) |
| `forks` | int | Fork count (contribution/usage metric) |
| `open_issues` | int | Open issue count (activity metric) |
| `language` | string | Primary programming language |
| `created_at` | datetime | Repository creation date |
| `pushed_at` | datetime | Last push date |
| `license` | string | SPDX license identifier |
| `fetched_at` | datetime | When data was collected |

**Categories tracked:**
- `orchestration` (7 repos): Airflow, Dagster, Prefect, etc.
- `transformation` (6 repos): dbt, Spark, pandas, Polars, etc.
- `warehouse` (4 repos): ClickHouse, DuckDB, etc.
- `streaming` (5 repos): Kafka, Flink, Pulsar, etc.
- `table_format` (4 repos): Delta Lake, Iceberg, Hudi
- `etl_elt` (4 repos): Airbyte, Meltano, dlt
- `bi` (5 repos): Metabase, Superset, Redash, etc.
- `ml_framework` (8 repos): PyTorch, TensorFlow, scikit-learn, etc.
- `llm` (8 repos): LangChain, Transformers, Ollama, etc.
- `mlops` (6 repos): MLflow, Kubeflow, W&B, etc.
- `vector_db` (6 repos): Chroma, Qdrant, Milvus, etc.
- `data_quality` (4 repos): Great Expectations, DataHub, etc.
- `infrastructure` (5 repos): Kubernetes, Docker, Terraform, etc.
- `database` (9 repos): PostgreSQL, Redis, MongoDB, etc.

**Notes:**
- No auth required for basic stats (60 req/hour)
- With GITHUB_TOKEN: 5000 req/hour
- Historical star counts require separate API or third-party tools
- Provides "developer interest" signal complementing job market data

---

## Exploration Scripts

### `exploration/01_explore_hn_data.py`

**Purpose:** Download and explore the HN "Who Is Hiring" dataset.

**What it does:**
1. Loads data from HuggingFace
2. Flattens nested thread/comments structure into individual posts
3. Computes basic statistics (row counts, nulls)
4. Analyzes time distribution (posts per year)
5. Samples job postings for manual review
6. Checks keyword frequency for common terms

**Outputs:**
- `data/raw/hn_who_is_hiring.parquet` - Full flattened dataset
- `data/raw/hn_sample_100.csv` - 100 sample posts for manual review

---

### `exploration/02_explore_linkedin_data.py`

**Purpose:** Explore the Kaggle LinkedIn dataset.

**Prerequisite:** Download dataset from Kaggle and extract to `data/raw/linkedin/`

**What it does:**
1. Loads all three CSV files
2. Analyzes schema and data quality
3. Examines pre-extracted skills format
4. Filters for data engineering relevant jobs
5. Analyzes join relationships between tables

**Outputs:**
- `data/raw/linkedin_de_jobs_sample.csv` - 500 DE/ML job samples
- `data/raw/linkedin_top_skills.csv` - Top 200 skill strings

---

### `exploration/03_skill_extraction_prototype.py`

**Purpose:** Prototype and test skill/role extraction logic on HN data.

**What it does:**
1. Loads taxonomy definitions from `taxonomy.py`
2. Applies extraction functions to HN posts
3. Reports role/technology/database frequencies
4. Shows trends over time (2018-2025)
5. Outputs sample extractions for validation

**Outputs:**
- `data/processed/hn_with_extractions.parquet` - HN data enriched with extracted roles, technologies, and databases

---

### `exploration/04_explore_github_data.py`

**Purpose:** Fetch and explore GitHub repository stats for tools in our taxonomy.

**What it does:**
1. Defines 81 repositories across 14 categories
2. Fetches current stats from GitHub API (stars, forks, issues)
3. Compares tools within categories (Airflow vs Dagster vs Prefect)
4. Sorts by popularity and category

**Outputs:**
- `data/raw/github_repo_stats.json` - Full API response with metadata
- `data/raw/github_repo_stats.csv` - Simplified CSV for quick viewing

**Notes:**
- Requires GITHUB_TOKEN env var for higher rate limits (5000/hr vs 60/hr)
- Run daily in pipeline to build historical trend data

---

## Taxonomy Definitions

### `exploration/taxonomy.py`

**Purpose:** Central definitions for all role, technology, and database taxonomies.

**Structure:**

Each taxonomy is a Python dictionary mapping canonical names to configuration:

```python
"Canonical Name": {
    "keywords": ["exact", "phrases", "to match"],
    "variations": ["abbrev", "fuzzy"],
    "category": "category_name",
    "era": "legacy|modern|current",
    "tier": 1,  # for roles only
    "require_word_boundary": True,  # optional
}
```

---

### Role Taxonomy (27 roles)

| Tier | Description | Example Roles |
|------|-------------|---------------|
| 1 | Core Data Roles | Data Engineer, Analytics Engineer, Data Scientist |
| 2 | Adjacent Data Roles | ML Engineer, BI Engineer, DBA, Data Warehouse Engineer |
| 3 | AI/ML Specialized | AI Engineer, NLP Engineer, LLM Engineer |
| 4 | Historical/Legacy | Hadoop Developer, Statistician, Report Developer |
| 5 | Overlapping Tech | Software Engineer, Backend Engineer, DevOps |

---

### Technology Taxonomy (171 technologies)

| Category | Count | Examples |
|----------|-------|----------|
| `orchestration` | 12 | Airflow, Dagster, Prefect, Oozie |
| `transformation` | 11 | dbt, Spark, pandas, Hive, Presto |
| `warehouse_cloud` | 9 | Snowflake, BigQuery, Redshift, Databricks |
| `warehouse_legacy` | 7 | Teradata, Oracle, Netezza, Vertica |
| `streaming` | 11 | Kafka, Flink, Kinesis, Storm |
| `table_format` | 6 | Delta Lake, Iceberg, Hudi, Parquet |
| `cloud_storage` | 4 | S3, GCS, Azure Blob, HDFS |
| `etl_elt` | 12 | Fivetran, Airbyte, Informatica, SSIS |
| `bi` | 16 | Tableau, Looker, Power BI, Cognos |
| `ml_classical` | 7 | scikit-learn, XGBoost, SAS, SPSS |
| `ml_deep` | 7 | PyTorch, TensorFlow, Keras, Theano |
| `llm` | 11 | OpenAI, Claude, Llama, LangChain |
| `mlops` | 12 | MLflow, SageMaker, Weights & Biases |
| `vector_db` | 7 | Pinecone, Weaviate, Chroma, pgvector |
| `language` | 10 | Python, SQL, Scala, Java, Go, Rust |
| `infrastructure` | 6 | Kubernetes, Docker, Terraform |
| `cloud` | 3 | AWS, GCP, Azure |
| `big_data` | 10 | Hadoop, HBase, Impala, Cloudera |
| `data_quality` | 4 | Great Expectations, Monte Carlo, Soda |
| `data_catalog` | 6 | DataHub, Atlan, Alation, Collibra |

**Era classifications:**
- `legacy` - Pre-2015 technologies (Hadoop ecosystem, on-prem warehouses)
- `modern` - 2015-2020 technologies (Cloud warehouses, Kubernetes)
- `current` - 2020+ technologies (LLMs, lakehouse formats, vector DBs)

---

### Database Taxonomy (33 databases)

| Category | Count | Examples |
|----------|-------|----------|
| `relational_oss` | 6 | PostgreSQL, MySQL, MariaDB, SQLite |
| `relational_commercial` | 3 | Oracle, SQL Server, DB2 |
| `nosql_document` | 5 | MongoDB, DynamoDB, Couchbase |
| `nosql_kv` | 3 | Redis, Memcached, etcd |
| `nosql_column` | 2 | Cassandra, ScyllaDB |
| `nosql_graph` | 5 | Neo4j, Neptune, JanusGraph |
| `search` | 5 | Elasticsearch, OpenSearch, Solr |
| `timeseries` | 4 | InfluxDB, TimescaleDB, Prometheus |

---

## Processed Data

### `data/processed/hn_with_extractions.parquet`

HN data enriched with extraction results.

| Column | Type | Description |
|--------|------|-------------|
| (all original columns) | | From raw HN data |
| `roles` | list[str] | Extracted role names |
| `role_count` | int | Number of roles extracted |
| `technologies` | list[str] | Extracted technology names |
| `tech_count` | int | Number of technologies extracted |
| `databases` | list[str] | Extracted database names |
| `db_count` | int | Number of databases extracted |

---

## File Structure

```
data-ai-industry-index-tracker/
├── docs/
│   ├── DATA_DICTIONARY.md     # This file
│   └── INSIGHTS.md            # Analysis insights
├── exploration/
│   ├── 01_explore_hn_data.py
│   ├── 02_explore_linkedin_data.py
│   ├── 03_skill_extraction_prototype.py
│   ├── 04_explore_github_data.py
│   └── taxonomy.py
├── data/
│   ├── raw/
│   │   ├── hn_who_is_hiring.parquet
│   │   ├── hn_sample_100.csv
│   │   ├── github_repo_stats.json
│   │   ├── github_repo_stats.csv
│   │   └── linkedin/
│   │       ├── linkedin_job_postings.csv
│   │       ├── job_skills.csv
│   │       └── job_summary.csv
│   └── processed/
│       └── hn_with_extractions.parquet
├── requirements.txt
├── CLAUDE.md
└── PROJECT_PROPOSAL.md
```
