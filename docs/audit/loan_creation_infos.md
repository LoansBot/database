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
 old_country         | text                        |           |          |                                                      | extended |              |
 new_country         | text                        |           |          |                                                      | extended |              |
 old_deleted         | boolean                     |           | not null |                                                      | plain    |              |
 new_deleted         | boolean                     |           | not null |                                                      | plain    |              |
 changed_at          | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                                    | plain    |              |
 purged_at           | timestamp without time zone |           |          |                                                      | plain    |              |
Indexes:
    "user_demographic_history_pkey" PRIMARY KEY, btree (id)
    "user_demographic_history_on_changed_by" btree (changed_by_user_id)
    "user_demographic_history_on_demographic" btree (user_demographic_id)
Foreign-key constraints:
    "user_demographic_history_changed_by_user_id_fkey" FOREIGN KEY (changed_by_user_id) REFERENCES users(id) ON DELETE SET NULL
    "user_demographic_history_user_demographic_id_fkey" FOREIGN KEY (user_demographic_id) REFERENCES user_demographics(id) ON DELETE CASCADE
```
