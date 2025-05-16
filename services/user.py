import bcrypt
from fastapi import HTTPException
from api.types import UserCreate
from repositories.database import Database
from shared.types import User
from time import time

class UserService():
    def __init__(self, database: Database):
        self.database = database

    async def create_user(self, user_data: UserCreate) -> dict:
        # Validate user existence
        fetched_user_by_email = await self.database.get_user_by_any_field("email", user_data.email)
        if fetched_user_by_email:
            raise HTTPException(status_code=409, detail="User already exists with this email")
        
        fetched_user_by_username = await self.database.get_user_by_any_field("username", user_data.username)
        if fetched_user_by_username:
            raise HTTPException(status_code=409, detail="User already exists with this username")
        
        # Encrypt the password
        user_data.password = await self._hash_password(user_data.password)

        # Parse to User object
        user_to_insert = User(**user_data.dict())

        # Create user in the database
        inserted_user = await self.database.create_user(user_to_insert)

        # Check if the user was inserted successfully
        if not inserted_user:
            raise ValueError("Failed to create user")
    
        return {"message": "User created successfully", "userid": inserted_user["id"]}


    async def _hash_password(self, password: str) -> str:
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')