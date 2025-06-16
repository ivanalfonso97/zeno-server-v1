from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Supabase settings
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str
    SUPABASE_JWT_SECRET: str

    # Google settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_API_KEY: str
    GOOGLE_CALENDAR_REDIRECT_URI: str

    # Frontend settings
    FRONTEND_URL: str

    class Config:
        env_file = ".env"

settings = Settings() 