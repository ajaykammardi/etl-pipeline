import json
import configparser
import pandas as pd
import psycopg2 as pg

from helpers import SqlQueries
from pymongo import MongoClient

config = configparser.ConfigParser()
config.read('/opt/airflow/plugins/config/runtime.cnf')


def loadDataToPostgres(**kwargs):
    df = pd.read_json('/opt/airflow/data/organization.json')
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
    cursor.execute(SqlQueries.target_organization_dimension_table_create)
    cursor.execute(SqlQueries.staging_events_table_create)
    dbconnect.commit()
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))
    query = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s)" % ('dim_organization', cols)

    try:
        cursor.executemany(query, tuples)
        dbconnect.commit()
    except (Exception, pg.DatabaseError) as error:
        print(error)
        dbconnect.rollback()
    cursor.close()


def loadDataToMongoDB(**kwargs):
    client = MongoClient(host=config.get('source_mongo_details', 'host'),
                         port=config.getint('source_mongo_details', 'port'),
                         username=config.get('source_mongo_details', 'username'),
                         password=config.get('source_mongo_details', 'password'))

    db = client['events_db']
    collection_events = db['events']

    with open('/opt/airflow/data/events.json') as events:
        file_data = json.load(events)

    collection_events.insert_many(file_data)
    client.close()
