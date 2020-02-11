import unittest
from pypika import PostgreSQLQuery as Query, Table, Schema, Parameter
import psycopg2
import helper

class UpTest(unittest.TestCase):
    def setUp(self):
        self.connection = helper.setup_connection()
        self.cursor = self.connection.cursor()

    def tearDown(self):
        self.cursor.close()
        helper.teardown_connection(self.connection)

    def test_users_does_exist(self):
        info_schema = Schema('information_schema').tables
        self.cursor.execute(
            Query.from_(info_schema)
            .where(info_schema.table_type == 'BASE TABLE')
            .where(info_schema.table_schema == 'public')
            .select(1).limit(1).get_sql()
        )
        result = self.cursor.fetchone()
        self.connection.commit()
        self.assertIsNotNone(result)

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


if __name__ == '__main__':
    unittest.main()
