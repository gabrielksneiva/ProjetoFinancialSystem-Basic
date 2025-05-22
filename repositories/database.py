from shared.types import User

class Database:
    def __init__(self, connection):
        self.connection = connection

    async def initialize_database(self):
        query = """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE IF NOT EXISTS users (
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            is_active BOOLEAN DEFAULT TRUE
        );

        CREATE TABLE IF NOT EXISTS transactions (
            email VARCHAR(255) NOT NULL,
            transaction_id UUID DEFAULT uuid_generate_v4(),
            amount NUMERIC(10, 2) NOT NULL,
            transaction_type VARCHAR(50) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS balance (
            email VARCHAR(255) NOT NULL UNIQUE,
            balance NUMERIC(10, 2) DEFAULT 0.00,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        await self.connection.execute(query)

    async def create_user(self, user_data: User):
        query = """
        INSERT INTO users (email, password_hash, created_at, updated_at, is_active) 
        VALUES ($1, $2, $3, $4, $5) 
        RETURNING email, created_at, updated_at, is_active
        """
        return await self.connection.fetchrow(
            query,
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
        SET email = $1, password_hash = $2, updated_at = $3, is_active = $4
        WHERE email = $5
        RETURNING email, created_at, updated_at, is_active
        """
        return await self.connection.fetchrow(
            query,
            user_data.email,
            user_data.password_hash,
            user_data.updated_at,
            user_data.is_active,
            previous_email
        )
    
    async def delete_user(self, email: str):
        query = "DELETE FROM users WHERE email = $1 RETURNING email"
        return await self.connection.fetchrow(query, email)
    
    async def create_deposit(self, email: str, amount: float):
        query = """
        WITH new_transaction AS (
            INSERT INTO transactions (email, amount, transaction_type, created_at, updated_at)
            VALUES ($1, $2, 'deposit', NOW(), NOW())
            RETURNING transaction_id
        ),
        upsert_balance AS (
            INSERT INTO balance (email, balance, created_at, updated_at)
            VALUES ($1, $2, NOW(), NOW())
            ON CONFLICT (email) DO UPDATE
            SET balance = balance.balance + EXCLUDED.balance,
            updated_at = NOW()
            RETURNING balance
        )
        SELECT transaction_id FROM new_transaction
        """
        return await self.connection.fetchrow(query, email, amount)
    
    async def create_withdraw(self, email: str, amount: float):
        query = """
        WITH updated_balance AS (
            UPDATE balance
            SET balance = balance - $2,
                updated_at = NOW()
            WHERE email = $1 AND balance >= $2
            RETURNING balance
        ),
        new_transaction AS (
            INSERT INTO transactions (email, amount, transaction_type, created_at, updated_at)
            SELECT $1, $2, 'withdraw', NOW(), NOW()
            FROM updated_balance
            RETURNING transaction_id
        )
        SELECT transaction_id FROM new_transaction
        """
        return await self.connection.fetchrow(query, email, amount)
    
    async def get_balance(self, email: str):
        query = "SELECT balance FROM balance WHERE email = $1"
        return await self.connection.fetchrow(query, email)
    
    async def get_transaction_history(self, email: str, limit: int = 10, page: int = 1):
        offset = (page - 1) * limit
        query = """
        SELECT transaction_id, amount, transaction_type, created_at, updated_at
        FROM transactions
        WHERE email = $1
        ORDER BY created_at DESC
        LIMIT $2 OFFSET $3
        """
        return await self.connection.fetch(query, email, limit, offset)
    
    async def close(self):
        await self.connection.close()

