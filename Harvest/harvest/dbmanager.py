import psycopg2
import logging

""" logs"""
logger = logging.getLogger(__name__)


def create_db(params, db):
    try:
        database = db['dbname']
        # connect to the postgres
        conn = psycopg2.connect(**params)
        # auto commit the sql
        conn.autocommit = True
        # create the cursor
        cur = conn.cursor()
        # check if database exist
        cur.execute("select exists(SELECT datname FROM pg_catalog.pg_database WHERE datname = '{}');".format(database))
        if cur.fetchone()[0]:
            # if database exist, log a message that it is already on the server
            logger.info("{} Database already exist...".format(database))
        else:
            # if not create the database
            logger.info("Creating Database {}....".format(database))
            database_create = """CREATE DATABASE {};""".format(database)
            cur.execute(database_create)
            cur.close()
            conn.close()
    except Exception as error:
        # log the error message
        logger.exception(error)


def create_table(table_name, table_field, params, db):
    try:
        # connect to the postgres
        conn = psycopg2.connect(**params, **db)
        # auto commit the sql
        conn.autocommit = True
        # create the cursor
        cur = conn.cursor()
        # check if the table exist
        cur.execute("SELECT to_regclass('{}');".format(table_name))
        if cur.fetchone()[0]:
            # if table exist, log a message that it is already on the database
            logger.info("{} Table already exist...".format(table_name))
            cur.close()
        else:
            # if not create the table
            logger.info("Creating table {}....".format(table_name))
            table = '''CREATE TABLE IF NOT EXISTS {} ({});'''.format(table_name, table_field)
            cur.execute(table)
            cur.close()
            conn.close()
            logger.info("{} table Created....".format(table_name))
    except Exception as error:
        # log the error message
        logger.exception(error)


def insert(query, params, db):
    try:
        # connect to the postgres
        conn = psycopg2.connect(**params, **db)
        # auto commit the sql
        conn.autocommit = True
        # create the cursor
        cur = conn.cursor()
        # insert data to table
        cur.execute(query)
        cur.close()
        conn.close()
    except Exception as error:
        # log the error message
        logger.exception(error)


def select(query, params, db):
    try:
        # connect to the postgres
        conn = psycopg2.connect(**params, **db)
        # auto commit the sql
        conn.autocommit = True
        # create the cursor
        cur = conn.cursor()
        # insert data to table
        cur.execute(query)
        row = cur.fetchall()
        cur.close()
        conn.close()
        return row
    except Exception as error:
        # log the error message
        logger.exception(error)