"""銘柄・株価APIルーター"""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.fundamental import FundamentalData
from app.models.signal import Signal
from app.models.stock import Stock, StockPrice
from app.models.technical import TechnicalIndicator
from app.models.user import User
from app.schemas.signal import SignalResponse
from app.schemas.stock import (
    FundamentalDataResponse,
    PaginatedStockResponse,
    StockDetailResponse,
    StockPriceResponse,
    TechnicalIndicatorResponse,
)

# NOTE: get_current_user / User は /{code}/plan エンドポイントで引き続き使用

router = APIRouter()


@router.get("", response_model=PaginatedStockResponse)
async def list_stocks(
    db: Annotated[AsyncSession, Depends(get_db)],
    market: str | None = None,
    sector: str | None = None,
    search: str | None = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
) -> PaginatedStockResponse:
    """銘柄一覧取得"""
    query = select(Stock).where(Stock.is_active.is_(True))

    if market:
        query = query.where(Stock.market == market)
    if sector:
        query = query.where(Stock.sector == sector)
    if search:
        query = query.where(
            (Stock.code.ilike(f"%{search}%")) | (Stock.name.ilike(f"%{search}%"))
        )

    # 件数取得
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # ページネーション
    query = query.offset((page - 1) * per_page).limit(per_page).order_by(Stock.code)
    result = await db.execute(query)
    stocks = result.scalars().all()

    return PaginatedStockResponse(
        items=[StockDetailResponse.model_validate(s) for s in stocks],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/{code}", response_model=StockDetailResponse)
async def get_stock(
    code: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StockDetailResponse:
    """銘柄詳細取得"""
    result = await db.execute(select(Stock).where(Stock.code == code))
    stock = result.scalar_one_or_none()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="銘柄が見つかりません")
    return StockDetailResponse.model_validate(stock)


@router.get("/{code}/prices", response_model=list[StockPriceResponse])
async def get_stock_prices(
    code: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    from_date: date | None = None,
    to_date: date | None = None,
) -> list[StockPriceResponse]:
    """株価履歴取得"""
    stock_result = await db.execute(select(Stock).where(Stock.code == code))
    stock = stock_result.scalar_one_or_none()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="銘柄が見つかりません")

    query = select(StockPrice).where(StockPrice.stock_id == stock.id)
    if from_date:
        query = query.where(StockPrice.date >= from_date)
    if to_date:
        query = query.where(StockPrice.date <= to_date)
    query = query.order_by(StockPrice.date.desc())

    result = await db.execute(query)
    return [StockPriceResponse.model_validate(p) for p in result.scalars().all()]


@router.get("/{code}/fundamentals", response_model=list[FundamentalDataResponse])
async def get_stock_fundamentals(
    code: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    from_date: date | None = None,
    to_date: date | None = None,
) -> list[FundamentalDataResponse]:
    """ファンダメンタルデータ取得"""
    stock_result = await db.execute(select(Stock).where(Stock.code == code))
    stock = stock_result.scalar_one_or_none()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="銘柄が見つかりません")

    query = select(FundamentalData).where(FundamentalData.stock_id == stock.id)
    if from_date:
        query = query.where(FundamentalData.date >= from_date)
    if to_date:
        query = query.where(FundamentalData.date <= to_date)
    query = query.order_by(FundamentalData.date.desc())

    result = await db.execute(query)
    return [FundamentalDataResponse.model_validate(f) for f in result.scalars().all()]


@router.get("/{code}/technicals", response_model=list[TechnicalIndicatorResponse])
async def get_stock_technicals(
    code: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    from_date: date | None = None,
    to_date: date | None = None,
) -> list[TechnicalIndicatorResponse]:
    """テクニカル指標取得"""
    stock_result = await db.execute(select(Stock).where(Stock.code == code))
    stock = stock_result.scalar_one_or_none()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="銘柄が見つかりません")

    query = select(TechnicalIndicator).where(TechnicalIndicator.stock_id == stock.id)
    if from_date:
        query = query.where(TechnicalIndicator.date >= from_date)
    if to_date:
        query = query.where(TechnicalIndicator.date <= to_date)
    query = query.order_by(TechnicalIndicator.date.desc())

    result = await db.execute(query)
    return [TechnicalIndicatorResponse.model_validate(t) for t in result.scalars().all()]


@router.get("/{code}/signals", response_model=list[SignalResponse])
async def get_stock_signals(
    code: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    signal_type: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
) -> list[SignalResponse]:
    """シグナル履歴取得"""

    stock_result = await db.execute(select(Stock).where(Stock.code == code))
    stock = stock_result.scalar_one_or_none()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="銘柄が見つかりません")

    query = select(Signal).where(Signal.stock_id == stock.id)
    if signal_type:
        query = query.where(Signal.signal_type == signal_type)
    if from_date:
        query = query.where(Signal.date >= from_date)
    if to_date:
        query = query.where(Signal.date <= to_date)
    query = query.order_by(Signal.date.desc())

    result = await db.execute(query)
    return [SignalResponse.model_validate(s) for s in result.scalars().all()]


@router.get("/{code}/plan")
async def get_stock_plan(
    code: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """売買プラン取得"""
    from app.services.planner import generate_trade_plan

    stock_result = await db.execute(select(Stock).where(Stock.code == code))
    stock = stock_result.scalar_one_or_none()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="銘柄が見つかりません")

    plan = await generate_trade_plan(db, stock, current_user)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="プランを生成できません（株価データ不足）")

    return {
        "stock_code": code,
        "plan_type": plan.plan_type,
        "entry_price": float(plan.entry_price),
        "target_price_1": float(plan.target_price_1) if plan.target_price_1 else None,
        "target_price_2": float(plan.target_price_2) if plan.target_price_2 else None,
        "target_price_3": float(plan.target_price_3) if plan.target_price_3 else None,
        "stop_loss_price": float(plan.stop_loss_price) if plan.stop_loss_price else None,
        "position_size": plan.position_size,
        "risk_reward_ratio": float(plan.risk_reward_ratio) if plan.risk_reward_ratio else None,
        "status": plan.status,
    }
