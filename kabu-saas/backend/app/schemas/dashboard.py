"""ダッシュボードスキーマ"""

from decimal import Decimal

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    """ダッシュボードサマリ"""

    total_assets: Decimal
    total_profit_loss: Decimal
    daily_change: Decimal
    buy_signal_count: int
    sell_signal_count: int


class MarketOverview(BaseModel):
    """マーケット概況"""

    nikkei225: Decimal
    nikkei225_change: Decimal
    topix: Decimal
    topix_change: Decimal
    usd_jpy: Decimal
    usd_jpy_change: Decimal
