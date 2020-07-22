"""Creates the X"""


def up(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE loan_creation_infos
            ADD CONSTRAINT loan_creation_infos_pk PRIMARY KEY (id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE password_authentication_events
            ADD CONSTRAINT password_authentication_events_pk PRIMARY KEY (id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE user_settings_events
            ADD CONSTRAINT user_settings_events_pk PRIMARY KEY (id)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE user_settings_events DROP CONSTRAINT loan_creation_infos_pk
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE password_authentication_events DROP CONSTRAINT password_authentication_events_pk
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE user_settings_events DROP CONSTRAINT user_settings_events_pk
        '''
    )
    print(cursor.query.decode('utf-8'))
