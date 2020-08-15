"""Creates the delayed queue table"""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE delayed_queue (
            id SERIAL PRIMARY KEY,
            uuid TEXT UNIQUE NOT NULL,
            queue_type INTEGER NOT NULL,
            event_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_delayed_queue_on_queue_type_event_at
            ON delayed_queue(queue_type, event_at)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP TABLE delayed_queue CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))
