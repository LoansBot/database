# User Demographic Views

Whenever anyone views the demographic information on a user, we log it. As we
generally do, `admin_user_id` is referring to the user who viewed the info,
which means they had permission to view the information. This could be the
user himself.

If the view was a result of a demographic lookup, we store a reference to
which lookup led to this information.

It is our intention to make the frontend very clear that demographic views are
logged and that they should only attempt to view this information if there is
a good reason to do so. Furthermore, not only to we require the permission on
any requests to view this information, we do not allow authtokens which are not
human, and we do not allow authtokens which are more than an hour old from
viewing this information.

## Schema

```
                                                             Table "public.user_demographic_views"
    Column     |            Type             | Collation | Nullable |                      Default                       | Storage | Stats target | Description
---------------+-----------------------------+-----------+----------+----------------------------------------------------+---------+--------------+-------------
 id            | integer                     |           | not null | nextval('user_demographic_views_id_seq'::regclass) | plain   |              |
 user_id       | integer                     |           | not null |                                                    | plain   |              |
 admin_user_id | integer                     |           | not null |                                                    | plain   |              |
 lookup_id     | integer                     |           |          |                                                    | plain   |              |
 viewed_at     | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                  | plain   |              |
Indexes:
    "user_demographic_views_pkey" PRIMARY KEY, btree (id)
    "user_demographic_views_on_user" btree (user_id)
Foreign-key constraints:
    "user_demographic_views_admin_user_id_fkey" FOREIGN KEY (admin_user_id) REFERENCES users(id) ON DELETE CASCADE
    "user_demographic_views_lookup_id_fkey" FOREIGN KEY (lookup_id) REFERENCES user_demographic_lookups(id) ON DELETE CASCADE
    "user_demographic_views_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```
