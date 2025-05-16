from shared.types import UserCreate
from fastapi import HTTPException
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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