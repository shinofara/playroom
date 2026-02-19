"""売買プラン生成モジュール

シグナルに基づいてエントリーポイント、利確/損切りライン、
ポジションサイズを計算する。
"""

import logging
from dataclasses import dataclass
from decimal import Decimal

logger = logging.getLogger(__name__)

# デフォルトの利確/損切り設定
DEFAULT_TAKE_PROFIT_RATES = [0.10, 0.20, 0.30]  # +10%, +20%, +30%
DEFAULT_STOP_LOSS_RATE = 0.05  # -5%
DEFAULT_MAX_POSITION_RATIO = 0.10  # 総資金の10%まで


@dataclass(frozen=True)
class TradePlanResult:
    """売買プラン計算結果"""
    entry_price: Decimal
    target_price_1: Decimal
    target_price_2: Decimal
    target_price_3: Decimal
    stop_loss_price: Decimal
    position_size: int
    risk_reward_ratio: Decimal


def calculate_entry_price(
    close_price: float,
    sma_25: float | None = None,
) -> float:
    """エントリー価格を計算する

    直近終値とSMA25の中間付近を推奨エントリーとする。
    """
    if sma_25 and sma_25 < close_price:
        # SMA25が終値より低い場合、押し目を想定
        return (close_price + sma_25) / 2
    return close_price


def calculate_trade_plan(
    close_price: float,
    sma_25: float | None = None,
    total_capital: float = 1_000_000,
    take_profit_rates: list[float] | None = None,
    stop_loss_rate: float = DEFAULT_STOP_LOSS_RATE,
    max_position_ratio: float = DEFAULT_MAX_POSITION_RATIO,
) -> TradePlanResult:
    """売買プランを計算する"""
    tp_rates = take_profit_rates or DEFAULT_TAKE_PROFIT_RATES

    entry = calculate_entry_price(close_price, sma_25)

    # 利確目標
    target_1 = entry * (1 + tp_rates[0])
    target_2 = entry * (1 + tp_rates[1])
    target_3 = entry * (1 + tp_rates[2])

    # 損切りライン
    stop_loss = entry * (1 - stop_loss_rate)

    # ポジションサイズ（100株単位に丸め）
    max_investment = total_capital * max_position_ratio
    raw_size = max_investment / entry
    position_size = max(int(raw_size // 100) * 100, 100)

    # リスクリワード比
    risk = entry - stop_loss
    reward = target_1 - entry
    risk_reward = reward / risk if risk > 0 else 0

    return TradePlanResult(
        entry_price=Decimal(str(round(entry, 2))),
        target_price_1=Decimal(str(round(target_1, 2))),
        target_price_2=Decimal(str(round(target_2, 2))),
        target_price_3=Decimal(str(round(target_3, 2))),
        stop_loss_price=Decimal(str(round(stop_loss, 2))),
        position_size=position_size,
        risk_reward_ratio=Decimal(str(round(risk_reward, 2))),
    )
