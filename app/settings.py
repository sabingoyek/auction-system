from lib2to3.pytree import Base
import secrets
from pydantic import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    sqlalchemy_url: str = "sqlite:///./app.db"
    access_token_expire_minutes: int = 60 * 24 * 8
    super_user_email: str = "kimbasabingoye@gmail.com"
    super_user_password: str = None

    class Config:
        env_file = "../.env"

settings = Settings()

if settings.super_user_password is None:
    settings.super_user_password = settings.secret_key