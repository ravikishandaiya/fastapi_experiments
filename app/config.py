from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str 
    db_password: str

    class Config:
        env_file = ".env"


# Class object
settings = Settings()