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

    def test_log_events_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'log_events')
        )

    def test_log_applications_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'log_applications')
        )

    def test_log_identifiers_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'log_identifiers')
        )


if __name__ == '__main__':
    unittest.main()
