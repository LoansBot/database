"""Creates the responses tables, which store the format of the messages that
the loansbot (and occassionally the site) send out. The may be edited and we
maintain a history of edits."""


def up(conn, cursor):
    cursor.execute(
        '''
CREATE TABLE responses(
    id SERIAL PRIMARY KEY,
    name CHARACTER VARYING(255) NOT NULL UNIQUE,
    response_body TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
CREATE TABLE response_histories(
    id SERIAL PRIMARY KEY,
    response_id INTEGER NOT NULL REFERENCES responses(id) ON DELETE CASCADE,
    user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
    old_raw TEXT NOT NULL,
    new_raw TEXT NOT NULL,
    reason TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
CREATE INDEX idx_resp_hists_resp_id ON response_histories (response_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
CREATE INDEX idx_resp_hists_user_id ON response_histories (user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute('DROP TABLE response_histories CASCADE')
    print(cursor.query.decode('utf-8'))

    cursor.execute('DROP TABLE responses CASCADE')
    print(cursor.query.decode('utf-8'))
