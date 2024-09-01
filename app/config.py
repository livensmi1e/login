from pydantic import computed_field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="allow"
    )

    PROJECT_NAME: str = "My Auth"

    API_V1_STR: str = "/api/v1"

    SERVER_HOST: str = "localhost"
    PORT: int = 443

    SECRET_KEY: str = "default_secret_key"
    ACCESS_TOKEN_EXPIRE: int = 60 * 30
    SESSION_EXPIRE: int = 60 * 30
    RECOVERY_TOKEN_EXPIRE: int = 60 * 20

    CORS_WHITELIST: list[str] = ["http://localhost:3001", "https://localhost:3001"]

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

    REDIRECT_URI: str

    PROVIDER: list[str] = ["google", "facebook", "github"]

    GOOGLE_CLIENT_ID: str 
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_AUTHORIZATION_URL: str
    GOOGLE_TOKEN_URL: str
    GOOGLE_USERINFO_URL: str
    GOOGLE_SCOPE: list[str] = [
        "https://www.googleapis.com/auth/userinfo.email", 
        "https://www.googleapis.com/auth/userinfo.profile"
    ]

    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    GITHUB_AUTHORIZATION_URL: str
    GITHUB_TOKEN_URL: str
    GITHUB_USERINFO_URL: str
    GITHUB_SCOPE: list[str] = ["user:email"]

    @computed_field
    @property
    def OAUTH(self) -> dict[str, dict[str, list | str]]:
        oauth_config = {
            "google": {
                "client_id": self.GOOGLE_CLIENT_ID,
                "client_secret": self.GOOGLE_CLIENT_SECRET,
                "auth_url": self.GOOGLE_AUTHORIZATION_URL,
                "token_url": self.GOOGLE_TOKEN_URL,
                "userinfo_url": self.GOOGLE_USERINFO_URL,
                "scope": self.GOOGLE_SCOPE,
            },
            "github": {
                "client_id": self.GITHUB_CLIENT_ID,
                "client_secret": self.GITHUB_CLIENT_SECRET,
                "auth_url": self.GITHUB_AUTHORIZATION_URL,
                "token_url": self.GITHUB_TOKEN_URL,
                "userinfo_url": self.GITHUB_USERINFO_URL,
                "scope": self.GITHUB_SCOPE,
            }
        }
        return oauth_config






settings = Settings()