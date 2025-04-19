# config.py

# Use pydantic_settings to manage application settings, loading from environment variables or a .env file.
from pydantic_settings import BaseSettings

# Define the Settings class to hold application configuration.
class Settings(BaseSettings):
    # Define configuration variables with their expected types.
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GROQ_API_KEY: str

    # Configure pydantic to load settings from a .env file.
    class Config:
        env_file = ".env"

# Create an instance of Settings, loading the configuration values.
settings = Settings()