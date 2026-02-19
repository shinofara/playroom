"""テクニカル指標モデル"""

from datetime import date
from decimal import Decimal

from sqlalchemy import BigInteger, Date, ForeignKey, Index, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TechnicalIndicator(Base):
    """テクニカル指標"""

    __tablename__ = "technical_indicators"
    __table_args__ = (
        UniqueConstraint("stock_id", "date", name="uq_technical_indicators_stock_date"),
        Index("ix_technical_indicators_stock_date_desc", "stock_id", "date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, comment="日付")

    # 移動平均線
    sma_5: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="5日SMA")
    sma_25: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="25日SMA")
    sma_75: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="75日SMA")
    sma_200: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="200日SMA")
    ema_12: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="12日EMA")
    ema_26: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="26日EMA")

    # RSI
    rsi_14: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True, comment="14日RSI")

    # MACD
    macd_line: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True, comment="MACDライン")
    macd_signal: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True, comment="シグナルライン")
    macd_histogram: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True, comment="ヒストグラム")

    # ボリンジャーバンド
    bb_upper_2: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="ボリンジャー上限(2σ)")
    bb_middle: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="ボリンジャー中央")
    bb_lower_2: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="ボリンジャー下限(2σ)")

    # 出来高
    volume_sma_25: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="出来高25日SMA")

    # リレーション
    stock: Mapped["Stock"] = relationship(back_populates="technical_indicators")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<TechnicalIndicator(stock_id={self.stock_id}, date={self.date})>"
