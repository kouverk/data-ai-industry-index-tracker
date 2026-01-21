# Airflow DAGs for Data & AI Industry Index

## DAGs

| DAG | Schedule | Description |
|-----|----------|-------------|
| `github_daily_stats` | Daily @ 6 AM UTC | Fetches GitHub repo stats (stars, forks, activity) |
| `hn_monthly_hiring` | 2nd of month @ 12 PM UTC | Extracts new HN "Who Is Hiring" thread |
| `dbt_transform` | Manual trigger | Runs dbt models (staging → intermediate → marts) |
| `dbt_full_refresh` | Daily @ 7 AM UTC | Full dbt refresh after GitHub data load |

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
│                                                  │
│  1. dbt deps                                     │
│  2. dbt seed (taxonomy mappings)                 │
│  3. dbt run (all models)                         │
│  4. dbt test                                     │
└──────────────────────────────────────────────────┘
```

## Running Locally with Docker

### 1. Set Environment Variables

Create a `.env` file in the `airflow/` directory (copy from project root):

```bash
cp ../.env .env
```

### 2. Start Airflow

```bash
# Set Airflow user ID (Linux/Mac)
echo -e "AIRFLOW_UID=$(id -u)" >> .env

# Start services
docker-compose up -d

# Wait for init to complete
docker-compose logs -f airflow-init
```

### 3. Access Airflow UI

- URL: http://localhost:8080
- Username: `admin`
- Password: `admin`

### 4. Configure Snowflake Connection

The Snowflake connection is auto-configured from environment variables.
If you need to modify it:

1. Go to Admin → Connections
2. Edit `snowflake_default`
3. Update credentials

### 5. Trigger a DAG

```bash
# Via CLI
docker-compose exec airflow-scheduler airflow dags trigger dbt_full_refresh

# Or use the UI
```

## Running Without Docker

If you have Airflow installed locally:

```bash
# Set AIRFLOW_HOME
export AIRFLOW_HOME=/path/to/this/airflow/folder

# Initialize DB
airflow db init

# Create admin user
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com

# Start scheduler (in one terminal)
airflow scheduler

# Start webserver (in another terminal)
airflow webserver --port 8080
```

## Environment Variables Required

| Variable | Description |
|----------|-------------|
| `SNOWFLAKE_ACCOUNT` | Snowflake account identifier |
| `SNOWFLAKE_USER` | Snowflake username |
| `SNOWFLAKE_PASSWORD` | Snowflake password |
| `SNOWFLAKE_DATABASE` | Target database |
| `SNOWFLAKE_WAREHOUSE` | Compute warehouse |
| `SNOWFLAKE_SCHEMA` | Target schema |
| `GITHUB_TOKEN` | Optional: GitHub PAT for higher API rate limits |

## Testing DAGs

```bash
# Test DAG syntax
python dags/dag_github_daily.py
python dags/dag_hn_monthly.py
python dags/dag_dbt_transform.py

# Test individual tasks
docker-compose exec airflow-scheduler airflow tasks test github_daily_stats fetch_github_stats 2024-01-01
```
