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

    def test_response_desc_exists(self):
        self.assertTrue(
            helper.check_if_column_exist(self.cursor, 'responses', 'description')
        )

    def test_response_hist_old_desc_exists(self):
        self.assertTrue(
            helper.check_if_column_exist(self.cursor, 'responses', 'old_desc')
        )

    def test_response_hist_new_desc_exists(self):
        self.assertTrue(
            helper.check_if_column_exist(self.cursor, 'responses', 'new_desc')
        )


if __name__ == '__main__':
    unittest.main()
