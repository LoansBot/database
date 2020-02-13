"""Copies the database using pg_dump then upload the result to AWS S3. After
this is done the file is on S3 and also exists at uploaded.dump. There is
also a meta file uploaded.json
"""
import os
import time
import aws_utils
import json
import settings
import sys


REQUIRED_CFG = [
    'AWS_S3_FOLDER', 'DATABASE_HOST', 'AWS_ACCESS_KEY',
    'AWS_SECRET_KEY', 'DATABASE_PORT', 'DATABASE_USER',
    'DATABASE_PASSWORD', 'DATABASE_DBNAME', 'AWS_S3_BUCKET'
]


def main(args=None):
    cfg = settings.load_settings()
    for k in REQUIRED_CFG:
        if not cfg[k]:
            raise Exception(f'Environment variable {k} is required but not set')

    localf = f'{time.time()}.dump'
    key = os.path.join(cfg['AWS_S3_FOLDER'], localf)
    backup_database(localf)
    upload_to_aws(localf, cfg['AWS_S3_BUCKET'], key, cfg)
    if os.path.exists('uploaded.dump'):
        print('Deleting uploaded.dump')
        os.remove('uploaded.dump')
    if os.path.exists('uploaded.json'):
        print('Deleting uploaded.json')
        os.remove('uploaded.json')
    print(f'Moving local file {localf} to uploaded.dump')
    os.rename(localf, 'uploaded.dump')
    print('Saving meta info to uploaded.json')
    with open('uploaded.json', 'w') as outfile:
        json.dump({'key': key}, outfile)


def backup_database(local_file):
    """Backs up the database to the given local file"""
    cfg = settings.load_settings()
    db_host = cfg['DATABASE_HOST']
    db_port = int(cfg['DATABASE_PORT'])
    db_user = cfg['DATABASE_USER']
    db_pass = cfg['DATABASE_PASSWORD']
    db_name = cfg['DATABASE_DBNAME']

    print(f'Initiating database backup to {local_file}')
    old_pg_pass = os.environ.get('PGPASSWORD')
    os.environ['PGPASSWORD'] = db_pass
    status = os.system(f'pg_dump -Fc {db_name} -h {db_host} -p {db_port} -U {db_user} > {local_file}')
    if old_pg_pass is not None:
        os.environ['PGPASSWORD'] = old_pg_pass
    else:
        del os.environ['PGPASSWORD']
    if status == 0:
        print('Backup finished')
    else:
        print(f'Backup failed with status {status}')
        sys.exit(1)


def upload_to_aws(local_file, bucket, s3_file, cfg):
    """Upload the local file to the given bucket with the given name."""
    s3 = aws_utils.connect_to_s3(cfg)
    print(f'Starting upload {local_file} -> {s3_file}')
    s3.upload_file(local_file, bucket, s3_file)
    print(f'Upload {local_file} -> {s3_file} successful')


if __name__ == '__main__':
    main()
