"""
DAG: Weekly Insights Generator

Generates AI-powered market insights using Claude Sonnet.
Queries transformed data from dbt marts and produces a written summary.
"""

from datetime import datetime, timedelta
import os
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


# Astronomer path (project root is /usr/local/airflow)
AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/usr/local/airflow')
EXTRACTION_DIR = f'{AIRFLOW_HOME}/include/extraction'


def generate_weekly_insights(**context):
    """Generate weekly insights using the extraction script."""
    # Add extraction directory to path
    sys.path.insert(0, EXTRACTION_DIR)

    from generate_weekly_insights import run_weekly_insights

    insights, filepath = run_weekly_insights()

    # Push results to XCom
    context['ti'].xcom_push(key='insights_filepath', value=filepath)
    context['ti'].xcom_push(key='insights_length', value=len(insights))

    print(f"Generated insights: {len(insights)} characters")
    print(f"Saved to: {filepath}")

    return filepath


def log_completion(**context):
    """Log completion of the insights generation."""
    filepath = context['ti'].xcom_pull(key='insights_filepath', task_ids='generate_insights')
    insights_length = context['ti'].xcom_pull(key='insights_length', task_ids='generate_insights')

    print(f"Weekly insights generation complete!")
    print(f"  File: {filepath}")
    print(f"  Length: {insights_length} characters")


# DAG Definition
default_args = {
    'owner': 'data_ai_index',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=10),
}

with DAG(
    'weekly_insights',
    default_args=default_args,
    description='Generate AI-powered weekly market insights using Claude',
    schedule_interval='0 8 * * 1',  # 8 AM UTC every Monday
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['insights', 'llm', 'weekly'],
) as dag:

    # Verify environment is ready
    check_env = BashOperator(
        task_id='check_environment',
        bash_command='''
            echo "Checking environment variables..."
            if [ -z "$ANTHROPIC_API_KEY" ]; then
                echo "ERROR: ANTHROPIC_API_KEY not set"
                exit 1
            fi
            if [ -z "$SNOWFLAKE_ACCOUNT" ]; then
                echo "ERROR: SNOWFLAKE_ACCOUNT not set"
                exit 1
            fi
            echo "Environment OK"
        ''',
    )

    generate_insights = PythonOperator(
        task_id='generate_insights',
        python_callable=generate_weekly_insights,
    )

    log_done = PythonOperator(
        task_id='log_completion',
        python_callable=log_completion,
    )

    check_env >> generate_insights >> log_done
