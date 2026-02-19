"""ファンダメンタルデータ収集モジュール

yfinanceを使用して銘柄のファンダメンタル指標を取得し、DBに格納する。
"""

import asyncio
import logging
from datetime import date
from decimal import Decimal

import yfinance as yf
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fundamental import FundamentalData
from app.models.stock import Stock

logger = logging.getLogger(__name__)


def _safe_decimal(value, precision: int = 2) -> Decimal | None:
    """安全にDecimalに変換する"""
    if value is None or str(value) in ("nan", "inf", "-inf", "None"):
        return None
    try:
        return Decimal(str(round(float(value), precision)))
    except (ValueError, TypeError):
        return None


def _safe_int(value) -> int | None:
    """安全にintに変換する"""
    if value is None or str(value) in ("nan", "inf", "-inf", "None"):
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None


def fetch_fundamental_data(ticker_code: str) -> dict | None:
    """yfinanceからファンダメンタルデータを取得する"""
    try:
        ticker = yf.Ticker(ticker_code)
        info = ticker.info
        if not info or "symbol" not in info:
            logger.warning(f"ファンダメンタルデータなし: {ticker_code}")
            return None
        return info
    except Exception as e:
        logger.error(f"ファンダメンタルデータ取得エラー: {ticker_code} - {e}")
        return None


def transform_fundamental_data(
    info: dict,
    stock_id: int,
    target_date: date,
) -> dict | None:
    """取得したデータをDB挿入用辞書に変換する"""
    if not info:
        return None

    return {
        "stock_id": stock_id,
        "date": target_date,
        "per": _safe_decimal(info.get("trailingPE")),
        "pbr": _safe_decimal(info.get("priceToBook")),
        "dividend_yield": _safe_decimal(
            info.get("dividendYield", 0) * 100 if info.get("dividendYield") else None
        ),
        "roe": _safe_decimal(info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else None),
        "eps": _safe_decimal(info.get("trailingEps")),
        "bps": _safe_decimal(info.get("bookValue")),
        "market_cap": _safe_int(info.get("marketCap")),
        "revenue": _safe_int(info.get("totalRevenue")),
        "operating_income": _safe_int(info.get("operatingIncome")),
    }


async def upsert_fundamental_record(
    db: AsyncSession,
    record: dict,
) -> bool:
    """ファンダメンタルデータをUPSERTする"""
    stmt = pg_insert(FundamentalData).values(**record)
    stmt = stmt.on_conflict_do_update(
        constraint="uq_fundamental_data_stock_date",
        set_={k: v for k, v in record.items() if k not in ("stock_id", "date")},
    )
    await db.execute(stmt)
    return True


async def collect_stock_fundamentals(
    db: AsyncSession,
    stock: Stock,
    target_date: date | None = None,
) -> bool:
    """個別銘柄のファンダメンタルデータを収集してDBに格納する"""
    if target_date is None:
        target_date = date.today()

    logger.info(f"ファンダメンタル収集開始: {stock.code}")

    # yfinanceは同期I/Oのため別スレッドで実行
    info = await asyncio.to_thread(fetch_fundamental_data, stock.code)
    record = transform_fundamental_data(info, stock.id, target_date) if info else None

    if record:
        await upsert_fundamental_record(db, record)
        logger.info(f"ファンダメンタル収集完了: {stock.code}")
        return True

    logger.warning(f"ファンダメンタルデータなし: {stock.code}")
    return False


async def collect_all_fundamentals(
    db: AsyncSession,
    target_date: date | None = None,
) -> tuple[int, int, list[str]]:
    """全銘柄のファンダメンタルデータを収集する

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
            if await collect_stock_fundamentals(db, stock, target_date):
                success_count += 1
        except Exception as e:
            error_count += 1
            error_msg = f"{stock.code}: {str(e)}"
            errors.append(error_msg)
            logger.error(f"ファンダメンタル収集エラー: {error_msg}")

    return success_count, error_count, errors
