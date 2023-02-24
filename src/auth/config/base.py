from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    hunter_url: str = "https://api.hunter.io/v2/email-verifier"
    hunter_apikey: str = Field(..., env='HUNTER_API_KEY')
    clearbit_url: str = "https://risk.clearbit.com/v1/calculate"
    clearbit_apikey: str = Field(..., env='CLEARBIT_API_KEY')
    secret: str = Field(..., env='SECRET')
    algorithm: str = "HS256"
    ttl: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
