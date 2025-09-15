from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_USER: str

    DB_GET_SESSION_RETRIES: int
    DB_GET_SESSION_DELAY: float
    DB_GET_SESSION_TIMEOUT: float


    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra" : "ignore"
    }

settings = Settings()
