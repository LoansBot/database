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

    def test_verb_exists(self):
        self.assertTrue(
            helper.check_if_column_exist(
                self.cursor, 'endpoints', 'verb'
            )
        )


if __name__ == '__main__':
    unittest.main()
