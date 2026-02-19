"""スコアリングモデル

テクニカル指標とファンダメンタルデータを統合してスコアを計算する。
"""

from dataclasses import dataclass
from decimal import Decimal

from app.models.fundamental import FundamentalData
from app.models.technical import TechnicalIndicator


# デフォルトの重み設定
DEFAULT_WEIGHTS = {
    "sma_cross": 0.15,
    "rsi": 0.10,
    "macd": 0.15,
    "bollinger": 0.10,
    "volume": 0.10,
    "per": 0.10,
    "pbr": 0.10,
    "dividend_yield": 0.10,
    "roe": 0.10,
}


@dataclass(frozen=True)
class ScoreResult:
    """スコアリング結果"""
    total_score: float
    technical_score: float
    fundamental_score: float
    reasons: list[dict[str, str]]


def score_sma_cross(indicator: TechnicalIndicator) -> tuple[float, str | None]:
    """SMA/EMAクロスのスコアを計算する"""
    if indicator.sma_5 is None or indicator.sma_25 is None:
        return 50.0, None

    sma_5 = float(indicator.sma_5)
    sma_25 = float(indicator.sma_25)
    sma_75 = float(indicator.sma_75) if indicator.sma_75 else None

    score = 50.0
    reason = None

    # ゴールデンクロス傾向（短期 > 長期）
    if sma_5 > sma_25:
        score = 70.0
        reason = "短期SMAが中期SMAを上回っている"

        # パーフェクトオーダー
        if sma_75 and sma_25 > sma_75:
            score = 90.0
            reason = "パーフェクトオーダー（SMA5 > SMA25 > SMA75）"
    elif sma_5 < sma_25:
        score = 30.0
        reason = "短期SMAが中期SMAを下回っている"

    return score, reason


def score_rsi(indicator: TechnicalIndicator) -> tuple[float, str | None]:
    """RSIのスコアを計算する"""
    if indicator.rsi_14 is None:
        return 50.0, None

    rsi = float(indicator.rsi_14)
    reason = None

    if rsi <= 30:
        score = 80.0
        reason = f"RSI={rsi:.1f}（売られすぎ）"
    elif rsi <= 40:
        score = 65.0
        reason = f"RSI={rsi:.1f}（やや売られすぎ）"
    elif rsi >= 70:
        score = 20.0
        reason = f"RSI={rsi:.1f}（買われすぎ）"
    elif rsi >= 60:
        score = 40.0
        reason = f"RSI={rsi:.1f}（やや買われすぎ）"
    else:
        score = 50.0

    return score, reason


def score_macd(indicator: TechnicalIndicator) -> tuple[float, str | None]:
    """MACDのスコアを計算する"""
    if indicator.macd_line is None or indicator.macd_signal is None:
        return 50.0, None

    macd = float(indicator.macd_line)
    signal = float(indicator.macd_signal)
    histogram = float(indicator.macd_histogram) if indicator.macd_histogram else 0

    reason = None

    if macd > signal:
        score = 70.0
        reason = "MACDがシグナルラインを上回っている"
        if histogram > 0:
            score = 80.0
            reason = "MACDがシグナルラインを上回り、ヒストグラムが正"
    else:
        score = 30.0
        reason = "MACDがシグナルラインを下回っている"

    return score, reason


def score_bollinger(
    indicator: TechnicalIndicator,
    close_price: float,
) -> tuple[float, str | None]:
    """ボリンジャーバンドのスコアを計算する"""
    if indicator.bb_lower_2 is None or indicator.bb_upper_2 is None:
        return 50.0, None

    lower = float(indicator.bb_lower_2)
    upper = float(indicator.bb_upper_2)
    middle = float(indicator.bb_middle) if indicator.bb_middle else (lower + upper) / 2

    reason = None

    if close_price <= lower:
        score = 80.0
        reason = "株価がボリンジャーバンド下限(-2σ)に接触"
    elif close_price <= middle:
        score = 60.0
        reason = "株価がボリンジャーバンド中央より下"
    elif close_price >= upper:
        score = 20.0
        reason = "株価がボリンジャーバンド上限(+2σ)に接触"
    else:
        score = 40.0

    return score, reason


def score_volume(indicator: TechnicalIndicator, current_volume: int) -> tuple[float, str | None]:
    """出来高のスコアを計算する"""
    if indicator.volume_sma_25 is None or indicator.volume_sma_25 == 0:
        return 50.0, None

    ratio = current_volume / indicator.volume_sma_25
    reason = None

    if ratio >= 2.0:
        score = 80.0
        reason = f"出来高が25日平均の{ratio:.1f}倍（急増）"
    elif ratio >= 1.5:
        score = 65.0
        reason = f"出来高が25日平均の{ratio:.1f}倍（増加）"
    elif ratio <= 0.5:
        score = 30.0
        reason = f"出来高が25日平均の{ratio:.1f}倍（低迷）"
    else:
        score = 50.0

    return score, reason


