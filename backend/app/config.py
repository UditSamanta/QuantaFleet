import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "QuantumFleet Backend"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "quantumfleet_sih26138_super_secret_quantum_key_2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./quantumfleet.db")
    
    # Weather and Maritime API configurations (Server-side only)
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1/forecast"
    EU_ETS_CARBON_TAX_PER_TON: float = 85.0  # USD per ton CO2

    class Config:
        case_sensitive = True

settings = Settings()
