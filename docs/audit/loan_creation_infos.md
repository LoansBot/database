# Loan Creation Infos

This provides additional information about how loans were created, including
enough information to generate a link to the generating comment, if the loan
was created by a comment.

The type column is an enum which takes the following values:

- 0: The loan was created by parsing a comment on reddit. This must have a
  comment and thread fullname set and must not have a mod user id set.
- 1: The loan was created by a moderator action on the website. This must
  not have a comment and thread fullname set and should have a mod user id
  set. The mod user id will be null if the mod which created this loan has
  since been deleted.
- 2: This loan was created from a paid command, where we assumed the presence
  of a loan command that we didn't see yet. We only enable this when the
  loansbot gets really far behind, since it's easier to parse comments from
  older to newer. When we find what we think is the correct loan command we
  update this to loan type 0. If this is set then comment fullname, thread
  fullname, and mod user id must be all null.

The following link format will redirect to the appropriate permalink:

https://reddit.com/comments/{parent_id}/any_text_here/{comment_id}


## Explain

```
                                                     Table "public.loan_creation_infos"
      Column      |  Type   | Collation | Nullable |                     Default                     | Storage  | Stats target | Description
------------------+---------+-----------+----------+-------------------------------------------------+----------+--------------+-------------
 id               | integer |           | not null | nextval('loan_creation_infos_id_seq'::regclass) | plain    |              |
 loan_id          | integer |           | not null |                                                 | plain    |              |
 type             | integer |           | not null |                                                 | plain    |              |
 parent_fullname  | text    |           |          |                                                 | extended |              |
 comment_fullname | text    |           |          |                                                 | extended |              |
 mod_user_id      | integer |           |          |                                                 | plain    |              |
Indexes:
    "loan_creation_infos_loan_id_key" UNIQUE CONSTRAINT, btree (loan_id)
    "index_loan_creation_infos_on_mod_user_id" btree (mod_user_id)
Foreign-key constraints:
    "loan_creation_infos_loan_id_fkey" FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE CASCADE
    "loan_creation_infos_mod_user_id_fkey" FOREIGN KEY (mod_user_id) REFERENCES users(id) ON DELETE SET NULL
```
