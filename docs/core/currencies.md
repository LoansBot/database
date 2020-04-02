# Currencies

Describes a single currency in a somewhat simplified format. Contains the
iso4217 code, a symbol (which may just be the code with a space if there
isn't a good way to represent it that's supported by all browsers),
how much the amount should be multiplied by for integer-storage (and
divided by for display), and which side of the amount to display the
symbol on.

To clarify on how "exponent" works; if the currency is USD, then the
exponent is **2**, because if we take the amount in USD and multiply it
by 10^**2** we get an integer amount (cents).

## Explain

```
                                                           Table "public.currencies"
     Column     |         Type         | Collation | Nullable |                Default                 | Storage  | Stats target | Description
----------------+----------------------+-----------+----------+----------------------------------------+----------+--------------+-------------
 id             | integer              |           | not null | nextval('currencies_id_seq'::regclass) | plain    |              |
 code           | character varying(4) |           | not null |                                        | extended |              |
 symbol         | character varying(5) |           | not null |                                        | extended |              |
 symbol_on_left | boolean              |           | not null |                                        | plain    |              |
 exponent       | smallint             |           | not null |                                        | plain    |              |
Indexes:
    "currencies_pkey" PRIMARY KEY, btree (id)
    "currencies_code_key" UNIQUE CONSTRAINT, btree (code)
Referenced by:
    TABLE "moneys" CONSTRAINT "moneys_currency_id_fkey" FOREIGN KEY (currency_id) REFERENCES currencies(id) ON DELETE RESTRICT
```