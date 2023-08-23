import os
import threading
import time
from uuid import uuid4

import psycopg2
from dotenv import load_dotenv
from faker import Faker
from psycopg2._psycopg import cursor, connection
from psycopg2.extras import execute_batch


def prepare_conn():
    load_dotenv()
    return psycopg2.connect(os.getenv('DB_LOCAL'))


def prepare_data():
    data = []
    ln = 10000
    fake = Faker('ru_RU')
    for i in range(ln):
        data.append(
            (uuid4(), fake.name(), fake.pystr() + fake.company_email(), fake.pyint(), fake.pystr(max_chars=200),
             fake.pyfloat()))
    return data


def insert(data):
    conn: connection = prepare_conn()
    cur: cursor = conn.cursor()
    execute_batch(cur,
                  'INSERT INTO speed_testing (spec_id, name, email, test_field1, test_field2, test_field3) VALUES (%s, %s, %s, %s, %s, %s)',
                  data)
    conn.commit()


def main():
    psycopg2.extras.register_uuid()
    data = prepare_data()
    ln = len(data)
    numThreads = 10

    treads = []

    for i in range(numThreads):
        tr = threading.Thread(target=insert, args=(data[i * ln // numThreads: (i + 1) * ln // numThreads],))
        treads.append(tr)

    start0 = time.time()
    for i in treads:
        i.start()

    for i in treads:
        i.join()

    end0 = time.time()
    print(threading.current_thread().name, end0 - start0, len(data) / (end0 - start0), len(data))


main()
