from shared.types import UserCreate

async def create_user_request_validation(body: UserCreate):
    if not body.username:
        raise ValueError("Username is required")
    
    if not body.email:
        raise ValueError("Email is required")
    
    if not body.password:
        raise ValueError("Password is required")

    if "@" not in body.email or "." not in body.email.split("@")[-1]:
        raise ValueError("Email is not valid")