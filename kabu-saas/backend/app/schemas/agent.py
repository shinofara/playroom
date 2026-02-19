"""エージェントAPIスキーマ"""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class SignalReason(BaseModel):
    """シグナル理由"""
    indicator: str
    description: str
    score: float


class OrderRecommendation(BaseModel):
    """注文推奨"""
    stock_code: str
    stock_name: str
    action: str  # "buy" | "sell"
    order_type: str  # "market" | "limit"
    price: Decimal
    quantity: int
    score: Decimal
    reasons: list[SignalReason]
    take_profit_1: Decimal | None = None
    take_profit_2: Decimal | None = None
    take_profit_3: Decimal | None = None
    stop_loss: Decimal | None = None
    risk_reward_ratio: Decimal | None = None


class PipelineStepStatus(BaseModel):
    """パイプラインステップ状態"""
    name: str
    success_count: int
    error_count: int
    errors: list[str]


class PipelineStatusResponse(BaseModel):
    """パイプライン実行状態"""
    status: str
    started_at: str | None = None
    finished_at: str | None = None
    steps: list[PipelineStepStatus]


class TodayActionsResponse(BaseModel):
    """今日の推奨アクション"""
    date: date
    pipeline_status: str  # "not_run" | "running" | "completed" | "failed"
    pipeline_last_run: datetime | None = None
    buy_recommendations: list[OrderRecommendation]
    sell_recommendations: list[OrderRecommendation]
    summary: str
