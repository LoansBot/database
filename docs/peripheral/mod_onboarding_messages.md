# Mod Onboarding Messages

We send moderators a series of messages, one message per day, when they first
join to introduce them to all the features that are available to them. This
table keeps the messages that we send as responses (one response for the title
and one response for the body) as well as the order of the messages.

The acceptable substitutions for each of these messages is typically just
`{username}` which holds the username of the moderator.

## Schema

```text
                                                 Table "public.mod_onboarding_messages"
  Column   |  Type   | Collation | Nullable |                       Default                       | Storage | Stats target | Description
-----------+---------+-----------+----------+-----------------------------------------------------+---------+--------------+-------------
 id        | integer |           | not null | nextval('mod_onboarding_messages_id_seq'::regclass) | plain   |              |
 msg_order | integer |           | not null |                                                     | plain   |              |
 title_id  | integer |           | not null |                                                     | plain   |              |
 body_id   | integer |           | not null |                                                     | plain   |              |
Indexes:
    "mod_onboarding_messages_pkey" PRIMARY KEY, btree (id)
    "mod_onboarding_messages_msg_order_key" UNIQUE CONSTRAINT, btree (msg_order)
Foreign-key constraints:
    "mod_onboarding_messages_body_id_fkey" FOREIGN KEY (body_id) REFERENCES responses(id) ON DELETE CASCADE
    "mod_onboarding_messages_title_id_fkey" FOREIGN KEY (title_id) REFERENCES responses(id) ON DELETE CASCADE
Access method: heap
```
