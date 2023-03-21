from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.settings import get_settings
from app.database.connection import get_db_client
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi_jwt_auth import AuthJWT as BaseAuthJWT

http_bearer = HTTPBearer()

settings = get_settings()


class CustomAuthJWT(BaseAuthJWT):
    def _get_secret_key(self, algorithm, action):
        return settings.AUTHJWT_SECRET_KEY

    # 使用 decode_jwt 方法
    def decode_token(self, token, verify_exp=True, csrf_token=None):
        return self.decode_jwt(token, secret=settings.AUTHJWT_SECRET_KEY, verify_exp=verify_exp, csrf_token=csrf_token)


def create_custom_jwt_auth():
    return CustomAuthJWT()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> str:
    token = credentials.credentials
    print(f"Token: {token}")  # 输出接收到的 token
    try:
        jwt = create_custom_jwt_auth()
        payload = jwt.decode_token(token)
        print(f"Payload: {payload}")  # 输出解码后的 payload
        return payload["sub"]
    except Exception as e:
        print(f"Error: {e}")  # 输出错误信息
        raise HTTPException(status_code=401, detail="Invalid JWT token")
