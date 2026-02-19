"""エージェントAPIルーター

売買エージェントの推奨アクション・パイプライン制御を提供する。
"""

import asyncio
import logging
import threading
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings
from app.database import get_db
from app.models.signal import Signal
from app.models.stock import Stock
from app.models.trade import TradePlan
from app.schemas.agent import (
    OrderRecommendation,
    PipelineStatusResponse,
    PipelineStepStatus,
    SignalReason,
    TodayActionsResponse,
)
from app.services.pipeline import get_pipeline_status, run_pipeline

logger = logging.getLogger(__name__)

router = APIRouter()

# スコア閾値による注文種別判定
MARKET_ORDER_THRESHOLD = 80.0


def _determine_order_type(score: Decimal, action: str) -> str:
    """スコアに基づいて注文種別を決定する"""
    if action == "sell":
        return "market"
    return "market" if float(score) >= MARKET_ORDER_THRESHOLD else "limit"


def _build_recommendation(
    signal: Signal,
    stock: Stock,
    plan: TradePlan | None,
) -> OrderRecommendation:
    """シグナルと売買プランから注文推奨を組み立てる"""
    action = signal.signal_type
    order_type = _determine_order_type(signal.score, action)

    # 理由の抽出（scoring.pyは{"category":..,"reason":..}形式で保存）
    reasons: list[SignalReason] = []
    if signal.reasons and isinstance(signal.reasons, dict):
        for item in signal.reasons.get("items", []):
            indicator = item.get("indicator") or item.get("category", "")
            description = item.get("description") or item.get("reason", "")
            if indicator or description:
                reasons.append(SignalReason(
                    indicator=indicator,
                    description=description,
                    score=item.get("score", 0),
                ))

    price = plan.entry_price if plan else Decimal("0")
    quantity = plan.position_size if plan else 100

    return OrderRecommendation(
        stock_code=stock.code,
        stock_name=stock.name,
        action=action,
        order_type=order_type,
        price=price,
        quantity=quantity,
        score=signal.score,
        reasons=reasons,
        take_profit_1=plan.target_price_1 if plan else None,
        take_profit_2=plan.target_price_2 if plan else None,
        take_profit_3=plan.target_price_3 if plan else None,
        stop_loss=plan.stop_loss_price if plan else None,
        risk_reward_ratio=plan.risk_reward_ratio if plan else None,
    )


@router.get("/today-actions", response_model=TodayActionsResponse)
async def get_today_actions(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TodayActionsResponse:
    """今日の推奨アクションを取得する（認証不要）"""
    today = date.today()

    # パイプライン状態
    pipeline_info = get_pipeline_status()
    pipeline_status = pipeline_info["status"] if pipeline_info else "not_run"
    pipeline_last_run = pipeline_info["started_at"] if pipeline_info else None

    # 当日のシグナルを取得
    signal_result = await db.execute(
        select(Signal)
        .where(Signal.date == today)
        .order_by(Signal.score.desc())
    )
    signals = signal_result.scalars().all()

    buy_recs: list[OrderRecommendation] = []
    sell_recs: list[OrderRecommendation] = []

    for signal in signals:
        # 銘柄情報を取得
        stock_result = await db.execute(
            select(Stock).where(Stock.id == signal.stock_id)
        )
        stock = stock_result.scalar_one_or_none()
        if not stock:
            continue

        # 対応する売買プランを取得
        plan_result = await db.execute(
            select(TradePlan)
            .where(
                TradePlan.signal_id == signal.id,
                TradePlan.status == "active",
            )
            .limit(1)
        )
        plan = plan_result.scalar_one_or_none()

        rec = _build_recommendation(signal, stock, plan)

        if signal.signal_type == "buy":
            buy_recs.append(rec)
        else:
            sell_recs.append(rec)

    # サマリー生成
    summary = _generate_summary(buy_recs, sell_recs, pipeline_status)

    return TodayActionsResponse(
        date=today,
        pipeline_status=pipeline_status,
        pipeline_last_run=datetime.fromisoformat(pipeline_last_run) if pipeline_last_run else None,
        buy_recommendations=buy_recs,
        sell_recommendations=sell_recs,
        summary=summary,
    )


def _generate_summary(
    buy_recs: list[OrderRecommendation],
    sell_recs: list[OrderRecommendation],
    pipeline_status: str,
) -> str:
    """推奨アクションのサマリーを生成する"""
    if pipeline_status == "not_run":
        return "分析パイプラインが未実行です。「パイプライン実行」ボタンで分析を開始してください。"
    if pipeline_status == "running":
        return "分析パイプラインを実行中です。しばらくお待ちください。"
    if pipeline_status == "failed":
        return "分析パイプラインの実行に失敗しました。ログを確認してください。"

    if not buy_recs and not sell_recs:
        return "本日は明確なシグナルが検出されませんでした。"

    parts: list[str] = []
    if buy_recs:
        top_buy = buy_recs[0]
        parts.append(f"買い推奨 {len(buy_recs)}銘柄（最高スコア: {top_buy.stock_name} {top_buy.score}点）")
    if sell_recs:
        parts.append(f"売り推奨 {len(sell_recs)}銘柄")

    return "。".join(parts) + "。"


def _run_pipeline_in_thread() -> None:
    """別スレッド＋専用DB接続でパイプラインを実行する"""
    settings = get_settings()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # 専用のDBエンジン・セッションを作成（メインループと完全に分離）
        bg_engine = create_async_engine(
            settings.database_url,
            echo=False,
            pool_size=3,
            max_overflow=5,
        )
        bg_session_factory = async_sessionmaker(
            bg_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async def _run() -> None:
            async with bg_session_factory() as db:
                await run_pipeline(db)
            await bg_engine.dispose()

        loop.run_until_complete(_run())
    except Exception as e:
        logger.error(f"バックグラウンドパイプライン失敗: {e}")
    finally:
        loop.close()


@router.post("/run-pipeline")
async def trigger_pipeline() -> dict[str, str]:
    """分析パイプラインを手動実行する（認証不要）"""
    current = get_pipeline_status()
    if current and current["status"] == "running":
        return {"status": "already_running", "message": "パイプラインは既に実行中です"}

    thread = threading.Thread(target=_run_pipeline_in_thread, daemon=True)
    thread.start()
    return {"status": "triggered", "message": "分析パイプラインをバックグラウンドで開始しました"}


@router.get("/pipeline-status")
async def pipeline_status() -> dict[str, Any]:
    """パイプライン実行状態を取得する（認証不要）"""
    info = get_pipeline_status()
    if info is None:
        return {"status": "not_run", "message": "パイプラインは未実行です"}
    return info
