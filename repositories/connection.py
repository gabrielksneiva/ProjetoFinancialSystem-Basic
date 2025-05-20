import asyncpg
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def connect_to_postgres(admin: str, password: str, database: str, host: str, port: int):
    conn = await asyncpg.connect(f'postgresql://{admin}:{password}@{host}/{database}')
    return conn

async def test_connection_db(admin: str, password: str, database: str, host: str, port: int):
    connection_status = await connect_to_postgres(admin=admin, password=password, database=database, host=host, port=port)
    if connection_status:
        logger.info("Connection to the database was successful")
    else:
        logger.critical("Connection to the database failed")
        raise Exception("Database connection failed")