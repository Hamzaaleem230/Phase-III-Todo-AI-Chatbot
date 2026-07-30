from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

# Sahi Path: config.py se 3 step peeche 'backend' folder tak
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    NEXT_PUBLIC_BACKEND_URL: str | None = None

    # Pydantic V2 ke mutabiq model_config use karna behtar hai
    class Config:
        env_file = str(env_path)  # Path object ko string mein convert karna safe rehta hai
        extra = "ignore"

settings = Settings()

# DEBUG (temporary)
print("DEBUG DATABASE_URL:", settings.DATABASE_URL)
print("DEBUG JWT_SECRET_KEY:", settings.JWT_SECRET_KEY)