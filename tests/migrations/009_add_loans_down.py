import unittest
import helper


TABLES = (
    'loan_unpaid_events',
    'loan_admin_events',
    'loan_repayment_events',
    'loans',
    'moneys',
    'currencies'
)


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

    def test_foo(self):
        self.assertTrue(False)

    def test_tables_do_not_exist(self):
        for tbl in TABLES:
            self.assertFalse(
                helper.check_if_table_exist(self.cursor, tbl)
            )


if __name__ == '__main__':
    unittest.main()
