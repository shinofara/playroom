"""シグナル検出モジュール

テクニカル指標とファンダメンタルデータからスコアを計算し、
買い/売りシグナルを検出してDBに格納する。
"""

import logging
from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.analysis.scoring import calculate_total_score
from app.models.fundamental import FundamentalData
from app.models.signal import Signal
from app.models.stock import Stock, StockPrice
from app.models.technical import TechnicalIndicator

logger = logging.getLogger(__name__)

# シグナル判定閾値
BUY_THRESHOLD = 60.0
STRONG_BUY_THRESHOLD = 80.0
SELL_THRESHOLD = 40.0


def determine_signal_type(score: float) -> str | None:
    """スコアからシグナルタイプを判定する"""
    if score >= BUY_THRESHOLD:
        return "buy"
    elif score <= SELL_THRESHOLD:
        return "sell"
    return None


async def detect_stock_signal(
    db: AsyncSession,
    stock: Stock,
    target_date: date | None = None,
) -> Signal | None:
    """個別銘柄のシグナルを検出する"""
    if target_date is None:
        target_date = date.today()

    # 最新のテクニカル指標を取得
    indicator_result = await db.execute(
        select(TechnicalIndicator)
        .where(
            TechnicalIndicator.stock_id == stock.id,
            TechnicalIndicator.date <= target_date,
        )
        .order_by(TechnicalIndicator.date.desc())
        .limit(1)
    )
    indicator = indicator_result.scalar_one_or_none()
    if not indicator:
        return None

    # 最新のファンダメンタルデータを取得
    fund_result = await db.execute(
        select(FundamentalData)
        .where(
            FundamentalData.stock_id == stock.id,
            FundamentalData.date <= target_date,
        )
        .order_by(FundamentalData.date.desc())
        .limit(1)
    )
    fundamental = fund_result.scalar_one_or_none()

    # 最新の株価を取得
    price_result = await db.execute(
        select(StockPrice)
        .where(
            StockPrice.stock_id == stock.id,
            StockPrice.date <= target_date,
        )
        .order_by(StockPrice.date.desc())
        .limit(1)
    )
    price = price_result.scalar_one_or_none()
    if not price:
        return None

    # スコア計算
    score_result = calculate_total_score(
        indicator=indicator,
        fundamental=fundamental,
        close_price=float(price.close),
        current_volume=price.volume,
    )

    # シグナル判定
    signal_type = determine_signal_type(score_result.total_score)
    if signal_type is None:
        return None

    # シグナルをDBに保存
    signal = Signal(
        stock_id=stock.id,
        date=target_date,
        signal_type=signal_type,
        score=Decimal(str(score_result.total_score)),
        technical_score=Decimal(str(score_result.technical_score)),
        fundamental_score=Decimal(str(score_result.fundamental_score)),
        reasons={"items": score_result.reasons},
    )
    db.add(signal)
    return signal


async def detect_all_signals(
    db: AsyncSession,
    target_date: date | None = None,
) -> tuple[int, int, list[str]]:
    """全銘柄のシグナルを検出する

    Returns:
        (成功件数, エラー件数, エラー詳細リスト)
    """
    result = await db.execute(select(Stock).where(Stock.is_active.is_(True)))
    stocks = result.scalars().all()

    success_count = 0
    error_count = 0
    errors: list[str] = []

    for stock in stocks:
        try:
            signal = await detect_stock_signal(db, stock, target_date)
            if signal:
                success_count += 1
                logger.info(
                    f"シグナル検出: {stock.code} - {signal.signal_type} (スコア: {signal.score})"
                )
        except Exception as e:
            error_count += 1
            error_msg = f"{stock.code}: {str(e)}"
            errors.append(error_msg)
            logger.error(f"シグナル検出エラー: {error_msg}")

    await db.commit()
    return success_count, error_count, errors
