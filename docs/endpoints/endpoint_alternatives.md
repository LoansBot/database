# Endpoint Alternatives

Describes perfect or near-alternatives for an endpoint. This is most meaningful
for endpoints which are deprecated. Alternatives are considered as
unidirectional by default to allow documentation for how to migrate to be very
specific.

Fields:
- `id (serial, primary key)`: The surrogate identifier for this row
- `old_endpoint_id (integer, references endpoints(id) on delete cascade)`: The
  endpoint which would be replaced when using this alternative.
- `new_endpoint_id (integer, references endpoints(id) on delete cascade)`: The
  endpoint which would be used instead.
- `explanation_markdown (text)`: How to switch from using the old endpoint to
  the new endpoint. Should be standard markdown, and ideally the subset of
  markdown that reddit supports.
- `created_at (datetime)`: When we created this row
- `updated_at (datetime)`: When we last updated the explanation.

## Schema

```
                                                                 Table "public.endpoint_alternatives"
        Column        |            Type             | Collation | Nullable |                      Default                      | Storage  | Stats target | Description
----------------------+-----------------------------+-----------+----------+---------------------------------------------------+----------+--------------+-------------
 id                   | integer                     |           | not null | nextval('endpoint_alternatives_id_seq'::regclass) | plain    |              |
 old_endpoint_id      | integer                     |           | not null |                                                   | plain    |              |
 new_endpoint_id      | integer                     |           | not null |                                                   | plain    |              |
 explanation_markdown | text                        |           | not null |                                                   | extended |              |
 created_at           | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                 | plain    |              |
 updated_at           | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                 | plain    |              |
Indexes:
    "endpoint_alternatives_pkey" PRIMARY KEY, btree (id)
    "index_ep_alts_on_old_new" UNIQUE, btree (old_endpoint_id, new_endpoint_id)
    "index_endpoint_alternatives_on_new_endpoint_id" btree (new_endpoint_id)
Foreign-key constraints:
    "endpoint_alternatives_new_endpoint_id_fkey" FOREIGN KEY (new_endpoint_id) REFERENCES endpoints(id) ON DELETE CASCADE
    "endpoint_alternatives_old_endpoint_id_fkey" FOREIGN KEY (old_endpoint_id) REFERENCES endpoints(id) ON DELETE CASCADE
```
