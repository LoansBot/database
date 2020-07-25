"""Drops the email verified fields on user demographic history"""


def up(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE user_demographic_history
            DROP COLUMN old_email_verified
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE user_demographic_history
            DROP COLUMN new_email_verified
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        ALTER TABLE user_demographic_history
            ADD COLUMN old_email_verified BOOLEAN NULL
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE user_demographic_history
            ADD COLUMN new_email_verified BOOLEAN NULL
        '''
    )
    print(cursor.query.decode('utf-8'))
