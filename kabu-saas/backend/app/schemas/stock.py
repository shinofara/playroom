"""銘柄・株価スキーマ"""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class StockDetailResponse(BaseModel):
    """銘柄詳細レスポンス"""

    id: int
    code: str
    name: str
    sector: str | None = None
    market: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedStockResponse(BaseModel):
    """ページネーション付き銘柄一覧レスポンス"""

    items: list[StockDetailResponse]
    total: int
    page: int
    per_page: int


class StockPriceResponse(BaseModel):
    """株価レスポンス"""

    id: int
    stock_id: int
    date: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    adjusted_close: Decimal

    model_config = {"from_attributes": True}


class FundamentalDataResponse(BaseModel):
    """ファンダメンタルデータレスポンス"""

    id: int
    stock_id: int
    date: date
    per: Decimal | None = None
    pbr: Decimal | None = None
    dividend_yield: Decimal | None = None
    roe: Decimal | None = None
    eps: Decimal | None = None
    bps: Decimal | None = None
    market_cap: int | None = None
    revenue: int | None = None
    operating_income: int | None = None

    model_config = {"from_attributes": True}


class TechnicalIndicatorResponse(BaseModel):
    """テクニカル指標レスポンス"""

    id: int
    stock_id: int
    date: date
    sma_5: Decimal | None = None
    sma_25: Decimal | None = None
    sma_75: Decimal | None = None
    sma_200: Decimal | None = None
    ema_12: Decimal | None = None
    ema_26: Decimal | None = None
    rsi_14: Decimal | None = None
    macd_line: Decimal | None = None
    macd_signal: Decimal | None = None
    macd_histogram: Decimal | None = None
    bb_upper_2: Decimal | None = None
    bb_middle: Decimal | None = None
    bb_lower_2: Decimal | None = None
    volume_sma_25: int | None = None

    model_config = {"from_attributes": True}
