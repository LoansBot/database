# Loan Unpaid Events

When unpaid is true, this is an event where-in the lender indicates that the
loan is past the originally agreed upon repayment date and there wasn't an
agreement to extend the loan in place.

When unpaid is false, one of two things happened:

- The lender and borrower updated the terms of the loan, so now the loan is
  no longer past its expiration date
- The borrower finished repaying the principal of the loan

Note that for the purposes of the LoansBot, once the principal is repaid the
loan is complete - regardless of how much interest the lender and borrower
agreed to.

## Explain

```
                                                            Table "public.loan_unpaid_events"
   Column   |            Type             | Collation | Nullable |                    Default                     | Storage | Stats target | Description
------------+-----------------------------+-----------+----------+------------------------------------------------+---------+--------------+-------------
 id         | integer                     |           | not null | nextval('loan_unpaid_events_id_seq'::regclass) | plain   |              |
 loan_id    | integer                     |           | not null |                                                | plain   |              |
 unpaid     | boolean                     |           | not null |                                                | plain   |              |
 created_at | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                              | plain   |              |
Indexes:
    "loan_unpaid_events_pkey" PRIMARY KEY, btree (id)
    "idx_loan_unpaid_events_loan" btree (loan_id)
Foreign-key constraints:
    "loan_unpaid_events_loan_id_fkey" FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE CASCADE
```
