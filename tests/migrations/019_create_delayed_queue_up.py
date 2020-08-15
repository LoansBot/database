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

    def test_delayed_queue_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'delayed_queue')
        )

    def test_delayed_queue_has_pkey(self):
        self.assertTrue(
            helper.check_if_pkey_exists(self.cursor, 'delayed_queue')
        )


if __name__ == '__main__':
    unittest.main()
