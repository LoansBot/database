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

    def test_endpoints_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'endpoints')
        )

    def test_endpoints_has_pkey(self):
        self.assertTrue(
            helper.check_if_pkey_exists(self.cursor, 'endpoints')
        )

    def test_endpoint_params_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'endpoint_params')
        )

    def test_endpoint_params_has_pkey(self):
        self.assertTrue(
            helper.check_if_pkey_exists(self.cursor, 'endpoint_params')
        )

    def test_endpoint_alternatives_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'endpoint_alternatives')
        )

    def test_endpoint_alternatives_has_pkey(self):
        self.assertTrue(
            helper.check_if_pkey_exists(self.cursor, 'endpoint_alternatives')
        )

    def test_endpoint_users_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'endpoint_users')
        )

    def test_endpoint_users_has_pkey(self):
        self.assertTrue(
            helper.check_if_pkey_exists(self.cursor, 'endpoint_users')
        )

    def test_endpoint_alerts_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'endpoint_alerts')
        )

    def test_endpoint_alerts_has_pkey(self):
        self.assertTrue(
            helper.check_if_pkey_exists(self.cursor, 'endpoint_alerts')
        )


if __name__ == '__main__':
    unittest.main()
