# Endpoint Alerts

Stores what alerts we have already sent out for deprecated but not yet
sunsetted endpoints. This is cleared once the endpoint is sunsetted as we only
need to remember it in order to avoid duplicating pms to users.

We attempt to batch these messages. For the most part they are sent once
per month but they increase in frequency as the sunset schedule nears.

Fields:
- `id (serial, primary key)`: The identifier for this row
- `endpoint_id (integer, references endpoints(id) on delete cascade)`: The
  endpoint which we warned the user that they are using even though it has
  been deprecated.
- `user_id (integer, references users(id) on delete cascade)`: The user that
  we warned.
- `alert_type (string)`: The type of alert that we sent. Acts as an enum and
  takes one of the following values:
  - `initial_pm`: We sent them an initial reddit PM warning for the first time
    we saw them use this endpoint. Intended to happen within 1-2 hours of use,
    since often many endpoints get deprecated at once and we want to batch the
    pms.
  - `reminder`: We sent them a reminder reddit PM warning that we're continuing
    to see uses of the deprecated endpoint since the last alert.
- `sent_at (datetime)`: When we sent this alert

## Schema

```
                                                             Table "public.endpoint_alerts"
   Column    |            Type             | Collation | Nullable |                   Default                   | Storage  | Stats target | Description
-------------+-----------------------------+-----------+----------+---------------------------------------------+----------+--------------+-------------
 id          | integer                     |           | not null | nextval('endpoint_alerts_id_seq'::regclass) | plain    |              |
 endpoint_id | integer                     |           | not null |                                             | plain    |              |
 user_id     | integer                     |           | not null |                                             | plain    |              |
 alert_type  | text                        |           | not null |                                             | extended |              |
 sent_at     | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                           | plain    |              |
Indexes:
    "endpoint_alerts_pkey" PRIMARY KEY, btree (id)
    "index_ep_alerts_on_endpoint_user_alert_sent_at" btree (endpoint_id, user_id, alert_type, sent_at)
    "index_ep_alerts_on_user_endpoint_alert_sent_at" btree (user_id, endpoint_id, alert_type, sent_at)
Foreign-key constraints:
    "endpoint_alerts_endpoint_id_fkey" FOREIGN KEY (endpoint_id) REFERENCES endpoints(id) ON DELETE CASCADE
    "endpoint_alerts_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```
