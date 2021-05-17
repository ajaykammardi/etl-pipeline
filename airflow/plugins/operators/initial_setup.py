import json
import pandas as pd
import psycopg2 as pg

from helpers import SqlQueries


def loadDataToPostgres(**kwargs):
    df = pd.read_json('/opt/airflow/data/organization.json')
    try:
        dbconnect = pg.connect(
            database='postgres_db',
            user='postgres_user',
            password='postgres',
            host='etl-pipeline_postgresdb_1',
            port='5432'
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
