"""Creates the X"""


def up(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE endpoint_history
            ADD COLUMN old_verb TEXT NULL DEFAULT NULL
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE endpoint_history
            ADD COLUMN new_verb TEXT NOT NULL
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE endpoint_history
            DROP COLUMN new_verb
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE endpoint_history
            DROP COLUMN old_verb
        '''
    )
    print(cursor.query.decode('utf-8'))
