"""Creates the tables for claiming an account or resetting your password. These
are sent to the users reddits accounts."""


def up(conn, cursor):
    cursor.execute(
        '''
CREATE TABLE claim_tokens(
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token CHARACTER (63) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute('DROP TABLE claim_tokens CASCADE')
    print(cursor.query.decode('utf-8'))
