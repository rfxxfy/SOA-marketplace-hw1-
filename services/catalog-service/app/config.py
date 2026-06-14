from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://catalog:catalog@localhost:5432/catalog_db"
    app_name: str = "Catalog Service"

    model_config = {"env_prefix": "CATALOG_"}


settings = Settings()
