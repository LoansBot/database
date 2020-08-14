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

    def test_trusts_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'trusts')
        )

    def test_trusts_has_pkey(self):
        self.assertTrue(
            helper.check_if_pkey_exists(self.cursor, 'trusts')
        )

    def test_trust_events_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'trust_events')
        )

    def test_trust_events_has_pkey(self):
        self.assertTrue(
            helper.check_if_pkey_exists(self.cursor, 'trust_events')
        )


if __name__ == '__main__':
    unittest.main()
