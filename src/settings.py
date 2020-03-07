"""Utility function for loading settings"""
import configparser
import os


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


def load_settings():
    if os.path.exists('settings.ini'):
        cfg = configparser.ConfigParser()
        cfg.read('settings.ini')
        cfg = cfg['DEFAULT']
    else:
        cfg = {}
    for nm in EXPECTED_KEYS:
        if os.environ.get(nm):
            cfg[nm] = os.environ[nm]
    return cfg
