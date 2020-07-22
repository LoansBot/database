# User Demographics

A users demographical information. This information can be voluntarily submitted
by a user to improve general confidence in them. The main purpose of a user
submitting this information to the LoansBot is that we can verify they are not
providing different information to each lender without requiring the lenders to
share information with each other. This is tricky in practice, but theoretically
a lender can hash the information, send it to us, and then we hash what we have,
and we verify a match (like a password). This usually requires some manual effort
right now, since with hashing even minor differences can be a big change.

Another advantage is we have a way to contact the user via mail or email, and it
helps us get a general idea of the userbase.

Direct access to this table is carefully monitored; any automated access is
logged to another audit table. Furthermore changes are logged. If the user
requests it we will purge this information here and in our history table.
However, because this makes it impossible for us to monitor who had what
information at what time, once a user does this we will never allow them to
submit demographic information again.

The less paranoid way for a user to delete information is to just modify their
demographics to all nulls without purging the history. Historical information
is all but exclusively used in cases of suspected fraud.

## Schema

```
                                                              Table "public.user_demographics"
     Column     |            Type             | Collation | Nullable |                    Default                    | Storage  | Stats target | Description
----------------+-----------------------------+-----------+----------+-----------------------------------------------+----------+--------------+-------------
 id             | integer                     |           | not null | nextval('user_demographics_id_seq'::regclass) | plain    |              |
 user_id        | integer                     |           | not null |                                               | plain    |              |
 email          | text                        |           |          |                                               | extended |              |
 name           | text                        |           |          |                                               | extended |              |
 street_address | text                        |           |          |                                               | extended |              |
 city           | text                        |           |          |                                               | extended |              |
 state          | text                        |           |          |                                               | extended |              |
 zip            | text                        |           |          |                                               | extended |              |
 country        | text                        |           |          |                                               | extended |              |
 deleted        | boolean                     |           | not null | false                                         | plain    |              |
 created_at     | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                             | plain    |              |
Indexes:
    "user_demographics_pkey" PRIMARY KEY, btree (id)
    "user_demographics_user_id_key" UNIQUE CONSTRAINT, btree (user_id)
Foreign-key constraints:
    "user_demographics_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
Referenced by:
    TABLE "user_demographic_history" CONSTRAINT "user_demographic_history_user_demographic_id_fkey" FOREIGN KEY (user_demographic_id) REFERENCES user_demographics(id) ON DELETE CASCADE
```
