from fastapi import HTTPException
from api.types import create_user_request_validation
from shared.types import UserCreate
from services.user import UserService
from repositories.connection import connect_to_postgres
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Handler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def create_user(self, body: UserCreate) -> dict:
        # Validate the request body
        await create_user_request_validation(body)

        user_created = await self.user_service.create_user(user_data=body)

        
        return user_created
















# Test conection to the database
async def test_connection_db(admin: str, password: str, database: str, host: str, port: int):
    connection_status = await connect_to_postgres(admin=admin, password=password, database=database, host=host, port=port)
    if connection_status:
        logger.info("Connection to the database was successful")
    else:
        logger.critical("Connection to the database failed")
        raise Exception("Database connection failed")