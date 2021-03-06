"""Run any pending migrations.
"""
import json
import os
import importlib
import psycopg2
import settings


MIGRATIONS_PATH = os.environ.get('MIGRATIONS_PATH', 'migrations.json')


def main(migrations_dir='migrations'):
    migrs = _load_migrations()
    files = sorted(os.listdir(migrations_dir))
    files = [f[:-3] for f in files if f.endswith('.py')]

    if files[:len(migrs)] != migrs:
        raise Exception('Existing migrations aren\'t just the beginning of expected migrations')

    conn = setup_connection()
    cursor = conn.cursor()
    for i in range(len(migrs), len(files)):
        file_ = files[i]
        print(f'Running migration migrations.{file_}')
        module = importlib.import_module(f'migrations.{file_}')
        try:
            module.up(conn, cursor)
            print('Success! Committing..')
            conn.commit()
            print('Success! Saving migration as complete..')
            migrs.append(file_)
            _save_migrations(migrs)
            print('Success!')
        except:  # noqa: E722
            print('An exception occurred! Rolling back...')
            conn.rollback()
            print('Closing connection...')
            conn.close()
            raise

    print('All migrations succeeded.')
    conn.close()


def _save_migrations(arr):
    """Saves the given array of migrations"""
    with open(MIGRATIONS_PATH, 'w') as outfile:
        json.dump(arr, outfile)


def _load_migrations():
    """Loads the migrations that have already been applied"""
    if not os.path.isfile(MIGRATIONS_PATH):
        return []

    with open(MIGRATIONS_PATH, 'r') as infile:
        return json.load(infile)


def setup_connection():
    """Create a psycopg2 connection to the postgres database"""
    cfg = settings.load_settings()
    return psycopg2.connect(
        host=cfg['DATABASE_HOST'],
        port=int(cfg['DATABASE_PORT']),
        user=cfg['DATABASE_USER'],
        password=cfg['DATABASE_PASSWORD'],
        dbname=cfg['DATABASE_DBNAME']
    )


if __name__ == '__main__':
    main()
