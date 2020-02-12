"""Restore the backup specified to the database. Requires user confirmation or
--confirm
"""
import argparse
import os
import sys


def main(args=None):
    parser = argparse.ArgumentParser(description='Restore backup')
    parser.add_argument('--confirm', action='store_true',
                        help='Skip user confirmation requirement.')
    parser.add_argument('dump', help='The path to the .dump file')
    args = parser.parse_args(args=args)
    if not args.confirm:
        print('You are performing a DANGEROUS operation!')
        print('This will DELETE the entire database! Are you sure? [y/N]')
        res = input()
        if res != 'y' and res != 'Y':
            print('Cancelling')
            return

    if not os.path.exists(args.dump):
        print(f'Dump file at {args.dump} does not exist')
        sys.exit(1)

    if not os.path.isfile(args.dump):
        print(f'Dump file at {args.dump} is not a file')
        sys.exit(1)

    restore_database(args.dump)


def restore_database(local_file):
    """Backs up the database to the given local file"""
    db_host = os.environ('DATABASE_HOST')
    db_port = int(os.environ('DATABASE_PORT'))
    db_user = os.environ('DATABASE_USER')
    db_pass = os.environ('DATABASE_PASSWORD')
    db_name = os.environ('DATABASE_DBNAME')

    print(f'Initiating restore from {local_file}')
    old_pg_pass = os.environ.get('PGPASSWORD')
    os.environ['PGPASSWORD'] = db_pass
    os.system(f'pg_restore -Fc --clean --create --dbname {db_name} -h {db_host} -p {db_port} -U {db_user} {local_file}')
    os.environ['PGPASSWORD'] = old_pg_pass
    print('Restore finished')


if __name__ == '__main__':
    main()
