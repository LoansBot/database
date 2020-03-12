# Permissions

A permission is a the ability to perform a given action. They have a name which
is url-safe and typically how the permission is looked up.

## Schema

```
                                                          Table "public.permissions"
   Column    |         Type          | Collation | Nullable |                 Default                 | Storage  | Stats target | Description
-------------+-----------------------+-----------+----------+-----------------------------------------+----------+--------------+-------------
 id          | integer               |           | not null | nextval('permissions_id_seq'::regclass) | plain    |              |
 name        | character varying(63) |           | not null |                                         | extended |              |
 description | text                  |           | not null |                                         | extended |              |
Indexes:
    "permissions_pkey" PRIMARY KEY, btree (id)
    "permissions_name_key" UNIQUE CONSTRAINT, btree (name)
Referenced by:
    TABLE "authtoken_permissions" CONSTRAINT "authtoken_permissions_permission_id_fkey" FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
    TABLE "password_auth_permissions" CONSTRAINT "password_auth_permissions_permission_id_fkey" FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
```
