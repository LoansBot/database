# Users

Describes a user in the LoansBot database. There is a 1-1 correspondance
between these users and reddit accounts.

## Explain

```text
                                                            Table "public.users"
   Column   |            Type             | Collation | Nullable |              Default              | Storage  | Stats target | Description
------------+-----------------------------+-----------+----------+-----------------------------------+----------+--------------+-------------
 id         | integer                     |           | not null | nextval('users_id_seq'::regclass) | plain    |              |
 username   | character varying(63)       |           | not null |                                   | extended |              |
 created_at | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                 | plain    |              |
 updated_at | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                 | plain    |              |
Indexes:
    "users_pkey" PRIMARY KEY, btree (id)
    "users_username_key" UNIQUE CONSTRAINT, btree (username)
Referenced by:
    TABLE "authtokens" CONSTRAINT "authtokens_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    TABLE "claim_tokens" CONSTRAINT "claim_tokens_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    TABLE "loan_admin_events" CONSTRAINT "loan_admin_events_admin_id_fkey" FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE SET NULL
    TABLE "loan_creation_infos" CONSTRAINT "loan_creation_infos_mod_user_id_fkey" FOREIGN KEY (mod_user_id) REFERENCES users(id) ON DELETE SET NULL
    TABLE "loans" CONSTRAINT "loans_borrower_id_fkey" FOREIGN KEY (borrower_id) REFERENCES users(id) ON DELETE CASCADE
    TABLE "loans" CONSTRAINT "loans_lender_id_fkey" FOREIGN KEY (lender_id) REFERENCES users(id) ON DELETE CASCADE
    TABLE "password_authentication_events" CONSTRAINT "password_authentication_events_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
    TABLE "password_authentications" CONSTRAINT "password_authentications_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    TABLE "response_histories" CONSTRAINT "response_histories_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
    TABLE "trust_comments" CONSTRAINT "trust_comments_author_id_fkey" FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
    TABLE "trust_comments" CONSTRAINT "trust_comments_target_id_fkey" FOREIGN KEY (target_id) REFERENCES users(id) ON DELETE CASCADE
    TABLE "trust_events" CONSTRAINT "trust_events_mod_user_id_fkey" FOREIGN KEY (mod_user_id) REFERENCES users(id) ON DELETE SET NULL
    TABLE "trust_loan_delays" CONSTRAINT "trust_loan_delays_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    TABLE "trusts" CONSTRAINT "trusts_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    TABLE "user_demographic_history" CONSTRAINT "user_demographic_history_changed_by_user_id_fkey" FOREIGN KEY (changed_by_user_id) REFERENCES users(id) ON DELETE SET NULL
    TABLE "user_demographic_lookups" CONSTRAINT "user_demographic_lookups_admin_user_id_fkey" FOREIGN KEY (admin_user_id) REFERENCES users(id) ON DELETE CASCADE
    TABLE "user_demographic_views" CONSTRAINT "user_demographic_views_admin_user_id_fkey" FOREIGN KEY (admin_user_id) REFERENCES users(id) ON DELETE CASCADE
    TABLE "user_demographic_views" CONSTRAINT "user_demographic_views_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    TABLE "user_demographics" CONSTRAINT "user_demographics_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    TABLE "user_settings_events" CONSTRAINT "user_settings_events_changer_user_id_fkey" FOREIGN KEY (changer_user_id) REFERENCES users(id) ON DELETE SET NULL
    TABLE "user_settings_events" CONSTRAINT "user_settings_events_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```
