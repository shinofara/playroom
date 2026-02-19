"""シグナルスキーマ"""

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel


class SignalResponse(BaseModel):
    """シグナルレスポンス"""

    id: int
    stock_id: int
    date: date
    signal_type: str
    score: Decimal
    technical_score: Decimal | None = None
    fundamental_score: Decimal | None = None
    reasons: dict[str, Any] | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
