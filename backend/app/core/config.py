from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    GROQ_API_KEY: str
    HUGGINGFACE_API_KEY: str

    QDRANT_URL: str
    QDRANT_API_KEY: str

    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()