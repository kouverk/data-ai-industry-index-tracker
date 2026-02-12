"""
DAG: dbt Transformation Pipeline

Runs dbt models after data loads to refresh analytics tables.
Can be triggered manually or by upstream DAGs.
"""

from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


# Astronomer path (project root is /usr/local/airflow)
AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/usr/local/airflow')
DBT_PROJECT_DIR = f'{AIRFLOW_HOME}/dbt'
DBT_PROFILES_DIR = DBT_PROJECT_DIR


def log_run_start(**context):
    """Log the start of dbt run."""
    print("Starting dbt run")
    print(f"DBT_PROJECT_DIR: {DBT_PROJECT_DIR}")
    print(f"DBT_PROFILES_DIR: {DBT_PROFILES_DIR}")


# DAG Definition
default_args = {
    'owner': 'data_ai_index',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dbt_transform',
    default_args=default_args,
    description='Run dbt transformations to refresh analytics models',
    schedule_interval=None,  # Triggered by other DAGs or manually
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['dbt', 'transformation'],
) as dag:

    log_start = PythonOperator(
        task_id='log_run_start',
        python_callable=log_run_start,
    )

    # Install dbt packages (idempotent)
    dbt_deps = BashOperator(
        task_id='dbt_deps',
        bash_command=f"""
            cd {DBT_PROJECT_DIR} && \
            dbt deps --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    # Run seeds (taxonomy mappings)
    dbt_seed = BashOperator(
        task_id='dbt_seed',
        bash_command=f"""
            cd {DBT_PROJECT_DIR} && \
            dbt seed --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    # Run staging models
    dbt_run_staging = BashOperator(
        task_id='dbt_run_staging',
        bash_command=f"""
            cd {DBT_PROJECT_DIR} && \
            dbt run --select staging --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    # Run intermediate models
    dbt_run_intermediate = BashOperator(
        task_id='dbt_run_intermediate',
        bash_command=f"""
            cd {DBT_PROJECT_DIR} && \
            dbt run --select intermediate --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    # Run mart models
    dbt_run_marts = BashOperator(
        task_id='dbt_run_marts',
        bash_command=f"""
            cd {DBT_PROJECT_DIR} && \
            dbt run --select marts --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    # Run tests
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=f"""
            cd {DBT_PROJECT_DIR} && \
            dbt test --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    # Task dependencies
    log_start >> dbt_deps >> dbt_seed >> dbt_run_staging >> dbt_run_intermediate >> dbt_run_marts >> dbt_test


# Create a simpler "full refresh" DAG for convenience
with DAG(
    'dbt_full_refresh',
    default_args=default_args,
    description='Run full dbt refresh (all models)',
    schedule_interval='0 7 * * *',  # 7 AM UTC daily (after github_daily)
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['dbt', 'transformation', 'daily'],
) as dag_full:

    dbt_full_run = BashOperator(
        task_id='dbt_full_run',
        bash_command=f"""
            cd {DBT_PROJECT_DIR} && \
            dbt deps --profiles-dir {DBT_PROFILES_DIR} && \
            dbt seed --profiles-dir {DBT_PROFILES_DIR} && \
            dbt run --profiles-dir {DBT_PROFILES_DIR} && \
            dbt test --profiles-dir {DBT_PROFILES_DIR}
        """,
    )
