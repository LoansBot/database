"""Creates a table to keep track of what messages we've sent moderators in
case we want to change the behavior in the future."""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE mod_onboarding_msg_history(
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            title_response_id INTEGER NULL REFERENCES responses(id) ON DELETE SET NULL,
            title_response_name TEXT NOT NULL,
            body_response_id INTEGER NULL REFERENCES responses(id) ON DELETE SET NULL,
            body_response_name TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_mod_onboarding_msg_history_on_user_id
            ON mod_onboarding_msg_history(user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_mod_onboarding_msg_history_on_title_id
            ON mod_onboarding_msg_history(title_response_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_mod_onboarding_msg_history_on_body_id
            ON mod_onboarding_msg_history(body_response_id)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP TABLE mod_onboarding_msg_history
        '''
    )
    print(cursor.query.decode('utf-8'))
