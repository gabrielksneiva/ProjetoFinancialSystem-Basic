from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from fastapi import HTTPException
from datetime import datetime, timedelta
from typing import Any, Dict

class AuthService:
    def __init__(self, secret_key: str, expiration_time_in_seconds: int):
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.expiration = expiration_time_in_seconds

    def generate_token(self, email: str) -> str:
        payload= {
            "email": email,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(seconds=self.expiration),
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return decoded
        
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired",
            )

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )
