from __future__ import division, absolute_import, print_function

from airflow.plugins_manager import AirflowPlugin

import operators
import helpers


class ETLPlugin(AirflowPlugin):
    name = "etl_plugin"
    operators = [
        operators.initial_setup,
        operators.load_data_source_to_stage,
        operators.data_validation,
        operators.dimension_load,
        operators.aggregation_table_load
    ]
    helpers = [
        helpers.SqlQueries
    ]