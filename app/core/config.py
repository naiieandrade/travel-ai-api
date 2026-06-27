from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str = "travel-api-key"

    class Config:
        env_file = ".env"


settings = Settings()
