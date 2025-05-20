import os
import hmac
import hashlib
from dotenv import load_dotenv

load_dotenv()

def hash_any_string(any_string: str) -> str:
    private_key: str = os.getenv("SECRET_KEY", "")
    h = hmac.new(private_key.encode('utf-8'), any_string.encode('utf-8'), hashlib.sha256)
    return h.hexdigest()