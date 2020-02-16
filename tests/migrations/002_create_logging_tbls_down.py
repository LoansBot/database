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
