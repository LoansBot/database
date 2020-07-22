"""Shared functions for migration tests
"""
import configparser
import psycopg2
import os
import argparse
from psycopg2 import IntegrityError
from pypika import PostgreSQLQuery as Query, Schema, Table, Parameter
from pypika.functions import Cast


EXPECTED_KEYS = [
    'DATABASE_HOST',
    'DATABASE_PORT',
    'DATABASE_USER',
    'DATABASE_PASSWORD',
    'DATABASE_DBNAME',
    'AWS_ACCESS_KEY',
    'AWS_SECRET_KEY',
    'AWS_S3_BUCKET',
    'AWS_S3_FOLDER'
]


def check_if_table_exist(cursor, tblname):
    """Returns true if the given table exists and false otherwise"""
    info_schema = Schema('information_schema').tables
    cursor.execute(
        Query.from_(info_schema)
        .where(info_schema.table_type == 'BASE TABLE')
        .where(info_schema.table_schema == 'public')
        .where(info_schema.table_name == Parameter('%s'))
        .select(1).limit(1).get_sql(),
        (tblname,)
    )
    result = cursor.fetchone()
    return result is not None


def check_if_column_exist(cursor, tblname, colname):
    columns = Schema('information_schema').columns
    cursor.execute(
        Query.from_(columns)
        .where(columns.table_name == Parameter('%s'))
        .where(columns.column_name == Parameter('%s'))
        .select(1).limit(1).get_sql(),
        (tblname, colname)
    )
    result = cursor.fetchone()
    return result is not None


def check_if_pkey_exists(cursor, tblname):
    pg_indices = Table('pg_index')
    pg_attributes = Table('pg_attribute')
    cursor.execute(
        Query.from_(pg_indices).select(1)
        .where(
            pg_indices.indrelid == Cast(Parameter('%s'), 'regclass')
        )
        .where(
            pg_indices.indisprimary
        )
        .get_sql(),
        (tblname,)
    )
    return cursor.fetchone() is not None


def assert_fails_with_pgcode(asserter, pgcode, cursor, query, q_args=tuple()):
    """Asserts that the given query fails with the given code. Note that this
    puts the transaction in a bad state, so this is typically the last test in a
    testcase"""
    try:
        cursor.execute(query, q_args)
        asserter.assertFalse(True, 'expected an error to be raised')
    except IntegrityError as ex:
        asserter.assertEqual(ex.pgcode, str(pgcode))


def require_confirm_or_user_input(desc):
    """Requires either --confirm is passed or user input is provided to
    confirm the operation"""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--confirm', action='store_true',
                        help='Skip user confirmation requirement.')
    args = parser.parse_args()
    if not args.confirm:
        print('You are performing a DANGEROUS operation!')
        print('This will DELETE the entire database! Are you sure? [y/N]')
        res = input()
        if res != 'y' and res != 'Y':
            print('Cancelling')
            return


def load_settings():
    cfg = configparser.ConfigParser()
    cfg.read('settings.ini')
    cfg = cfg['DEFAULT']
    for nm in EXPECTED_KEYS:
        if os.environ.get(nm):
            cfg[nm] = os.environ[nm]
    return cfg


def setup_connection():
    """Create a psycopg2 connection to the postgres database"""
    cfg = load_settings()
    return psycopg2.connect(
        host=cfg['DATABASE_HOST'],
        port=int(cfg['DATABASE_PORT']),
        user=cfg['DATABASE_USER'],
        password=cfg['DATABASE_PASSWORD'],
        dbname=cfg['DATABASE_DBNAME']
    )


def teardown_connection(conn):
    """Teardown the given psycopg2 connection"""
    conn.close()
