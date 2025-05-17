from fastapi import HTTPException
from api.types import create_user_request_validation, UserUpdate, update_user_request_validation
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
    
    async def get_users(self, user_id: int) -> dict:
        if user_id is None:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        if not isinstance(user_id, int):
            raise HTTPException(status_code=400, detail="User ID must be an integer")
        
        if user_id <= 0:    
            raise HTTPException(status_code=400, detail="User ID must be greater than 0")

        users = await self.user_service.get_users(user_id=user_id)
        return users

    async def update_user(self, user_id: int, body: UserUpdate) -> dict:
        await update_user_request_validation(body, user_id)

        user_updated = await self.user_service.update_user(user_id=user_id, user_data=body)

        return user_updated















# Test conection to the database
async def test_connection_db(admin: str, password: str, database: str, host: str, port: int):
    connection_status = await connect_to_postgres(admin=admin, password=password, database=database, host=host, port=port)
    if connection_status:
        logger.info("Connection to the database was successful")
    else:
        logger.critical("Connection to the database failed")
        raise Exception("Database connection failed")