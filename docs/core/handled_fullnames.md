# Handled Fullnames

A single-column table with a uniqueness constraint. The only column is
"fullname" with the type `varchar(63)`. If a fullname is in this table, then
the LoansBot has already handled it (and hence won't look at it again).

## Explain

```
                                     Table "public.handled_fullnames"
  Column  |         Type          | Collation | Nullable | Default | Storage  | Stats target | Description
----------+-----------------------+-----------+----------+---------+----------+--------------+-------------
 fullname | character varying(63) |           | not null |         | extended |              |
Indexes:
    "handled_fullnames_fullname_key" UNIQUE CONSTRAINT, btree (fullname)
```
