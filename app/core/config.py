from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str = "travel-api-key"
    OLLAMA_MODEL: str = "llama3.2:1b"
    USE_LLM: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
