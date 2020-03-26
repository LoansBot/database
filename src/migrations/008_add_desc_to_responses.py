"""Adds the description column to the responses table"""


def up(conn, cursor):
    cursor.execute(
        'ALTER TABLE responses ADD COLUMN description TEXT NOT NULL'
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        'ALTER TABLE response_histories ADD COLUMN old_desc TEXT NOT NULL'
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        'ALTER TABLE response_histories ADD COLUMN new_desc TEXT NOT NULL'
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        'ALTER TABLE responses DROP COLUMN description'
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        'ALTER TABLE response_histories DROP COLUMN old_desc'
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        'ALTER TABLE response_histories DROP COLUMN new_desc'
    )
    print(cursor.query.decode('utf-8'))
