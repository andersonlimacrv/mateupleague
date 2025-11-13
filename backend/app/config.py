import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, EmailStr

load_dotenv()

class Settings(BaseSettings):
    
    APP_NAME: str = Field(default="Leitura", alias="APP_NAME")
    ENVIRONMENT: str = Field(default="development", alias="ENVIRONMENT")
    fe_port: int = Field(default=3000, alias="VITE_FRONTEND_PORT")
    fe_deploy_url: str = Field(default="http://localhost:3000", alias="DEPLOY_FRONTEND_URL")
    be_port: int = Field(default=8000, alias="VITE_BACKEND_PORT")
    enable_api_test_routes: bool = Field(default=False, alias="ENABLE_API_TEST_ROUTES")
    ADD_ROOT_USER : bool = Field(default=False, alias="ADD_ROOT_USER")
    SECRET_KEY_HASH: str
    SECRET_KEY_HASH_REFRESH: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ROOT_USERNAME: str
    ROOT_PASSWORD: str
    ROOT_EMAIL: EmailStr
    DATABASE_URL: str
    ALEMBIC_DB_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True  

settings = Settings()
