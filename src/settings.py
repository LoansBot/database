"""Utility function for loading settings"""
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
    cfg = {}
    for nm in EXPECTED_KEYS:
        if os.environ.get(nm):
            cfg[nm] = os.environ[nm]
    return cfg
