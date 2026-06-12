from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Production Agent"
    app_version: str = "1.0.0"
    environment: str = "production"
    port: int = 8000
    host: str = "0.0.0.0"
    debug: bool = False
    
    redis_url: str = "redis://localhost:6379/0"
    agent_api_key: str = "secret-key"
    log_level: str = "INFO"
    rate_limit_per_minute: int = 10
    monthly_budget_usd: float = 10.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
