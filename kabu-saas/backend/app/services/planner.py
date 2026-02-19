"""売買プランサービス

シグナルとテクニカル分析に基づいて売買プランを生成する。
"""

import logging
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.analysis.trade_planner import calculate_trade_plan
from app.models.signal import Signal
from app.models.stock import Stock, StockPrice
from app.models.technical import TechnicalIndicator
from app.models.trade import TradePlan
from app.models.user import User

logger = logging.getLogger(__name__)


async def _fetch_latest_price_and_sma(
    db: AsyncSession,
    stock: Stock,
) -> tuple[float, float | None] | None:
    """直近の株価とSMA25を取得する"""
    price_result = await db.execute(
        select(StockPrice)
        .where(StockPrice.stock_id == stock.id)
        .order_by(StockPrice.date.desc())
        .limit(1)
    )
    price = price_result.scalar_one_or_none()
    if not price:
        return None

    tech_result = await db.execute(
        select(TechnicalIndicator)
        .where(TechnicalIndicator.stock_id == stock.id)
        .order_by(TechnicalIndicator.date.desc())
        .limit(1)
    )
    tech = tech_result.scalar_one_or_none()
    sma_25 = float(tech.sma_25) if tech and tech.sma_25 else None

    return float(price.close), sma_25


async def generate_trade_plan(
    db: AsyncSession,
    stock: Stock,
    user: User,
    total_capital: float = 1_000_000,
) -> TradePlan | None:
    """ユーザー紐付きの売買プランを生成する"""
    result = await _fetch_latest_price_and_sma(db, stock)
    if not result:
        return None

    close_price, sma_25 = result
    plan_result = calculate_trade_plan(
        close_price=close_price,
        sma_25=sma_25,
        total_capital=total_capital,
    )

    trade_plan = TradePlan(
        stock_id=stock.id,
        user_id=user.id,
        plan_type="buy",
        entry_price=plan_result.entry_price,
        target_price_1=plan_result.target_price_1,
        target_price_2=plan_result.target_price_2,
        target_price_3=plan_result.target_price_3,
        stop_loss_price=plan_result.stop_loss_price,
        position_size=plan_result.position_size,
        risk_reward_ratio=plan_result.risk_reward_ratio,
        status="active",
    )
    db.add(trade_plan)
    await db.flush()
    return trade_plan


async def generate_system_trade_plan(
    db: AsyncSession,
    stock: Stock,
    signal: Signal,
    total_capital: float = 1_000_000,
) -> TradePlan | None:
    """エージェント用のシステム売買プランを生成する（ユーザー紐付けなし）"""
    result = await _fetch_latest_price_and_sma(db, stock)
    if not result:
        logger.warning(f"株価データなし、プラン生成スキップ: {stock.code}")
        return None

    close_price, sma_25 = result
    plan_result = calculate_trade_plan(
        close_price=close_price,
        sma_25=sma_25,
        total_capital=total_capital,
    )

    trade_plan = TradePlan(
        stock_id=stock.id,
        user_id=None,
        signal_id=signal.id,
        plan_type=signal.signal_type,
        entry_price=plan_result.entry_price,
        target_price_1=plan_result.target_price_1,
        target_price_2=plan_result.target_price_2,
        target_price_3=plan_result.target_price_3,
        stop_loss_price=plan_result.stop_loss_price,
        position_size=plan_result.position_size,
        risk_reward_ratio=plan_result.risk_reward_ratio,
        status="active",
    )
    db.add(trade_plan)
    await db.flush()
    logger.info(f"システム売買プラン生成: {stock.code} ({signal.signal_type}, スコア: {signal.score})")
    return trade_plan
