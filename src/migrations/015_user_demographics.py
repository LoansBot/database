"""Creates the X"""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE user_demographics (
            id SERIAL PRIMARY KEY,
            user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            email TEXT NULL DEFAULT NULL,
            name TEXT NULL DEFAULT NULL,
            street_address TEXT NULL DEFAULT NULL,
            city TEXT NULL DEFAULT NULL,
            state TEXT NULL DEFAULT NULL,
            zip TEXT NULL DEFAULT NULL,
            country TEXT NULL DEFAULT NULL,
            deleted BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE user_demographic_lookups (
            id SERIAL PRIMARY KEY,
            admin_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            email TEXT NULL,
            name TEXT NULL,
            street_address TEXT NULL,
            city TEXT NULL,
            state TEXT NULL,
            zip TEXT NULL,
            country TEXT NULL,
            reason TEXT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX user_demographic_lookups_on_admin
            ON user_demographic_lookups(admin_user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE user_demographic_views (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            admin_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            lookup_id INTEGER NULL DEFAULT NULL REFERENCES user_demographic_lookups(id) ON DELETE CASCADE,
            viewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX user_demographic_views_on_user
            ON user_demographic_views(user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE user_demographic_history (
            id SERIAL PRIMARY KEY,
            user_demographic_id INTEGER NOT NULL REFERENCES user_demographics(id) ON DELETE CASCADE,
            changed_by_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE SET NULL,
            old_email TEXT NULL,
            new_email TEXT NULL,
            old_email_verified BOOLEAN NOT NULL,
            new_email_verified BOOLEAN NOT NULL,
            old_name TEXT NULL,
            new_name TEXT NULL,
            old_street_address TEXT NULL,
            new_street_address TEXT NULL,
            old_city TEXT NULL,
            new_city TEXT NULL,
            old_state TEXT NULL,
            new_state TEXT NULL,
            old_zip TEXT NULL,
            new_zip TEXT NULL,
            old_country TEXT NULL,
            new_country TEXT NULL,
            old_deleted BOOLEAN NOT NULL,
            new_deleted BOOLEAN NOT NULL,
            changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            purged_at TIMESTAMP NULL
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX user_demographic_history_on_demographic
            ON user_demographic_history(user_demographic_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX user_demographic_history_on_changed_by
            ON user_demographic_history(changed_by_user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP TABLE user_demographic_history
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        DROP TABLE user_demographic_views
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        DROP TABLE user_demographic_lookups
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        DROP TABLE user_demographics
        '''
    )
    print(cursor.query.decode('utf-8'))
