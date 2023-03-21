from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import get_db_client, startup_event, shutdown_event
from app.routers import auth, department
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings
from app.config.auth import CustomAuthJWT
from app.config.settings import Settings


@AuthJWT.load_config
def get_config():
    return Settings()


app = FastAPI()

# 添加 CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源
    allow_credentials=True,
    allow_methods=["*"],  # 請根據需要調整允許的方法
    allow_headers=["*"],  # 請根據需要調整允許的標頭
)

app.include_router(auth.router)
app.include_router(department.router)

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
