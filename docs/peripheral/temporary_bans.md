# Temporary Bans

This table stores temporary bans to relevant subreddits for users for the
duration of the temporary ban. This is used to flush the users permissions after
the temporary ban would expire, as there is no unban event generated in the
moderator log when a temporary ban expires.

## Schema

```text
                                                             Table "public.temporary_bans"
   Column    |            Type             | Collation | Nullable |                  Default                   | Storage  | Stats target | Description
-------------+-----------------------------+-----------+----------+--------------------------------------------+----------+--------------+-------------
 id          | integer                     |           | not null | nextval('temporary_bans_id_seq'::regclass) | plain    |              |
 user_id     | integer                     |           | not null |                                            | plain    |              |
 mod_user_id | integer                     |           |          |                                            | plain    |              |
 subreddit   | text                        |           | not null |                                            | extended |              |
 created_at  | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                          | plain    |              |
 ends_at     | timestamp without time zone |           | not null |                                            | plain    |              |
Indexes:
    "temporary_bans_pkey" PRIMARY KEY, btree (id)
    "idx_temporary_bans_on_ends_at" btree (ends_at)
    "idx_temporary_bans_on_mod_user_id" btree (mod_user_id)
    "idx_temporary_bans_on_user_id" btree (user_id)
Foreign-key constraints:
    "temporary_bans_mod_user_id_fkey" FOREIGN KEY (mod_user_id) REFERENCES users(id) ON DELETE SET NULL
    "temporary_bans_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
Access method: heap
```
