from fastapi import HTTPException, Request
from api.types import create_user_request_validation, UserUpdate, update_user_request_validation, login_request_validation
from shared.types import UserCreate, LoginRequest, DepositRequest, WithdrawRequest
from services.deposit import DepositService
from services.withdraw import WithdrawService
from services.statement import StatementService
from services.user import UserService
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Handler:
    def __init__(self, user_service: UserService, deposit_service: DepositService, withdraw_service: WithdrawService, statement_service: StatementService):
        self.withdraw_service = withdraw_service
        self.user_service = user_service
        self.deposit_service = deposit_service
        self.statement_service = statement_service

    async def create_user(self, body: UserCreate) -> dict:
        # Validate the request body
        await create_user_request_validation(body)

        user_created = await self.user_service.create_user(user_data=body)

        return user_created
    
    async def get_users(self, request: Request) -> dict:
        email = request.state.user.get("email")

        if email is None:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        if not isinstance(email, str):
            raise HTTPException(status_code=400, detail="User ID must be an integer")

        users = await self.user_service.get_users(email=email)
        return users

    async def update_user(self, request: Request, body: UserUpdate) -> dict:
        email = request.state.user.get("email")
        await update_user_request_validation(email, body)

        user_updated:dict = await self.user_service.update_user(email=email, user_data=body)

        return user_updated
    
    async def delete_user(self, request: Request) -> dict:
        email = request.state.user.get("email")
        
        if not email:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        if not isinstance(email, str):
            raise HTTPException(status_code=400, detail="User ID must be an integer")

        user_deleted = await self.user_service.delete_user(email=email)

        return user_deleted

    async def login_user(self, body: LoginRequest) -> dict:
        await login_request_validation(body)

        user_logged_in = await self.user_service.login_user(body.email, body.password_hash)

        if not user_logged_in:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return user_logged_in
    
    async def deposit(self, request: Request, body: DepositRequest) -> dict:
        email = request.state.user.get("email")

        if not isinstance(body.amount, float):
            raise HTTPException(status_code=400, detail="Amount must be a float")
        
        if body.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than zero") 
        
        deposit_received = await self.deposit_service.create(email, body.amount)

        return deposit_received
    
    async def withdraw(self, request: Request, body: WithdrawRequest) -> dict:
        email = request.state.user.get("email")

        if not isinstance(body.amount, float):
            raise HTTPException(status_code=400, detail="Amount must be a float")

        if body.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than zero") 

        withdraw_received = await self.withdraw_service.create(email, body.amount)

        return withdraw_received
    
    async def balance(self, request: Request) -> dict:
        email = request.state.user.get("email")

        balance_fetched = await self.statement_service.get_balance(email=email)

        return balance_fetched
    
    async def transaction_history(self, request: Request, limit: int, page: int) -> dict:
        email = request.state.user.get("email")

        transaction_history = await self.statement_service.get_transaction_history(email, limit, page)

        return transaction_history
    
    async def statement(self, request: Request, limit: int, page: int) -> dict:
        email = request.state.user.get("email")

        statement = await self.statement_service.get_statement(email, limit, page)

        return statement