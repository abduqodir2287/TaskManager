from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str
    APP_PORT: str
    APP_HOST: str
    DOCKER_COMPOSE_PORT: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

