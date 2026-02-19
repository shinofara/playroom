"""スケジュールジョブ定義

APSchedulerを使用して定時データ収集・分析バッチを実行する。
"""

import logging
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.collectors.fundamental_collector import collect_all_fundamentals
from app.collectors.master_collector import seed_initial_stocks
from app.collectors.price_collector import collect_all_prices
from app.models.data_collection_log import DataCollectionLog

logger = logging.getLogger(__name__)


async def _log_job_start(db: AsyncSession, job_name: str) -> DataCollectionLog:
    """ジョブ開始ログを記録する"""
    log = DataCollectionLog(
        job_name=job_name,
        status="running",
    )
    db.add(log)
    await db.flush()
    return log


async def _log_job_finish(
    db: AsyncSession,
    log: DataCollectionLog,
    success_count: int,
    error_count: int,
    errors: list[str],
) -> None:
    """ジョブ完了ログを記録する"""
    log.finished_at = datetime.now(timezone.utc)
    log.total_count = success_count + error_count
    log.success_count = success_count
    log.error_count = error_count
    log.error_details = [{"message": e} for e in errors]
    log.status = "success" if error_count == 0 else ("partial" if success_count > 0 else "failed")
    await db.commit()


async def run_collect_prices(db: AsyncSession) -> None:
    """株価データ収集ジョブ"""
    logger.info("株価データ収集ジョブ開始")
    log = await _log_job_start(db, "collect_prices")

    try:
        success, errors_count, error_details = await collect_all_prices(db)
        await _log_job_finish(db, log, success, errors_count, error_details)
        logger.info(f"株価データ収集ジョブ完了: 成功={success}, エラー={errors_count}")
    except Exception as e:
        logger.error(f"株価データ収集ジョブ失敗: {e}")
        await _log_job_finish(db, log, 0, 1, [str(e)])


async def run_collect_fundamentals(db: AsyncSession) -> None:
    """ファンダメンタルデータ収集ジョブ"""
    logger.info("ファンダメンタルデータ収集ジョブ開始")
    log = await _log_job_start(db, "collect_fundamentals")

    try:
        success, errors_count, error_details = await collect_all_fundamentals(db)
        await _log_job_finish(db, log, success, errors_count, error_details)
        logger.info(f"ファンダメンタルデータ収集ジョブ完了: 成功={success}, エラー={errors_count}")
    except Exception as e:
        logger.error(f"ファンダメンタルデータ収集ジョブ失敗: {e}")
        await _log_job_finish(db, log, 0, 1, [str(e)])


async def run_seed_stocks(db: AsyncSession) -> None:
    """初期銘柄データ投入ジョブ"""
    logger.info("初期銘柄データ投入ジョブ開始")
    count = await seed_initial_stocks(db)
    logger.info(f"初期銘柄データ投入完了: {count}件")
