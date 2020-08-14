# Trust Events

Describes any changes made to trusts. See "peripheral/trusts.md" for more info
on what trusts are used for.

## Schema

```
                                                             Table "public.trust_events"
   Column    |            Type             | Collation | Nullable |                 Default                  | Storage  | Stats target | Description
-------------+-----------------------------+-----------+----------+------------------------------------------+----------+--------------+-------------
 id          | integer                     |           | not null | nextval('trust_events_id_seq'::regclass) | plain    |              |
 trust_id    | integer                     |           | not null |                                          | plain    |              |
 mod_user_id | integer                     |           |          |                                          | plain    |              |
 old_status  | text                        |           |          |                                          | extended |              |
 new_status  | text                        |           | not null |                                          | extended |              |
 old_reason  | text                        |           |          |                                          | extended |              |
 new_reason  | text                        |           | not null |                                          | extended |              |
 created_at  | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                        | plain    |              |
Indexes:
    "trust_events_pkey" PRIMARY KEY, btree (id)
    "created_at_on_trust_events" btree (created_at)
    "mod_user_id_on_trust_events" btree (mod_user_id)
Foreign-key constraints:
    "trust_events_mod_user_id_fkey" FOREIGN KEY (mod_user_id) REFERENCES users(id) ON DELETE SET NULL
    "trust_events_trust_id_fkey" FOREIGN KEY (trust_id) REFERENCES trusts(id) ON DELETE CASCADE
```
