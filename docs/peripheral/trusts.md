# Trusts

When lenders reach key thresholds, such as a X loans completed, moderators will
look over their reddit accounts on a best-effort, no-promises basis to sanity
check for any obvious concerns (such has posting continuously which might
indicate there is a team of users running the account).

How this is actually implemented is that when a user reaches these key
thresholds they automatically get a trust row in this table with the status
"unknown". The moderators are notified by the LoansBot to review the account.
Typically after the review, in order of frequency, one of the following things
happen:

- We change their trust standing from "unknown" to "good" and grant them a few
  permissions, such as access to rechecks or additional analytics.
- We decide that we want to wait a little longer before considering them trusted,
  so we set a reminder after another Y loans and/or Z days pass. The user remains
  in the "unknown" status meanwhile. We may give a reduced number of permissions.
- We detect that the lender is breaking one of our rules or reddits terms of
  service. The lender is notified and banned and the trust status is changed to
  "bad".
- The lender is not technically breaking one of our rules or reddits terms of
  service as far as we are aware but there is a preponderance of evidence that
  they are not acting in the best interest of the borrowers. We change their
  trust status to "bad" but allow them to post on the subreddit, meaning
  borrowers are allowed to make up their own mind. We may give a reduced number
  of permissions.

Our trust status is used as one data point amongst many that borrowers use, and
lenders in good standing will often prominently state it.

The following is our guideline for trust statuses:

- Good: There is a preponderance of evidence to suggest this lender is operating with good intention within the community
- Bad: There is either clear and convincing evidence to suggest this lender is operating with bad intention within the community, or there is a preponderance of evidence this lender is operating with bad intention within the subreddit.

## Schema

```
                                                            Table "public.trusts"
   Column   |            Type             | Collation | Nullable |              Default               | Storage  | Stats target | Description
------------+-----------------------------+-----------+----------+------------------------------------+----------+--------------+-------------
 id         | integer                     |           | not null | nextval('trusts_id_seq'::regclass) | plain    |              |
 user_id    | integer                     |           | not null |                                    | plain    |              |
 status     | text                        |           | not null |                                    | extended |              |
 reason     | text                        |           | not null |                                    | extended |              |
 created_at | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                  | plain    |              |
Indexes:
    "trusts_pkey" PRIMARY KEY, btree (id)
    "trusts_user_id_key" UNIQUE CONSTRAINT, btree (user_id)
    "user_id_and_status_on_trusts" btree (user_id, status)
Foreign-key constraints:
    "trusts_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
Referenced by:
    TABLE "trust_events" CONSTRAINT "trust_events_trust_id_fkey" FOREIGN KEY (trust_id) REFERENCES trusts(id) ON DELETE CASCADE
```
