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

    def test_endpoint_history_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'endpoint_history')
        )

    def test_endpoint_param_history_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'endpoint_param_history')
        )

    def test_endpoint_alternative_history_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'endpoint_alternative_history')
        )


if __name__ == '__main__':
    unittest.main()
