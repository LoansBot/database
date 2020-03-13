# Password Authentications

Password authentications are a method of proving ones identity by a constant
secret which the client knows but the server does not. The clients secret
is hashed and then compared with what the server knows; the hashed value of
the secret.

Password authentications are associated with permissions. A user may have
multiple password authentications which are associated with different
permissions. The permissions are passed to the authtoken upon a successful
login. For non-human logins, the client must provide the id of the password
authentication they are attempting to use.

## Schema

```
                                                            Table "public.password_authentications"
   Column   |            Type             | Collation | Nullable |                       Default                        | Storage  | Stats target | Description
------------+-----------------------------+-----------+----------+------------------------------------------------------+----------+--------------+-------------
 id         | integer                     |           | not null | nextval('password_authentications_id_seq'::regclass) | plain    |              |
 user_id    | integer                     |           | not null |                                                      | plain    |              |
 human      | boolean                     |           | not null |                                                      | plain    |              |
 hash_name  | character varying(16)       |           | not null |                                                      | extended |              |
 hash       | text                        |           | not null |                                                      | extended |              |
 salt       | text                        |           | not null |                                                      | extended |              |
 iterations | integer                     |           | not null |                                                      | plain    |              |
 created_at | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                    | plain    |              |
 last_seen  | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                    | plain    |              |
Indexes:
    "password_authentications_pkey" PRIMARY KEY, btree (id)
    "ind_passw_auths_on_human_uid" UNIQUE, btree (user_id, human)
    "password_authentications_hash_key" UNIQUE CONSTRAINT, btree (hash)
    "ind_passw_auths_on_user_id" btree (user_id)
Foreign-key constraints:
    "password_authentications_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
Referenced by:
    TABLE "password_auth_permissions" CONSTRAINT "password_auth_permissions_password_authentication_id_fkey" FOREIGN KEY (password_authentication_id) REFERENCES password_authentications(id) ON DELETE CASCADE
```