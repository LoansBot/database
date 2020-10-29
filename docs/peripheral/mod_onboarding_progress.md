# Mod Onboarding Progress

This table just keeps track of where each moderator is within
`mod_onboarding_messages`. A moderator which does not have a row in this table
has not received any onboarding messages yet.

We purposely join to `moderators` and not `users` so that if a user comes as a
moderator, leaves, and rejoins later they restart the onboarding process.

## Schema

```text
                                                             Table "public.mod_onboarding_progress"
    Column    |            Type             | Collation | Nullable |                       Default                       | Storage | Stats target | Description
--------------+-----------------------------+-----------+----------+-----------------------------------------------------+---------+--------------+-------------
 id           | integer                     |           | not null | nextval('mod_onboarding_progress_id_seq'::regclass) | plain   |              |
 moderator_id | integer                     |           | not null |                                                     | plain   |              |
 msg_order    | integer                     |           | not null |                                                     | plain   |              |
 created_at   | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                   | plain   |              |
 updated_at   | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                   | plain   |              |
Indexes:
    "mod_onboarding_progress_pkey" PRIMARY KEY, btree (id)
    "mod_onboarding_progress_moderator_id_key" UNIQUE CONSTRAINT, btree (moderator_id)
Foreign-key constraints:
    "mod_onboarding_progress_moderator_id_fkey" FOREIGN KEY (moderator_id) REFERENCES moderators(id) ON DELETE CASCADE
Access method: heap
```
