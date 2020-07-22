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

    def test_user_demographics_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'user_demographics')
        )

    def test_user_demographic_lookups_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'user_demographic_lookups')
        )

    def test_user_demographic_views_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'user_demographic_views')
        )

    def test_user_demographic_history_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'user_demographic_history')
        )


if __name__ == '__main__':
    unittest.main()
