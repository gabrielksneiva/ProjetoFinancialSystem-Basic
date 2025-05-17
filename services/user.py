import bcrypt
from fastapi import HTTPException
from api.types import UserCreate, UserUpdate
from repositories.database import Database
from shared.types import User
from shared.hash import hash_any_string
from time import time
from datetime import datetime
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
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> dict:
        fetched_user = await self.database.get_user_by_any_field("id", user_id)
        logger.info(f"Fetched user: {fetched_user}")
        if not fetched_user:
            logger.error("User not found")
            raise HTTPException(status_code=404, detail="User not found")
        
        if user_data.email:
            fetched_user_by_email = await self.database.get_user_by_any_field("email", user_data.email)
            if fetched_user_by_email and fetched_user_by_email["id"] == user_id and fetched_user_by_email["email"] == user_data.email:
                logger.error("Email not different")
                raise HTTPException(status_code=409, detail="Email not different")
        
        if user_data.username:
            fetched_user_by_username = await self.database.get_user_by_any_field("username", user_data.username)
            if fetched_user_by_username and fetched_user_by_username["id"] == user_id and fetched_user_by_username["username"] == user_data.username:
                logger.error("Username not different")
                raise HTTPException(status_code=409, detail="Username not different")
        
        if user_data.password:
            user_data.password = hash_any_string(user_data.password)
            fetched_user_by_password = await self.database.get_user_by_any_field("password", user_data.password)
            if fetched_user_by_password and fetched_user_by_password["id"] == user_id and fetched_user_by_password["password"] == user_data.password:
                logger.error("Password not different")
                raise HTTPException(status_code=409, detail="Password not different")
            
        if user_data.is_active is not None:
            fetched_user_by_is_active = await self.database.get_user_by_any_field("is_active", user_data.is_active)
            if fetched_user_by_is_active and fetched_user_by_is_active["id"] == user_id and fetched_user_by_is_active["is_active"] == user_data.is_active:
                logger.error("is_active not different")
                raise HTTPException(status_code=409, detail="is_active not different")
            
        user_to_update = User( 
                              updated_at=datetime.utcnow(), 
                              created_at=fetched_user["created_at"], 
                              id=user_id, 
                              username=user_data.username if user_data.username else fetched_user["username"], 
                              email=user_data.email if user_data.email else fetched_user["email"], 
                              password=user_data.password if user_data.password else fetched_user["password"], 
                              is_active=user_data.is_active if user_data.is_active is not None else fetched_user["is_active"]
                            )

        updated_user = await self.database.update_user(user_id, user_to_update)

        return {"message": "User updated successfully"}