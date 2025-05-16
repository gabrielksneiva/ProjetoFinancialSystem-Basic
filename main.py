from fastapi import FastAPI
import uvicorn
from api.routes import router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    return {"message": "OK"}

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
