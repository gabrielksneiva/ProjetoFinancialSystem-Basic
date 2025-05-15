import asyncpg

async def connect_to_postgres(admin: str, password: str, database: str, host: str, port: int):
    conn = await asyncpg.connect(f'postgresql://{admin}:{password}@{host}/{database}')
    return conn