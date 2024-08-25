from pydantic import computed_field, PostgresDsn, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="allow"
    )

    PROJECT_NAME: str = "My Auth"

    API_V1_STR: str = "/api/v1"

    SERVER_HOST: str = "localhost"

    SECRET_KEY: str = "default_secret_key"
    ACCESS_TOKEN_EXPIRE: int = 60 * 30
    SESSION_EXPIRE: int = 60 * 30
    RECOVERY_TOKEN_EXPIRE: int = 60 * 20

    CORS_WHITELIST: list[HttpUrl] = ["http://localhost:5000", "http://localhost:5001"]

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str

    @computed_field
    @property
    def POSTGRES_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        )
    
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_MAX_CONNECTIONS: int = 10

    PASSWORD_ALGORITHM: str = "sha256"
    PASSWORD_INTERATIONS: int = 100_000

    TOKEN_ALGORITHM: str = "HS256"

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False



settings = Settings()