import asyncpg
import bcrypt
from shared.types import User

class Database:
    def __init__(self, connection):
        self.connection = connection

    async def initialize_database(self):
        query = """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            uuid UUID NOT NULL DEFAULT uuid_generate_v4(),
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            is_active BOOLEAN DEFAULT TRUE
        );
        """
        await self.connection.execute(query)

    async def create_user(self, user_data: User):
        query = """
        INSERT INTO users (name, email, password_hash, created_at, updated_at, is_active) 
        VALUES ($1, $2, $3, $4, $5, $6) 
        RETURNING name, email, created_at, updated_at, is_active
        """
        return await self.connection.fetchrow(
            query,
            user_data.name,
            user_data.email,
            user_data.password_hash,
            user_data.created_at,
            user_data.updated_at,
            user_data.is_active
        )
    
    async def get_user_by_any_field(self, field, value):
        query = f"SELECT * FROM users WHERE {field} = $1"
        return await self.connection.fetchrow(query, value)
    
    async def update_user(self, previous_email: str, user_data: User):
        query = """
        UPDATE users 
        SET name = $1, email = $2, password_hash = $3, updated_at = $4, is_active = $5 
        WHERE email = $6
        RETURNING name, email, created_at, updated_at, is_active
        """
        return await self.connection.fetchrow(
            query,
            user_data.name,
            user_data.email,
            user_data.password_hash,
            user_data.updated_at,
            user_data.is_active,
            previous_email
        )
    
    async def delete_user(self, email: str):
        query = "DELETE FROM users WHERE email = $1 RETURNING email"
        return await self.connection.fetchrow(query, email)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return result
    
    async def close(self):
        await self.connection.close()
