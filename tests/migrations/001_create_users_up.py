import unittest
from pypika import PostgreSQLQuery as Query, Table, Parameter
import helper


class UpTest(unittest.TestCase):
    def setUpClass(self):
        self.connection = helper.setup_connection()
        self.cursor = self.connection.cursor()

    def tearDownClass(self):
        self.cursor.close()
        self.connection.rollback()
        helper.teardown_connection(self.connection)

    def tearDown(self):
        self.connection.rollback()

    def test_users_does_exist(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'users')
        )

    def test_default_values(self):
        users = Table('users')
        self.cursor.execute(
            Query.into(users).columns('username').insert(Parameter('%s')).get_sql(),
            ('test-user',)
        )
        self.cursor.execute('SELECT currval(pg_get_serial_sequence(\'users\', \'id\'))')
        user_id = self.cursor.fetchone()
        self.cursor.execute(
            Query.from_(users)
            .select(users.username, users.auth, users.password_digest, users.created_at, users.updated_at)
            .where(users.id == Parameter('%s'))
            .limit(1).get_sql(),
            (user_id,)
        )
        row = self.cursor.fetchone()
        self.connection.rollback()
        self.assertIsNotNone(row)

        uname, auth, pdig, cat, updat = row
        self.assertEqual(uname, 'test-user')
        self.assertEqual(auth, 0)
        self.assertIsNone(pdig)
        self.assertIsNotNone(cat)
        self.assertIsNotNone(updat)

    def test_uname_uniqueness(self):
        users = Table('users')
        q_str = Query.into(users).columns('username').insert(Parameter('%s')).get_sql()
        q_args = ('test-user',)
        self.cursor.execute(q_str, q_args)
        helper.assert_fails_with_pgcode(self, '23505', self.cursor, q_str, q_args)

if __name__ == '__main__':
    unittest.main()
