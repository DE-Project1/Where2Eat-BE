from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    mongo_db: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()