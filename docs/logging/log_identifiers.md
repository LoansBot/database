# Log Identifiers

Describes the identifiers that are used within applications for their loggers.
Some identifiers may be reused across applications. The identifier is typically
just the path to the file that created the logger.

## Schema

```
                                                         Table "public.log_identifiers"
   Column   |         Type          | Collation | Nullable |                   Default                   | Storage  | Stats target | Description
------------+-----------------------+-----------+----------+---------------------------------------------+----------+--------------+-------------
 id         | integer               |           | not null | nextval('log_identifiers_id_seq'::regclass) | plain    |              |
 identifier | character varying(63) |           | not null |                                             | extended |              |
Indexes:
    "log_identifiers_pkey" PRIMARY KEY, btree (id)
    "log_identifiers_identifier_key" UNIQUE CONSTRAINT, btree (identifier)
Referenced by:
    TABLE "log_events" CONSTRAINT "log_events_identifier_id_fkey" FOREIGN KEY (identifier_id) REFERENCES log_identifiers(id) ON DELETE CASCADE
```