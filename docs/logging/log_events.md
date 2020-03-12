# Log Events

Describes a single logging message from any of the LoansBot applications.
Messages are typically queried by a time range, but are sometimes filtered by
application or identifier ids as well.

## Schema

```
                                                              Table "public.log_events"
     Column     |            Type             | Collation | Nullable |                Default                 | Storage  | Stats target | Description
----------------+-----------------------------+-----------+----------+----------------------------------------+----------+--------------+-------------
 id             | integer                     |           | not null | nextval('log_events_id_seq'::regclass) | plain    |              |
 level          | smallint                    |           | not null |                                        | plain    |              |
 application_id | integer                     |           | not null |                                        | plain    |              |
 identifier_id  | integer                     |           | not null |                                        | plain    |              |
 message        | text                        |           | not null |                                        | extended |              |
 created_at     | timestamp without time zone |           | not null | now()                                  | plain    |              |
Indexes:
    "log_events_pkey" PRIMARY KEY, btree (id)
    "idx_log_evts_appid" btree (application_id)
    "idx_log_evts_createdat" btree (created_at)
    "idx_log_evts_idenid" btree (identifier_id)
Foreign-key constraints:
    "log_events_application_id_fkey" FOREIGN KEY (application_id) REFERENCES log_applications(id) ON DELETE CASCADE
    "log_events_identifier_id_fkey" FOREIGN KEY (identifier_id) REFERENCES log_identifiers(id) ON DELETE CASCADE
```