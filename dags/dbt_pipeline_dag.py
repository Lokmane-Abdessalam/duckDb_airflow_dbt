from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'local_dbt_duckdb_dag',
    default_args=default_args,
    description='A simple Airflow DAG to run dbt tasks locally with DuckDB',
    schedule_interval=None, # Run manually
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    # Task 1: Run dbt seed
    dbt_seed = BashOperator(
        task_id='dbt_seed',
        bash_command='cd /opt/airflow && pip install -r requirements.txt && dbt seed --profiles-dir .',
    )

    # Task 2: Run dbt models
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow && dbt run --profiles-dir .',
    )

    # Task 3: Run dbt tests
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow && dbt test --profiles-dir .',
    )

    # Define the pipeline order
    dbt_seed >> dbt_run >> dbt_test
