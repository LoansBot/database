"""Creates the tables for moderators and moderator onboarding."""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE moderators (
            id SERIAL PRIMARY KEY,
            user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE mod_onboarding_messages (
            id SERIAL PRIMARY KEY,
            order INTEGER UNIQUE NOT NULL,
            title_id INTEGER NOT NULL REFERENCES responses(id) ON DELETE CASCADE,
            body_id INTEGER NOT NULL REFERENCES responses(id) ON DELETE CASCADE
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE mod_onboarding_progress (
            id SERIAL PRIMARY KEY,
            moderator_id INTEGER UNIQUE NOT NULL REFERENCES moderators(id) ON DELETE CASCADE,
            msg_order INTEGER NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP TABLE mod_onboarding_progress
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        DROP TABLE mod_onboarding_messages
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        DROP TABLE moderators
        '''
    )
    print(cursor.query.decode('utf-8'))
