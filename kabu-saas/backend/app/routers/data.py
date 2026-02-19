"""データ管理APIルーター"""

import asyncio
from datetime import date
from typing import Annotated, Any

from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.collectors.fundamental_collector import collect_all_fundamentals
from app.collectors.master_collector import get_active_stock_count, seed_initial_stocks
from app.collectors.price_collector import collect_all_prices, collect_historical_prices
from app.database import async_session_factory, get_db
from app.dependencies import get_current_user
from app.models.data_collection_log import DataCollectionLog
from app.models.user import User

router = APIRouter()


async def _run_collection_in_background() -> None:
    """バックグラウンドでデータ収集を実行する"""
    async with async_session_factory() as db:
        await collect_all_prices(db)
        await collect_all_fundamentals(db)
        await db.commit()


@router.post("/collect")
async def trigger_data_collection(
    background_tasks: BackgroundTasks,
    _current_user: Annotated[User, Depends(get_current_user)],
    historical: bool = Query(default=False, description="ヒストリカルデータを取得するか"),
) -> dict[str, str]:
    """データ収集の手動実行"""
    background_tasks.add_task(_run_collection_in_background)
    return {"status": "triggered", "message": "データ収集ジョブをバックグラウンドで開始しました"}


@router.post("/seed")
async def seed_stocks(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, Any]:
    """初期銘柄データ投入（認証不要 - セットアップ用）"""
    count = await seed_initial_stocks(db)
    return {"status": "success", "count": count, "message": f"{count}件の銘柄を登録しました"}


@router.get("/status")
async def get_data_status(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, Any]:
    """データ収集状況確認"""
    # 直近のジョブ実行ログを取得
    result = await db.execute(
        select(DataCollectionLog)
        .order_by(DataCollectionLog.started_at.desc())
        .limit(5)
    )
    logs = result.scalars().all()

    stock_count = await get_active_stock_count(db)

    return {
        "active_stocks": stock_count,
        "recent_jobs": [
            {
                "job_name": log.job_name,
                "status": log.status,
                "started_at": log.started_at.isoformat() if log.started_at else None,
                "finished_at": log.finished_at.isoformat() if log.finished_at else None,
                "total_count": log.total_count,
                "success_count": log.success_count,
                "error_count": log.error_count,
            }
            for log in logs
        ],
    }
