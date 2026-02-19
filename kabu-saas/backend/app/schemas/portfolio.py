"""ポートフォリオスキーマ"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PortfolioResponse(BaseModel):
    """ポートフォリオレスポンス"""

    id: int
    name: str
    total_investment: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}


class PortfolioUpdate(BaseModel):
    """ポートフォリオ更新リクエスト"""

    name: str | None = None
    total_investment: Decimal | None = None


class HoldingResponse(BaseModel):
    """保有銘柄レスポンス"""

    id: int
    portfolio_id: int
    stock_id: int
    quantity: int
    avg_purchase_price: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class HoldingCreate(BaseModel):
    """保有銘柄追加リクエスト"""

    stock_id: int
    quantity: int
    avg_purchase_price: Decimal


class HoldingUpdate(BaseModel):
    """保有銘柄更新リクエスト"""

    quantity: int | None = None
    avg_purchase_price: Decimal | None = None
