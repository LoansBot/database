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

## Schema

```

```
