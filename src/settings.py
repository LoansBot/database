"""Utility function for loading settings"""
import configparser
import os


EXPECTED_KEYS = [
    'DATABASE_HOST'
    'DATABASE_PORT'
    'DATABASE_USER'
    'DATABASE_PASSWORD'
    'DATABASE_DBNAME'
    'AWS_ACCESS_KEY'
    'AWS_SECRET_KEY'
    'AWS_S3_BUCKET'
    'AWS_S3_FOLDER'
]


def load_settings():
    cfg = configparser.ConfigParser()
    cfg.read('settings.ini')
    cfg = cfg['DEFAULT']
    for nm in EXPECTED_KEYS:
        if os.environ.get(nm):
            print(f'Found environment variable {nm}')
            cfg[nm] = os.environ[nm]
        else:
            print(f'No environment variable found for {nm}')
    return cfg
