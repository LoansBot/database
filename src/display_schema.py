"""Shows the database schema on relevant tables."""
from run_migrations import setup_connection
from pypika import PostgreSQLQuery as Query, Schema
import os
import settings


def main():
    conn = setup_connection()
    cursor = conn.cursor()
    tbls = Schema('information_schema').tables
    cursor.execute(
        Query.from_(tbls)
        .where(tbls.table_type == 'BASE TABLE')
        .where(tbls.table_schema == 'public')
        .select(tbls.table_name).get_sql(),
    )
    rows = cursor.fetchall()
    rows = map(lambda r: r[0], rows)
    cursor.close()
    conn.close()

    cfg = settings.load_settings()
    db_host = cfg['DATABASE_HOST']
    db_port = int(cfg['DATABASE_PORT'])
    db_user = cfg['DATABASE_USER']
    db_pass = cfg['DATABASE_PASSWORD']
    db_name = cfg['DATABASE_DBNAME']

    old_pg_pass = os.environ.get('PGPASSWORD')
    os.environ['PGPASSWORD'] = db_pass

    for tbl in rows:
        print('=' * 50)
        print(f'DESCRIBE {tbl}')
        os.system(
            f'psql -d {db_name} -h {db_host} -p {db_port} '
            f'-U {db_user} -c "\\d+ {tbl}"'
        )
        print()

    if old_pg_pass is not None:
        os.environ['PGPASSWORD'] = old_pg_pass
    else:
        del os.environ['PGPASSWORD']


if __name__ == '__main__':
    main()
