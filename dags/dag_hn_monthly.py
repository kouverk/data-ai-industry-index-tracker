"""
DAG: Hacker News "Who Is Hiring" - Monthly Extraction

Fetches the full HN "Who Is Hiring" dataset from HuggingFace.
The HuggingFace dataset is updated monthly with new threads.
Runs on the 2nd of each month to catch the new thread.

Uses extraction scripts:
- include/extraction/fetch_hn_data.py - Fetches from HuggingFace
- include/extraction/load_to_snowflake.py - Loads to Snowflake
"""

from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


# Astronomer path (project root is /usr/local/airflow)
AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/usr/local/airflow')


def log_extraction_complete(**context):
    """Log completion of HN extraction."""
    execution_date = context['execution_date']
    print(f"HN extraction complete for {execution_date.strftime('%B %Y')}")
    print("Data refreshed from HuggingFace dataset")


# DAG Definition
default_args = {
    'owner': 'data_ai_index',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=10),
}

with DAG(
    'hn_monthly_hiring',
    default_args=default_args,
    description='Extract monthly HN Who Is Hiring job postings',
    schedule_interval='0 12 2 * *',  # 12 PM UTC on the 2nd of each month
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['hn', 'monthly', 'extraction'],
) as dag:

    # Step 1: Fetch HN data from HuggingFace
    fetch_hn_data = BashOperator(
        task_id='fetch_hn_data',
        bash_command=f'python {AIRFLOW_HOME}/include/extraction/fetch_hn_data.py',
    )

    # Step 2: Load to Snowflake
    load_to_snowflake = BashOperator(
        task_id='load_to_snowflake',
        bash_command=f'python {AIRFLOW_HOME}/include/extraction/load_to_snowflake.py hn',
    )

    # Step 3: Log completion
    log_complete = PythonOperator(
        task_id='log_completion',
        python_callable=log_extraction_complete,
    )

    fetch_hn_data >> load_to_snowflake >> log_complete
