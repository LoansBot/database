# Endpoint Alternative History

A row in this table is created whenever an important column in a row of the
endpoint_alternatives table is created. This includes creating and deleting
rows.

## Schema

```
                                                                     Table "public.endpoint_alternative_history"
            Column            |            Type             | Collation | Nullable |                         Default                          | Storage  | Stats target | Description
------------------------------+-----------------------------+-----------+----------+----------------------------------------------------------+----------+--------------+-------------
 id                           | integer                     |           | not null | nextval('endpoint_alternative_history_id_seq'::regclass) | plain    |              |
 user_id                      | integer                     |           |          |                                                          | plain    |              |
 old_endpoint_slug            | text                        |           | not null |                                                          | extended |              |
 new_endpoint_slug            | text                        |           | not null |                                                          | extended |              |
 old_explanation_markdown     | text                        |           |          |                                                          | extended |              |
 new_explanation_markdown     | text                        |           | not null |                                                          | extended |              |
 old_in_endpoint_alternatives | boolean                     |           | not null |                                                          | plain    |              |
 new_in_endpoint_alternatives | boolean                     |           | not null |                                                          | plain    |              |
 created_at                   | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                        | plain    |              |
Indexes:
    "endpoint_alternative_history_pkey" PRIMARY KEY, btree (id)
    "index_endpoint_alt_history_on_created_at" btree (created_at)
    "index_endpoint_alt_history_on_logical_id_and_created_at" btree (old_endpoint_slug, new_endpoint_slug, created_at)
    "index_endpoint_alt_history_on_user_id_and_created_at" btree (user_id, created_at) WHERE user_id IS NOT NULL
Foreign-key constraints:
    "endpoint_alternative_history_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
```
