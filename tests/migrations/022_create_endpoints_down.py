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

    def test_endpoints_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'endpoints')
        )

    def test_endpoint_params_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'endpoint_params')
        )

    def test_endpoint_alternatives_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'endpoint_alternatives')
        )

    def test_endpoint_users_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'endpoint_users')
        )

    def test_endpoint_alerts_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'endpoint_alerts')
        )


if __name__ == '__main__':
    unittest.main()
