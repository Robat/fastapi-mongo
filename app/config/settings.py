from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017/"
    MONGODB_DATABASE_NAME: str = "hmconsulting"
    AUTHJWT_SECRET_KEY: str = "your_secret_key_here"

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
