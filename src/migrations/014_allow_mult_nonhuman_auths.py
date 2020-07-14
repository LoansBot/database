"""Creates the X"""


def up(conn, cursor):
    cursor.execute(
        '''
        DROP INDEX ind_passw_auths_on_human_uid
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE UNIQUE INDEX ind_passw_auths_on_human_uid
            ON password_authentications(user_id, human) WHERE (human)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP INDEX ind_passw_auths_on_human_uid
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE UNIQUE INDEX ind_passw_auths_on_human_uid
            ON password_authentications(user_id, human)
        '''
    )
    print(cursor.query.decode('utf-8'))
