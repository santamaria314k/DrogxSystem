from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST:     str = "localhost"
    DB_PORT:     int = 3306
    DB_NAME:     str = "gestion_productos"
    DB_USER:     str = "gestion_user"
    DB_PASSWORD: str = "gestion_pass"

    class Config:
        env_file = ".env"


settings = Settings()
