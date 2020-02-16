import unittest
import helper


class DownTest(unittest.TestCase):
    def setUp(self):
        self.connection = helper.setup_connection()
        self.cursor = self.connection.cursor()

    def tearDown(self):
        self.cursor.close()
        self.connection.rollback()
        helper.teardown_connection(self.connection)

    def test_users_does_not_exist(self):
        self.assertFalse(
            helper.check_if_table_exist(self.connection, self.cursor, 'users')
        )


if __name__ == '__main__':
    unittest.main()
