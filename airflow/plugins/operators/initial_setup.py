import pandas as pd
import psycopg2 as pg

from helpers import SqlQueries


def loadDataToPostgres():
    df = pd.read_json('../../../data/organization.json')
    try:
        dbconnect = pg.connect(
            database='postgres_db',
            user='postgres_user',
            password='postgres',
            host='localhost',
            port='5433'
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

