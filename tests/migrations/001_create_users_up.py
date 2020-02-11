import unittest
from pypika import Query, Table, Parameter
import psycopg2
import helper

class UpTest(unittest.TestCase):
    def setUp(self):
        self.connection = helper.setup_connection()


    def tearDown(self):
        helper.teardown_connection(self.connection)


    def test_users_does_exist(self):
        info_schema = Table('information_schema.tables')
        self.cursor.execute(
            Query.from_(info_schema)
            .where(info_schema.table_type == 'BASE TABLE')
            .where(info_schema.table_schema == 'public')
            .select(1).limit(1).get_sql()
        )
        result = self.cursor.fetchone()
        self.connection.commit()
        self.assertNotNone(result)


    def test_default_values(self):
        users = Table('users')
        self.cursor.execute(
            Query.into(users).columns('username').insert(Parameter('$1')).get_sql(),
            'test-user'
        )
        self.cursor.execute('SELECT currval(pg_get_serial_sequence(\'users\', \'id\'))')
        user_id = self.cursor.fetchone()
        self.cursor.execute(
            Query.from_(users)
            .select(users.username, users.auth, users.password_digest, users.created_at, users.updated_at)
            .where(users.id == Parameter('$1'))
            .limit(1).get_sql(),
            user_id
        )
        row = self.cursor.fetchone()
        self.connection.rollback()

        uname, auth, pdig, cat, updat = row
        self.assertEqual(uname, 'test-user')
        self.assertEqual(auth, 0)
        self.assertNone(pdig)
        self.assertNotNone(cat)
        self.assertNotNone(updat)


if __name__ == '__main__':
    unittest.main()
