from fastapi_jwt_auth import AuthJWT as BaseAuthJWT
from app.config.settings import get_settings

settings = get_settings()


class CustomAuthJWT(BaseAuthJWT):
    def _get_secret_key(self, algorithm, action):
        return settings.AUTHJWT_SECRET_KEY


def create_custom_jwt_auth():
    return CustomAuthJWT()
