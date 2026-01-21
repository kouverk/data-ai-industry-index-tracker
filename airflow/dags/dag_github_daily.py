"""
DAG: GitHub Repository Stats - Daily Refresh

Fetches star counts and activity metrics for tracked data/AI repositories.
Runs daily to provide fresh engagement signals for the dashboard.
"""

from datetime import datetime, timedelta
import os
import json
import requests
import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

# Repository list - same as exploration/04_explore_github_data.py
REPOS_TO_TRACK = {
    "orchestration": [
        "apache/airflow", "dagster-io/dagster", "PrefectHQ/prefect",
        "spotify/luigi", "mage-ai/mage-ai", "kestra-io/kestra"
    ],
    "transformation": [
        "dbt-labs/dbt-core", "apache/spark", "pola-rs/polars",
        "dask/dask", "tobymao/sqlglot"
    ],
    "warehouses": [
        "trinodb/trino", "ClickHouse/ClickHouse", "duckdb/duckdb",
        "apache/druid", "StarRocks/starrocks"
    ],
    "streaming": [
        "apache/kafka", "apache/flink", "apache/pulsar",
        "redpanda-data/redpanda", "vectordotdev/vector"
    ],
    "table_formats": [
        "apache/iceberg", "delta-io/delta", "apache/hudi"
    ],
    "etl_elt": [
        "airbytehq/airbyte", "meltano/meltano", "dlt-hub/dlt",
        "singer-io/singer-python", "transferwise/pipelinewise"
    ],
    "bi": [
        "metabase/metabase", "apache/superset", "getredash/redash",
        "lightdash/lightdash", "evidence-dev/evidence"
    ],
    "ml_classical": [
        "scikit-learn/scikit-learn", "dmlc/xgboost",
        "microsoft/LightGBM", "catboost/catboost"
    ],
    "ml_deep": [
        "pytorch/pytorch", "tensorflow/tensorflow",
        "keras-team/keras", "google/jax"
    ],
    "llm": [
        "openai/openai-python", "anthropics/anthropic-sdk-python",
        "langchain-ai/langchain", "run-llama/llama_index",
        "huggingface/transformers", "ollama/ollama", "vllm-project/vllm"
    ],
    "mlops": [
        "mlflow/mlflow", "wandb/wandb", "iterative/dvc",
        "kubeflow/kubeflow", "bentoml/BentoML"
    ],
    "vector_db": [
        "chroma-core/chroma", "qdrant/qdrant", "weaviate/weaviate",
        "milvus-io/milvus", "pgvector/pgvector"
    ],
    "data_quality": [
        "great-expectations/great_expectations", "sodadata/soda-core",
        "elementary-data/elementary"
    ],
    "data_catalog": [
        "datahub-project/datahub", "amundsen-io/amundsen",
        "open-metadata/OpenMetadata"
    ],
}


def fetch_github_stats(**context):
    """Fetch repository stats from GitHub API."""
    token = os.environ.get('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'} if token else {}

    results = []
    errors = []

    for category, repos in REPOS_TO_TRACK.items():
        for repo_path in repos:
            try:
                url = f"https://api.github.com/repos/{repo_path}"
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()

                results.append({
                    'repo_name': data['name'],
                    'full_name': data['full_name'],
                    'category': category,
                    'stars': data['stargazers_count'],
                    'forks': data['forks_count'],
                    'open_issues': data['open_issues_count'],
                    'watchers': data['watchers_count'],
                    'language': data.get('language'),
                    'description': data.get('description', '')[:500] if data.get('description') else None,
                    'created_at': data['created_at'],
                    'updated_at': data['updated_at'],
                    'pushed_at': data['pushed_at'],
                    'fetched_at': datetime.utcnow().isoformat()
                })
            except Exception as e:
                errors.append({'repo': repo_path, 'error': str(e)})

    # Push to XCom for next task
    context['ti'].xcom_push(key='github_stats', value=results)
    context['ti'].xcom_push(key='fetch_errors', value=errors)

    print(f"Fetched {len(results)} repos, {len(errors)} errors")
    return len(results)


def load_to_snowflake(**context):
    """Load GitHub stats to Snowflake."""
    results = context['ti'].xcom_pull(key='github_stats', task_ids='fetch_github_stats')

    if not results:
        print("No data to load")
        return 0

    df = pd.DataFrame(results)

    # Convert timestamps to strings for Snowflake
    for col in ['created_at', 'updated_at', 'pushed_at', 'fetched_at']:
        ts = pd.to_datetime(df[col], utc=True)
        df[col] = ts.dt.strftime('%Y-%m-%d %H:%M:%S')

    df.columns = [c.upper() for c in df.columns]

    # Load to Snowflake
    hook = SnowflakeHook(snowflake_conn_id='snowflake_default')
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Truncate and reload
    cursor.execute("TRUNCATE TABLE raw_github_repo_stats")

    # Insert rows
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO raw_github_repo_stats
            (repo_name, full_name, category, stars, forks, open_issues,
             watchers, language, description, created_at, updated_at, pushed_at, fetched_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))

    conn.commit()
    cursor.close()

    print(f"Loaded {len(df)} rows to raw_github_repo_stats")
    return len(df)


# DAG Definition
default_args = {
    'owner': 'data_ai_index',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'github_daily_stats',
    default_args=default_args,
    description='Fetch daily GitHub repo stats for data/AI tools',
    schedule_interval='0 6 * * *',  # 6 AM UTC daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['github', 'daily', 'extraction'],
) as dag:

    fetch_stats = PythonOperator(
        task_id='fetch_github_stats',
        python_callable=fetch_github_stats,
    )

    load_stats = PythonOperator(
        task_id='load_to_snowflake',
        python_callable=load_to_snowflake,
    )

    trigger_dbt = SnowflakeOperator(
        task_id='trigger_dbt_refresh',
        snowflake_conn_id='snowflake_default',
        sql="""
            -- This is a placeholder. In production, you'd trigger dbt via:
            -- 1. dbt Cloud API
            -- 2. Bash operator running dbt run
            -- 3. Separate DAG trigger
            SELECT 'dbt refresh triggered' as status;
        """,
    )

    fetch_stats >> load_stats >> trigger_dbt
