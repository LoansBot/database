# Users

Describes a user in the LoansBot database. There is a 1-1 correspondance
between these users and reddit accounts.

## Explain

```text
                                                            Table "public.users"
   Column   |            Type             | Collation | Nullable |              Default              | Storage  | Stats target | Description
------------+-----------------------------+-----------+----------+-----------------------------------+----------+--------------+-------------
 id         | integer                     |           | not null | nextval('users_id_seq'::regclass) | plain    |              |
 auth       | integer                     |           | not null | 0                                 | plain    |              |
 username   | character varying(63)       |           | not null |                                   | extended |              |
 created_at | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                 | plain    |              |
 updated_at | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                 | plain    |              |
Indexes:
    "users_pkey" PRIMARY KEY, btree (id)
    "users_username_key" UNIQUE CONSTRAINT, btree (username)
Referenced by:
    TABLE "authtokens" CONSTRAINT "authtokens_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    TABLE "password_authentications" CONSTRAINT "password_authentications_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```
