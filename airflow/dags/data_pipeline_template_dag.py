import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

default_args = {"owner": "airflow"}

with DAG(
    dag_id="data_pipeline_template_dag",
    start_date=datetime.datetime.today() - datetime.timedelta(days=1),
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
) as dag:
    start_operator = DummyOperator(task_id='Begin_execution')
    stage_load_operator = DummyOperator(task_id='Load_events_data_from_source_to_stage')
    data_validation_operator = DummyOperator(task_id='Validate_events_data_in_stage')
    user_dimension_table_operator = DummyOperator(task_id='Load_user_dimension_table')
    facts_table_operator = DummyOperator(task_id='Load_facts_table')
    end_operator = DummyOperator(task_id='Stop_execution', dag=dag)

    # DAG dependencies
    start_operator >> stage_load_operator
    stage_load_operator >> data_validation_operator
    data_validation_operator >> user_dimension_table_operator
    user_dimension_table_operator >> facts_table_operator
    facts_table_operator >> end_operator
