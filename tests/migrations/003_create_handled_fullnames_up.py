import unittest
from pypika import PostgreSQLQuery as Query, Table, Parameter
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

    def test_handled_fullnames_does_exist(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'handled_fullnames')
        )

    def test_fullname_uniqueness(self):
        hfullnms = Table('handled_fullnames')
        q_str = Query.into(hfullnms).columns('fullname').insert(Parameter('%s')).get_sql()
        q_args = ('t1_test',)
        self.cursor.execute(q_str, q_args)
        helper.assert_fails_with_pgcode(self, '23505', self.cursor, q_str, q_args)

if __name__ == '__main__':
    unittest.main()
