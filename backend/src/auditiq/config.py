from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://auditiq:auditiq@localhost:5432/auditiq"
    redis_url: str = "redis://localhost:6379/0"

    # AI
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-20250514"

    # Stripe
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_report: str = ""

    # App
    app_url: str = "http://localhost:3000"
    api_url: str = "http://localhost:8000"
    environment: str = "development"
    secret_key: str = "change-me-in-production"

    # PDF
    pdf_storage_path: str = "./data/pdfs"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
