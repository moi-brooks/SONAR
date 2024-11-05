from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    REDIS_URL: str
    RABBITMQ_URL: str
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Phishing Detection System"
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()