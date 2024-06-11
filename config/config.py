from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    QUARANTINE_DIR: str = "quarantine"  # Каталог карантина для хранения файлов
    HOST: str = "localhost"             # Адрес сервера для подключения
    SERVER_HOST: str = "0.0.0.0"        # Адрес сервера при запуске
    SERVER_PORT: int = 9999             # Порт сервера

settings = Settings()
