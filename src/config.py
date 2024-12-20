from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Ollama Configuration
    OLLAMA_URL: str = "http://localhost:11434/api/chat"
    OLLAMA_MODEL: str = "llama3.2"

    # App Settings
    APP_NAME: str = "Diverge"
    DEBUG: bool = False

settings = Settings()
