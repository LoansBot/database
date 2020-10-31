# Mod Onboarding Msg History

This table keeps track of what messages we have sent moderators for
onboarding. It's mainly intended for debugging purposes or if we change
our mind about wanting to duplicate messages to users which become a
moderator, receive a message, and then leave moderator, then gain
moderator again.

## Schema

```
                                             Table "public.mod_onboarding_msg_history"
       Column        |            Type             | Collation | Nullable |                        Default
---------------------+-----------------------------+-----------+----------+--------------------------------------------------------
 id                  | integer                     |           | not null | nextval('mod_onboarding_msg_history_id_seq'::regclass)
 user_id             | integer                     |           | not null |
 title_response_id   | integer                     |           |          |
 title_response_name | text                        |           | not null |
 body_response_id    | integer                     |           |          |
 body_response_name  | text                        |           | not null |
 created_at          | timestamp without time zone |           | not null | CURRENT_TIMESTAMP
Indexes:
    "mod_onboarding_msg_history_pkey" PRIMARY KEY, btree (id)
    "index_mod_onboarding_msg_history_on_body_id" btree (body_response_id)
    "index_mod_onboarding_msg_history_on_title_id" btree (title_response_id)
    "index_mod_onboarding_msg_history_on_user_id" btree (user_id)
Foreign-key constraints:
    "mod_onboarding_msg_history_body_response_id_fkey" FOREIGN KEY (body_response_id) REFERENCES responses(id) ON DELETE SET NULL
    "mod_onboarding_msg_history_title_response_id_fkey" FOREIGN KEY (title_response_id) REFERENCES responses(id) ON DELETE SET NULL
    "mod_onboarding_msg_history_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```
