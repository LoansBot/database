import unittest
import helper


class DownTest(unittest.TestCase):
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

    def test_loan_creation_infos_missing_pkey(self):
        self.assertFalse(
            helper.check_if_pkey_exists(self.cursor, 'loan_creation_infos')
        )

    def test_password_authentication_events_missing_pkey(self):
        self.assertFalse(
            helper.check_if_pkey_exists(self.cursor, 'password_authentication_events')
        )

    def test_user_settings_events_missing_pkey(self):
        self.assertFalse(
            helper.check_if_pkey_exists(self.cursor, 'user_settings_events')
        )


if __name__ == '__main__':
    unittest.main()
