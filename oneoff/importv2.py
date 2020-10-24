import brotli
import io
import json
import sys
import os.path
import psycopg2
import re
from datetime import datetime
from tqdm import trange
from dotenv import load_dotenv

INFILE = 'export.jsonlines.brotli'


def main():
    if os.path.exists('.env'):
        load_dotenv()
    conn = psycopg2.connect('')
    cursor = conn.cursor()

    rdr = readlines_brotli(INFILE)
    line = next(rdr)
    if line != '"users"':
        print(f'expected "users" table hint, got {line}')
        return

    print('Loading users...')
    inserter = BatchInserter(cursor, 'INSERT INTO users (id, username, created_at, updated_at) VALUES ', 4)
    num_users = int(next(rdr))
    for idx in trange(num_users):
        user = json.loads(next(rdr))
        inserter.append((
            user['id'], user['username'].lower(),
            datetime.fromtimestamp(user['created_at']),
            datetime.fromtimestamp(user['updated_at'])
        ))

    inserter.flush()

    line = next(rdr)
    if line != '"loans"':
        print(f'expected "loans" hint, got {line}')
        return

    cursor.execute(
        'SELECT id FROM currencies WHERE code=%s',
        ('USD',)
    )
    row = cursor.fetchone()
    if row is None:
        cursor.execute(
            'INSERT INTO currencies (code, symbol, symbol_on_left, exponent) VALUES (%s, %s, %s, %s) RETURNING id',
            ('USD', '$', True, 2)
        )
        row = cursor.fetchone()
    (currency_id,) = row

    cursor.execute(
        'PREPARE find_money (int) AS SELECT id FROM moneys WHERE amount_usd_cents=$1 AND currency_id=%s',
        (currency_id,)
    )

    cursor.execute(
        'PREPARE create_money (int) AS INSERT INTO moneys (currency_id, amount, amount_usd_cents) VALUES (%s, $1, $1) RETURNING id',
        (currency_id,)
    )

    print('Loading loans...')
    num_loans = int(next(rdr))
    inserter = BatchInserter(
        cursor,
        'INSERT INTO loans (id,lender_id,borrower_id,principal_id,principal_repayment_id,created_at,repaid_at,unpaid_at,deleted_at) VALUES ',
        9
    )

    money_amount_to_id = dict()

    for idx in trange(num_loans):
        loan = json.loads(next(rdr))

        principal_id = money_amount_to_id.get(loan['principal_cents'])
        if principal_id is None:
            cursor.execute('EXECUTE find_money(%s)', (loan['principal_cents'],))
            row = cursor.fetchone()
            if row is None:
                cursor.execute('EXECUTE create_money(%s)', (loan['principal_cents'],))
                row = cursor.fetchone()
            (principal_id,) = row
            money_amount_to_id[loan['principal_cents']] = principal_id

        principal_repayment_id = money_amount_to_id.get(loan['principal_repayment_cents'])
        if principal_repayment_id is None:
            cursor.execute('EXECUTE find_money(%s)', (loan['principal_repayment_cents'],))
            row = cursor.fetchone()
            if row is None:
                cursor.execute('EXECUTE create_money(%s)', (loan['principal_repayment_cents'],))
                row = cursor.fetchone()
            (principal_repayment_id,) = row
            money_amount_to_id[loan['principal_repayment_cents']] = principal_repayment_id

        repaid_at = None
        if principal_id == principal_repayment_id:
            repaid_at = datetime.fromtimestamp(loan['updated_at'])
        unpaid_at = None
        if loan['unpaid']:
            unpaid_at = datetime.fromtimestamp(loan['updated_at'])
        deleted_at = None
        if loan['deleted_at'] is not None:
            deleted_at = datetime.fromtimestamp(loan['deleted_at'])
        inserter.append((
            loan['id'],
            loan['lender_id'],
            loan['borrower_id'],
            principal_id,
            principal_repayment_id,
            datetime.fromtimestamp(loan['created_at']),
            repaid_at,
            unpaid_at,
            deleted_at
        ))
    inserter.flush()

    line = next(rdr)
    if line != '"creation_infos"':
        print(f'expected "creation_infos" hint, got {line}')
        return

    print('Loading creation infos...')
    pattern = re.compile(r'(https://(www|oauth).reddit.com)?/r/[^/]+/comments/(?P<thread_id>[^/]+)/.*')
    num_cinfos = int(next(rdr))
    inserter = BatchInserter(cursor, 'INSERT INTO loan_creation_infos (loan_id, type, parent_fullname, comment_fullname, mod_user_id) VALUES ', 5)
    for idx in trange(num_cinfos):
        cinfo = json.loads(next(rdr))
        parent_fullname = None
        comment_fullname = None
        if cinfo['thread'] is not None:
            m = pattern.match(cinfo['thread'])
            if m is None:
                print('Invalid thread: ' + cinfo['thread'])
                return
            parent_fullname = m['thread_id']
            comment_fullname = ''
        inserter.append((
            cinfo['loan_id'], cinfo['type'],
            parent_fullname, comment_fullname, cinfo['user_id']
        ))
    inserter.flush()

    line = next(rdr)
    if line != '"repayments"':
        print(f'expected "repayments" hint, got {line}')
        return

    print('Loading repayments...')
    inserter = BatchInserter(cursor, 'INSERT INTO loan_repayment_events (loan_id, repayment_id, created_at) VALUES ', 3, 256)
    num_repayments = int(next(rdr))
    for idx in trange(num_repayments):
        repayment = json.loads(next(rdr))
        repayment_id = money_amount_to_id.get(repayment['amount_cents'])
        if repayment_id is None:
            cursor.execute('EXECUTE find_money(%s)', (repayment['amount_cents'],))
            row = cursor.fetchone()
            if row is None:
                cursor.execute('EXECUTE create_money(%s)', (repayment['amount_cents'],))
                row = cursor.fetchone()
            (repayment_id,) = row
            money_amount_to_id[repayment['amount_cents']] = repayment_id
        inserter.append((
            repayment['loan_id'],
            repayment_id,
            datetime.fromtimestamp(repayment['created_at'])
        ))
    inserter.flush()

    line = next(rdr)
    if line != '"fullnames"':
        print(f'expected "fullnames" hint, got {line}')
        return

    print('Loading fullnames...')
    inserter = BatchInserter(cursor, 'INSERT INTO handled_fullnames VALUES ', 1, 512)
    num_fullnames = int(next(rdr))
    for idx in trange(num_fullnames):
        fullname = json.loads(next(rdr))
        inserter.append((fullname,))
    inserter.flush()

    line = next(rdr)
    if line != '"trusts"':
        print(f'expected "trusts" hint, got {line}')
        return

    cursor.execute(
        'SELECT id FROM users WHERE username=%s',
        ('loansbot',)
    )
    row = cursor.fetchone()
    if row is None:
        cursor.execute(
            'INSERT INTO users (username) VALUES (%s) RETURNING id',
            ('loansbot',)
        )
        row = cursor.fetchone()
    (loansbot_user_id,) = row

    print('Loading trusts...')
    cursor.execute(
        'PREPARE add_trust (int, text, timestamp without time zone) AS '
        'INSERT INTO trusts (user_id, status, reason, created_at) VALUES ($1, %s, $2, $3) '
        'RETURNING id',
        ('bad',)
    )
    cursor.execute(
        'PREPARE add_trust_event (int, text, timestamp without time zone) AS '
        'INSERT INTO trust_events (trust_id, mod_user_id, old_status, new_status, old_reason, new_reason, created_at) '
        'VALUES ($1, %s, %s, %s, %s, $2, $3)',
        (loansbot_user_id, None, 'bad', None)
    )
    num_trusts = int(next(rdr))
    for idx in trange(num_trusts):
        trust = json.loads(next(rdr))
        cursor.execute(
            'EXECUTE add_trust(%s, %s, %s)',
            (trust['user_id'], trust['reason'], datetime.fromtimestamp(trust['added_at']))
        )
        (trust_id,) = cursor.fetchone()
        cursor.execute(
            'EXECUTE add_trust_event (%s, %s, %s)',
            (trust_id, trust['reason'], datetime.fromtimestamp(trust['added_at']))
        )

    conn.commit()
    conn.close()


