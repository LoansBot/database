# Loan Admin Events

Sometimes users make mistakes or operate maliciously, and a non-standard event
intervenes to correct the issue. For example, a user might accidentally set
a principal of $1.00 instead of $100.

These have a reason which is typically a short bit of text provided by the
admin that explains why they did what they did. Admins are encouraged to
use this field to just link the modmail related to the event, where it
exists.

## Explain

```
                                                                    Table "public.loan_admin_events"
           Column           |            Type             | Collation | Nullable |                    Default                    | Storage  | Stats target | Description
----------------------------+-----------------------------+-----------+----------+-----------------------------------------------+----------+--------------+-------------
 id                         | integer                     |           | not null | nextval('loan_admin_events_id_seq'::regclass) | plain    |              |
 loan_id                    | integer                     |           | not null |                                               | plain    |              |
 admin_id                   | integer                     |           |          |                                               | plain    |              |
 reason                     | text                        |           | not null |                                               | extended |              |
 old_principal_id           | integer                     |           | not null |                                               | plain    |              |
 new_principal_id           | integer                     |           | not null |                                               | plain    |              |
 old_principal_repayment_id | integer                     |           | not null |                                               | plain    |              |
 new_principal_repayment_id | integer                     |           | not null |                                               | plain    |              |
 old_created_at             | timestamp without time zone |           | not null |                                               | plain    |              |
 new_created_at             | timestamp without time zone |           | not null |                                               | plain    |              |
 old_repaid_at              | timestamp without time zone |           |          |                                               | plain    |              |
 new_repaid_at              | timestamp without time zone |           |          |                                               | plain    |              |
 old_unpaid_at              | timestamp without time zone |           |          |                                               | plain    |              |
 new_unpaid_at              | timestamp without time zone |           |          |                                               | plain    |              |
 old_deleted_at             | timestamp without time zone |           |          |                                               | plain    |              |
 new_deleted_at             | timestamp without time zone |           |          |                                               | plain    |              |
 created_at                 | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                             | plain    |              |
Indexes:
    "loan_admin_events_pkey" PRIMARY KEY, btree (id)
    "idx_loan_admin_events_on_admin_and_created_at" btree (admin_id, created_at)
    "idx_loan_admin_events_on_loan" btree (loan_id)
Foreign-key constraints:
    "loan_admin_events_admin_id_fkey" FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE SET NULL
    "loan_admin_events_loan_id_fkey" FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE CASCADE
    "loan_admin_events_new_principal_id_fkey" FOREIGN KEY (new_principal_id) REFERENCES moneys(id) ON DELETE RESTRICT
    "loan_admin_events_new_principal_repayment_id_fkey" FOREIGN KEY (new_principal_repayment_id) REFERENCES moneys(id) ON DELETE RESTRICT
    "loan_admin_events_old_principal_id_fkey" FOREIGN KEY (old_principal_id) REFERENCES moneys(id) ON DELETE RESTRICT
    "loan_admin_events_old_principal_repayment_id_fkey" FOREIGN KEY (old_principal_repayment_id) REFERENCES moneys(id) ON DELETE RESTRICT
```