"""Creates the delays for users to have their trust status reviewd based on
the number of completed loans as lender"""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE trust_loan_delays(
            id SERIAL PRIMARY KEY,
            user_id UNIQUE INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            loans_completed_as_lender INTEGER NOT NULL,
            min_review_at TIMESTAMP NULL,
            created_at NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP TABLE trust_loan_delays CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))
