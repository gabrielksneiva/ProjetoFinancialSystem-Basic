import bcrypt
from fastapi import HTTPException
from api.types import UserCreate, UserUpdate
from repositories.database import Database
from services.auth import AuthService
from shared.types import User
from shared.hash import hash_any_string
from services.types import validate_update_fields
from time import time
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService():
    def __init__(self, database: Database, auth_service: AuthService):
        self.database = database
        self.auth_service = auth_service

    async def create_user(self, user_data: UserCreate) -> dict:
        # Validate user existence
        fetched_user_by_email = await self.database.get_user_by_any_field("email", user_data.email)
        if fetched_user_by_email:
            logger.error("User already exists with this email")
            raise HTTPException(status_code=409, detail="User already exists with this email")
        
        fetched_user_by_name = await self.database.get_user_by_any_field("name", user_data.name)
        if fetched_user_by_name:
            logger.error("User already exists with this name")
            raise HTTPException(status_code=409, detail="User already exists with this name")
        
        # Encrypt the password_hash
        user_data.password_hash = hash_any_string(user_data.password_hash)

        # Parse to User object
        user_to_insert = User(**user_data.dict())

        # Create user in the database
        inserted_user = await self.database.create_user(user_to_insert)

        # Check if the user was inserted successfully
        if not inserted_user:
            logger.error("Failed to create user in the database")
            raise HTTPException(status_code=500, detail="Failed to create user")
    
        return {"message": "User created successfully", "email": inserted_user["email"]}
    
    async def get_users(self, email: str) -> dict:
        retrieved_user = await self.database.get_user_by_any_field("email", email)

        if not retrieved_user:
            logger.error("User not found")
            raise HTTPException(status_code=404, detail="User not found")
        
        user = {
            "id": retrieved_user["id"],
            "name": retrieved_user["name"],
            "email": retrieved_user["email"],
            "created_at": retrieved_user["created_at"],
            "updated_at": retrieved_user["updated_at"],
            "is_active": retrieved_user["is_active"]
        }

        return user
    
    async def update_user(self, email: str, user_data: UserUpdate) -> dict:
        fetched_user = await self.database.get_user_by_any_field("email", email)
        logger.info(f"Fetched user: {fetched_user}")
        if not fetched_user:
            logger.error("User not found")
            raise HTTPException(status_code=404, detail="User not found")
        
        await validate_update_fields(self.database, email, user_data)
            
        user_to_update = User( 
                              updated_at=datetime.utcnow(), 
                              created_at=fetched_user["created_at"],  
                              name=user_data.name if user_data.name else fetched_user["name"], 
                              email=user_data.email if user_data.email else fetched_user["email"], 
                              password_hash=user_data.password_hash if user_data.password_hash else fetched_user["password_hash"], 
                              is_active=user_data.is_active if user_data.is_active is not None else fetched_user["is_active"]
                            )

        updated_user = await self.database.update_user(email, user_to_update)

        return {"message": "User updated successfully"}
    
    async def delete_user(self, email: str) -> dict:
        fetched_user = await self.database.get_user_by_any_field("email", email)
        if not fetched_user:
            logger.error("User not found")
            raise HTTPException(status_code=404, detail="User not found")
        
        deleted_user = await self.database.delete_user(email)

        return {"message": "User deleted successfully"}

    async def login_user(self, email: str, password_hash: str) -> dict:
        fetched_user = await self.database.get_user_by_any_field("email", email)
        if not fetched_user:
            logger.error("User not found")
            raise HTTPException(status_code=404, detail="User not found")
        
        password_hash_requested_hashed = hash_any_string(password_hash)
        if fetched_user["password_hash"] != password_hash_requested_hashed:
            logger.error("Invalid password_hash")
            raise HTTPException(status_code=401, detail="Invalid password_hash")

        token_to_return = self.auth_service.generate_token(fetched_user.get("email", None))
        
        return {"message": "Login successful", "token": token_to_return}