

def create_user(user_data):
    """
    Create a new user.
    :param user_data: User data
    :return: User ID
    """

    return {"user_id": user_data.id, "username": user_data.username, "email": user_data.email}