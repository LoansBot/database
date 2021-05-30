"""Creates the temporary_bans table"""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE temporary_bans (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            mod_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
            modaction_id TEXT NOT NULL,
            subreddit TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            ends_at TIMESTAMP NOT NULL
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX idx_temporary_bans_on_user_id
            ON temporary_bans(user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX idx_temporary_bans_on_mod_user_id
            ON temporary_bans(mod_user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX idx_temporary_bans_on_ends_at
            ON temporary_bans(ends_at)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP TABLE temporary_bans
        '''
    )
    print(cursor.query.decode('utf-8'))
