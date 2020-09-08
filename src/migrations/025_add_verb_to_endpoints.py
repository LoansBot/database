"""Creates the X"""


def up(conn, cursor):
    cursor.execute(
        '''
        DROP INDEX endpoints_path_key
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
        CREATE UNIQUE INDEX index_endpoints_on_path_and_verb
            ON endpoints(path, verb)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP INDEX index_endpoints_on_path_and_verb
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
