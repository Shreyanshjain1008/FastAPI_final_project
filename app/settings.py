import os
from pydantic_settings import BaseSettings, SettingsConfigDict

print("ENV FILE EXISTS:", os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env"))))

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    redis_host: str
    redis_port: int

    model_config = SettingsConfigDict(
        env_file=os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env"))
    )

settings = Settings()
print("Loaded DB URL:", settings.database_url)
print("Loaded Secret Key:", settings.secret_key)
print("Loaded Algorithm:", settings.algorithm)
print("Loaded Access Token Expiry:", settings.access_token_expire_minutes)
print("Loaded Redis Host:", settings.redis_host)
print("Loaded Redis Port:", settings.redis_port)