import asyncio
import os
import time
from uuid import uuid4

from asyncpg import create_pool, Connection
from dotenv import load_dotenv
from faker import Faker


async def prepare_pool():
    load_dotenv()
    return await create_pool(os.getenv('DB_LOCAL'))


def prepare_data():
    data = []
    ln = 100000
    fake = Faker('ru_RU')
    for i in range(ln):
        data.append(
            (uuid4(), fake.name(), fake.pystr() + fake.company_email(), fake.pyint(), fake.pystr(max_chars=200),
             fake.pyfloat()))
    return data


async def main():
    conn: Connection
    data = prepare_data()
    ln = len(data)
    pool = await prepare_pool()
    async with pool.acquire() as conn:
        start0 = time.time()
        await conn.executemany(
            'INSERT INTO speed_testing (spec_id, name, email, test_field1, test_field2, test_field3) VALUES ($1, $2, $3, $4, $5, $6)',
            data)
        end0 = time.time()
        t0 = end0 - start0
        print(f"Вставка: {t0}, RPC: {round(ln / t0)}")

        # data = prepare_data()
        # start1 = time.time()
        # for i in range(ln):
        #     await conn.execute(
        #         'UPDATE speed_testing SET spec_id=$1, name=$2, email=$3, test_field1=$4, test_field2=$5, test_field3=$6 WHERE id=$7',
        #         *data[i], i
        #     )
        # time.sleep(0.001)
        # end1 = time.time()
        # t1 = end1 - start1
        # print(f"Обновление: {t1}, RPC: {round(ln / t1)}")

        start2 = time.time()
        await conn.execute(
            'DELETE FROM speed_testing where id > 0'
        )
        end2 = time.time()
        t2 = end2 - start2
        print(f"Удаление: {t2}, RPC: {round(ln / t2)}")
    await pool.close()

    # print(f"Всего времени: {t0 + t1 + t2}, RPC: {round(ln / (t0 + t1 + t2))}")


asyncio.run(main())
