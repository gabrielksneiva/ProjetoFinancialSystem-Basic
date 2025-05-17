from shared.types import UserCreate
from fastapi import HTTPException
from pydantic import BaseModel
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserUpdate(BaseModel):
    username: str = None
    email: str = None
    password: str = None
    is_active: bool = None


async def create_user_request_validation(body: UserCreate):
    if not body.username:
        logger.error("Username is required")
        raise HTTPException(status_code=400, detail="Username is required")
    
    if not body.email:
        logger.error("Email is required")
        raise HTTPException(status_code=400, detail="Email is required")
    
    if not body.password:
        logger.error("Password is required")
        raise HTTPException(status_code=400, detail="Password is required")

    if "@" not in body.email or "." not in body.email.split("@")[-1]:
        logger.error("Email is not valid")
        raise HTTPException(status_code=400, detail="Email is not valid")

async def update_user_request_validation(body: UserUpdate, user_id: int):
    if not user_id:
        logger.error("User ID is required")
        raise HTTPException(status_code=400, detail="User ID is required")
    
    if not isinstance(user_id, int):
        logger.error("User ID must be an integer")
        raise HTTPException(status_code=400, detail="User ID must be an integer")
    
    if user_id <= 0:
        logger.error("User ID must be greater than 0")
        raise HTTPException(status_code=400, detail="User ID must be greater than 0")
    
    if not body.username and not body.email and not body.password and not body.is_active:
        logger.error("At least one field must be provided for update")
        raise HTTPException(status_code=400, detail="At least one field must be provided for update")
    
    if body.email and ("@" not in body.email or "." not in body.email.split("@")[-1]):
        logger.error("Email is not valid")
        raise HTTPException(status_code=400, detail="Email is not valid")
    