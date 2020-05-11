"""Creates the loan creation infos, which identify some information surrounding
why a loan was created."""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE loan_creation_infos (
            id SERIAL,
            loan_id INTEGER UNIQUE NOT NULL REFERENCES loans(id) ON DELETE CASCADE,
            type INTEGER NOT NULL,
            parent_fullname TEXT NULL,
            comment_fullname TEXT NULL,
            mod_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX index_loan_creation_infos_on_mod_user_id
            ON loan_creation_infos(mod_user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        'DROP TABLE loan_creation_infos'
    )
    print(cursor.query.decode('utf-8'))
