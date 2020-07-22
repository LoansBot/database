"""Creates the X"""


def up(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE loan_creation_infos ADD PRIMARY KEY (id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE password_authentication_events ADD PRIMARY KEY (id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE user_settings_events ADD PRIMARY KEY (id)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE user_settings_events DROP PRIMARY KEY
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE password_authentication_events DROP PRIMARY KEY
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE loan_creation_infos DROP PRIMARY KEY
        '''
    )
    print(cursor.query.decode('utf-8'))
