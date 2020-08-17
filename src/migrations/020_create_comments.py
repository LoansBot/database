"""Creates a simple model for a simple list of comments on an item"""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE comments (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
            item_type INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_comments_on_list_query
            ON comments (item_type, item_id, created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_comments_on_user_id
            ON comments (user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP TABLE comments CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))
