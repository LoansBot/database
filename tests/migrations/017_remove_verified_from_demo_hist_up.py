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

    def test_old_email_verified_dne(self):
        self.assertFalse(
            helper.check_if_column_exist(
                self.cursor,
                'user_demographic_history',
                'old_email_verified'
            )
        )

    def test_new_email_verified_dne(self):
        self.assertFalse(
            helper.check_if_column_exist(
                self.cursor,
                'user_demographic_history',
                'new_email_verified'
            )
        )



if __name__ == '__main__':
    unittest.main()
