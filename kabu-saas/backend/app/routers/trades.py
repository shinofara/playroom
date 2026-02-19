"""取引APIルーター"""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.portfolio import Portfolio
from app.models.stock import Stock
from app.models.trade import Trade
from app.models.user import User
from app.schemas.trade import TradeCreate, TradeResponse

router = APIRouter()


@router.get("", response_model=list[TradeResponse])
async def list_trades(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    stock_code: str | None = None,
    trade_type: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
) -> list[TradeResponse]:
    """取引履歴取得"""
    portfolio_result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == current_user.id)
    )
    portfolio = portfolio_result.scalar_one_or_none()
    if not portfolio:
        return []

    query = select(Trade).where(Trade.portfolio_id == portfolio.id)

    if stock_code:
        stock_result = await db.execute(select(Stock).where(Stock.code == stock_code))
        stock = stock_result.scalar_one_or_none()
        if stock:
            query = query.where(Trade.stock_id == stock.id)
    if trade_type:
        query = query.where(Trade.trade_type == trade_type)
    if from_date:
        query = query.where(Trade.transaction_date >= from_date)
    if to_date:
        query = query.where(Trade.transaction_date <= to_date)

    query = query.order_by(Trade.transaction_date.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    return [TradeResponse.model_validate(t) for t in result.scalars().all()]


@router.post("", response_model=TradeResponse, status_code=status.HTTP_201_CREATED)
async def create_trade(
    request: TradeCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> TradeResponse:
    """取引記録追加"""
    portfolio_result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == current_user.id)
    )
    portfolio = portfolio_result.scalar_one_or_none()
    if not portfolio:
        portfolio = Portfolio(
            user_id=current_user.id,
            name="メインポートフォリオ",
            total_investment=0,
        )
        db.add(portfolio)
        await db.flush()

    trade = Trade(
        portfolio_id=portfolio.id,
        stock_id=request.stock_id,
        trade_type=request.trade_type,
        quantity=request.quantity,
        price=request.price,
        commission=request.commission or 0,
        transaction_date=request.transaction_date,
        notes=request.notes,
    )
    db.add(trade)
    await db.flush()
    return TradeResponse.model_validate(trade)
