from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAPI_API_KEY: str
    GROQ_API_KEY: str
    APP_NAME: str = "AstraRAG"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
settings = Settings()
