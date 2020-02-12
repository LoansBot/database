"""Shared functions for migration tests
"""
import configparser
import psycopg2
import os
import argparse


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
