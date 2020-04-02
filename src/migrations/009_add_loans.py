"""Creates the core tables related to loans."""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE currencies (
            id SERIAL PRIMARY KEY,
            code CHARACTER VARYING(4) NOT NULL UNIQUE,
            symbol CHARACTER VARYING(3) NOT NULL,
            symbol_on_left BOOLEAN NOT NULL,
            exponent SMALLINT NOT NULL
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE moneys (
            id SERIAL PRIMARY KEY,
            currency_id INTEGER NOT NULL REFERENCES currencies(id) ON DELETE RESTRICT,
            amount INTEGER NOT NULL,
            amount_usd_cents INTEGER NOT NULL
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE loans (
            id SERIAL PRIMARY KEY,
            lender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            borrower_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            principal_id INTEGER NOT NULL REFERENCES moneys(id) ON DELETE RESTRICT,
            principal_repayment_id INTEGER NOT NULL REFERENCES moneys(id) ON DELETE RESTRICT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            repaid_at TIMESTAMP NULL DEFAULT NULL,
            unpaid_at TIMESTAMP NULL DEFAULT NULL,
            deleted_at TIMESTAMP NULL DEFAULT NULL
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        'CREATE INDEX idx_loans_lender ON loans (lender_id)'
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        'CREATE INDEX idx_loans_borrower ON loans (borrower_id)'
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        'CREATE INDEX idx_loans_created_at ON loans (created_at)'
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        'CREATE INDEX idx_loans_repaid_at ON loans (repaid_at)'
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        'CREATE INDEX idx_loans_unpaid_at ON loans (unpaid_at)'
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE loan_repayment_events (
            id SERIAL PRIMARY KEY,
            loan_id INTEGER NOT NULL REFERENCES loans(id) ON DELETE CASCADE,
            repayment_id INTEGER NOT NULL REFERENCES moneys(id) ON DELETE RESTRICT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX idx_loan_repayments_on_loan
            ON loan_repayment_events (loan_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX idx_loan_repayments_on_created_at
            ON loan_repayment_events (created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE loan_admin_events (
            id SERIAL PRIMARY KEY,
            loan_id INTEGER NOT NULL REFERENCES loans(id) ON DELETE CASCADE,
            admin_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
            reason TEXT NOT NULL,
            old_principal_id INTEGER NOT NULL REFERENCES moneys(id) ON DELETE RESTRICT,
            new_principal_id INTEGER NOT NULL REFERENCES moneys(id) ON DELETE RESTRICT,
            old_principal_repayment_id INTEGER NOT NULL REFERENCES moneys(id) ON DELETE RESTRICT,
            new_principal_repayment_id INTEGER NOT NULL REFERENCES moneys(id) ON DELETE RESTRICT,
            old_created_at TIMESTAMP NOT NULL,
            new_created_at TIMESTAMP NOT NULL,
            old_repaid_at TIMESTAMP NULL,
            new_repaid_at TIMESTAMP NULL,
            old_unpaid_at TIMESTAMP NULL,
            new_unpaid_at TIMESTAMP NULL,
            old_deleted_at TIMESTAMP NULL,
            new_deleted_at TIMESTAMP NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX idx_loan_admin_events_on_loan
            ON loan_admin_events (loan_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX idx_loan_admin_events_on_admin_and_created_at
            ON loan_admin_events (admin_id, created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE TABLE loan_unpaid_events (
            id SERIAL PRIMARY KEY,
            loan_id INTEGER NOT NULL REFERENCES loans(id) ON DELETE CASCADE,
            unpaid BOOLEAN NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX idx_loan_unpaid_events_loan
            ON loan_unpaid_events (loan_id)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    TABLES = (
        'loan_unpaid_events',
        'loan_admin_events',
        'loan_repayment_events',
        'loans',
        'moneys',
        'currencies'
    )
    for tbl in TABLES:
        cursor.execute(f'DROP TABLE {tbl} CASCADE')
        print(cursor.query.decode('utf-8'))
