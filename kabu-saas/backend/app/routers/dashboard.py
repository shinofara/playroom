"""ダッシュボードAPIルーター"""

from fastapi import APIRouter

from app.schemas.dashboard import DashboardSummary, MarketOverview

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary() -> DashboardSummary:
    """ダッシュボードサマリ取得"""
    # TODO: 実装はTask #4-6で行う
    return DashboardSummary(
        total_assets=0,
        total_profit_loss=0,
        daily_change=0,
        buy_signal_count=0,
        sell_signal_count=0,
    )


@router.get("/market", response_model=MarketOverview)
async def get_market_overview() -> MarketOverview:
    """マーケット概況取得"""
    # TODO: 実装はTask #4で行う
    return MarketOverview(
        nikkei225=0,
        nikkei225_change=0,
        topix=0,
        topix_change=0,
        usd_jpy=0,
        usd_jpy_change=0,
    )
