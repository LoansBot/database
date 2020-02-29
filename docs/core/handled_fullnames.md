# Handled Fullnames

A single-column table with a uniqueness constraint. The only column is
"fullname" with the type `varchar(63)`. If a fullname is in this table, then
the LoansBot has already handled it (and hence won't look at it again).

## Explain

```text
```
