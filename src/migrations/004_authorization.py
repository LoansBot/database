"""Amends the users table to be very friendly to PBKDF2_HMAC password auth,
and adds a sessions table. All passwords stored are lost in both directions."""


def up(conn, cursor):
    cursor.execute(
        '''
CREATE TABLE permissions(
    id SERIAL,
    name CHARACTER VARYING (63) UNIQUE NOT NULL,
    description TEXT NOT NULL
)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
CREATE TABLE authtokens(
    id SERIAL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token CHARACTER (127) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        'CREATE INDEX ind_authtokens_user_id ON authtokens(user_id)'
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
CREATE TABLE authtoken_permissions(
    id SERIAL,
    authtoken_id INTEGER NOT NULL REFERENCES authtokens(id) ON DELETE CASCADE,
    permission_id INTEGER NOT NULL REFERENCES permissions(id) ON DELETE CASCADE
)
        '''
    )
    print(cursor.query.decode('utf-8'))
    cursor.execute(
        '''
CREATE INDEX ind_authtokenperms_authtoken_id
    ON authtoken_permissions(authtoken_id)
        '''
    )
    print(cursor.query.decode('utf-8'))
    cursor.execute(
        '''
CREATE INDEX ind_authtokenperms_perm_id
    ON authtoken_permissions(permission_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
CREATE TABLE password_authentications(
    id SERIAL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    human BOOLEAN NOT NULL,
    hash_name CHARACTER VARYING(16) NOT NULL,
    hash TEXT NOT NULL UNIQUE,
    salt TEXT NOT NULL,
    iterations INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
CREATE INDEX ind_passw_auths_on_user_id
    ON password_authentications(user_id)

        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
CREATE UNIQUE INDEX ind_passw_auths_on_human_uid
    ON password_authentications(user_id, human)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
CREATE TABLE password_auth_permissions(
    id SERIAL,
    password_authentication_id
        INTEGER NOT NULL
        REFERENCES password_authentications(id)
        ON DELETE CASCADE,
    permission_id INTEGER NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
CREATE INDEX ind_passw_auth_perm_on_paid
    ON password_auth_permissions(password_authentication_id)
        '''
    )

    cursor.execute(
        '''
CREATE INDEX ind_passw_auth_perm_on_permid
    ON password_auth_permissions(permission_id)
        '''
    )

    cursor.execute(
        'ALTER TABLE users REMOVE COLUMN password_digest'
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        'ALTER TABLE users ADD COLUMN password_digest TEXT NULL'
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute('DROP TABLE password_auth_permissions CASCADE')
    print(cursor.query.decode('utf-8'))

    cursor.execute('DROP TABLE password_authentications CASCADE')
    print(cursor.query.decode('utf-8'))

    cursor.execute('DROP TABLE authtoken_permissions CASCADE')
    print(cursor.query.decode('utf-8'))

    cursor.execute('DROP TABLE authtokens CASCADE')
    print(cursor.query.decode('utf-8'))
