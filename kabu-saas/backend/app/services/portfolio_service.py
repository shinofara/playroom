"""ポートフォリオサービス

損益計算、パフォーマンス分析、資産配分の計算を行う。
"""

from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portfolio import Portfolio, PortfolioHolding
from app.models.stock import Stock, StockPrice


@dataclass(frozen=True)
class HoldingPerformance:
    """保有銘柄パフォーマンス"""
    stock_code: str
    stock_name: str
    quantity: int
    avg_purchase_price: Decimal
    current_price: Decimal
    market_value: Decimal
    cost_basis: Decimal
    unrealized_pnl: Decimal
    unrealized_pnl_percent: Decimal
    weight: Decimal  # ポートフォリオ内の比率


@dataclass(frozen=True)
class PortfolioPerformance:
    """ポートフォリオパフォーマンス"""
    total_market_value: Decimal
    total_cost_basis: Decimal
    total_unrealized_pnl: Decimal
    total_unrealized_pnl_percent: Decimal
    holdings: list[HoldingPerformance]


async def get_current_price(
    db: AsyncSession,
    stock_id: int,
) -> Decimal | None:
    """銘柄の直近終値を取得する"""
    result = await db.execute(
        select(StockPrice)
        .where(StockPrice.stock_id == stock_id)
        .order_by(StockPrice.date.desc())
        .limit(1)
    )
    price = result.scalar_one_or_none()
    return price.close if price else None


async def calculate_portfolio_performance(
    db: AsyncSession,
    portfolio: Portfolio,
) -> PortfolioPerformance:
    """ポートフォリオのパフォーマンスを計算する"""
    holdings_result = await db.execute(
        select(PortfolioHolding)
        .where(PortfolioHolding.portfolio_id == portfolio.id)
    )
    holdings = holdings_result.scalars().all()

    holding_performances: list[HoldingPerformance] = []
    total_market_value = Decimal("0")
    total_cost_basis = Decimal("0")

    for holding in holdings:
        # 銘柄情報取得
        stock_result = await db.execute(
            select(Stock).where(Stock.id == holding.stock_id)
        )
        stock = stock_result.scalar_one_or_none()
        if not stock:
            continue

        # 現在価格取得
        current_price = await get_current_price(db, holding.stock_id)
        if current_price is None:
            current_price = holding.avg_purchase_price

        # 損益計算
        market_value = current_price * holding.quantity
        cost_basis = holding.avg_purchase_price * holding.quantity
        unrealized_pnl = market_value - cost_basis
        unrealized_pnl_percent = (
            (unrealized_pnl / cost_basis * 100) if cost_basis > 0 else Decimal("0")
        )

        total_market_value += market_value
        total_cost_basis += cost_basis

        holding_performances.append(HoldingPerformance(
            stock_code=stock.code,
            stock_name=stock.name,
            quantity=holding.quantity,
            avg_purchase_price=holding.avg_purchase_price,
            current_price=current_price,
            market_value=market_value,
            cost_basis=cost_basis,
            unrealized_pnl=unrealized_pnl,
            unrealized_pnl_percent=round(unrealized_pnl_percent, 2),
            weight=Decimal("0"),  # 後で計算
        ))

    # ポートフォリオ内比率を計算
    if total_market_value > 0:
        holding_performances = [
            HoldingPerformance(
                **{
                    **h.__dict__,
                    "weight": round(h.market_value / total_market_value * 100, 2),
                }
            )
            for h in holding_performances
        ]

    total_pnl = total_market_value - total_cost_basis
    total_pnl_percent = (
        (total_pnl / total_cost_basis * 100) if total_cost_basis > 0 else Decimal("0")
    )

    return PortfolioPerformance(
        total_market_value=total_market_value,
        total_cost_basis=total_cost_basis,
        total_unrealized_pnl=total_pnl,
        total_unrealized_pnl_percent=round(total_pnl_percent, 2),
        holdings=holding_performances,
    )
