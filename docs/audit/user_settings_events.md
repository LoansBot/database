# User Settings Events

Contains the history of a users settings. Note that this should not be used
to reconstruct the users settings; the current value of a users settings are
stored in Arango, since it's much more convenient if there are a lot of
settings (but not an enormous number of settings) to access them as a json
blob.

## Schema

```
                                                               Table "public.user_settings_events"
     Column      |            Type             | Collation | Nullable |                     Default                      | Storage  | Stats target | Description
-----------------+-----------------------------+-----------+----------+--------------------------------------------------+----------+--------------+-------------
 id              | integer                     |           | not null | nextval('user_settings_events_id_seq'::regclass) | plain    |              |
 user_id         | integer                     |           | not null |                                                  | plain    |              |
 changer_user_id | integer                     |           |          |                                                  | plain    |              |
 property_name   | text                        |           | not null |                                                  | extended |              |
 old_value       | text                        |           |          |                                                  | extended |              |
 new_value       | text                        |           |          |                                                  | extended |              |
 created_at      | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                | plain    |              |
Indexes:
    "user_settings_events_pk" PRIMARY KEY, btree (id)
    "idx_user_settings_events_on_changer_user_id" btree (changer_user_id)
    "idx_user_settings_events_on_user_id" btree (user_id)
Foreign-key constraints:
    "user_settings_events_changer_user_id_fkey" FOREIGN KEY (changer_user_id) REFERENCES users(id) ON DELETE SET NULL
    "user_settings_events_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```
