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

    def test_mod_onboarding_msg_history_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'mod_onboarding_msg_history')
        )

    def test_mod_onboarding_msg_history_has_pkey(self):
        self.assertTrue(
            helper.check_if_pkey_exists(self.cursor, 'mod_onboarding_msg_history')
        )


if __name__ == '__main__':
    unittest.main()
