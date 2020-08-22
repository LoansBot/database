# Trust Loan Delays

Although the trust queue is mainly stored in the delayed queue table, which
supports a time-ordered queue, we also sometimes want to review a users trust
status after they have made more loans and thus we have more information.

This table allows specifying that "after user X has completed Y loans as lender,
add them back to the delayed queue with a review date of Z". Specifically in the
above X is the user_id, Y is `loans_completed_as_lender`, and Z is
`min_review_at`.

## Schema

```
                                                                   Table "public.trust_loan_delays"
          Column           |            Type             | Collation | Nullable |                    Default                    | Storage | Stats target | Description
---------------------------+-----------------------------+-----------+----------+-----------------------------------------------+---------+--------------+-------------
 id                        | integer                     |           | not null | nextval('trust_loan_delays_id_seq'::regclass) | plain   |              |
 user_id                   | integer                     |           | not null |                                               | plain   |              |
 loans_completed_as_lender | integer                     |           | not null |                                               | plain   |              |
 min_review_at             | timestamp without time zone |           |          |                                               | plain   |              |
 created_at                | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                             | plain   |              |
Indexes:
    "trust_loan_delays_pkey" PRIMARY KEY, btree (id)
    "trust_loan_delays_user_id_key" UNIQUE CONSTRAINT, btree (user_id)
Foreign-key constraints:
    "trust_loan_delays_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```
