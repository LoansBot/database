"""This runs while connected to the MySQL LoansBot v2 database, which operated from
2014 through 2020, and produces "export.jsonlines.brotli" which can be imported with
importv2.py into the PostgreSQL based LoansBot v3 operating from 2020 onwards.

This is a logical dump with one JSON value per line, encoded using UTF-8, and
compressed using Brotli.

The format is as follows
"users"
(number of users)
object with keys ["id", "username", "created_at", "updated_at"]
"loans"
(number of loans)
object with keys [
    "id", "lender_id", "borrower_id", "principal_cents",
    "principal_repayment_cents", "unpaid", "deleted",
    "created_at", "updated_at", "deleted_at"
]
"creation_infos"
(number of creation infos)
object with keys ["loan_id", "type", "thread", "user_id", "created_at"]
"repayments"
(number of repayments)
object with keys ["loan_id", "amount_cents", "created_at"]
"fullnames"
(number of fullnames)
string
"trusts"
(number of promo blacklist users)
object with keys ["user_id", "status", "reason"] (status="unknown" if Vetting required, else "bad")
"""
import mysql.connector
from pypika import MySQLQuery as Query, Table, Parameter, Order
from pypika.functions import Function, Count
from pypika.terms import Star
import brotli
import os
from tqdm import tqdm


def main():
    conn = mysql.connector.connect(
        host='localhost',
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASS'),
        database='loans'
    )
    cursor = conn.cursor()

    with open('export.json.brotli', 'wb') as outfile:
        compr = brotli.Compressor(mode=brotli.MODE_TEXT, quality=11)
        def out(sr: str):
            outfile.write(compr.process(sr.encode('utf-8')))

        print('Writing users...')
        write_users(conn, cursor, out)
        print('Writing loans...')
        write_loans(conn, cursor, out)
        print('Writing creation infos...')
        write_creation_infos(conn, cursor, out)
        print('Writing repayments...')
        write_repayments(conn, cursor, out)
        print('Writing fullnames...')
        write_fullnames(conn, cursor, out)
        print('Writing trusts...')
        write_trusts(conn, cursor, out)

        print('Flushing...')
        outfile.write(compr.flush())

    print('All done')


def write_users(conn, cursor, out):
    usernames = Table('usernames')
    users = Table('users')
    cursor.execute(
        Query.from_(usernames)
        .join(users).on(users.id == usernames.user_id)
        .select(Count(Star()))
        .get_sql()
    )
    (cnt_rows,) = cursor.fetchone()

    cursor.execute(
        Query.from_(usernames)
        .join(users).on(users.id == usernames.user_id)
        .orderby(users.id, order=Order.asc)
        .select(
            users.id,
            usernames.username,
            Function('UNIX_TIMESTAMP', users.created_at),
            Function('UNIX_TIMESTAMP', users.updated_at)
        )
        .get_sql()
    )

    fmt = '{{"id":{},"username":"{}","created_at":{},"updated_at":{}}}\n'
    last_user_id = None
    row = cursor.fetchone()
    print('first row:')
    print(fmt.format(*row))
    out('"users"\n')
    with tqdm(total=cnt_rows) as pbar:
        while row is not None:
            if row[0] == last_user_id:
                pbar.update(1)
                row = cursor.fetchone()
                continue
            last_user_id = row[0]
            out(fmt.format(*row))
            pbar.update(1)
            row = cursor.fetchone()


def write_loans(conn, cursor, out):
    loans = Table('loans')
    cursor.execute(
        Query.from_(loans)
        .select(Count(Star()))
        .get_sql()
    )
    (cnt_rows,) = cursor.fetchone()

    cursor.execute(
        Query.from_(loans)
        .select(
            loans.id,
            loans.lender_id,
            loans.borrower_id,
            loans.principal_cents,
            loans.principal_repayment_cents,
            loans.unpaid,
            loans.deleted,
            loans.deleted_reason,
            loans.created_at,
            loans.updated_at,
            loans.deleted_at
        )
        .get_sql()
    )

    fmt = (
        '{{"id":{},"lender_id":{},"borrower_id":{},"principal_cents":{},"principal_repayment_cents":{}'
        '"unpaid":{},"deleted":{},"deleted_reason":{},"created_at":{},"updated_at":{},"deleted_at":{}}}\n'
    )

    row = cursor.fetchone()
    print('first row:')
    print(fmt.format(*row))
    with tqdm(total=cnt_rows):
        while row is not None:
            out(fmt.format(*row))
            tqdm.update(1)
            row = cursor.fetchone()


def write_creation_infos(conn, cursor, out):
    pass


def write_repayments(conn, cursor, out):
    pass


def write_fullnames(conn, cursor, out):
    pass


def write_trusts(conn, cursor, out):
    pass


if __name__ == '__main__':
    main()