def readlines_brotli(file):
    with open(file, 'rb') as infile:
        dec = brotli.Decompressor()
        inbuf = io.BytesIO()
        line_extra_from_previous = 0
        while True:
            raw_rem: bytes = infile.read(4096)
            if not raw_rem:
                break
            rem = dec.process(raw_rem)
            previous_ind = 0
            newline_ind = rem.find(b'\n')
            while newline_ind != -1:
                inbuf.write(rem[previous_ind:newline_ind])
                inbuf.seek(0)
                available_bytes = line_extra_from_previous + newline_ind - previous_ind
                line_bytes = inbuf.read(available_bytes)
                line = line_bytes.decode('utf-8')
                line_extra_from_previous = 0
                inbuf.seek(0)

                yield line

                previous_ind = newline_ind + 1
                newline_ind = rem.find(b'\n', newline_ind + 1)

            line_extra_from_previous = len(rem) - previous_ind
            inbuf.seek(0)
            inbuf.write(rem[previous_ind:])


class BatchInserter:
    def __init__(self, cursor, query, numargs, max_per_query=128):
        self.cursor = cursor
        self.query = query
        self.argline = self.build_argline(numargs)
        self.max_query_prebuilt = self.build_sql_for(max_per_query)
        self.max_per_query = max_per_query

        self.current_items = []
        self.num_rows = 0

    def append(self, row):
        for itm in row:
            self.current_items.append(itm)
        self.num_rows += 1
        if self.num_rows == self.max_per_query:
            self.flush()

    def flush(self):
        if self.num_rows == 0:
            return

        full_sql = None
        if self.num_rows == self.max_per_query:
            full_sql = self.max_query_prebuilt
        else:
            full_sql = self.build_sql_for(self.num_rows)

        self.cursor.execute(
            full_sql,
            self.current_items
        )
        self.current_items = []
        self.num_rows = 0

    def build_argline(self, numargs):
        res = ['(']
        for idx in range(numargs):
            if idx > 0:
                res.append(',')
            res.append('%s')
        res.append(')')
        return ''.join(res)

    def build_sql_for(self, numrows):
        return self.query + ','.join([self.argline] * numrows)

if __name__ == '__main__':
    main()
