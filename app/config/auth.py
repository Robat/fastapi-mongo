from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.config.settings import get_settings
from app.database.connection import get_db_client
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi_jwt_auth import AuthJWT as BaseAuthJWT

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

settings = get_settings()


class CustomAuthJWT(BaseAuthJWT):
    def _get_secret_key(self, algorithm, action):
        return settings.AUTHJWT_SECRET_KEY


def create_custom_jwt_auth():
    return CustomAuthJWT()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        jwt = create_custom_jwt_auth()
        payload = jwt.decode_token(token)
        return payload["sub"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid JWT token")
