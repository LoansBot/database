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

    def test_permissions_does_exist(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'permissions')
        )

    def test_authtokens_does_exist(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'authtokens')
        )

    def test_authtoken_permissions_does_exist(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'authtoken_permissions')
        )

    def test_password_auths_does_exist(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'password_authentications')
        )

    def test_password_auth_permissions_does_exist(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'password_auth_permissions')
        )

    def test_password_digest_on_users_does_not_exist(self):
        self.assertFalse(
            helper.check_if_column_exist(self.cursor, 'users', 'password_digest')
        )


if __name__ == '__main__':
    unittest.main()
