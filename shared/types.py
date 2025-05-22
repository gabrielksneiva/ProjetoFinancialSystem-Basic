from pydantic import BaseModel, Field
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password_hash: str

class LoginRequest(BaseModel):
    email: str
    password_hash: str

class DepositRequest(BaseModel):
    amount: float

class WithdrawRequest(BaseModel):
    amount: float


class User(BaseModel):
    email: str
    password_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    is_active: bool = True