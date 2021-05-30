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

    def test_modaction_in_temporary_tables(self):
        self.assertTrue(
            helper.check_if_column_exist(self.cursor, 'temporary_bans', 'modaction_id')
        )


if __name__ == '__main__':
    unittest.main()
