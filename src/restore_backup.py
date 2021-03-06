"""Restore the backup specified to the database. Requires user confirmation or
--confirm
"""
import argparse
import os
import sys
import settings
import subprocess


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
    cfg = settings.load_settings()
    db_host = cfg['DATABASE_HOST']
    db_port = int(cfg['DATABASE_PORT'])
    db_user = cfg['DATABASE_USER']
    db_pass = cfg['DATABASE_PASSWORD']
    auth_str = f'-h {db_host} -p {db_port} -U {db_user}'

    old_pg_pass = os.environ.get('PGPASSWORD')
    os.environ['PGPASSWORD'] = db_pass

    pg_restore_version = subprocess.check_output('pg_restore --version', shell=True)
    print(f'Initiating restore from {local_file} using {pg_restore_version}')
    status = os.system(f'pg_restore -Fc --clean --create --dbname template1 {auth_str} {local_file}')
    if old_pg_pass is not None:
        os.environ['PGPASSWORD'] = old_pg_pass
    else:
        del os.environ['PGPASSWORD']
    if status == 0:
        print('Restore finished')
    else:
        print(f'Status failed with code {status}')
        sys.exit(1)


if __name__ == '__main__':
    main()
