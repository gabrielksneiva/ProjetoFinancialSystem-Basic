from .types import User

def create_user_handler(user_data: User):
    try:
        xpto=create_user(user_data)
    except Exception as e:
        raise e
    return {"user_id": user_data.id, "username": user_data.username, "email": user_data.email}