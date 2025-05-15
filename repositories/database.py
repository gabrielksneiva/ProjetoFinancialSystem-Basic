import asyncpg
import bcrypt
from services.types import User

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

    async def get_user(self, user_id):
        query = "SELECT id, username, email FROM users WHERE id = $1"
        return await self.connection.fetchrow(query, user_id)
    
    async def get_user_by_any_field(self, field, value):
        if field not in ["username", "email"]:
            raise ValueError("Invalid field for user lookup")
        query = f"SELECT id, username, email FROM users WHERE {field} = $1"
        return await self.connection.fetchrow(query, value)
    
    async def close(self):
        await self.connection.close()
