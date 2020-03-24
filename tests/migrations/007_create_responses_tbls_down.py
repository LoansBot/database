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

    def test_responses_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'responses')
        )

    def test_response_histories_dne(self):
        self.assertFalse(
            helper.check_if_table_exist(self.cursor, 'response_histories')
        )


if __name__ == '__main__':
    unittest.main()
