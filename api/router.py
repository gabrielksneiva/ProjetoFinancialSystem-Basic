from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from api.types import UserCreate, UserUpdate
from shared.types import LoginRequest, DepositRequest, WithdrawRequest
from repositories.database import Database
from services.deposit import DepositService
from services.withdraw import WithdrawService
from services.statement import StatementService
from services.user import UserService
from services.auth import AuthService
from api.handler import Handler
from repositories.connection import connect_to_postgres, test_connection_db
from api.handler import Handler
import os

router = APIRouter()


@router.on_event("startup")
async def startup_events():
    global connection, database_instance, user_service, handler, auth

    connection = await connect_to_postgres(
        admin=os.getenv("DB_ADMIN", ""),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", ""),
        host=os.getenv("DB_HOST", ""),
        port=int(os.getenv("DB_PORT", "")),
        )

    database_instance = Database(connection)
    await database_instance.initialize_database()
    auth_service = AuthService(
        secret_key=os.getenv("SECRET_KEY", ""),
        expiration_time_in_seconds=int(os.getenv("EXPIRATION_TIME", ""))
    )
    user_service = UserService(database_instance, auth_service)
    deposit_service = DepositService(database_instance)
    withdraw_service = WithdrawService(database_instance)
    statement_service = StatementService(database_instance)
    
    handler = Handler(user_service, deposit_service, withdraw_service, statement_service)
    
    await test_connection_db(
        os.getenv("DB_ADMIN", ""),
        os.getenv("DB_PASSWORD", ""),
        os.getenv("DB_NAME", ""),
        os.getenv("DB_HOST", ""),
        int(os.getenv("DB_PORT", ""))
    )

@router.on_event("shutdown")
async def shutdown_event():
    if connection:
        await connection.close()

# CRUD Users
@router.post("/users", tags=["users"], status_code=201)
async def create_user(body: UserCreate) -> dict:
    user_created = await handler.create_user(body)

    return user_created

@router.get("/users/get", tags=["users"], dependencies=[Depends(HTTPBearer())])
async def get_users(request: Request) -> dict:
    user_returned = await handler.get_users(request)

    return user_returned

@router.put("/users/update", tags=["users"], dependencies=[Depends(HTTPBearer())])
async def update_user(request: Request, body: UserUpdate) -> dict:
    user_updated = await handler.update_user(request, body)
    
    return user_updated

@router.delete("/users/delete", tags=["users"], dependencies=[Depends(HTTPBearer())])
async def delete_user(request: Request) -> dict:
    user_deleted = await handler.delete_user(request)

    return user_deleted

# Login
@router.post("/login", tags=["auth"])
async def login(body: LoginRequest) -> dict:
    user_logged_in = await handler.login_user(body)

    return user_logged_in

# Deposit
@router.post("/deposit", tags=["transactions"], dependencies=[Depends(HTTPBearer())])
async def deposit(request: Request, body: DepositRequest) -> dict:
    deposit_received = await handler.deposit(request, body)

    return deposit_received

# Withdraw
@router.post("/withdraw", tags=["transactions"], dependencies=[Depends(HTTPBearer())])
async def withdraw(request: Request, body: WithdrawRequest) -> dict:
    withdraw_received = await handler.withdraw(request, body)

    return withdraw_received

# Balance
@router.get("/balance", tags=["transactions"], dependencies=[Depends(HTTPBearer())])
async def balance(request: Request) -> dict:
    balance_received = await handler.balance(request)

    return balance_received

# Transaction-history
@router.get("/transaction-history", tags=["transactions"], dependencies=[Depends(HTTPBearer())])
async def transaction_history(request: Request, limit: int = 10, page: int = 1) -> dict:
    transaction_history_received = await handler.transaction_history(request, limit, page)

    return transaction_history_received

# Statement
@router.get("/statement", tags=["transactions"], dependencies=[Depends(HTTPBearer())])
async def statement(request: Request, limit: int = 10, page: int = 1) -> dict:
    statement_received = await handler.statement(request, limit, page)

    return statement_received