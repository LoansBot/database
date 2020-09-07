"""Adds updated_at to endpoint_params"""


def up(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE endpoint_params
            ADD COLUMN updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE endpoint_params
            DROP COLUMN updated_at
        '''
    )
    print(cursor.query.decode('utf-8'))
