from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    JWT_SECRET: SecretStr
    MONGO_CONN: SecretStr
    AES_KEY: SecretStr

    model_config = SettingsConfigDict(env_prefix="L4T_", env_file=".env")

CONFIG = Config()
