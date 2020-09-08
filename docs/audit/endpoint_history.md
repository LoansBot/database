# Endpoint History

A record in this table is created whenever the important columns on a row in
endpoints changes. This includes creation and deletion.

## Schema

```
                                                                       Table "public.endpoint_history"
             Column              |            Type             | Collation | Nullable |                   Default                    | Storage  | Stats target | Description
---------------------------------+-----------------------------+-----------+----------+----------------------------------------------+----------+--------------+-------------
 id                              | integer                     |           | not null | nextval('endpoint_history_id_seq'::regclass) | plain    |              |
 user_id                         | integer                     |           |          |                                              | plain    |              |
 slug                            | text                        |           | not null |                                              | extended |              |
 old_path                        | text                        |           |          |                                              | extended |              |
 new_path                        | text                        |           | not null |                                              | extended |              |
 old_description_markdown        | text                        |           |          |                                              | extended |              |
 new_description_markdown        | text                        |           | not null |                                              | extended |              |
 old_deprecation_reason_markdown | text                        |           |          |                                              | extended |              |
 new_deprecation_reason_markdown | text                        |           |          |                                              | extended |              |
 old_deprecated_on               | date                        |           |          |                                              | plain    |              |
 new_deprecated_on               | date                        |           |          |                                              | plain    |              |
 old_sunsets_on                  | date                        |           |          |                                              | plain    |              |
 new_sunsets_on                  | date                        |           |          |                                              | plain    |              |
 old_in_endpoints                | boolean                     |           | not null |                                              | plain    |              |
 new_in_endpoints                | boolean                     |           | not null |                                              | plain    |              |
 created_at                      | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                            | plain    |              |
 old_verb                        | text                        |           |          |                                              | extended |              |
 new_verb                        | text                        |           | not null |                                              | extended |              |
Indexes:
    "endpoint_history_pkey" PRIMARY KEY, btree (id)
    "index_endpoint_history_on_created_at" btree (created_at)
    "index_endpoint_history_on_endpoint_slug_and_created_at" btree (slug, created_at)
    "index_endpoint_history_on_user_id_and_created_at" btree (user_id, created_at) WHERE user_id IS NOT NULL
Foreign-key constraints:
    "endpoint_history_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
```
