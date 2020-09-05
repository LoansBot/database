# Endpoint Users

This table tracks which users are using which endpoints and at what frequency.
If requests are unauthenticated we fallback to storing ip address and user
agent.

This table is _only_ used for deprecated endpoints which have not yet sunsetted.
Although normally I'm hesitant to ever store this type of data, in this
particular case it provides a clear and significant benefit to the user, and
opting out is extremely easy (although it is an opt out). Furthermore it only
affects users which are directly calling endpoints (since the website itself
doesn't use deprecated endpoints) and hence are technically proficient enough to
understand what this is doing and why.

We will use this to fail a small number of requests prior to the sunset if they
do not pass `deprecated=true` and to send pms warning authenticated users they
are using a deprecated endpoint.

To avoid us having to use ip address and user agent we strongly encourage in
our documentation always making authenticated requests for all automated
traffic. Furthermore, we punish unauthenticated requests since they cannot get
around the global ratelimit.

This information is purged as soon as it isn't helpful for this particular job.
After sunsetting an endpoint we delete all references in this table to that
endpoint automatically. It is still available in backups until that clears after
372 days, but backups are not accessed under normal circumstances and are not
easily queryable.

Fields:
- `id (serial, primary key)`: The primary key for this row
- `endpoint_id (integer, references endpoints(id) on delete cascade)`: The
  endpoint which was accessed.
- `user_id (integer, null, references users(id) on delete cascade)`: The user
  which accessed the endpoint, if the request was authenticated. If not null
  then the ip address and user agent will be null. Otherwise the ip address and
  user agent will be set.
- `ip_address (text, null)`: If the request was not authenticated, this is the
  remote ip address.
- `user_agent (text, null)`: If the request was not authenticated, this is the
  provided user agent.
- `response_type (text)`: How the request was handled. Acts as an enum and takes
  one of the following values:
  - `passthrough`: We allowed the request to act as it normally would.
  - `error`: We swapped to an error response (400 Bad Request) where the body
    was formatted in json and indicated this endpoint has been deprecated and
    to pass the `deprecated` flag to suppress this behavior.
`created_at (datetime)`: When the request was performed.

## Schema

```
                                                              Table "public.endpoint_users"
    Column     |            Type             | Collation | Nullable |                  Default                   | Storage  | Stats target | Description
---------------+-----------------------------+-----------+----------+--------------------------------------------+----------+--------------+-------------
 id            | integer                     |           | not null | nextval('endpoint_users_id_seq'::regclass) | plain    |              |
 endpoint_id   | integer                     |           | not null |                                            | plain    |              |
 user_id       | integer                     |           |          |                                            | plain    |              |
 ip_address    | text                        |           |          |                                            | extended |              |
 user_agent    | text                        |           |          |                                            | extended |              |
 response_type | text                        |           | not null |                                            | extended |              |
 created_at    | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                          | plain    |              |
Indexes:
    "endpoint_users_pkey" PRIMARY KEY, btree (id)
    "index_endpoint_users_on_endpoint_id_and_created_at" btree (endpoint_id, created_at)
    "index_epu_on_ip_ua_ep_rt_cat" btree (ip_address, user_agent, endpoint_id, response_type, created_at) WHERE ip_address IS NOT NULL AND user_agent IS NOT NULL
    "index_epu_on_user_ep_resp_type_cat" btree (user_id, endpoint_id, response_type, created_at)
Foreign-key constraints:
    "endpoint_users_endpoint_id_fkey" FOREIGN KEY (endpoint_id) REFERENCES endpoints(id) ON DELETE CASCADE
    "endpoint_users_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
```
