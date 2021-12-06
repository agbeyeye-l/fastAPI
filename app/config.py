from pydantic import BaseSettings

class APPSettings(BaseSettings):
    """
    Application configuration settings
    """
    DB_HOST:str 
    DB_USERNAME:str 
    DB_PASSWORD:str
    DB_NAME:str
    DB_PORT:int
    SECRET_KEY:str
    ACCESS_TOKEN_EXPIRATION_DURATION_MINUTES:int
    ALGORITHM:str

    class Config:
        env_file = ".env"

Settings = APPSettings()