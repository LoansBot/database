# Loans

The core of the "LoansBot". This is a mutable table that describes the current
state of a loan. For knowing a prior state of the loan, there are events
tables (loan_*_events).

The following information is purposely not stored, as the terms for which loans
are given is considered entirely out-of-scope of the LoansBot:

- Any non-principal transfers (i.e., interest)
- When the loan *should* be repaid (including if they expect multiple installments)
- Requests for loans which are not fulfilled

## Explain

```
                                                                  Table "public.loans"
         Column         |            Type             | Collation | Nullable |              Default              | Storage | Stats target | Description
------------------------+-----------------------------+-----------+----------+-----------------------------------+---------+--------------+-------------
 id                     | integer                     |           | not null | nextval('loans_id_seq'::regclass) | plain   |              |
 lender_id              | integer                     |           | not null |                                   | plain   |              |
 borrower_id            | integer                     |           | not null |                                   | plain   |              |
 principal_id           | integer                     |           | not null |                                   | plain   |              |
 principal_repayment_id | integer                     |           | not null |                                   | plain   |              |
 created_at             | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                 | plain   |              |
 repaid_at              | timestamp without time zone |           |          |                                   | plain   |              |
 unpaid_at              | timestamp without time zone |           |          |                                   | plain   |              |
 deleted_at             | timestamp without time zone |           |          |                                   | plain   |              |
Indexes:
    "loans_pkey" PRIMARY KEY, btree (id)
    "idx_loans_borrower" btree (borrower_id)
    "idx_loans_created_at" btree (created_at)
    "idx_loans_lender" btree (lender_id)
    "idx_loans_repaid_at" btree (repaid_at)
    "idx_loans_unpaid_at" btree (unpaid_at)
Foreign-key constraints:
    "loans_borrower_id_fkey" FOREIGN KEY (borrower_id) REFERENCES users(id) ON DELETE CASCADE
    "loans_lender_id_fkey" FOREIGN KEY (lender_id) REFERENCES users(id) ON DELETE CASCADE
    "loans_principal_id_fkey" FOREIGN KEY (principal_id) REFERENCES moneys(id) ON DELETE RESTRICT
    "loans_principal_repayment_id_fkey" FOREIGN KEY (principal_repayment_id) REFERENCES moneys(id) ON DELETE RESTRICT
Referenced by:
    TABLE "loan_admin_events" CONSTRAINT "loan_admin_events_loan_id_fkey" FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE CASCADE
    TABLE "loan_creation_infos" CONSTRAINT "loan_creation_infos_loan_id_fkey" FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE CASCADE
    TABLE "loan_repayment_events" CONSTRAINT "loan_repayment_events_loan_id_fkey" FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE CASCADE
    TABLE "loan_unpaid_events" CONSTRAINT "loan_unpaid_events_loan_id_fkey" FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE CASCADE
```