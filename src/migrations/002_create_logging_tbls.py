"""Creates the tables necessary for the logging utility.
"""


def up(conn, cursor):
    cursor.execute(
        '''
CREATE TABLE log_applications(
    id SERIAL PRIMARY KEY,
    name CHARACTER VARYING(63) NOT NULL UNIQUE
)
        '''
    )
    print(cursor.query.decode('utf-8'))
    cursor.execute(
        '''
CREATE TABLE log_identifiers(
    id SERIAL PRIMARY KEY,
    identifier CHARACTER VARYING(63) NOT NULL UNIQUE
)
        '''
    )
    print(cursor.query.decode('utf-8'))
    cursor.execute(
        '''
CREATE TABLE log_events(
    id SERIAL PRIMARY KEY,
    level SMALLINT NOT NULL,
    application_id INTEGER NOT NULL REFERENCES log_applications(id) ON DELETE CASCADE,
    identifier_id INTEGER NOT NULL REFERENCES log_identifiers(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
)
        '''
    )
    print(cursor.query.decode('utf-8'))
    cursor.execute(
        '''
CREATE INDEX idx_log_evts_appid ON log_events (application_id)
        '''
    )
    print(cursor.query.decode('utf-8'))
    cursor.execute(
        '''
CREATE INDEX idx_log_evts_idenid ON log_events (identifier_id)
        '''
    )
    print(cursor.query.decode('utf-8'))
    cursor.execute(
        '''
CREATE INDEX idx_log_evts_createdat ON log_events (created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute('DROP TABLE log_events CASCADE')
    print(cursor.query.decode('utf-8'))
    cursor.execute('DROP TABLE log_identifiers CASCADE')
    print(cursor.query.decode('utf-8'))
    cursor.execute('DROP TABLE log_applications CASCADE')
    print(cursor.query.decode('utf-8'))
