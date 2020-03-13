import unittest
import helper
from pypika import PostgreSQLQuery as Query, Table, Parameter


class UpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = helper.setup_connection()
        cls.cursor = cls.connection.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.cursor.close()
        cls.connection.rollback()
        helper.teardown_connection(cls.connection)

    def tearDown(self):
        self.connection.rollback()

    def test_claim_tokens_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'claim_tokens')
        )


if __name__ == '__main__':
    unittest.main()
