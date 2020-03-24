import unittest
import helper
from pypika import PostgreSQLQuery as Query, Table, Parameter


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

    def test_responses_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'responses')
        )

    def test_response_histories_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.cursor, 'response_histories')
        )

    def test_responses_unique_name(self):
        responses = Table('responses')
        q_str = Query.into(responses).columns(
            responses.name, responses.response_body
        ).insert(Parameter('%s'), Parameter('%s')).get_sql()
        self.cursor.execute(q_str, ('test_nm', 'Test body'))
        helper.assert_fails_with_pgcode(
            self, '23505', self.cursor, q_str, ('test_nm', 'Test body 2')
        )

    def test_responses_cascades_histories(self):
        resps = Table('responses')
        resp_hists = Table('response_histories')

        self.cursor.execute(
            Query.into(resps).columns(resps.name, resps.response_body)
            .insert(Parameter('%s'), Parameter('%s')).returning(resps.id)
            .get_sql(),
            ('test_nm', 'My response body')
        )
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)
        resp_id = row[0]
        self.assertIsInstance(resp_id, int)

        self.cursor.execute(
            Query.from_(resps).select(1).where(resps.id == Parameter('%s'))
            .get_sql(),
            (resp_id,)
        )
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)

        self.cursor.execute(
            Query.into(resp_hists).columns(
                resp_hists.response_id, resp_hists.old_raw, resp_hists.new_raw,
                resp_hists.reason
            ).insert(*(Parameter('%s') for _ in range(4)))
            .returning(resp_hists.id).get_sql(),
            (resp_id, 'My response body', 'My response body 2', 'testing')
        )
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)
        resp_hist_id = row[0]
        self.assertIsInstance(resp_hist_id, int)

        self.cursor.execute(
            Query.from_(resp_hists).select(1)
            .where(resp_hists.id == Parameter('%s')).get_sql(),
            (resp_hist_id,)
        )
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)

        self.cursor.execute(
            Query.from_(resps).delete().where(resps.id == Parameter('%s'))
            .get_sql(),
            (resp_id,)
        )
        self.cursor.execute(
            Query.from_(resp_hists).select(1)
            .where(resp_hists.id == Parameter('%s')).get_sql(),
            (resp_hist_id,)
        )
        row = self.cursor.fetchone()
        self.assertIsNone(row)
        self.cursor.execute(
            Query.from_(resp_hists).select(1)
            .where(resp_hists.id == Parameter('%s')).get_sql(),
            (resp_hist_id,)
        )
        row = self.cursor.fetchone()
        self.assertIsNone(row)


if __name__ == '__main__':
    unittest.main()
