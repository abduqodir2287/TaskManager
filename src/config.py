from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APPLICATION_PORT: str
    APPLICATION_HOST: str
    DOCKER_EXPOSED_PORT: str
    DOCKER_REDIS_HOST: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DATABASE: int
    REDIS_CACHE_EXPIRATION: int
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_DOCKER_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    LOG_WRITE_STATUS: bool

# Замените env_file=".env" на env_file=".env.example" и напишите в .env.example свои данные,
# Такие как DB_URL, APPLICATION_PORT и т.д.

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

