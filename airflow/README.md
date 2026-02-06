# Airflow DAGs for Data & AI Industry Index

## DAGs

| DAG | Schedule | Description |
|-----|----------|-------------|
| `github_daily_stats` | Daily @ 6 AM UTC | Fetches GitHub repo stats (stars, forks, activity) |
| `hn_monthly_hiring` | 2nd of month @ 12 PM UTC | Extracts HN "Who Is Hiring" from HuggingFace |
| `dbt_transform` | Manual trigger | Runs dbt models (staging → intermediate → marts) |
| `dbt_full_refresh` | Daily @ 7 AM UTC | Full dbt refresh after GitHub data load |
| `weekly_insights` | Mondays @ 8 AM UTC | Generates AI-powered market insights with Claude |

## Pipeline Flow

```
┌─────────────────────┐     ┌─────────────────────┐
│  github_daily_stats │     │  hn_monthly_hiring  │
│  (Daily @ 6 AM)     │     │  (2nd of month)     │
└──────────┬──────────┘     └──────────┬──────────┘
           │                           │
           ▼                           ▼
┌──────────────────────────────────────────────────┐
│              dbt_full_refresh                    │
│              (Daily @ 7 AM)                      │
└──────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────┐
│              weekly_insights                     │
│              (Mondays @ 8 AM)                    │
│              Claude Sonnet analysis              │
└──────────────────────────────────────────────────┘
```

---

## Astronomer Cloud Deployment

### Prerequisites

1. Install Astro CLI: https://docs.astronomer.io/astro/cli/install-cli
2. Create Astronomer account: https://www.astronomer.io/

### Setup

```bash
# Clone and navigate to airflow directory
cd airflow

# Prepare for deployment (replaces symlinks with actual files)
./scripts/prepare_deploy.sh

# Login to Astronomer
astro login

# Create a new deployment (first time only)
astro deployment create

# Deploy
astro deploy
```

### Environment Variables

Set these in Astronomer UI (Deployment → Variables):

| Variable | Description |
|----------|-------------|
| `SNOWFLAKE_ACCOUNT` | Snowflake account identifier |
| `SNOWFLAKE_USER` | Snowflake username |
| `SNOWFLAKE_PASSWORD` | Snowflake password |
| `SNOWFLAKE_DATABASE` | Target database (KOUVERK_DATA_INDUSTRY) |
| `SNOWFLAKE_WAREHOUSE` | Compute warehouse |
| `SNOWFLAKE_SCHEMA` | Target schema (raw) |
| `GITHUB_TOKEN` | GitHub PAT for API (optional, increases rate limit) |
| `ANTHROPIC_API_KEY` | Anthropic API key (for weekly insights) |

### Connections

Create a Snowflake connection in Airflow UI:
- **Conn ID:** `snowflake_default`
- **Conn Type:** Snowflake
- Fill in account, user, password, database, warehouse, schema

---

## Local Development with Docker Compose

### 1. Set Environment Variables

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 2. Start Airflow

```bash
# Set Airflow user ID (Linux/Mac)
echo "AIRFLOW_UID=$(id -u)" >> .env

# Start services
docker-compose up -d

# Wait for init to complete
docker-compose logs -f airflow-init
```

### 3. Access Airflow UI

- URL: http://localhost:8080
- Username: `admin`
- Password: `admin`

### 4. Trigger a DAG

```bash
# Via CLI
docker-compose exec airflow-scheduler airflow dags trigger dbt_full_refresh

# Or use the UI
```

---

## Local Development with Astro CLI

For a more production-like local experience:

```bash
# Start local Airflow
astro dev start

# Access UI at http://localhost:8080
# Username: admin, Password: admin

# Stop
astro dev stop
```

---

## Project Structure

```
airflow/
├── Dockerfile              # Astronomer runtime image
├── requirements.txt        # Python dependencies
├── packages.txt           # System packages
├── docker-compose.yml     # Local Docker setup
├── .env.example           # Environment template
├── dags/                  # Airflow DAGs
│   ├── dag_github_daily.py
│   ├── dag_hn_monthly.py
│   ├── dag_dbt_transform.py
│   └── dag_weekly_insights.py
├── include/               # Shared code (symlinks to parent dirs)
│   ├── extraction/        # → ../../extraction
│   └── dbt/              # → ../../dbt
├── plugins/              # Airflow plugins
├── logs/                 # Airflow logs
└── scripts/
    └── prepare_deploy.sh # Prepares for Astronomer deploy
```

---

## Testing DAGs

```bash
# Test DAG syntax
python dags/dag_github_daily.py
python dags/dag_hn_monthly.py
python dags/dag_dbt_transform.py
python dags/dag_weekly_insights.py

# Test individual tasks (Docker Compose)
docker-compose exec airflow-scheduler airflow tasks test github_daily_stats fetch_github_data 2024-01-01

# Test individual tasks (Astro CLI)
astro dev run tasks test github_daily_stats fetch_github_data 2024-01-01
```
