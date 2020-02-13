"""Clears the database, then runs the _down test for the first migration, then
runs the migration, then runs the _up test. If The migration is reversible
(i.e., has a down function), the migration is then reversed and the _down test
is run again. Then the up function is run, and the process is repeated for the
next migration. At the end the database is cleared again.

For safety, either the argument --confirm needs to be passed or user
confirmation is required
"""
import importlib
import sys
import os
import helper
from pypika import PostgreSQLQuery as Query, Schema
import unittest


def main():
    helper.require_confirm_or_user_input('Run migration tests')

    print('Loading migrations...')
    sys.path.append('../src')
    files = sorted(os.listdir('../src/migrations'))
    files = [f[:-3] for f in files if f.endswith('.py')]
    print('Loading all the modules to verify...')
    for f in files:
        mod = importlib.import_module(f'migrations.{f}')
        if not hasattr(mod, 'up'):
            print(f'Module {mod} is missing the up function!')
            sys.exit(1)
        down_test_mod = importlib.import_module(f'migrations.{f}_down')
        if not hasattr(down_test_mod, 'DownTest'):
            print(f'Module {mod} down test missing class DownTest')
            sys.exit(1)
        up_test_mod = importlib.import_module(f'migrations.{f}_up')
        if not hasattr(up_test_mod, 'UpTest'):
            print(f'Module {mod} up test missing class UpTest')
            sys.exit(1)

    conn = helper.setup_connection()
    cursor = conn.cursor()
    print('Dropping all tables...')
    drop_all_tables(conn)
    print('Success!')
    print()
    runner = unittest.TextTestRunner()
    for f in files:
        mod = importlib.import_module(f'migrations.{f}')
        up_test_mod = importlib.import_module(f'migrations.{f}_up')
        down_test_mod = importlib.import_module(f'migrations.{f}_down')

        print(f'Running down test for {f}')
        result = run_tests(runner, down_test_mod.DownTest)
        if result.failures or result.errors:
            sys.exit(1)
        print(f'Applying migration {f}')
        mod.up(conn, cursor)
        conn.commit()
        print(f'Running up test for {f}')
        result = run_tests(runner, up_test_mod.UpTest)
        if result.failures or result.errors:
            sys.exit(1)
        if hasattr(mod, 'down'):
            print(f'Rolling back migration {f}')
            mod.down(conn, cursor)
            conn.commit()
            print(f'Running down test for {f}')
            result = run_tests(runner, down_test_mod.DownTest)
            if result.failures or result.errors:
                sys.exit(1)
            print(f'Reapplying migration {f}')
            mod.up(conn, cursor)
            conn.commit()
            print(f'Running up test for {f}')
            result = run_tests(runner, up_test_mod.UpTest)
            if result.failures or result.errors:
                sys.exit(1)

    print()
    print('All migrations completed successfully!')
    print('Dropping tables...')
    drop_all_tables(conn)
    conn.commit()
    print('All done')
    conn.close()


def run_tests(runner, testcase):
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testcase)
    return runner.run(suite)


def drop_all_tables(conn):
    """Drop all the tables in the default database"""
    cursor = conn.cursor()
    info_schema = Schema('information_schema').tables

    cursor.execute(
        Query.from_(info_schema)
        .where(info_schema.table_type == 'BASE TABLE')
        .where(info_schema.table_schema == 'public')
        .select(info_schema.table_name).get_sql()
    )
    table_names = cursor.fetchall()
    for (tbl_name,) in table_names:
        cursor.execute(f'DROP TABLE {tbl_name} CASCADE')
    conn.commit()
    cursor.close()


if __name__ == '__main__':
    main()
