from pydantic import SecretStr, BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict



class VacancyURLS(BaseModel):
    remotive: str = "https://remotive.com/api"



class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

class BotConfig(BaseModel):
    token: SecretStr
    admin_ids: list[int] = []


class AIConfig(BaseModel):
    api_key: SecretStr | None = None
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o-mini"
    max_tokens: int = 1024


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: DatabaseConfig
    bot: BotConfig
    vacancy: VacancyURLS = VacancyURLS()
    log_level: str = "INFO"


settings = Settings()
