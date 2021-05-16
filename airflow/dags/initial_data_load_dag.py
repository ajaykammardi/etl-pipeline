import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from operators import initial_setup

default_args = {"owner": "airflow"}

with DAG(
    dag_id="initial_setup_dag",
    start_date=datetime.datetime.today() - datetime.timedelta(days=1),
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
) as dag:
    start_operator = DummyOperator(task_id='Begin_execution')

    setup_target_postgres_db = PythonOperator(
        task_id="setup_postgres_db",
        dag=dag,
        provide_context=True,
        python_callable=initial_setup.loadDataToPostgres
    )

    setup_source_mongo_db = PythonOperator(
        task_id="setup_mongo_db",
        dag=dag,
        provide_context=True,
        python_callable=initial_setup.loadDataToMongoDB
    )

    end_operator = DummyOperator(task_id='Stop_execution', dag=dag)

    # DAG dependencies
    start_operator >> setup_target_postgres_db
    start_operator >> setup_source_mongo_db
    setup_target_postgres_db >> end_operator
    setup_source_mongo_db >> end_operator
