from api.types import UserUpdate
from repositories.database import Database
from fastapi import HTTPException
from shared.hash import hash_any_string
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def validate_update_fields(database: Database, email: str, user_data: UserUpdate):
    if user_data.email:
        fetched_user_by_email = await database.get_user_by_any_field("email", user_data.email)
        if fetched_user_by_email and fetched_user_by_email["id"] == email and fetched_user_by_email["email"] == user_data.email:
            logger.error("Email not different")
            raise HTTPException(status_code=409, detail="Email not different")
    
    if user_data.password_hash:
        user_data.password_hash = hash_any_string(user_data.password_hash)
        fetched_user_by_password_hash = await database.get_user_by_any_field("password_hash", user_data.password_hash)
        if fetched_user_by_password_hash and fetched_user_by_password_hash["email"] == email and fetched_user_by_password_hash["password_hash"] == user_data.password_hash:
            logger.error("password_hash not different")
            raise HTTPException(status_code=409, detail="password_hash not different")
        
    if user_data.is_active is not None:
        fetched_user_by_is_active = await database.get_user_by_any_field("is_active", user_data.is_active)
        if fetched_user_by_is_active and fetched_user_by_is_active["id"] == email and fetched_user_by_is_active["is_active"] == user_data.is_active:
            logger.error("is_active not different")
        raise HTTPException(status_code=409, detail="is_active not different")