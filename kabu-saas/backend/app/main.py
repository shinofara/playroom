"""FastAPI アプリケーション エントリポイント"""

import logging
import sys
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

# ログ設定（INFO以上をstderrに出力）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    stream=sys.stderr,
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import get_settings
from app.database import engine
from app.models import Base
from app.routers import agent, auth, dashboard, data, portfolio, screening, settings as settings_router, signals, stocks, trades, watchlists
from app.scheduler import shutdown_scheduler, start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """アプリケーションのライフサイクル管理"""
    # 起動時にテーブルを自動作成
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # スケジューラ起動
    start_scheduler()
    yield
    # 終了時の処理
    shutdown_scheduler()


def create_app() -> FastAPI:
    """FastAPIアプリケーションを作成する"""
    app_settings = get_settings()

    app = FastAPI(
        title=app_settings.app_name,
        description="日本株分析SaaS - テクニカル分析・シグナル検出・ポートフォリオ管理API",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORSミドルウェア
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ルーター登録
    app.include_router(auth.router, prefix="/api/auth", tags=["認証"])
    app.include_router(stocks.router, prefix="/api/stocks", tags=["銘柄・株価"])
    app.include_router(signals.router, prefix="/api/signals", tags=["シグナル"])
    app.include_router(screening.router, prefix="/api/screening", tags=["スクリーニング"])
    app.include_router(portfolio.router, prefix="/api/portfolio", tags=["ポートフォリオ"])
    app.include_router(trades.router, prefix="/api/trades", tags=["取引"])
    app.include_router(watchlists.router, prefix="/api/watchlists", tags=["ウォッチリスト"])
    app.include_router(dashboard.router, prefix="/api/dashboard", tags=["ダッシュボード"])
    app.include_router(data.router, prefix="/api/data", tags=["データ管理"])
    app.include_router(settings_router.router, prefix="/api/settings", tags=["設定"])
    app.include_router(agent.router, prefix="/api/agent", tags=["エージェント"])

    @app.get("/api/health", tags=["ヘルスチェック"])
    async def health_check() -> dict[str, str]:
        """ヘルスチェックエンドポイント"""
        return {"status": "ok"}

    return app


app = create_app()
