# User Demographic History

Whenever a users demographics information is changed, we log the old and new
value. Note that the values in this table are purged by request from the user,
but this bars them from further changes (see user_demographics for more info).

To check if information is purged, see the `purged_at` date. All sensitive
fields (i.e., every field except id, user_demographic_id, changed_by_user_id,
old_deleted, new_deleted, and changed_at) will have been replaced with an
arbitrary value (typically null or false) if `purged_at` is set.

## Schema

```
                                                                 Table "public.user_demographic_history"
       Column        |            Type             | Collation | Nullable |                       Default                        | Storage  | Stats target | Description
---------------------+-----------------------------+-----------+----------+------------------------------------------------------+----------+--------------+-------------
 id                  | integer                     |           | not null | nextval('user_demographic_history_id_seq'::regclass) | plain    |              |
 user_demographic_id | integer                     |           | not null |                                                      | plain    |              |
 changed_by_user_id  | integer                     |           | not null |                                                      | plain    |              |
 old_email           | text                        |           |          |                                                      | extended |              |
 new_email           | text                        |           |          |                                                      | extended |              |
 old_email_verified  | boolean                     |           | not null |                                                      | plain    |              |
 new_email_verified  | boolean                     |           | not null |                                                      | plain    |              |
 old_name            | text                        |           |          |                                                      | extended |              |
 new_name            | text                        |           |          |                                                      | extended |              |
 old_street_address  | text                        |           |          |                                                      | extended |              |
 new_street_address  | text                        |           |          |                                                      | extended |              |
 old_city            | text                        |           |          |                                                      | extended |              |
 new_city            | text                        |           |          |                                                      | extended |              |
 old_state           | text                        |           |          |                                                      | extended |              |
 new_state           | text                        |           |          |                                                      | extended |              |
 old_zip             | text                        |           |          |                                                      | extended |              |
 new_zip             | text                        |           |          |                                                      | extended |              |
 old_country         | text                        |           |          |                                                      | extended |              |
 new_country         | text                        |           |          |                                                      | extended |              |
 old_deleted         | boolean                     |           | not null |                                                      | plain    |              |
 new_deleted         | boolean                     |           | not null |                                                      | plain    |              |
 changed_at          | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                    | plain    |              |
 purged_at           | timestamp without time zone |           |          |                                                      | plain    |              |
Indexes:
    "user_demographic_history_pkey" PRIMARY KEY, btree (id)
    "user_demographic_history_on_changed_by" btree (changed_by_user_id)
    "user_demographic_history_on_demographic" btree (user_demographic_id)
Foreign-key constraints:
    "user_demographic_history_changed_by_user_id_fkey" FOREIGN KEY (changed_by_user_id) REFERENCES users(id) ON DELETE SET NULL
    "user_demographic_history_user_demographic_id_fkey" FOREIGN KEY (user_demographic_id) REFERENCES user_demographics(id) ON DELETE CASCADE
```
