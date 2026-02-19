"""テクニカル指標計算モジュール

pandasのrolling/ewm関数を使用して各種テクニカル指標を計算し、DBに格納する。
（pandas-taはDocker ARM環境でSIGILLを起こすため不使用）
"""

import logging
from datetime import date
from decimal import Decimal

import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stock import Stock, StockPrice
from app.models.technical import TechnicalIndicator

logger = logging.getLogger(__name__)


def _to_decimal(value, precision: int = 2) -> Decimal | None:
    """NaN安全にDecimalへ変換する"""
    if pd.isna(value):
        return None
    return Decimal(str(round(float(value), precision)))


def _to_int(value) -> int | None:
    """NaN安全にintへ変換する"""
    if pd.isna(value):
        return None
    return int(float(value))


def _calc_rsi(close: pd.Series, length: int = 14) -> pd.Series:
    """RSIを計算する"""
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1 / length, min_periods=length).mean()
    avg_loss = loss.ewm(alpha=1 / length, min_periods=length).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def _calc_macd(
    close: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """MACD（ライン、シグナル、ヒストグラム）を計算する"""
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    macd_signal = macd_line.ewm(span=signal, adjust=False).mean()
    macd_histogram = macd_line - macd_signal
    return macd_line, macd_signal, macd_histogram


def _calc_bollinger_bands(
    close: pd.Series,
    length: int = 20,
    std_dev: float = 2.0,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """ボリンジャーバンド（上限、中央、下限）を計算する"""
    middle = close.rolling(window=length).mean()
    std = close.rolling(window=length).std()
    upper = middle + std_dev * std
    lower = middle - std_dev * std
    return upper, middle, lower


def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """株価DataFrameからテクニカル指標を計算する（純粋関数）

    Args:
        df: 株価データ（columns: open, high, low, close, volume, date）

    Returns:
        テクニカル指標を追加したDataFrame
    """
    if df.empty or len(df) < 26:
        return pd.DataFrame()

    result = df.copy()
    close = result["close"]

    # SMA（単純移動平均線）
    result["sma_5"] = close.rolling(window=5).mean()
    result["sma_25"] = close.rolling(window=25).mean()
    result["sma_75"] = close.rolling(window=75).mean()
    result["sma_200"] = close.rolling(window=200).mean()

    # EMA（指数移動平均線）
    result["ema_12"] = close.ewm(span=12, adjust=False).mean()
    result["ema_26"] = close.ewm(span=26, adjust=False).mean()

    # RSI
    result["rsi_14"] = _calc_rsi(close, 14)

    # MACD
    macd_line, macd_signal, macd_histogram = _calc_macd(close, 12, 26, 9)
    result["macd_line"] = macd_line
    result["macd_signal"] = macd_signal
    result["macd_histogram"] = macd_histogram

    # ボリンジャーバンド
    bb_upper, bb_middle, bb_lower = _calc_bollinger_bands(close, 20, 2.0)
    result["bb_upper_2"] = bb_upper
    result["bb_middle"] = bb_middle
    result["bb_lower_2"] = bb_lower

    # 出来高SMA
    result["volume_sma_25"] = result["volume"].astype(float).rolling(window=25).mean()

    return result


def transform_to_indicator_records(
    df: pd.DataFrame,
    stock_id: int,
) -> list[dict]:
    """計算結果をDB挿入用のレコードリストに変換する"""
    if df.empty:
        return []

    records = []
    for _, row in df.iterrows():
        records.append({
            "stock_id": stock_id,
            "date": row["date"] if isinstance(row["date"], date) else row["date"].date(),
            "sma_5": _to_decimal(row.get("sma_5")),
            "sma_25": _to_decimal(row.get("sma_25")),
            "sma_75": _to_decimal(row.get("sma_75")),
            "sma_200": _to_decimal(row.get("sma_200")),
            "ema_12": _to_decimal(row.get("ema_12")),
            "ema_26": _to_decimal(row.get("ema_26")),
            "rsi_14": _to_decimal(row.get("rsi_14")),
            "macd_line": _to_decimal(row.get("macd_line"), 4),
            "macd_signal": _to_decimal(row.get("macd_signal"), 4),
            "macd_histogram": _to_decimal(row.get("macd_histogram"), 4),
            "bb_upper_2": _to_decimal(row.get("bb_upper_2")),
            "bb_middle": _to_decimal(row.get("bb_middle")),
            "bb_lower_2": _to_decimal(row.get("bb_lower_2")),
            "volume_sma_25": _to_int(row.get("volume_sma_25")),
        })
    return records


async def upsert_indicator_records(
    db: AsyncSession,
    records: list[dict],
) -> int:
    """テクニカル指標レコードをUPSERTする"""
    if not records:
        return 0

    for record in records:
        stmt = pg_insert(TechnicalIndicator).values(**record)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_technical_indicators_stock_date",
            set_={k: v for k, v in record.items() if k not in ("stock_id", "date")},
        )
        await db.execute(stmt)
    return len(records)


async def calculate_stock_technicals(
    db: AsyncSession,
    stock: Stock,
) -> int:
    """個別銘柄のテクニカル指標を計算してDBに格納する"""
    logger.info(f"テクニカル分析開始: {stock.code}")

    # 株価データを取得
    result = await db.execute(
        select(StockPrice)
        .where(StockPrice.stock_id == stock.id)
        .order_by(StockPrice.date.asc())
    )
    prices = result.scalars().all()

    if len(prices) < 26:
        logger.warning(f"株価データ不足: {stock.code} ({len(prices)}件)")
        return 0

    # DataFrameに変換
    df = pd.DataFrame([{
        "date": p.date,
        "open": float(p.open),
        "high": float(p.high),
        "low": float(p.low),
        "close": float(p.close),
        "volume": p.volume,
    } for p in prices])

    # テクニカル指標計算
    indicators_df = calculate_technical_indicators(df)
    records = transform_to_indicator_records(indicators_df, stock.id)
    count = await upsert_indicator_records(db, records)

    logger.info(f"テクニカル分析完了: {stock.code} - {count}件")
    return count


async def calculate_all_technicals(
    db: AsyncSession,
) -> tuple[int, int, list[str]]:
    """全銘柄のテクニカル指標を計算する

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
            count = await calculate_stock_technicals(db, stock)
            if count > 0:
                success_count += 1
        except Exception as e:
            error_count += 1
            error_msg = f"{stock.code}: {str(e)}"
            errors.append(error_msg)
            logger.error(f"テクニカル分析エラー: {error_msg}")

    return success_count, error_count, errors
