import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {"owner": "airflow"}

dag = DAG(
    dag_id="initial_setup_dag",
    start_date=datetime.datetime.today() - datetime.timedelta(days=1),
    schedule_interval="@once",
    default_args=default_args,
    catchup=False,
)
start_operator = DummyOperator(task_id='Begin_execution', dag=dag)

setup_target_postgres_ddb = PythonOperator(
        task_id="setup_postgres_db",
        dag=dag,
        python_callable=loadDataToPostgres
    )

# DAG dependencies
start_operator >> setup_target_postgres_ddb