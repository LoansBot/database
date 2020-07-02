"""Adds a source multi-table reference to authtokens, so that
we can revoke all authtokens from a particular source, etc."""


def up(conn, cursor):
    cursor.execute(
        'TRUNCATE authtokens CASCADE'
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE authtokens ADD COLUMN source_type TEXT NOT NULL
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE authtokens ADD COLUMN source_id INTEGER NOT NULL
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX idx_authtokens_on_source (source_type, source_id)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP INDEX idx_authtokens_on_source
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE authtokens DROP COLUMN source_id
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE authtokens DROP COLUMN source_type
        '''
    )
    print(cursor.query.decode('utf-8'))
