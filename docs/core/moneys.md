# Moneys

Describes some amount of money. This contains both the currency and the amount
of the currency that the money is actually in, plus the value of that money
in USD at the time. It's strongly encouraged that every manipulation on moneys
is done within the same currency to avoid confusion surrounding conversion rate
fluctuation, however it's much easier to perform many bulk queries in a single
currency.

## Explain

```
                                                     Table "public.moneys"
      Column      |  Type   | Collation | Nullable |              Default               | Storage | Stats target | Description
------------------+---------+-----------+----------+------------------------------------+---------+--------------+-------------
 id               | integer |           | not null | nextval('moneys_id_seq'::regclass) | plain   |              |
 currency_id      | integer |           | not null |                                    | plain   |              |
 amount           | integer |           | not null |                                    | plain   |              |
 amount_usd_cents | integer |           | not null |                                    | plain   |              |
Indexes:
    "moneys_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "moneys_currency_id_fkey" FOREIGN KEY (currency_id) REFERENCES currencies(id) ON DELETE RESTRICT
Referenced by:
    TABLE "loan_admin_events" CONSTRAINT "loan_admin_events_new_principal_id_fkey" FOREIGN KEY (new_principal_id) REFERENCES moneys(id) ON DELETE RESTRICT
    TABLE "loan_admin_events" CONSTRAINT "loan_admin_events_new_principal_repayment_id_fkey" FOREIGN KEY (new_principal_repayment_id) REFERENCES moneys(id) ON DELETE RESTRICT
    TABLE "loan_admin_events" CONSTRAINT "loan_admin_events_old_principal_id_fkey" FOREIGN KEY (old_principal_id) REFERENCES moneys(id) ON DELETE RESTRICT
    TABLE "loan_admin_events" CONSTRAINT "loan_admin_events_old_principal_repayment_id_fkey" FOREIGN KEY (old_principal_repayment_id) REFERENCES moneys(id) ON DELETE RESTRICT
    TABLE "loan_repayment_events" CONSTRAINT "loan_repayment_events_repayment_id_fkey" FOREIGN KEY (repayment_id) REFERENCES moneys(id) ON DELETE RESTRICT
    TABLE "loans" CONSTRAINT "loans_principal_id_fkey" FOREIGN KEY (principal_id) REFERENCES moneys(id) ON DELETE RESTRICT
    TABLE "loans" CONSTRAINT "loans_principal_repayment_id_fkey" FOREIGN KEY (principal_repayment_id) REFERENCES moneys(id) ON DELETE RESTRICT
```