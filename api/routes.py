from fastapi import APIRouter
from api.types import UserCreate, UserUpdate
from services.user import UserService
from repositories.database import Database
from repositories.connection import connect_to_postgres
from api.handler import Handler, test_connection_db
import os

router = APIRouter()

# Inicialização das dependências
connection = None
database_instance = None
user_service = None
handler = None

@router.on_event("startup")
async def startup_event():
    admin = os.getenv("DB_ADMIN")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT", 5432))
    global connection, database_instance, user_service, handler
    connection = await connect_to_postgres(admin=admin, password=password, database=database, host=host, port=port)
    database_instance = Database(connection)
    await database_instance.initialize_database()
    user_service = UserService(database_instance)
    handler = Handler(user_service)
    await test_connection_db(admin, password, database, host, port)

@router.on_event("shutdown")
async def shutdown_event():
    if connection:
        await connection.close()

# Users
@router.post("/users", tags=["users"], status_code=201)
async def create_user(body: UserCreate) -> dict:
    # Call Handler
    user_created = await handler.create_user(body)

    return user_created

@router.get("/users/{user_id}", tags=["users"])
async def get_users(user_id: int) -> dict:
    # CaL Handler
    users = await handler.get_users(user_id)
    return users

@router.put("users/{user_id}", tags=["users"])
async def update_user(user_id: int, body: UserUpdate) -> dict:
    # Call Handler
    user_updated = await handler.update_user(user_id, body)
    return user_updated

@router.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: int) -> dict:
    # Call Handler
    user_deleted = await handler.delete_user(user_id)
    return user_deleted

# Deposit
@router.post("/deposit", tags=["transactions"])
async def deposit() -> dict:
    raise NotImplemented

# Withdraw
@router.post("/withdraw", tags=["transactions"])
async def withdraw() -> dict:
    raise NotImplemented

# Balance
@router.get("/Balance", tags=["transactions"])
async def balance() -> dict:
    raise NotImplemented

# Transaction-history
@router.get("/transaction-history", tags=["transactions"])
async def transaction_history() -> dict:
    raise NotImplemented

# ...