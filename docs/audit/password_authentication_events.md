# Password Authentication Events

Describe the changes made to a password authentication method. The reason is
sometimes auto-generated, since permission grants / revocations are sometimes
autogenerated (i.e., "Banned from /r/borrow").

Valid types:

- created: The authentication method was created. Permission should be null.
- deleted: The authentication method was soft-deleted. Permission should be null.
- permission-granted: A permission was granted. Permission should not be null.
- permission-revoked: A permission was revoked. Permission should not be null.
- password-changed: The password was changed. Permission should be null.


## Schema

```
                                                                    Table "public.password_authentication_events"
           Column           |            Type             | Collation | Nullable |                          Default                           | Storage  | Stats target | Description
----------------------------+-----------------------------+-----------+----------+------------------------------------------------------------+----------+--------------+-------------
 id                         | integer                     |           | not null | nextval('password_authentication_events_id_seq'::regclass) | plain    |              |
 password_authentication_id | integer                     |           | not null |                                                            | plain    |              |
 type                       | text                        |           | not null |                                                            | extended |              |
 reason                     | text                        |           | not null |                                                            | extended |              |
 user_id                    | integer                     |           |          |                                                            | plain    |              |
 permission_id              | integer                     |           |          |                                                            | plain    |              |
 created_at                 | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                          | plain    |              |
Indexes:
    "password_authentication_events_pk" PRIMARY KEY, btree (id)
    "idx_pass_auth_events_on_pass_auth_id" btree (password_authentication_id)
    "idx_pass_auth_events_on_user_id" btree (user_id)
Foreign-key constraints:
    "password_authentication_events_password_authentication_id_fkey" FOREIGN KEY (password_authentication_id) REFERENCES password_authentications(id) ON DELETE CASCADE
    "password_authentication_events_permission_id_fkey" FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
    "password_authentication_events_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
```
