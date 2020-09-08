# Endpoints

Describes a single endpoint on the website. This can be used as a general form
of external documentation, however the main reason it exists (over just using
the auto-generated openapi docs) is for supporting a balanced deprecation and
sunsetting schedule.

This table is queried on directly with deprecated endpoints. The description and
alternatives are sent in PMs to users which are still using deprecated endpoints,
and the deprecation date will affect the frequency of messages (for logged in
users) and the enforced error rate (for logged out users).

Furthermore the sunset date programmatically disables the endpoint and eventually
releases the endpoint (returning 404s).

Fields:
- `id (serial, primary key)`: The surrogate identifier for this row
- `slug (text, unique)`: The identifier we use internally for this endpoint.
  This is hard-coded into the code when the row is added.
- `path (text)`: The path (e.g., `/api/users`) to this endpoint.
- `verb (text)`: The HTTP verb associated with this endpoint, uppercase (e.g.,
  GET). The combination of path and verb is unique.
- `description_markdown (text)`: The description of this endpoint, formatted in
  markdown. Although not absolutely required, we do send this via reddit so it's
  best if it uses the subset of markdown that reddit handles.
- `deprecation_reason_markdown (text, null)`: If this endpoint is deprecated,
  this should be the reason for the deprecation formatted like the description.
- `deprecated_on (date, null)` If not null the endpoint is treated as deprecated
  and this acts as the canonical deprecation date. This is specified as a date and
  not a date-time. This value may be in the future but must be before the sunset
  date.
- `sunsets_on (date, null)`: If the endpoint is deprecated this must be specified;
  this is the date the endpoint will no longer function. This may be localized to
  user local time for the actual sunset time.
- `created_at (datetime)`: Time this row was created
- `updated_at (datetime)`: Time this row or a referencing param or a referencing
  alternative was last updated.

## Schema

```
                                                                     Table "public.endpoints"
           Column            |            Type             | Collation | Nullable |                Default                | Storage  | Stats target | Description
-----------------------------+-----------------------------+-----------+----------+---------------------------------------+----------+--------------+-------------
 id                          | integer                     |           | not null | nextval('endpoints_id_seq'::regclass) | plain    |              |
 slug                        | text                        |           | not null |                                       | extended |              |
 path                        | text                        |           | not null |                                       | extended |              |
 description_markdown        | text                        |           | not null |                                       | extended |              |
 deprecation_reason_markdown | text                        |           |          |                                       | extended |              |
 deprecated_on               | date                        |           |          |                                       | plain    |              |
 sunsets_on                  | date                        |           |          |                                       | plain    |              |
 created_at                  | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                     | plain    |              |
 updated_at                  | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                     | plain    |              |
 verb                        | text                        |           | not null | 'GET'::text                           | extended |              |
Indexes:
    "endpoints_pkey" PRIMARY KEY, btree (id)
    "endpoints_slug_key" UNIQUE CONSTRAINT, btree (slug)
    "index_endpoints_on_path_and_verb" UNIQUE CONSTRAINT, btree (path, verb)
Referenced by:
    TABLE "endpoint_alerts" CONSTRAINT "endpoint_alerts_endpoint_id_fkey" FOREIGN KEY (endpoint_id) REFERENCES endpoints(id) ON DELETE CASCADE
    TABLE "endpoint_alternatives" CONSTRAINT "endpoint_alternatives_new_endpoint_id_fkey" FOREIGN KEY (new_endpoint_id) REFERENCES endpoints(id) ON DELETE CASCADE
    TABLE "endpoint_alternatives" CONSTRAINT "endpoint_alternatives_old_endpoint_id_fkey" FOREIGN KEY (old_endpoint_id) REFERENCES endpoints(id) ON DELETE CASCADE
    TABLE "endpoint_params" CONSTRAINT "endpoint_params_endpoint_id_fkey" FOREIGN KEY (endpoint_id) REFERENCES endpoints(id) ON DELETE CASCADE
    TABLE "endpoint_users" CONSTRAINT "endpoint_users_endpoint_id_fkey" FOREIGN KEY (endpoint_id) REFERENCES endpoints(id) ON DELETE CASCADE
```
