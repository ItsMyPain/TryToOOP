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
    ln = 10000
    fake = Faker('ru_RU')
    for i in range(ln):
        data.append(
            (uuid4(), fake.name(), fake.pystr() + fake.company_email(), fake.pyint(), fake.pystr(max_chars=200),
             fake.pyfloat()))
    return data


async def main():
    conn: Connection
    data = prepare_data()
    pool = await prepare_pool()
    async with pool.acquire() as conn:
        start = time.time()
        await conn.executemany(
            'INSERT INTO speed_testing (spec_id, name, email, test_field1, test_field2, test_field3) VALUES ($1, $2, $3, $4, $5, $6)',
            data)
        inserted = time.time()
        await conn.execute(
            'DELETE FROM speed_testing'
        )
        deleted = time.time()

    print(f"Всего времени: {deleted - start}, RPC: {round(len(data) / (deleted - start))}")
    print(f"Вставка: {inserted - start}, RPC: {round(len(data) / (inserted - start))}")
    print(f"Удаление: {deleted - inserted},  RPC: {round(len(data) / (deleted - inserted))}")


asyncio.run(main())
# Всего времени: 0.042207956314086914, RPC: 23692
# Вставка: 0.03927803039550781, RPC: 25460
# Удаление: 0.0029299259185791016,  RPC: 341306

# Всего времени: 0.4351179599761963, RPC: 22982
# Вставка: 0.42642855644226074, RPC: 23451
# Удаление: 0.008689403533935547,  RPC: 1150827
