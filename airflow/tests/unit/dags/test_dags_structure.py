import unittest
from airflow.models import DagBag


class TestInitialDataLoadDag(unittest.TestCase):

    def setUp(self):
        self.dagbag = DagBag()

    def test_initial_setup_dag_task_count(self):
        dag_id = 'initial_setup_dag'
        dag = self.dagbag.get_dag(dag_id)
        self.assertEqual(len(dag.tasks), 4)

    def test_data_pipeline_template_dag_task_count(self):
        dag_id = 'data_pipeline_template_dag'
        dag = self.dagbag.get_dag(dag_id)
        self.assertEqual(len(dag.tasks), 6)

    def test_initial_setup_dag_for_any_import_error(self):
        dag_id = 'initial_setup_dag'
        dag = self.dagbag.get_dag(dag_id)
        assert self.dagbag.import_errors == {}
        assert dag is not None

    def test_data_pipeline_template_dag_for_any_import_error(self):
        dag_id = 'data_pipeline_template_dag'
        dag = self.dagbag.get_dag(dag_id)
        assert self.dagbag.import_errors == {}
        assert dag is not None

