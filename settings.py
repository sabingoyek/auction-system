from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    sqlalchemy_url: str = "sqlite:///./app.db"
    # sqlalchemy_url: str = "postgresql://user:password@postgresserver/db"
    access_token_expire_minutes: int = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days
    first_name: str = "Kimba"
    last_name: str = "SABI N'GOYE"
    super_user_email: str = "kimbasabingoye@gmail.com"
    super_user_password: str = "kalimba"

    class Config:
        env_file = ".env"


settings = Settings()

if settings.super_user_password is None:
    settings.super_user_password = settings.secret_key
