# from pydantic_settings import BaseSettings, EmailStr, conint
# from dotenv import load_dotenv
# import os

# load_dotenv()


# class Config(BaseSettings):
#     SECRET_KEY: str = os.getenv("SECRET_KEY")
#     DATABASE_URL: str = os.getenv("DATABASE_URL")
#     ACCESS_TOKEN_EXPIRE_MINUTES: conint(gt=0) = int(
#         os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
#     REFRESH_TOKEN_EXPIRE_DAYS: conint(gt=0) = int(
#         os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
#     MAIL_FROM_ADDRESS: EmailStr = os.getenv(
#         "MAIL_FROM_ADDRESS", "your_email@example.com")
#     MAIL_USERNAME: EmailStr = os.getenv("MAIL_USERNAME", "example@meta.ua")
#     MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "secretPassword")
#     MAIL_PORT: int = int(os.getenv("MAIL_PORT", 465))
#     MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.meta.ua")

#     CLOUDINARY_NAME: str = os.getenv("CLOUDINARY_NAME", "")
#     # Сделаем строкой для безопасности
#     CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "")
#     CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "")

#     class Config:
#         env_file = ".env"
#         env_file_encoding = "utf-8"


# config = Config()
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, EmailStr


class Config(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:567234@localhost:5432/todo_app"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = "secret"
    # redis
    REDIS_URL: str = "redis://localhost"
    # mail
    MAIL_USERNAME: EmailStr = "example@meta.ua"
    MAIL_PASSWORD: str = "secretPassword"
    MAIL_FROM: EmailStr = "example@meta.ua"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.meta.ua"
    MAIL_FROM_NAME: str = "Rest API Service"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    CLOUDINARY_NAME: str
    CLOUDINARY_API_KEY: int = 326488457974591
    CLOUDINARY_API_SECRET: str = "secret"

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


config = Config()
