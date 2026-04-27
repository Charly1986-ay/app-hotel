from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALG: str = Field(default="HS256", env="JWT_ALG")
    JWT_EXPIRES_MIN: int = Field(default=60*24, env="JWT_EXPIRES_MIN")
    STRIPE_SECRET_KEY: str = Field(..., env="STRIPE_SECRET_KEY")
    PROJECT_NAME: str = "Hotel Management Room"    

    class Config:
        env_file = ".env"


try:
    settings = Settings()
except Exception as e:
    print(f"Error al cargar la configuración: {e}")
    raise e