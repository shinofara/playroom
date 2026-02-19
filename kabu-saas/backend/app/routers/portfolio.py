"""ポートフォリオAPIルーター"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.portfolio import Portfolio, PortfolioHolding
from app.models.user import User
from app.schemas.portfolio import (
    HoldingCreate,
    HoldingResponse,
    HoldingUpdate,
    PortfolioResponse,
    PortfolioUpdate,
)
from app.services.portfolio_service import calculate_portfolio_performance

router = APIRouter()


@router.get("", response_model=PortfolioResponse)
async def get_portfolio(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> PortfolioResponse:
    """ポートフォリオ取得"""
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == current_user.id)
    )
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        # デフォルトポートフォリオを自動作成
        portfolio = Portfolio(
            user_id=current_user.id,
            name="メインポートフォリオ",
            total_investment=0,
        )
        db.add(portfolio)
        await db.flush()
    return PortfolioResponse.model_validate(portfolio)


@router.put("", response_model=PortfolioResponse)
async def update_portfolio(
    request: PortfolioUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> PortfolioResponse:
    """ポートフォリオ更新"""
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == current_user.id)
    )
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ポートフォリオが見つかりません")

    if request.name is not None:
        portfolio.name = request.name
    if request.total_investment is not None:
        portfolio.total_investment = request.total_investment

    return PortfolioResponse.model_validate(portfolio)


@router.get("/holdings", response_model=list[HoldingResponse])
async def list_holdings(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[HoldingResponse]:
    """保有銘柄一覧"""
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == current_user.id)
    )
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        return []

    holdings_result = await db.execute(
        select(PortfolioHolding).where(PortfolioHolding.portfolio_id == portfolio.id)
    )
    return [HoldingResponse.model_validate(h) for h in holdings_result.scalars().all()]


@router.post("/holdings", response_model=HoldingResponse, status_code=status.HTTP_201_CREATED)
async def add_holding(
    request: HoldingCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> HoldingResponse:
    """保有銘柄追加"""
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == current_user.id)
    )
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        portfolio = Portfolio(
            user_id=current_user.id,
            name="メインポートフォリオ",
            total_investment=0,
        )
        db.add(portfolio)
        await db.flush()

    holding = PortfolioHolding(
        portfolio_id=portfolio.id,
        stock_id=request.stock_id,
        quantity=request.quantity,
        avg_purchase_price=request.avg_purchase_price,
    )
    db.add(holding)
    await db.flush()
    return HoldingResponse.model_validate(holding)


@router.put("/holdings/{holding_id}", response_model=HoldingResponse)
async def update_holding(
    holding_id: int,
    request: HoldingUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> HoldingResponse:
    """保有銘柄更新"""
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == current_user.id)
    )
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ポートフォリオが見つかりません")

    holding_result = await db.execute(
        select(PortfolioHolding).where(
            PortfolioHolding.id == holding_id,
            PortfolioHolding.portfolio_id == portfolio.id,
        )
    )
    holding = holding_result.scalar_one_or_none()
    if not holding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="保有銘柄が見つかりません")

    if request.quantity is not None:
        holding.quantity = request.quantity
    if request.avg_purchase_price is not None:
        holding.avg_purchase_price = request.avg_purchase_price

    return HoldingResponse.model_validate(holding)


@router.delete("/holdings/{holding_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_holding(
    holding_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    """保有銘柄削除"""
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == current_user.id)
    )
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ポートフォリオが見つかりません")

    holding_result = await db.execute(
        select(PortfolioHolding).where(
            PortfolioHolding.id == holding_id,
            PortfolioHolding.portfolio_id == portfolio.id,
        )
    )
    holding = holding_result.scalar_one_or_none()
    if not holding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="保有銘柄が見つかりません")
    await db.delete(holding)


@router.get("/performance")
async def get_performance(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """ポートフォリオパフォーマンス取得"""
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == current_user.id)
    )
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        return {
            "total_market_value": 0,
            "total_cost_basis": 0,
            "total_unrealized_pnl": 0,
            "total_unrealized_pnl_percent": 0,
            "holdings": [],
        }

    perf = await calculate_portfolio_performance(db, portfolio)
    return {
        "total_market_value": float(perf.total_market_value),
        "total_cost_basis": float(perf.total_cost_basis),
        "total_unrealized_pnl": float(perf.total_unrealized_pnl),
        "total_unrealized_pnl_percent": float(perf.total_unrealized_pnl_percent),
        "holdings": [
            {
                "stock_code": h.stock_code,
                "stock_name": h.stock_name,
                "quantity": h.quantity,
                "avg_purchase_price": float(h.avg_purchase_price),
                "current_price": float(h.current_price),
                "market_value": float(h.market_value),
                "cost_basis": float(h.cost_basis),
                "unrealized_pnl": float(h.unrealized_pnl),
                "unrealized_pnl_percent": float(h.unrealized_pnl_percent),
                "weight": float(h.weight),
            }
            for h in perf.holdings
        ],
    }
