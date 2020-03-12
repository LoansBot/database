# Authtoken Permissions

The grants associated with authtokens.

## Schema

```
                                                   Table "public.authtoken_permissions"
    Column     |  Type   | Collation | Nullable |                      Default                      | Storage | Stats target | Description
---------------+---------+-----------+----------+---------------------------------------------------+---------+--------------+-------------
 id            | integer |           | not null | nextval('authtoken_permissions_id_seq'::regclass) | plain   |              |
 authtoken_id  | integer |           | not null |                                                   | plain   |              |
 permission_id | integer |           | not null |                                                   | plain   |              |
Indexes:
    "authtoken_permissions_pkey" PRIMARY KEY, btree (id)
    "ind_authtokenperms_authtoken_id" btree (authtoken_id)
    "ind_authtokenperms_perm_id" btree (permission_id)
Foreign-key constraints:
    "authtoken_permissions_authtoken_id_fkey" FOREIGN KEY (authtoken_id) REFERENCES authtokens(id) ON DELETE CASCADE
    "authtoken_permissions_permission_id_fkey" FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
```
