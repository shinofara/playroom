"""スケジューラモジュール

APSchedulerを使用して日次パイプラインを定時実行する。
スケジューラジョブはBackgroundScheduler（別スレッド）で実行し、
専用のDBエンジンを使ってメインイベントループをブロックしない。
"""

import asyncio
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings
from app.services.pipeline import run_pipeline

logger = logging.getLogger(__name__)

_scheduler: BackgroundScheduler | None = None


def _run_daily_pipeline_sync() -> None:
    """日次パイプラインジョブ（別スレッドから同期で呼ばれる）"""
    logger.info("日次パイプラインジョブ開始")
    settings = get_settings()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        bg_engine = create_async_engine(
            settings.database_url,
            echo=False,
            pool_size=3,
            max_overflow=5,
        )
        bg_session_factory = async_sessionmaker(
            bg_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async def _run() -> None:
            async with bg_session_factory() as db:
                result = await run_pipeline(db)
                logger.info(f"日次パイプラインジョブ完了: {result.status}")
            await bg_engine.dispose()

        loop.run_until_complete(_run())
    except Exception as e:
        logger.error(f"日次パイプラインジョブ失敗: {e}")
    finally:
        loop.close()


def start_scheduler() -> BackgroundScheduler:
    """スケジューラを起動する"""
    global _scheduler
    settings = get_settings()

    _scheduler = BackgroundScheduler(timezone="Asia/Tokyo")

    # 毎日18:00にパイプライン実行
    _scheduler.add_job(
        _run_daily_pipeline_sync,
        trigger=CronTrigger(
            hour=settings.collect_prices_hour,
            minute=settings.collect_prices_minute,
        ),
        id="daily_pipeline",
        name="日次分析パイプライン",
        replace_existing=True,
    )

    _scheduler.start()
    logger.info(
        f"スケジューラ起動: 日次パイプライン = 毎日 {settings.collect_prices_hour}:{settings.collect_prices_minute:02d}"
    )
    return _scheduler


def shutdown_scheduler() -> None:
    """スケジューラを停止する"""
    global _scheduler
    if _scheduler:
        _scheduler.shutdown(wait=False)
        logger.info("スケジューラ停止")
        _scheduler = None
