import asyncpg
import bcrypt
from shared.types import User

class Database:
    def __init__(self, connection):
        self.connection = connection

    async def initialize_database(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP NOT NULL,
        is_active BOOLEAN NOT NULL
        );
        """
        await self.connection.execute(query)

    async def create_user(self, user_data: User):
        query = """
        INSERT INTO users (username, email, password, created_at, updated_at, is_active) 
        VALUES ($1, $2, $3, $4, $5, $6) 
        RETURNING id, username, email, created_at, updated_at, is_active
        """
        return await self.connection.fetchrow(
            query,
            user_data.username,
            user_data.email,
            user_data.password,
            user_data.created_at,
            user_data.updated_at,
            user_data.is_active
        )
    
    async def get_user_by_any_field(self, field, value):
        query = f"SELECT * FROM users WHERE {field} = $1"
        return await self.connection.fetchrow(query, value)
    
    async def update_user(self, user_id: int, user_data: User):
        query = """
        UPDATE users 
        SET username = $1, email = $2, password = $3, updated_at = $4, is_active = $5 
        WHERE id = $6
        RETURNING id, username, email, created_at, updated_at, is_active
        """
        return await self.connection.fetchrow(
            query,
            user_data.username,
            user_data.email,
            user_data.password,
            user_data.updated_at,
            user_data.is_active,
            user_id
        )
    
    async def close(self):
        await self.connection.close()
