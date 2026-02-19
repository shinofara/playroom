"""アプリケーション設定管理モジュール"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定"""

    # データベース
    database_url: str = "postgresql+asyncpg://kabu_user:kabu_pass@localhost:5432/kabu_saas"

    # JWT認証
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    # アプリケーション
    app_name: str = "Kabu SaaS API"
    debug: bool = True

    # データ収集
    collect_prices_hour: int = 18
    collect_prices_minute: int = 0
    collect_fundamentals_hour: int = 18
    collect_fundamentals_minute: int = 30
    calculate_technicals_hour: int = 19
    calculate_technicals_minute: int = 0
    detect_signals_hour: int = 19
    detect_signals_minute: int = 30

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    """設定のシングルトンインスタンスを返す"""
    return Settings()
