"""A simple utility to create a new migration. This sets up the basic files
that are required"""
import argparse
import os
import shutil


def main(cl_args=None):
    parser = argparse.ArgumentParser(description='Scaffold a new migration')
    parser.add_argument(
        'name',
        type=str,
        help='The name of the migratin, i.e., 001_create_users'
    )
    args = parser.parse_args(cl_args)

    if len(args.name) < 3:
        raise Exception('That migration name is too short!')

    if not os.path.exists('migrations'):
        raise Exception('Could not find migrations directory')

    if not os.path.exists('scaffolds'):
        raise Exception('Could not find the scaffolds directory')

    migration_nm = args.name[:-3] if args.name[-3:] == '.py' else args.name
    if os.path.exists(os.path.join('migrations', migration_nm + '.py')):
        raise Exception('That migration already exists')

    if not os.path.exists('../tests/migrations'):
        raise Exception('Could not find test migrations dir')

    if os.path.exists(os.path.join('../tests/migrations', f'{migration_nm}_up.py')):
        raise Exception('The up-test already exists!')

    if os.path.exists(os.path.join('../tests/migrations', f'{migration_nm}_down.py')):
        raise Exception('The down-test already exists!')

    shutil.copy(
        'scaffolds/migration.py.scaffold',
        os.path.join('migrations', migration_nm + '.py')
    )
    shutil.copy(
        'scaffolds/migration_up.py.scaffold',
        os.path.join('..', 'tests', 'migrations', f'{migration_nm}_up.py')
    )
    shutil.copy(
        'scaffolds/migration_down.py.scaffold',
        os.path.join('..', 'tests', 'migrations', f'{migration_nm}_down.py')
    )


if __name__ == '__main__':
    main()
