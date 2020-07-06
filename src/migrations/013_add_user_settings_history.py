"""Creates the user settings history table. Although we do not actually store
user settings within Postgres (we store it in Arango), we do store the history
in Postgres because with regard to the history a row is meaningful. For the
actual settings, we would either need one column per setting or one row per
setting, neither of which is great if there are a very large number of user
settings."""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE user_settings_events (
            id SERIAL,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            changer_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
            property_name TEXT NOT NULL,
            old_value TEXT NULL,
            new_value TEXT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX idx_user_settings_events_on_user_id
            ON user_settings_events(user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX idx_user_settings_events_on_changer_user_id
            ON user_settings_events(changer_user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP TABLE user_settings_events
        '''
    )
    print(cursor.query.decode('utf-8'))
