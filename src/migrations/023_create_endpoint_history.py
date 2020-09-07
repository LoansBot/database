"""Creates the endpoint history tables. Not storing the history of tables is a
recipe for disaster, even with backups. Furthermore if we do not store a history
we essentially can never grant access to people we only sort of trust. With
these tables it's way easier for us to revert than for people to break things
via the website.

These tables are particularly nice for maintaining a history since we have
stable identifiers for everything which will be interpretable even when the
original records are lost.

This is true for users as well but we only delete user records when we
essentially _have_ to legally speaking, so we probably would have to zero out
usernames anyway, and user ids are faster.
"""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE endpoint_history (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
            slug TEXT NOT NULL,
            old_path TEXT NULL DEFAULT NULL,
            new_path TEXT NOT NULL,
            old_description_markdown TEXT NULL DEFAULT NULL,
            new_description_markdown TEXT NOT NULL,
            old_deprecation_reason_markdown TEXT NULL DEFAULT NULL,
            new_deprecation_reason_markdown TEXT NULL DEFAULT NULL,
            old_deprecated_on DATE NULL DEFAULT NULL,
            new_deprecated_on DATE NULL DEFAULT NULL,
            old_sunsets_on DATE NULL DEFAULT NULL,
            new_sunsets_on DATE NULL DEFAULT NULL,
            old_in_endpoints BOOLEAN NOT NULL,
            new_in_endpoints BOOLEAN NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_endpoint_history_on_endpoint_slug_and_created_at
            ON endpoint_history(slug, created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_endpoint_history_on_user_id_and_created_at
            ON endpoint_history(user_id, created_at)
            WHERE user_id IS NOT NULL
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_endpoint_history_on_created_at
            ON endpoint_history(created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE endpoint_param_history (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
            endpoint_slug TEXT NOT NULL,
            location TEXT NOT NULL,
            path TEXT NOT NULL,
            name TEXT NOT NULL,
            old_var_type TEXT NULL DEFAULT NULL,
            new_var_type TEXT NOT NULL,
            old_description_markdown TEXT NULL DEFAULT NULL,
            new_description_markdown TEXT NOT NULL,
            old_in_endpoint_params BOOLEAN NOT NULL,
            new_in_endpoint_params BOOLEAN NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_endpoint_param_history_on_endpoint_slug_and_created_at
            ON endpoint_param_history(endpoint_slug, created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_endpoint_param_history_on_logical_id_and_created_at
            ON endpoint_param_history(endpoint_slug, location, path, name, created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_endpoint_param_history_on_user_id_and_created_at
            ON endpoint_param_history(user_id, created_at)
            WHERE user_id IS NOT NULL
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_endpoint_param_history_on_created_at
            ON endpoint_param_history(created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE endpoint_alternative_history (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
            old_endpoint_slug TEXT NOT NULL,
            new_endpoint_slug TEXT NOT NULL,
            old_explanation_markdown TEXT NULL DEFAULT NULL,
            new_explanation_markdown TEXT NOT NULL,
            old_in_endpoint_alternatives BOOLEAN NOT NULL,
            new_in_endpoint_alternatives BOOLEAN NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_endpoint_alt_history_on_logical_id_and_created_at
            ON endpoint_alternative_history(old_endpoint_slug, new_endpoint_slug, created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_endpoint_alt_history_on_user_id_and_created_at
            ON endpoint_alternative_history(user_id, created_at)
            WHERE user_id IS NOT NULL
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_endpoint_alt_history_on_created_at
            ON endpoint_alternative_history(created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP TABLE endpoint_alternative_history CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        DROP TABLE endpoint_param_history CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        DROP TABLE endpoint_history CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))
