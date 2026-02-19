"""取引スキーマ"""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class TradeResponse(BaseModel):
    """取引レスポンス"""

    id: int
    portfolio_id: int
    stock_id: int
    trade_type: str
    quantity: int
    price: Decimal
    commission: Decimal
    transaction_date: date
    notes: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class TradeCreate(BaseModel):
    """取引記録追加リクエスト"""

    stock_id: int
    trade_type: str  # "buy" / "sell"
    quantity: int
    price: Decimal
    commission: Decimal | None = None
    transaction_date: date
    notes: str | None = None
