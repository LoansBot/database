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

    def test_allows_two_nonhuman(self):
        self.cursor.execute(
            'INSERT INTO users (username) VALUES (%s) RETURNING id', 'foo'
        )
        (user_id,) = self.cursor.fetchone()

        q_str = (
            'INSERT INTO password_authentications ' +
            '(user_id, human, hash_name, hash, salt, iterations) ' +
            'VALUES (%s, %s, %s, %s, %s, %s)'
        )
        q_args = (user_id, False, 'foo', 'foo', 'foo', 10)
        self.cursor.execute(q_str, q_args)
        self.cursor.execute(q_str, q_args)

    def test_allows_exactly_one_human(self):
        self.cursor.execute(
            'INSERT INTO users (username) VALUES (%s) RETURNING id', 'foo'
        )
        (user_id,) = self.cursor.fetchone()

        q_str = (
            'INSERT INTO password_authentications ' +
            '(user_id, human, hash_name, hash, salt, iterations) ' +
            'VALUES (%s, %s, %s, %s, %s, %s)'
        )
        q_args = (user_id, True, 'foo', 'foo', 'foo', 10)
        self.cursor.execute(q_str, q_args)
        helper.assert_fails_with_pgcode(
            self, '23505', self.cursor, q_str, q_args)


if __name__ == '__main__':
    unittest.main()
