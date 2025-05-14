from fastapi import APIRouter
from api.types import User

router = APIRouter()

@router.get("/healthcheck")
async def healthcheck():
    return {"message": "OK"}

# Users
@router.post("/users", tags=["users"])
async def create_user(user_data: User) -> dict:
    return {"user_id": user_data.id, "username": user_data.username, "email": user_data.email}

@router.get("/users/{user_id}", tags=["users"])
async def get_user(user_id: int) -> dict:
    return {"user_id": user_id, "name": "John Doe"}

@router.put("/users/{user_id}", tags=["users"])
async def update_user(user_id: int) -> dict:
    return {"user_id": user_id, "message": "User updated"}

@router.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: int) -> dict:
    return {"user_id": user_id, "message": "User deleted"}


# Deposit




# Withdraw




# Statement (Transaction History and Balance)

