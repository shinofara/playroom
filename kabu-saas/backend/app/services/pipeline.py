"""分析パイプラインオーケストレーター

株価収集 → ファンダメンタル収集 → テクニカル計算 → シグナル検出 → 売買プラン生成
の5ステップを順序実行する。
"""

import logging
from dataclasses import dataclass, field
from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import func as sql_func

from app.analysis.signal_detector import detect_all_signals
from app.analysis.technical import calculate_all_technicals
from app.collectors.fundamental_collector import collect_all_fundamentals
from app.collectors.price_collector import collect_all_prices, collect_historical_prices
from app.models.signal import Signal
from app.models.stock import Stock, StockPrice
from app.services.planner import generate_system_trade_plan

# テクニカル指標計算に必要な最低データ件数
MIN_PRICE_RECORDS_FOR_TECHNICALS = 200

logger = logging.getLogger(__name__)


@dataclass
class PipelineStepResult:
    """パイプライン各ステップの結果"""
    name: str
    success_count: int = 0
    error_count: int = 0
    errors: list[str] = field(default_factory=list)


@dataclass
class PipelineResult:
    """パイプライン全体の実行結果"""
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime | None = None
    steps: list[PipelineStepResult] = field(default_factory=list)
    status: str = "running"

    @property
    def summary(self) -> dict:
        return {
            "status": self.status,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "steps": [
                {
                    "name": s.name,
                    "success_count": s.success_count,
                    "error_count": s.error_count,
                    "errors": s.errors[:5],
                }
                for s in self.steps
            ],
        }


# パイプラインの実行状態をモジュールレベルで保持（シングルプロセス前提）
_current_pipeline: PipelineResult | None = None


def get_pipeline_status() -> dict | None:
    """現在のパイプライン実行状態を取得する"""
    if _current_pipeline is None:
        return None
    return _current_pipeline.summary


async def run_pipeline(db: AsyncSession, target_date: date | None = None) -> PipelineResult:
    """分析パイプラインを実行する"""
    global _current_pipeline

    if target_date is None:
        target_date = date.today()

    result = PipelineResult()
    _current_pipeline = result

    try:
        # Step 0: ヒストリカルデータチェック（初回のみ）
        needs_historical = await _needs_historical_data(db)
        if needs_historical:
            logger.info("パイプライン Step 0: ヒストリカルデータ取得（初回）")
            step0 = await _run_step("ヒストリカル取得", lambda: collect_historical_prices(db, years=1))
            result.steps.append(step0)
            await db.commit()

        # Step 1: 株価収集（直近分の更新）
        logger.info("パイプライン Step 1/5: 株価収集開始")
        step1 = await _run_step("株価収集", lambda: collect_all_prices(db))
        result.steps.append(step1)
        await db.commit()

        # Step 2: ファンダメンタル収集
        logger.info("パイプライン Step 2/5: ファンダメンタル収集開始")
        step2 = await _run_step("ファンダメンタル収集", lambda: collect_all_fundamentals(db))
        result.steps.append(step2)
        await db.commit()

        # Step 3: テクニカル指標計算
        logger.info("パイプライン Step 3/5: テクニカル指標計算開始")
        step3 = await _run_step("テクニカル計算", lambda: calculate_all_technicals(db))
        result.steps.append(step3)
        await db.commit()

        # Step 4: シグナル検出
        logger.info("パイプライン Step 4/5: シグナル検出開始")
        step4 = await _run_step("シグナル検出", lambda: detect_all_signals(db, target_date))
        result.steps.append(step4)
        await db.commit()

        # Step 5: 買いシグナル銘柄にシステム売買プラン生成
        logger.info("パイプライン Step 5/5: 売買プラン生成開始")
        step5 = await _run_generate_plans(db, target_date)
        result.steps.append(step5)
        await db.commit()

        result.status = "completed"
        logger.info("パイプライン完了")

    except Exception as e:
        result.status = "failed"
        logger.error(f"パイプライン失敗: {e}")
        raise
    finally:
        result.finished_at = datetime.now(timezone.utc)

    return result


async def _needs_historical_data(db: AsyncSession) -> bool:
    """テクニカル指標に必要なデータ量があるかチェックする"""
    result = await db.execute(
        select(sql_func.count(StockPrice.id))
    )
    total_prices = result.scalar_one()
    # 30銘柄 x 200日 = 6000件以上あればOK
    return total_prices < MIN_PRICE_RECORDS_FOR_TECHNICALS * 30


async def _run_step(
    name: str,
    func,
) -> PipelineStepResult:
    """パイプラインの1ステップを実行する"""
    step = PipelineStepResult(name=name)
    try:
        success, errors, error_details = await func()
        step.success_count = success
        step.error_count = errors
        step.errors = error_details
        logger.info(f"  {name} 完了: 成功={success}, エラー={errors}")
    except Exception as e:
        step.error_count = 1
        step.errors = [str(e)]
        logger.error(f"  {name} 失敗: {e}")
    return step


async def _run_generate_plans(
    db: AsyncSession,
    target_date: date,
) -> PipelineStepResult:
    """当日の買いシグナル銘柄に対してシステム売買プランを生成する"""
    step = PipelineStepResult(name="売買プラン生成")

    # 当日の買いシグナルを取得
    signal_result = await db.execute(
        select(Signal)
        .where(
            Signal.date == target_date,
            Signal.signal_type == "buy",
        )
        .order_by(Signal.score.desc())
    )
    buy_signals = signal_result.scalars().all()

    for signal in buy_signals:
        try:
            stock_result = await db.execute(
                select(Stock).where(Stock.id == signal.stock_id)
            )
            stock = stock_result.scalar_one_or_none()
            if not stock:
                continue

            plan = await generate_system_trade_plan(db, stock, signal)
            if plan:
                step.success_count += 1
        except Exception as e:
            step.error_count += 1
            step.errors.append(f"signal_id={signal.id}: {str(e)}")
            logger.error(f"売買プラン生成エラー: signal_id={signal.id} - {e}")

    logger.info(f"  売買プラン生成 完了: 成功={step.success_count}, エラー={step.error_count}")
    return step
