import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Prueba Técnica Soporte y Desarrollo"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Credenciales para la API Externa (GitHub)
    GITHUB_API_URL: str = os.getenv("GITHUB_API_URL", "https://api.github.com")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")

    class Config:
        env_file = ".env"

settings = Settings()