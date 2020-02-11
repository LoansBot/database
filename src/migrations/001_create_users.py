import psycopg2


def up(conn: psycopg2):
    cursor = conn.cursor()
    cursor.execute(
        '''
CREATE TABLE users(
    id serial PRIMARY KEY,
    auth INTEGER NOT NULL DEFAULT 0,
    username CHARACTER VARYING(63),
    password_digest TEXT NULL DEFAULT NULL,
    created_at NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at NOT NULL DEFAULT CURRENT_TIMESTAMP
)
        '''
    )
    print(cursor.query)
    cursor.close()


def down(conn: psycopg2):
    cursor = conn.cursor()
    cursor.execute('DROP TABLE users CASCADE')
    print(cursor.query)
    cursor.close()
