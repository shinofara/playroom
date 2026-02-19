"""スクリーニングスキーマ"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.schemas.stock import StockDetailResponse


class ScreeningRequest(BaseModel):
    """スクリーニングリクエスト"""

    market: str | None = None
    sector: str | None = None
    price_min: float | None = None
    price_max: float | None = None
    market_cap_min: int | None = None
    market_cap_max: int | None = None
    per_min: float | None = None
    per_max: float | None = None
    pbr_min: float | None = None
    pbr_max: float | None = None
    dividend_yield_min: float | None = None
    roe_min: float | None = None
    rsi_min: float | None = None
    rsi_max: float | None = None
    min_volume: int | None = None
    min_score: float | None = None
    sort_by: str = "score"
    sort_order: str = "desc"
    page: int = 1
    per_page: int = 20


class ScreeningResultResponse(BaseModel):
    """スクリーニング結果レスポンス"""

    items: list[StockDetailResponse]
    total: int


class ScreeningPresetResponse(BaseModel):
    """スクリーニングプリセットレスポンス"""

    id: int
    name: str
    conditions: dict[str, Any]
    created_at: datetime

    model_config = {"from_attributes": True}


class ScreeningPresetCreate(BaseModel):
    """スクリーニングプリセット作成リクエスト"""

    name: str
    conditions: dict[str, Any]
