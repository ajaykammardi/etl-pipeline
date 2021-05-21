import configparser
import pandas as pd
import psycopg2 as pg

from pymongo import MongoClient
from psycopg2 import extras

config = configparser.ConfigParser()
config.read('/opt/airflow/plugins/config/runtime.cnf')


def loadDataToStage(**context):
    inputdate = context['dag_run'].conf['date']
    client = MongoClient(host=config.get('source_mongo_details', 'host'),
                         port=config.getint('source_mongo_details', 'port'),
                         username=config.get('source_mongo_details', 'username'),
                         password=config.get('source_mongo_details', 'password'))

    db = client['events_db']
    collection_events = db['events']

    query = {'received_at': {'$regex': inputdate}}
    documents = collection_events.find(query, {'_id': 0})

    if not(documents.count() == 0):
        df = pd.DataFrame(list(documents))
        dbconnect = pg.connect(
            database=config.get('target_postgres_details', 'database'),
            user=config.get('target_postgres_details', 'user'),
            password=config.get('target_postgres_details', 'password'),
            host=config.get('target_postgres_details', 'host'),
            port=config.get('target_postgres_details', 'port')
        )
        cursor = dbconnect.cursor()
        tuples = [tuple(x) for x in df.to_numpy()]
        cols = ','.join(list(df.columns))
        query = "INSERT INTO %s(%s) VALUES %%s" % ('staging_events', cols)
        extras.execute_values(cursor, query, tuples)
        dbconnect.commit()
        return 'Validate_data_in_stage'
    return 'Stop_execution'
