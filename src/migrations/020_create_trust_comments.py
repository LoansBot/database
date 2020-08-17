"""Creates a simple model for a simple list of comments on an item"""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE trust_comments (
            id SERIAL PRIMARY KEY,
            author_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
            target_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            comment TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_trust_comments_on_list_query
            ON trust_comments (target_id, created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_comments_on_author_id
            ON trust_comments (author_id)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP TABLE trust_comments CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))
