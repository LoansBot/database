"""Creates the trust blocklist. Users are considered trusted if they meet some
specific set of criteria (for example, 15 loans completed), unless they are on
this blocklist. Users are automatically added to this blocklist when they reach
the criteria for the first time and then they are removed from this blocklist
after the account is manually reviewed.

This is preferred over a trust allow list mainly to make it easier to digest.
We can manually look over a blocklist to see if we missed anyone every once
and a while and it's a manageable number of users, whereas the reverse is not
the case (an allow list would contain the vast majority of lenders).

For some history, in the previous version of the LoansBot this was called the
"promotion_blacklist" because if you were on this list you would have
reduced permissions on the website. The trust blocklist is no longer explicitly
responsible for any permissions, although the tooling is intended to make the
normal path of removing a user from the trust blocklist include granting them
some common low to moderate risk permissions (e.g. rechecks).
"""


def up(conn, cursor):
    cursor.execute(
        '''
        CREATE TABLE trust_blocklist (
            id SERIAL PRIMARY KEY,
            user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            mod_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
            reason TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX mod_user_id_on_trust_blocklist
            ON trust_blocklist(mod_user_id)
        '''
    )
    print(cursor.query.decode('utf-8'))

    cursor.execute(
        '''
        CREATE INDEX created_at_on_trust_blocklist
            ON trust_blocklist(created_at)
        '''
    )
    print(cursor.query.decode('utf-8'))


def down(conn, cursor):
    cursor.execute(
        '''
        DROP TABLE trust_blocklist CASCADE
        '''
    )
    print(cursor.query.decode('utf-8'))