def score_per(fundamental: FundamentalData | None) -> tuple[float, str | None]:
    """PERのスコアを計算する"""
    if not fundamental or fundamental.per is None:
        return 50.0, None

    per = float(fundamental.per)
    reason = None

    if per <= 0:
        score = 20.0
        reason = f"PER={per:.1f}（赤字）"
    elif per <= 10:
        score = 90.0
        reason = f"PER={per:.1f}（割安）"
    elif per <= 15:
        score = 70.0
        reason = f"PER={per:.1f}（適正〜やや割安）"
    elif per <= 25:
        score = 50.0
    elif per <= 40:
        score = 30.0
        reason = f"PER={per:.1f}（やや割高）"
    else:
        score = 15.0
        reason = f"PER={per:.1f}（割高）"

    return score, reason


def score_pbr(fundamental: FundamentalData | None) -> tuple[float, str | None]:
    """PBRのスコアを計算する"""
    if not fundamental or fundamental.pbr is None:
        return 50.0, None

    pbr = float(fundamental.pbr)
    reason = None

    if pbr <= 0:
        score = 20.0
    elif pbr <= 0.5:
        score = 90.0
        reason = f"PBR={pbr:.2f}（大幅割安）"
    elif pbr <= 1.0:
        score = 75.0
        reason = f"PBR={pbr:.2f}（割安）"
    elif pbr <= 2.0:
        score = 50.0
    else:
        score = 25.0
        reason = f"PBR={pbr:.2f}（割高）"

    return score, reason


def score_dividend_yield(fundamental: FundamentalData | None) -> tuple[float, str | None]:
    """配当利回りのスコアを計算する"""
    if not fundamental or fundamental.dividend_yield is None:
        return 50.0, None

    dy = float(fundamental.dividend_yield)
    reason = None

    if dy >= 5.0:
        score = 90.0
        reason = f"配当利回り={dy:.1f}%（高配当）"
    elif dy >= 3.0:
        score = 75.0
        reason = f"配当利回り={dy:.1f}%（魅力的）"
    elif dy >= 2.0:
        score = 55.0
    elif dy > 0:
        score = 40.0
    else:
        score = 30.0

    return score, reason


def score_roe(fundamental: FundamentalData | None) -> tuple[float, str | None]:
    """ROEのスコアを計算する"""
    if not fundamental or fundamental.roe is None:
        return 50.0, None

    roe = float(fundamental.roe)
    reason = None

    if roe >= 20:
        score = 90.0
        reason = f"ROE={roe:.1f}%（高効率）"
    elif roe >= 10:
        score = 70.0
        reason = f"ROE={roe:.1f}%（効率的）"
    elif roe >= 5:
        score = 50.0
    elif roe > 0:
        score = 30.0
    else:
        score = 15.0
        reason = f"ROE={roe:.1f}%（赤字）"

    return score, reason


def calculate_total_score(
    indicator: TechnicalIndicator,
    fundamental: FundamentalData | None,
    close_price: float,
    current_volume: int,
    weights: dict[str, float] | None = None,
) -> ScoreResult:
    """総合スコアを計算する"""
    w = weights or DEFAULT_WEIGHTS

    reasons: list[dict[str, str]] = []

    def _add_reason(category: str, reason: str | None) -> None:
        if reason:
            reasons.append({"category": category, "reason": reason})

    # テクニカルスコア
    sma_score, sma_reason = score_sma_cross(indicator)
    _add_reason("SMA", sma_reason)

    rsi_score, rsi_reason = score_rsi(indicator)
    _add_reason("RSI", rsi_reason)

    macd_score, macd_reason = score_macd(indicator)
    _add_reason("MACD", macd_reason)

    bb_score, bb_reason = score_bollinger(indicator, close_price)
    _add_reason("ボリンジャーバンド", bb_reason)

    vol_score, vol_reason = score_volume(indicator, current_volume)
    _add_reason("出来高", vol_reason)

    technical_score = (
        sma_score * w["sma_cross"]
        + rsi_score * w["rsi"]
        + macd_score * w["macd"]
        + bb_score * w["bollinger"]
        + vol_score * w["volume"]
    ) / (w["sma_cross"] + w["rsi"] + w["macd"] + w["bollinger"] + w["volume"])

    # ファンダメンタルスコア
    per_score, per_reason = score_per(fundamental)
    _add_reason("PER", per_reason)

    pbr_score, pbr_reason = score_pbr(fundamental)
    _add_reason("PBR", pbr_reason)

    dy_score, dy_reason = score_dividend_yield(fundamental)
    _add_reason("配当利回り", dy_reason)

    roe_score, roe_reason = score_roe(fundamental)
    _add_reason("ROE", roe_reason)

    fundamental_score = (
        per_score * w["per"]
        + pbr_score * w["pbr"]
        + dy_score * w["dividend_yield"]
        + roe_score * w["roe"]
    ) / (w["per"] + w["pbr"] + w["dividend_yield"] + w["roe"])

    # 総合スコア
    tech_weight = w["sma_cross"] + w["rsi"] + w["macd"] + w["bollinger"] + w["volume"]
    fund_weight = w["per"] + w["pbr"] + w["dividend_yield"] + w["roe"]
    total_score = (
        technical_score * tech_weight + fundamental_score * fund_weight
    ) / (tech_weight + fund_weight)

    return ScoreResult(
        total_score=round(total_score, 2),
        technical_score=round(technical_score, 2),
        fundamental_score=round(fundamental_score, 2),
        reasons=reasons,
    )
