from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_host: str
    mongo_port: int
    mongo_db: str
    csv_url: str
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    app_reload: bool = True
    mongo_ttl_seconds: int = 600  # Default TTL of 10 minutes

    class Config:
        env_file = ".env"

settings = Settings()
