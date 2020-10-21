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
from pypika.functions import Function
import brotli
import os


def main():
    conn = mysql.connector.connect(
        host='localhost',
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASS')
    )
    cursor = mydb.cursor()

    with open('export.json', 'wb') as outfile:
        compr = brotli.Compressor(brotli.MODE_TEXT)
        def out(sr: str):
            outfile.write(compr.process(sr.encode('utf-8')))

        write_users(conn, cursor, compr)
        write_loans(conn, cursor, compr)
        write_creation_infos(conn, cursor, compr)
        write_repayments(conn, cursor, compr)
        write_fullnames(conn, cursor, compr)
        write_trusts(conn, cursor, compr)

        outfile.write(compr.flush())



def write_users(conn, cursor, out):
    usernames = Table('usernames')
    users = Table('users')
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

    last_user_id = None
    row = cursor.fetchone()
    out('"users"\n')
    while row is not None:
        if row[0] == last_user_id:
            continue
        last_user_id = row[0]
        out('{"id":{},"username":"{}","created_at":{},"updated_at":{}}\n'.format(*row))
        row = cursor.fetchone()


def write_loans(conn, cursor, out):
    pass


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
