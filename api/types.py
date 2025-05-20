from shared.types import UserCreate, LoginRequest
from fastapi import HTTPException
from pydantic import BaseModel
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserUpdate(BaseModel):
    name: str = ""
    email: str = ""
    password_hash: str = ""
    is_active: bool = False


async def create_user_request_validation(body: UserCreate):
    if not body.name:
        logger.error("name is required")
        raise HTTPException(status_code=400, detail="name is required")
    
    if not body.email:
        logger.error("Email is required")
        raise HTTPException(status_code=400, detail="Email is required")
    
    if not body.password_hash:
        logger.error("password_hash is required")
        raise HTTPException(status_code=400, detail="password_hash is required")

    if "@" not in body.email or "." not in body.email.split("@")[-1]:
        logger.error("Email is not valid")
        raise HTTPException(status_code=400, detail="Email is not valid")

async def update_user_request_validation(email: str, body: UserUpdate):
    if not email:
        logger.error("Email is required")
        raise HTTPException(status_code=400, detail="Unnable to find user with empty email")

    if email and ("@" not in email or "." not in email.split("@")[-1]):
        logger.error("Email is not valid")
        raise HTTPException(status_code=400, detail="Unnable to update user with invalid email")
    
    if not body.name and not body.email and not body.password_hash and not body.is_active:
        logger.error("At least one field must be provided for update")
        raise HTTPException(status_code=400, detail="At least one field must be provided in update body")
    
    if body.email and ("@" not in body.email or "." not in body.email.split("@")[-1]):
        logger.error("Email is not valid")
        raise HTTPException(status_code=400, detail="Email in update body is not valid")
    
async def login_request_validation(body: LoginRequest):
    if not body.email:
        logger.error("Email is required")
        raise HTTPException(status_code=400, detail="Email is required")
    
    if not body.password_hash:
        logger.error("password_hash is required")
        raise HTTPException(status_code=400, detail="password_hash is required")

    if "@" not in body.email or "." not in body.email.split("@")[-1]:
        logger.error("Email is not valid")
        raise HTTPException(status_code=400, detail="Email is not valid")
    