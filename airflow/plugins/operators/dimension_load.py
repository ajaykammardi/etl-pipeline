import configparser
import psycopg2 as pg

from helpers import SqlQueries

config = configparser.ConfigParser()
config.read('/opt/airflow/plugins/config/runtime.cnf')


def loadDataToDimensionTables(**context):
    inputdate = context['dag_run'].conf['date']
    try:
        dbconnect = pg.connect(
            database=config.get('target_postgres_details', 'database'),
            user=config.get('target_postgres_details', 'user'),
            password=config.get('target_postgres_details', 'password'),
            host=config.get('target_postgres_details', 'host'),
            port=config.get('target_postgres_details', 'port')
        )
    except Exception as error:
        print(error)

    cursor = dbconnect.cursor()
    cursor.execute(SqlQueries.update_user_table % inputdate)
    dbconnect.commit()
    cursor.execute(SqlQueries.load_data_into_user_table % inputdate)
    cursor.execute(SqlQueries.load_data_into_user_event_table % inputdate)
    dbconnect.commit()
    cursor.close()
