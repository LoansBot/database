# Trust Comments

Stores a time-ordered list of comments on a particular users trustworthiness
status. This allows for some basic coordination among moderators. Often this
is expected to just be a link to a modmail thread.

## Schema

```
                                                            Table "public.trust_comments"
   Column   |            Type             | Collation | Nullable |                  Default                   | Storage  | Stats target | Description
------------+-----------------------------+-----------+----------+--------------------------------------------+----------+--------------+-------------
 id         | integer                     |           | not null | nextval('trust_comments_id_seq'::regclass) | plain    |              |
 author_id  | integer                     |           |          |                                            | plain    |              |
 target_id  | integer                     |           | not null |                                            | plain    |              |
 comment    | text                        |           | not null |                                            | extended |              |
 created_at | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                          | plain    |              |
 updated_at | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                          | plain    |              |
Indexes:
    "trust_comments_pkey" PRIMARY KEY, btree (id)
    "index_comments_on_author_id" btree (author_id)
    "index_trust_comments_on_list_query" btree (target_id, created_at)
Foreign-key constraints:
    "trust_comments_author_id_fkey" FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
    "trust_comments_target_id_fkey" FOREIGN KEY (target_id) REFERENCES users(id) ON DELETE CASCADE
```
