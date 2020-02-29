"""Creates the handled fullnames table.
"""


def up(conn, cursor):
    cursor.execute(
        '''
CREATE TABLE handled_fullnames(
    fullname CHARACTER VARYING(63) NOT NULL UNIQUE
)
        '''
    )
    print(cursor.query.decode('utf-8'))

def down(conn, cursor):
    cursor.execute('DROP TABLE handled_fullnames CASCADE')
    print(cursor.query.decode('utf-8'))
