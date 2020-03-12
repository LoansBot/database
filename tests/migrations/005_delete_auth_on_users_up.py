import unittest
import helper


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

    def test_auth_on_users_does_not_exist(self):
        self.assertFalse(
            helper.check_if_column_exist(self.cursor, 'users', 'auth')
        )


if __name__ == '__main__':
    unittest.main()
