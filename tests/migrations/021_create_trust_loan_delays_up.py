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

    def test_trust_loan_delays_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'trust_loan_delays')
        )

    def test_trust_loan_delays_has_pkey(self):
        self.assertTrue(
            helper.check_if_pkey_exists(self.cursor, 'trust_loan_delays')
        )


if __name__ == '__main__':
    unittest.main()
