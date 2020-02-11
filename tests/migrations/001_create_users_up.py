import unittest
import pypika
import psycopg2
import helper

class TestCreateUsers_Down(unittest.TestCase):
    def setUp(self):
        self.connection = helper.setup_connection()

    def tearDown(self):
        helper.teardown_connection(self.connection)

    def test_users_does_exist(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
