from dotenv import load_dotenv
import os

load_dotenv()

async def check_envs():
    required_envs = ["DB_ADMIN", "DB_PASSWORD", "DB_NAME", "DB_HOST", "SECRET_KEY", "EXPIRATION_TIME"]

    for env in required_envs:
        if not os.getenv(env):
            raise ValueError(f"Environment variable {env} is not set.")