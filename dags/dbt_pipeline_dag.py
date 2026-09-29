from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'autonomous_dbt_duckdb_dag',
    default_args=default_args,
    description='An event-driven DAG triggered by a File Sensor writing directly to the shared warehouse',
    schedule_interval='@daily',  # Runs automatically every day (or change to None if purely event-driven)
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    # Task 0: Wait for a new raw file to land in the seeds folder
    wait_for_raw_file = FileSensor(
        task_id='wait_for_raw_file',
        filepath='/opt/airflow/seeds/raw_sales.csv',  # Relative to /opt/airflow
        fs_conn_id='fs_default',          # Default filesystem connection in Airflow
        poke_interval=30,                 # Check every 30 seconds
        timeout=600,                      # Give up after 10 minutes if no file appears
        mode='poke',
    )

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

    # Define the pipeline order (Sensor -> Seed -> Run -> Test)
    wait_for_raw_file >> dbt_seed >> dbt_run >> dbt_test