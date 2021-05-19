import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from operators import load_data_source_to_stage

default_args = {"owner": "airflow"}

with DAG(
    dag_id="data_pipeline_template_dag",
    start_date=datetime.datetime.today() - datetime.timedelta(days=1),
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
) as dag:
    start_operator = DummyOperator(task_id='Begin_execution')
    load_data_into_stage = PythonOperator(
        task_id="load_data_into_stage",
        dag=dag,
        provide_context=True,
        python_callable=load_data_source_to_stage.loadDataToStage
    )

    #data_validation_operator = DummyOperator(task_id='Validate_events_data_in_stage')
    #user_dimension_table_operator = DummyOperator(task_id='Load_user_dimension_table')
    #facts_table_operator = DummyOperator(task_id='Load_facts_table')
    end_operator = DummyOperator(task_id='Stop_execution', dag=dag)

    # DAG dependencies
    start_operator >> load_data_into_stage >> end_operator
    #stage_load_operator >> data_validation_operator
    #data_validation_operator >> user_dimension_table_operator
    #user_dimension_table_operator >> facts_table_operator
    #facts_table_operator >> end_operator
