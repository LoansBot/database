# Endpoint Param History

A row in this table is created whenever any important column on a row in
endpoint_params changes. This includes creating and deleting rows.

## Scheam

```
                                                                   Table "public.endpoint_param_history"
          Column          |            Type             | Collation | Nullable |                      Default                       | Storage  | Stats target | Description
--------------------------+-----------------------------+-----------+----------+----------------------------------------------------+----------+--------------+-------------
 id                       | integer                     |           | not null | nextval('endpoint_param_history_id_seq'::regclass) | plain    |              |
 user_id                  | integer                     |           |          |                                                    | plain    |              |
 endpoint_slug            | text                        |           | not null |                                                    | extended |              |
 location                 | text                        |           | not null |                                                    | extended |              |
 path                     | text                        |           | not null |                                                    | extended |              |
 name                     | text                        |           | not null |                                                    | extended |              |
 old_var_type             | text                        |           |          |                                                    | extended |              |
 new_var_type             | text                        |           | not null |                                                    | extended |              |
 old_description_markdown | text                        |           |          |                                                    | extended |              |
 new_description_markdown | text                        |           | not null |                                                    | extended |              |
 old_in_endpoint_params   | boolean                     |           | not null |                                                    | plain    |              |
 new_in_endpoint_params   | boolean                     |           | not null |                                                    | plain    |              |
 created_at               | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                  | plain    |              |
Indexes:
    "endpoint_param_history_pkey" PRIMARY KEY, btree (id)
    "index_endpoint_param_history_on_created_at" btree (created_at)
    "index_endpoint_param_history_on_endpoint_slug_and_created_at" btree (endpoint_slug, created_at)
    "index_endpoint_param_history_on_logical_id_and_created_at" btree (endpoint_slug, location, path, name, created_at)
    "index_endpoint_param_history_on_user_id_and_created_at" btree (user_id, created_at) WHERE user_id IS NOT NULL
Foreign-key constraints:
    "endpoint_param_history_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
```
