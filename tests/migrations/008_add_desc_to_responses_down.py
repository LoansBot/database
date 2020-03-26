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

    def test_response_desc_dne(self):
        self.assertFalse(
            helper.check_if_column_exist(self.cursor, 'responses', 'description')
        )


if __name__ == '__main__':
    unittest.main()
