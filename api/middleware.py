from fastapi.responses import JSONResponse
from fastapi import HTTPException
from services.auth import AuthService
import os

auth_service = AuthService(
    secret_key=os.getenv("SECRET_KEY", ""),
    expiration_time_in_seconds=int(os.getenv("EXPIRATION_TIME", "900"))
)

async def is_this_path_protected(request):
        # Define the paths that require authentication
        protected_paths = [
            "/api/users/",
            "/api/deposit",
            "/api/withdraw",
            "/api/balance",
            "/api/transaction-history"
        ]

        for path in protected_paths:
            if request.url.path.startswith(path):
                return True
        return False

async def authorize_request_with_bearer_token(request, call_next):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"message": "Missing or invalid token"})

    token = auth_header.split(" ")[1] #Bearer <token>
    if not token:
        return JSONResponse(status_code=401, content={"message": "Missing or invalid token"})
    
    try:
        decoded_token = auth_service.decode_token(token)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    
    if not decoded_token:
        return JSONResponse(status_code=401, content={"message": "Missing or invalid token"})

    request.state.user = decoded_token

    response = await call_next(request)

    return response