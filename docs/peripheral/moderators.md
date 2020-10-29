# Moderators

This table keeps a list of all users we know are moderators on /r/borrow. We
send moderators through onboarding and automatically grant them new permissions.
Although we do monitor the event log for gains/losses in moderators, we also do
occassional poll-and-diff style syncing in case the subreddit changes or for
whatever reason we miss the mod change events.

## Schema

```text
                                                            Table "public.moderators"
   Column    |            Type             | Collation | Nullable |                Default                 | Storage | Stats target | Description
-------------+-----------------------------+-----------+----------+----------------------------------------+---------+--------------+-------------
 id          | integer                     |           | not null | nextval('moderators_id_seq'::regclass) | plain   |              |
 user_id     | integer                     |           | not null |                                        | plain   |              |
 detected_at | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                      | plain   |              |
Indexes:
    "moderators_pkey" PRIMARY KEY, btree (id)
    "moderators_user_id_key" UNIQUE CONSTRAINT, btree (user_id)
Foreign-key constraints:
    "moderators_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
Referenced by:
    TABLE "mod_onboarding_progress" CONSTRAINT "mod_onboarding_progress_moderator_id_fkey" FOREIGN KEY (moderator_id) REFERENCES moderators(id) ON DELETE CASCADE
Access method: heap
```
