# Log Applications

Describes an application which is using the postgres logging approach. Every
application has a unique application name, which corresponds to a particular
application id.

## Schema

```
                                                       Table "public.log_applications"
 Column |         Type          | Collation | Nullable |                   Default                    | Storage  | Stats target | Description
--------+-----------------------+-----------+----------+----------------------------------------------+----------+--------------+-------------
 id     | integer               |           | not null | nextval('log_applications_id_seq'::regclass) | plain    |              |
 name   | character varying(63) |           | not null |                                              | extended |              |
Indexes:
    "log_applications_pkey" PRIMARY KEY, btree (id)
    "log_applications_name_key" UNIQUE CONSTRAINT, btree (name)
Referenced by:
    TABLE "log_events" CONSTRAINT "log_events_application_id_fkey" FOREIGN KEY (application_id) REFERENCES log_applications(id) ON DELETE CASCADE
```