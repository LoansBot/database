"""Creates the X"""


def up(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE temporary_bans DROP COLUMN modaction_id
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE temporary_bans ADD COLUMN modaction_id TEXT NOT NULL
        '''
    )
    print(cursor.query.decode('utf-8'))
