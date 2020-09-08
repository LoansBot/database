"""Creates the X"""


def up(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE endpoints
            DROP CONSTRAINT endpoints_path_key
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE endpoints
            ADD COLUMN verb TEXT NOT NULL DEFAULT 'GET'
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE endpoints
            ADD CONSTRAINT index_endpoints_on_path_and_verb
            UNIQUE (path, verb)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE endpoints
            DROP CONSTRAINT index_endpoints_on_path_and_verb
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE endpoints
            DROP COLUMN verb
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE UNIQUE INDEX endpoints_path_key
            ON endpoints(path)
        '''
    )
    print(cursor.query.decode('utf-8'))
