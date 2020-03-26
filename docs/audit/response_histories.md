# Response Histories

Whenever there is an edit to the format of a response, we store it here for
historical reference.

## Schema

```
                                                             Table "public.response_histories"
   Column    |            Type             | Collation | Nullable |                    Default                     | Storage  | Stats target | Description
-------------+-----------------------------+-----------+----------+------------------------------------------------+----------+--------------+-------------
 id          | integer                     |           | not null | nextval('response_histories_id_seq'::regclass) | plain    |              |
 response_id | integer                     |           | not null |                                                | plain    |              |
 user_id     | integer                     |           |          |                                                | plain    |              |
 old_raw     | text                        |           | not null |                                                | extended |              |
 new_raw     | text                        |           | not null |                                                | extended |              |
 reason      | text                        |           | not null |                                                | extended |              |
 created_at  | timestamp without time zone |           | not null | now()                                          | plain    |              |
 old_desc    | text                        |           | not null |                                                | extended |              |
 new_desc    | text                        |           | not null |                                                | extended |              |
Indexes:
    "response_histories_pkey" PRIMARY KEY, btree (id)
    "idx_resp_hists_resp_id" btree (response_id)
    "idx_resp_hists_user_id" btree (user_id)
Foreign-key constraints:
    "response_histories_response_id_fkey" FOREIGN KEY (response_id) REFERENCES responses(id) ON DELETE CASCADE
    "response_histories_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
```
