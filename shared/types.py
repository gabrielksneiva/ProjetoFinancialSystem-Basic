from pydantic import BaseModel, Field
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password_hash: str

class LoginRequest(BaseModel):
    email: str
    password_hash: str


class User(BaseModel):
    id: int = 0
    name: str
    email: str
    password_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    is_active: bool = True