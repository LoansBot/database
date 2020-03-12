# Authtokens

Authentication tokens are used to prove ones identity with a randomly generated
secret, which the server provided when you used some other authentication
method, such as password authentication. An authentication token has many
grants, based on the original method of authentication.

## Schema

```
                                                             Table "public.authtokens"
    Column    |            Type             | Collation | Nullable |                Default                 | Storage  | Stats target | Description
--------------+-----------------------------+-----------+----------+----------------------------------------+----------+--------------+-------------
 id           | integer                     |           | not null | nextval('authtokens_id_seq'::regclass) | plain    |              |
 user_id      | integer                     |           | not null |                                        | plain    |              |
 token        | character(127)              |           | not null |                                        | extended |              |
 created_at   | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                      | plain    |              |
 last_seen_at | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                      | plain    |              |
 expires_at   | timestamp without time zone |           | not null |                                        | plain    |              |
Indexes:
    "authtokens_pkey" PRIMARY KEY, btree (id)
    "authtokens_token_key" UNIQUE CONSTRAINT, btree (token)
    "ind_authtokens_user_id" btree (user_id)
Foreign-key constraints:
    "authtokens_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
Referenced by:
    TABLE "authtoken_permissions" CONSTRAINT "authtoken_permissions_authtoken_id_fkey" FOREIGN KEY (authtoken_id) REFERENCES authtokens(id) ON DELETE CASCADE
```
