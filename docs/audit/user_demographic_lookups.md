# User Demographic Lookups

Moderators who have a users real information but not their reddit information
may attempt a lookup in our database. We store exactly what they were searching
for and require them to input a reason for the search. Furthermore, any hits
they get from the lookup will also be stored.

## Schema

```
                                                              Table "public.user_demographic_lookups"
     Column     |            Type             | Collation | Nullable |                       Default                        | Storage  | Stats target | Description
----------------+-----------------------------+-----------+----------+------------------------------------------------------+----------+--------------+-------------
 id             | integer                     |           | not null | nextval('user_demographic_lookups_id_seq'::regclass) | plain    |              |
 admin_user_id  | integer                     |           | not null |                                                      | plain    |              |
 email          | text                        |           |          |                                                      | extended |              |
 name           | text                        |           |          |                                                      | extended |              |
 street_address | text                        |           |          |                                                      | extended |              |
 city           | text                        |           |          |                                                      | extended |              |
 state          | text                        |           |          |                                                      | extended |              |
 zip            | text                        |           |          |                                                      | extended |              |
 country        | text                        |           |          |                                                      | extended |              |
 reason         | text                        |           |          |                                                      | extended |              |
 created_at     | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                    | plain    |              |
Indexes:
    "user_demographic_lookups_pkey" PRIMARY KEY, btree (id)
    "user_demographic_lookups_on_admin" btree (admin_user_id)
Foreign-key constraints:
    "user_demographic_lookups_admin_user_id_fkey" FOREIGN KEY (admin_user_id) REFERENCES users(id) ON DELETE CASCADE
Referenced by:
    TABLE "user_demographic_views" CONSTRAINT "user_demographic_views_lookup_id_fkey" FOREIGN KEY (lookup_id) REFERENCES user_demographic_lookups(id) ON DELETE CASCADE
```
