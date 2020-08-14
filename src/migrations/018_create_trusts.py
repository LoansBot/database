"""Creates the trusts table. Users are in one of a given list of trusted states,
initially 'unknown', 'good', or 'bad' for not vetted, good standing, and bad
standing respectively.
"""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE trusts (
            id SERIAL PRIMARY KEY,
            user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            status TEXT NOT NULL,
            reason TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX user_id_and_status_on_trusts
            ON trusts(user_id, status)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE trust_events(
            id SERIAL PRIMARY KEY,
            trust_id INTEGER NOT NULL REFERENCES trusts(id) ON DELETE CASCADE,
            mod_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
            old_status TEXT NULL,
            new_status TEXT NOT NULL,
            old_reason TEXT NULL,
            new_reason TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX mod_user_id_on_trust_events
            ON trust_events(mod_user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX created_at_on_trust_events
            ON trust_events(created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP TABLE trust_events CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        DROP TABLE trusts CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))
