"""
DAG: GitHub Repository Stats - Daily Refresh

Fetches star counts and activity metrics for tracked data/AI repositories.
Runs daily to provide fresh engagement signals for the dashboard.

Uses extraction scripts:
- include/extraction/fetch_github_data.py - Fetches from GitHub API
- include/extraction/load_to_snowflake.py - Loads to Snowflake
"""

from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator


# Astronomer path (project root is /usr/local/airflow)
AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/usr/local/airflow')


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

    # Step 1: Fetch GitHub data using extraction script
    fetch_github_data = BashOperator(
        task_id='fetch_github_data',
        bash_command=f'python {AIRFLOW_HOME}/include/extraction/fetch_github_data.py',
    )

    # Step 2: Load to Snowflake using extraction script
    load_to_snowflake = BashOperator(
        task_id='load_to_snowflake',
        bash_command=f'python {AIRFLOW_HOME}/include/extraction/load_to_snowflake.py github',
    )

    # Step 3: Trigger dbt refresh (placeholder - actual trigger handled by dbt_full_refresh DAG)
    trigger_dbt = SnowflakeOperator(
        task_id='trigger_dbt_refresh',
        snowflake_conn_id='snowflake_default',
        sql="""
            -- Log that GitHub data was refreshed
            -- dbt_full_refresh DAG runs at 7 AM UTC (after this DAG)
            SELECT 'GitHub data refreshed, dbt will run at 7 AM UTC' as status;
        """,
    )

    fetch_github_data >> load_to_snowflake >> trigger_dbt
