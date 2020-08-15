# Delayed Queue

Represents any sort of delayed event handling process. Events are just a queue
type associiated with a particular timestamp. Events are assigned uuids; it's
expected that most event handlers will store additional context information
based on the uuid elsewhere, such as in Arango.

Additional tooling is available in "lbshared.delayed_queue".

Expected common queries are:

- Insert event: `INSERT INTO delayed_queue (uuid, queue_type, event_at) VALUES (?, ?, ?)`
- Get next events: `SELECT * FROM delayed_queue WHERE queue_type = ? ORDER BY event_at LIMIT ?`
- Remove by uuid: `DELETE FROM delayed_queue WHERE uuid=?`

## Schema

```
                                                            Table "public.delayed_queue"
   Column   |            Type             | Collation | Nullable |                  Default                  | Storage  | Stats target | Description
------------+-----------------------------+-----------+----------+-------------------------------------------+----------+--------------+-------------
 id         | integer                     |           | not null | nextval('delayed_queue_id_seq'::regclass) | plain    |              |
 uuid       | text                        |           | not null |                                           | extended |              |
 queue_type | integer                     |           | not null |                                           | plain    |              |
 event_at   | timestamp without time zone |           | not null |                                           | plain    |              |
 created_at | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                         | plain    |              |
Indexes:
    "delayed_queue_pkey" PRIMARY KEY, btree (id)
    "delayed_queue_uuid_key" UNIQUE CONSTRAINT, btree (uuid)
    "index_delayed_queue_on_queue_type_event_at" btree (queue_type, event_at)
```
