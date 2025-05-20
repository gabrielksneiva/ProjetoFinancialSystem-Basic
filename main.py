from fastapi import FastAPI
from api.middleware import is_this_path_protected, authorize_request_with_bearer_token
from services.auth import AuthService
from api.router import router
from config.load import check_envs
import uvicorn, os

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    return {"message": "OK"}

@app.on_event("startup")
async def startup_event():
    await check_envs()

#Middleware
auth_service = AuthService(
        secret_key=os.getenv("SECRET_KEY", ""),
        expiration_time_in_seconds=int(os.getenv("EXPIRATION_TIME", "900"))
    )
@app.middleware("http")
async def handle_token_to_authorize_requests(request, call_next):
    if not await is_this_path_protected(request):
        return await call_next(request)

    response = await authorize_request_with_bearer_token(request, call_next)

    return response

app.include_router(router, prefix="/api")

if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)
