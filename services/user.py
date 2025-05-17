import bcrypt
from fastapi import HTTPException
from api.types import UserCreate
from repositories.database import Database
from shared.types import User
from shared.hash import hash_any_string
from time import time
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService():
    def __init__(self, database: Database):
        self.database = database

    async def create_user(self, user_data: UserCreate) -> dict:
        # Validate user existence
        fetched_user_by_email = await self.database.get_user_by_any_field("email", user_data.email)
        if fetched_user_by_email:
            logger.error("User already exists with this email")
            raise HTTPException(status_code=409, detail="User already exists with this email")
        
        fetched_user_by_username = await self.database.get_user_by_any_field("username", user_data.username)
        if fetched_user_by_username:
            logger.error("User already exists with this username")
            raise HTTPException(status_code=409, detail="User already exists with this username")
        
        # Encrypt the password
        user_data.password = await hash_any_string(user_data.password)

        # Parse to User object
        user_to_insert = User(**user_data.dict())

        # Create user in the database
        inserted_user = await self.database.create_user(user_to_insert)

        # Check if the user was inserted successfully
        if not inserted_user:
            logger.error("Failed to create user in the database")
            raise HTTPException(status_code=500, detail="Failed to create user")
    
        return {"message": "User created successfully", "userid": inserted_user["id"]}
    
    async def get_users(self, user_id: int) -> dict:
        retrieved_user = await self.database.get_user_by_any_field("id", user_id)

        if not retrieved_user:
            logger.error("User not found")
            raise HTTPException(status_code=404, detail="User not found")
        
        user = {
            "id": retrieved_user["id"],
            "username": retrieved_user["username"],
            "email": retrieved_user["email"],
            "created_at": retrieved_user["created_at"],
            "updated_at": retrieved_user["updated_at"],
            "is_active": retrieved_user["is_active"]
        }

        return user