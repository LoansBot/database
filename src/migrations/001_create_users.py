"""Creates the users table"""


def up(conn, cursor):
    cursor.execute(
        '''
CREATE TABLE users(
    id serial PRIMARY KEY,
    auth INTEGER NOT NULL DEFAULT 0,
    username CHARACTER VARYING(63) UNIQUE NOT NULL,
    password_digest TEXT NULL DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute('DROP TABLE users CASCADE')
    print(cursor.query.decode('utf-8'))
