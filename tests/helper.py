"""Shared functions for migration tests
"""
import configparser
import psycopg2
import os


def load_settings():
    cfg = configparser.ConfigParser()
    cfg.read('settings.ini')
    cfg = cfg['DEFAULT']
    for nm in list(cfg.keys()):
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
