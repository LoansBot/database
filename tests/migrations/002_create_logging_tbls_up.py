import unittest
from pypika import PostgreSQLQuery as Query, Table, Parameter
import helper


class UpTest(unittest.TestCase):
    def setUpClass(self):
        self.connection = helper.setup_connection()
        self.cursor = self.connection.cursor()
        self.apps = Table('log_applications')
        self.idens = Table('log_identifiers')
        self.events = Table('log_events')

    def tearDownClass(self):
        self.cursor.close()
        self.connection.rollback()
        helper.teardown_connection(self.connection)

    def tearDown(self):
        self.connection.rollback()

    def test_log_events_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.connection, self.cursor, 'log_events')
        )

    def test_log_applications_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.connection, self.cursor, 'log_applications')
        )

    def test_log_identifiers_exists(self):
        self.assertTrue(
            helper.check_if_table_exist(self.connection, self.cursor, 'log_identifiers')
        )

    def test_appname_unique(self):
        q_str = Query.into(self.apps).columns(self.apps.name).insert(Parameter('%s')).get_sql()
        q_args = ('appnm',)
        self.cursor.execute(q_str, q_args)
        helper.assert_fails_with_pgcode(self, '23505', self.connection, self.cursor, q_str, q_args)

    def test_iden_unique(self):
        q_str = Query.into(self.idens).columns(self.idens.identifier).insert(Parameter('%s')).get_sql()
        q_args = ('iden',)
        self.cursor.execute(q_str, q_args)
        helper.assert_fails_with_pgcode(self, '23505', self.connection, self.cursor, q_str, q_args)

    def test_event_defaults(self):
        self.cursor.execute(Query.into(self.apps).columns(self.apps.name).insert(Parameter('%s')).returning(self.apps.id).get_sql(), ('appnm',))
        app_id = self.cursor.fetchone()[0]
        self.cursor.execute(Query.into(self.idens).columns(self.idens.identifier).insert(Parameter('%s')).returning(self.idens.id).get_sql(), ('iden',))
        iden_id = self.cursor.fetchone()[0]
        self.cursor.execute(
            Query.into(self.events)
            .columns(self.events.level, self.events.application_id, self.events.identifier_id, self.events.message)
            .insert(*[Parameter('%s') for _ in range(4)])
            .returning(self.events.created_at).get_sql(),
            (1, app_id, iden_id, 'my message')
        )
        cat = self.cursor.fetchone()[0]
        self.assertIsNotNone(cat)

    def test_event_requires_level(self):
        self.cursor.execute(Query.into(self.apps).columns(self.apps.name).insert(Parameter('%s')).returning(self.apps.id).get_sql(), ('appnm',))
        app_id = self.cursor.fetchone()[0]
        self.cursor.execute(Query.into(self.idens).columns(self.idens.identifier).insert(Parameter('%s')).returning(self.idens.id).get_sql(), ('iden',))
        iden_id = self.cursor.fetchone()[0]
        helper.assert_fails_with_pgcode(
            self, '23502', self.connection, self.cursor,
            Query.into(self.events)
            .columns(self.events.application_id, self.events.identifier_id, self.events.message)
            .insert(*[Parameter('%s') for _ in range(3)])
            .get_sql(),
            (app_id, iden_id, 'my message')
        )

    def test_event_requires_appid(self):
        self.cursor.execute(Query.into(self.idens).columns(self.idens.identifier).insert(Parameter('%s')).returning(self.idens.id).get_sql(), ('iden',))
        iden_id = self.cursor.fetchone()[0]
        helper.assert_fails_with_pgcode(
            self, '23502', self.connection, self.cursor,
            Query.into(self.events)
            .columns(self.events.level, self.events.identifier_id, self.events.message)
            .insert(*[Parameter('%s') for _ in range(3)])
            .get_sql(),
            (1, iden_id, 'my message')
        )

    def test_event_requires_idenid(self):
        self.cursor.execute(Query.into(self.apps).columns(self.apps.name).insert(Parameter('%s')).returning(self.apps.id).get_sql(), ('appnm',))
        app_id = self.cursor.fetchone()[0]
        helper.assert_fails_with_pgcode(
            self, '23502', self.connection, self.cursor,
            Query.into(self.events)
            .columns(self.events.level, self.events.application_id, self.events.message)
            .insert(*[Parameter('%s') for _ in range(3)])
            .get_sql(),
            (1, app_id, 'my message')
        )

if __name__ == '__main__':
    unittest.main()
