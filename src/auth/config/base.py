import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # secret: str = Field(..., env='SECRET')
    algorithm: str = "HS256"

    # db_username = os.environ.get('POSTGRES_USER')
    # db_password = os.environ.get('POSTGRES_PASSWORD')
    # db_host = os.environ.get('POSTGRES_HOST')
    # db_name = os.environ.get('POSTGRES_DB')
    # db_port = os.environ.get('POSTGRES_PORT')
    #
    # secret = os.environ.get('JWT_SECRET')

    db_username = 'lafamilia'
    db_password = 'lafamilia'
    db_host = 'localhost'
    db_name = 'youtube'
    db_port = 5432

    secret = 'asd'
    ttl = 30
    # class Config:
    #     env_file = "./.env"
    #     env_file_encoding = "utf-8"


settings = Settings()
