from pydantic import SecretStr
from pydantic import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    chat_id: SecretStr
    moder: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

config = Settings()