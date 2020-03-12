# Password Auth Permissions

The permissions associated with a given password authentication.

## Schema

```
                                                                    Table "public.password_auth_permissions"
           Column           |            Type             | Collation | Nullable |                        Default                        | Storage | Stats target | Description
----------------------------+-----------------------------+-----------+----------+-------------------------------------------------------+---------+--------------+-------------
 id                         | integer                     |           | not null | nextval('password_auth_permissions_id_seq'::regclass) | plain   |              |
 password_authentication_id | integer                     |           | not null |                                                       | plain   |              |
 permission_id              | integer                     |           | not null |                                                       | plain   |              |
 created_at                 | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                     | plain   |              |
Indexes:
    "password_auth_permissions_pkey" PRIMARY KEY, btree (id)
    "ind_passw_auth_perm_on_paid" btree (password_authentication_id)
    "ind_passw_auth_perm_on_permid" btree (permission_id)
Foreign-key constraints:
    "password_auth_permissions_password_authentication_id_fkey" FOREIGN KEY (password_authentication_id) REFERENCES password_authentications(id) ON DELETE CASCADE
    "password_auth_permissions_permission_id_fkey" FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
```
