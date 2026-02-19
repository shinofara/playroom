"""株価データ収集モジュール

yfinanceを使用して日本株の日足データを取得し、DBに格納する。
"""

import asyncio
import logging
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

import pandas as pd
import yfinance as yf
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stock import Stock, StockPrice

logger = logging.getLogger(__name__)

JST = timezone(timedelta(hours=9))


def fetch_price_data(
    ticker_code: str,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """yfinanceから株価データを取得する（純粋関数に近い形で実装）"""
    try:
        ticker = yf.Ticker(ticker_code)
        df = ticker.history(
            start=start_date.isoformat(),
            end=end_date.isoformat(),
            auto_adjust=False,
        )
        if df.empty:
            logger.warning(f"株価データなし: {ticker_code}")
            return pd.DataFrame()
        return df
    except Exception as e:
        logger.error(f"株価データ取得エラー: {ticker_code} - {e}")
        return pd.DataFrame()


def transform_price_data(
    df: pd.DataFrame,
    stock_id: int,
) -> list[dict]:
    """DataFrameをDB挿入用の辞書リストに変換する"""
    if df.empty:
        return []

    records = []
    for idx, row in df.iterrows():
        record_date = idx.date() if hasattr(idx, "date") else idx
        records.append({
            "stock_id": stock_id,
            "date": record_date,
            "open": Decimal(str(round(row["Open"], 2))),
            "high": Decimal(str(round(row["High"], 2))),
            "low": Decimal(str(round(row["Low"], 2))),
            "close": Decimal(str(round(row["Close"], 2))),
            "volume": int(row["Volume"]),
            "adjusted_close": Decimal(str(round(row.get("Adj Close", row["Close"]), 2))),
        })
    return records


async def upsert_price_records(
    db: AsyncSession,
    records: list[dict],
) -> int:
    """株価レコードをUPSERTする"""
    if not records:
        return 0

    stmt = pg_insert(StockPrice).values(records)
    stmt = stmt.on_conflict_do_update(
        constraint="uq_stock_prices_stock_date",
        set_={
            "open": stmt.excluded.open,
            "high": stmt.excluded.high,
            "low": stmt.excluded.low,
            "close": stmt.excluded.close,
            "volume": stmt.excluded.volume,
            "adjusted_close": stmt.excluded.adjusted_close,
        },
    )
    await db.execute(stmt)
    return len(records)


async def collect_stock_prices(
    db: AsyncSession,
    stock: Stock,
    start_date: date | None = None,
    end_date: date | None = None,
) -> int:
    """個別銘柄の株価データを収集してDBに格納する"""
    today = date.today()
    if end_date is None:
        end_date = today
    if start_date is None:
        start_date = today - timedelta(days=7)

    logger.info(f"株価収集開始: {stock.code} ({start_date} ~ {end_date})")

    # yfinanceは同期I/Oのため別スレッドで実行
    df = await asyncio.to_thread(fetch_price_data, stock.code, start_date, end_date)
    records = transform_price_data(df, stock.id)
    count = await upsert_price_records(db, records)

    logger.info(f"株価収集完了: {stock.code} - {count}件")
    return count


async def collect_all_prices(
    db: AsyncSession,
    start_date: date | None = None,
    end_date: date | None = None,
) -> tuple[int, int, list[str]]:
    """全銘柄の株価データを収集する

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
            count = await collect_stock_prices(db, stock, start_date, end_date)
            if count > 0:
                success_count += 1
        except Exception as e:
            error_count += 1
            error_msg = f"{stock.code}: {str(e)}"
            errors.append(error_msg)
            logger.error(f"株価収集エラー: {error_msg}")

    return success_count, error_count, errors


async def collect_historical_prices(
    db: AsyncSession,
    years: int = 5,
) -> tuple[int, int, list[str]]:
    """全銘柄のヒストリカルデータを一括取得する"""
    today = date.today()
    start_date = today - timedelta(days=365 * years)
    return await collect_all_prices(db, start_date, today)
