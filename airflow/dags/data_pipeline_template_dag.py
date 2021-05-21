import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.python_operator import PythonOperator
from operators import *

default_args = {"owner": "airflow"}

with DAG(
    dag_id="data_pipeline_template_dag",
    start_date=datetime.datetime.today() - datetime.timedelta(days=1),
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
) as dag:
    start_operator = DummyOperator(task_id='Begin_execution')

    load_data_into_stage = BranchPythonOperator(
        task_id="Load_data_into_stage",
        dag=dag,
        provide_context=True,
        python_callable=load_data_source_to_stage.loadDataToStage
    )

    data_validation_in_stage = PythonOperator(
        task_id="Validate_data_in_stage",
        dag=dag,
        provide_context=True,
        python_callable=data_validation.dataValidation
    )

    load_data_into_dimensions = PythonOperator(
        task_id="Load_data_into_dimensions",
        dag=dag,
        provide_context=True,
        python_callable=dimension_load.loadDataToDimensionTables
    )

    load_data_into_aggregation_table = PythonOperator(
        task_id="Load_data_into_aggregation_table",
        dag=dag,
        provide_context=True,
        python_callable=aggregation_table_load.loadDataToAggregationTables
    )

    end_operator = DummyOperator(task_id='Stop_execution', dag=dag)

    # DAG dependencies
    start_operator >> load_data_into_stage
    load_data_into_stage >> [data_validation_in_stage, end_operator]
    data_validation_in_stage >> load_data_into_dimensions
    load_data_into_dimensions >> load_data_into_aggregation_table
    load_data_into_aggregation_table >> end_operator
