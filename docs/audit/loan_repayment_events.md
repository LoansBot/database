# Loan Repayment Events

An event on a loan that indicates the borrower repaid the lender some amount
of the principal. The created_at timestamp on the event is when the repayment
occurred. Rows in this table, like with all events, are immutable.

## Explain

```
                                                             Table "public.loan_repayment_events"
    Column    |            Type             | Collation | Nullable |                      Default                      | Storage | Stats target | Description
--------------+-----------------------------+-----------+----------+---------------------------------------------------+---------+--------------+-------------
 id           | integer                     |           | not null | nextval('loan_repayment_events_id_seq'::regclass) | plain   |              |
 loan_id      | integer                     |           | not null |                                                   | plain   |              |
 repayment_id | integer                     |           | not null |                                                   | plain   |              |
 created_at   | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                 | plain   |              |
Indexes:
    "loan_repayment_events_pkey" PRIMARY KEY, btree (id)
    "idx_loan_repayments_on_created_at" btree (created_at)
    "idx_loan_repayments_on_loan" btree (loan_id)
Foreign-key constraints:
    "loan_repayment_events_loan_id_fkey" FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE CASCADE
    "loan_repayment_events_repayment_id_fkey" FOREIGN KEY (repayment_id) REFERENCES moneys(id) ON DELETE RESTRICT
```