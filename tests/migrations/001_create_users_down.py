import unittest
from pypika import PostgreSQLQuery as Query, Schema
import psycopg2
import helper

class DownTest(unittest.TestCase):
    def setUp(self):
        self.connection = helper.setup_connection()
        self.cursor = self.connection.cursor()


    def tearDown(self):
        self.cursor.close()
        helper.teardown_connection(self.connection)


    def test_users_does_not_exist(self):
        info_schema = Schema('information_schema').tables
        self.cursor.execute(
            Query.from_(info_schema)
            .where(info_schema.table_type == 'BASE TABLE')
            .where(info_schema.table_schema == 'public')
            .select(1).limit(1).get_sql()
        )
        result = self.cursor.fetchone()
        self.connection.commit()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
