import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Resume AI"
    API_V1_STR: str = "/api/v1"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    OPENAI_API_KEY: str = ""  # Set in .env file

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
