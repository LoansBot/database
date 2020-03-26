# Responses

Describes a response that either the loansbot or the website can send to users;
this may include arrow brackets in the response body (`<>`) to indicate a value
should be substituted based on the context the response is being sent in. For
example, `Hello <user1>` might become `Hello Tjstretchalot` after formatting.

There is a history table described at `audit/response_histories`

## Schema

```
                                                              Table "public.responses"
    Column     |            Type             | Collation | Nullable |                Default                | Storage  | Stats target | Description
---------------+-----------------------------+-----------+----------+---------------------------------------+----------+--------------+-------------
 id            | integer                     |           | not null | nextval('responses_id_seq'::regclass) | plain    |              |
 name          | character varying(255)      |           | not null |                                       | extended |              |
 response_body | text                        |           | not null |                                       | extended |              |
 created_at    | timestamp without time zone |           | not null | now()                                 | plain    |              |
 updated_at    | timestamp without time zone |           | not null | now()                                 | plain    |              |
 description   | text                        |           | not null |                                       | extended |              |
Indexes:
    "responses_pkey" PRIMARY KEY, btree (id)
    "responses_name_key" UNIQUE CONSTRAINT, btree (name)
Referenced by:
    TABLE "response_histories" CONSTRAINT "response_histories_response_id_fkey" FOREIGN KEY (response_id) REFERENCES responses(id) ON DELETE CASCADE
```