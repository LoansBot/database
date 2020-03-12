"""Deletes the auth column on users which is unused"""


def up(conn, cursor):
    cursor.execute(
        'ALTER TABLE users DROP COLUMN auth'
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        'ALTER TABLE users ADD COLUMN auth INTEGER NOT NULL DEFAULT 0'
    )
    print(cursor.query.decode('utf-8'))
