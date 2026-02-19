"""シグナルAPIルーター"""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models.signal import Signal
from app.schemas.signal import SignalResponse

router = APIRouter()


@router.get("/buy", response_model=list[SignalResponse])
async def get_buy_signals(
    db: Annotated[AsyncSession, Depends(get_db)],
    min_score: float | None = None,
    target_date: date | None = None,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[SignalResponse]:
    """買いシグナル一覧取得"""
    query = select(Signal).where(Signal.signal_type == "buy").options(joinedload(Signal.stock))

    if min_score is not None:
        query = query.where(Signal.score >= min_score)
    if target_date:
        query = query.where(Signal.date == target_date)

    query = query.order_by(Signal.score.desc()).limit(limit)
    result = await db.execute(query)
    return [SignalResponse.model_validate(s) for s in result.scalars().all()]


@router.get("/sell", response_model=list[SignalResponse])
async def get_sell_signals(
    db: Annotated[AsyncSession, Depends(get_db)],
    target_date: date | None = None,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[SignalResponse]:
    """売りシグナル一覧取得"""
    query = select(Signal).where(Signal.signal_type == "sell").options(joinedload(Signal.stock))

    if target_date:
        query = query.where(Signal.date == target_date)

    query = query.order_by(Signal.date.desc()).limit(limit)
    result = await db.execute(query)
    return [SignalResponse.model_validate(s) for s in result.scalars().all()]
