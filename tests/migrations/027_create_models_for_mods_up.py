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

    def test_moderators_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'moderators')
        )

    def test_moderators_has_pkey(self):
        self.assertTrue(
            helper.check_if_pkey_exists(self.cursor, 'moderators')
        )

    def test_mod_onboarding_messages_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'mod_onboarding_messages')
        )

    def test_mod_onboarding_messages_has_pkey(self):
        self.assertTrue(
            helper.check_if_pkey_exists(self.cursor, 'mod_onboarding_messages')
        )

    def test_mod_onboarding_progress_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'mod_onboarding_progress')
        )

    def test_mod_onboarding_progress_has_pkey(self):
        self.assertTrue(
            helper.check_if_pkey_exists(self.cursor, 'mod_onboarding_progress')
        )


if __name__ == '__main__':
    unittest.main()
