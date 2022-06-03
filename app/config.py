from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_name: str
    database_username: str 
    database_password: str
    algorithm: str = "H256"
    secret_key: str
    access_token_expire_minutes: int = 7

    class Config:
        env_file = ".env"

settings = Settings()




