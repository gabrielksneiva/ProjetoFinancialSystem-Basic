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


def validate_email(email: str, field_name="Email"):
    if not email:
        logger.error(f"{field_name} is required")
        raise HTTPException(status_code=400, detail=f"{field_name} is required")
    if "@" not in email or "." not in email.split("@")[-1]:
        logger.error(f"{field_name} is not valid")
        raise HTTPException(status_code=400, detail=f"{field_name} is not valid")

def validate_password(password_hash: str):
    if not password_hash:
        logger.error("password_hash is required")
        raise HTTPException(status_code=400, detail="password_hash is required")

async def create_user_request_validation(body: UserCreate):
    if not body.name:
        logger.error("Name is required")
        raise HTTPException(status_code=400, detail="Name is required")
    validate_email(body.email)
    validate_password(body.password_hash)

async def update_user_request_validation(email: str, body: UserUpdate):
    validate_email(email, "Email")
    if not (body.name or body.email or body.password_hash or body.is_active):
        logger.error("At least one field must be provided for update")
        raise HTTPException(status_code=400, detail="At least one field must be provided in update body")
    if body.email:
        validate_email(body.email, "Email in update body")

async def login_request_validation(body: LoginRequest):
    validate_email(body.email)
    validate_password(body.password_hash)