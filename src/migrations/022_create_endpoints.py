"""Creates the database rows which describe endpoints. We use these endpoints
mainly for our endpoint deprecation schedules. We will generally have any
endpoint which is either deprecated, sunsetted, or referenced by a deprecated
or sunsetted endpoint.

Sunsetted endpoints may be removed from this table 1 month after they have
sunsetted, freeing the slug and path to be used by a new endpoint.
"""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE endpoints(
            id SERIAL PRIMARY KEY,
            slug TEXT UNIQUE NOT NULL,
            path TEXT UNIQUE NOT NULL,
            description_markdown TEXT NOT NULL,
            deprecation_reason_markdown TEXT NULL DEFAULT NULL,
            deprecated_on DATE NULL DEFAULT NULL,
            sunsets_on DATE NULL DEFAULT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE endpoint_params(
            id SERIAL PRIMARY KEY,
            endpoint_id INTEGER NOT NULL REFERENCES endpoints(id) ON DELETE CASCADE,
            location TEXT NOT NULL,
            path TEXT NOT NULL,
            name TEXT NOT NULL,
            var_type TEXT NOT NULL,
            description_markdown TEXT NOT NULL,
            added_date DATE NOT NULL DEFAULT CURRENT_DATE
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE UNIQUE INDEX index_endpoint_params_on_ep_loc_path_name
            ON endpoint_params(endpoint_id, location, path, name)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE endpoint_alternatives(
            id SERIAL PRIMARY KEY,
            old_endpoint_id INTEGER NOT NULL REFERENCES endpoints(id) ON DELETE CASCADE,
            new_endpoint_id INTEGER NOT NULL REFERENCES endpoints(id) ON DELETE CASCADE,
            explanation_markdown TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE UNIQUE INDEX index_ep_alts_on_old_new
            ON endpoint_alternatives(old_endpoint_id, new_endpoint_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_endpoint_alternatives_on_new_endpoint_id
            ON endpoint_alternatives(new_endpoint_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE endpoint_users (
            id SERIAL PRIMARY KEY,
            endpoint_id INTEGER NOT NULL REFERENCES endpoints(id) ON DELETE CASCADE,
            user_id INTEGER NULL DEFAULT NULL REFERENCES users(id) ON DELETE CASCADE,
            ip_address TEXT NULL,
            user_agent TEXT NULL,
            response_type TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_endpoint_users_on_endpoint_id_and_created_at
            ON endpoint_users(endpoint_id, created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_epu_on_user_ep_resp_type_cat
            ON endpoint_users(user_id, endpoint_id, response_type, created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_epu_on_ip_ua_ep_rt_cat
            ON endpoint_users(ip_address, user_agent, endpoint_id, response_type, created_at)
            WHERE ip_address IS NOT NULL AND user_agent IS NOT NULL
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE endpoint_alerts (
            id SERIAL PRIMARY KEY,
            endpoint_id INTEGER NOT NULL REFERENCES endpoints(id) ON DELETE CASCADE,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            alert_type TEXT NOT NULL,
            sent_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_ep_alerts_on_user_endpoint_alert_sent_at
            ON endpoint_alerts(user_id, endpoint_id, alert_type, sent_at)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_ep_alerts_on_endpoint_user_alert_sent_at
            ON endpoint_alerts(endpoint_id, user_id, alert_type, sent_at)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP TABLE endpoint_alerts CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        DROP TABLE endpoint_users CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        DROP TABLE endpoint_alternatives CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        DROP TABLE endpoint_params CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        DROP TABLE endpoints CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))
