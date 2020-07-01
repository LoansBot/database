"""Creates the X"""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE password_authentication_events (
            id SERIAL,
            password_authentication_id INTEGER NOT NULL REFERENCES password_authentications(id) ON DELETE CASCADE,
            type TEXT NOT NULL,
            reason TEXT NOT NULL,
            user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
            permission_id INTEGER NULL REFERENCES permissions(id) ON DELETE CASCADE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX idx_pass_auth_events_on_pass_auth_id
            ON password_authentication_events(password_authentication_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX idx_pass_auth_events_on_user_id
            ON password_authentication_events(user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        ALTER TABLE password_authentications ADD COLUMN deleted BOOLEAN NOT NULL DEFAULT FALSE
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        'DROP TABLE password_authentication_events CASCADE'
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        'ALTER TABLE password_authentications DROP COLUMN deleted'
    )
