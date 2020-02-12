"""Test backup and restore logic"""
import secrets
import helper
import sys
import filecmp
from pypika import PostgreSQLQuery as Query, Table, Parameter


def main():
    helper.require_confirm_or_user_input('Test backup and restore logic')

    # Run migrations
    sys.path.append('../src')
    import run_migrations
    run_migrations.main()

    name = secrets.token_urlsafe(8)
    print(f'Creating test user {name}')

    conn = helper.setup_connection()
    cursor = conn.cursor()
    users = Table('users')
    cursor.execute(
        Query.into(users).columns('username').insert(Parameter('%s')).get_sql(),
        (name,)
    )
    conn.commit()

    print('Initiating backup...')
    import create_backup
    create_backup.main(args=[])

    print('Initiating download...')
    import download_backup
    download_backup.main(args=['--meta', 'uploaded.json'])

    print('Verifying uploaded matches downloaded...')
    if not filecmp.cmp('uploaded.dump', 'downloaded.dump'):
        print('Files are different!')
        sys.exit(1)

    print('Deleting the test user...')
    cursor.execute(
        Query.from_(users).where(users.username == Parameter('%s')).delete().get_sql(),
        (name,)
    )
    conn.commit()

    print('Verifying the user does not exist')
    if _exists(conn, cursor, users, name):
        print('User exists!')
        sys.exit(1)

    print('Disconnecting...')
    cursor.close()
    conn.close()
    cursor = None
    conn = None

    print('Initiating restore...')
    import restore_backup
    restore_backup.main(args=['--confirm'])

    print('Reconnecting...')
    conn = helper.setup_connection()
    cursor = conn.cursor()

    print('Verifying the user does exist')
    if not _exists(conn, cursor, users, name):
        print('User does not exist!')
        sys.exit(1)

    print('All done')


def _exists(conn, cursor, users, name):
    cursor.execute(
        Query.from_(users).where(users.username == Parameter('%s')).select(1).limit(1).get_sql(),
        (name,)
    )
    res = cursor.fetchone()
    conn.commit()
    return res is not None


if __name__ == '__main__':
    main()
