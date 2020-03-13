# Claim Tokens

Claim tokens are very short-lived tokens which are sent to a users reddit
account to prove they control it. For our purposes, proving you own the reddit
account is just as good as providing your password. New users are required to
prove they control the corresponding reddit account before they can crette a
password. Claim tokens are also used to reset passwords.

## Schema

```
                                                            Table "public.claim_tokens"
   Column   |            Type             | Collation | Nullable |                 Default                  | Storage  | Stats target | Description
------------+-----------------------------+-----------+----------+------------------------------------------+----------+--------------+-------------
 id         | integer                     |           | not null | nextval('claim_tokens_id_seq'::regclass) | plain    |              |
 user_id    | integer                     |           | not null |                                          | plain    |              |
 token      | character(63)               |           | not null |                                          | extended |              |
 created_at | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                        | plain    |              |
 expires_at | timestamp without time zone |           | not null |                                          | plain    |              |
Indexes:
    "claim_tokens_pkey" PRIMARY KEY, btree (id)
    "claim_tokens_token_key" UNIQUE CONSTRAINT, btree (token)
    "claim_tokens_user_id_key" UNIQUE CONSTRAINT, btree (user_id)
Foreign-key constraints:
    "claim_tokens_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```
