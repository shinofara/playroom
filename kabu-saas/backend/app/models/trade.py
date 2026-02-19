"""取引・売買プランモデル"""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Index, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Trade(Base):
    """取引履歴"""

    __tablename__ = "trades"
    __table_args__ = (
        Index("ix_trades_stock_date_desc", "stock_id", "transaction_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    trade_type: Mapped[str] = mapped_column(String(4), nullable=False, comment="buy / sell")
    quantity: Mapped[int] = mapped_column(nullable=False, comment="数量")
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="約定単価")
    commission: Mapped[Decimal] = mapped_column(Numeric(8, 2), default=0, nullable=False, comment="手数料")
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False, comment="約定日")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True, comment="メモ")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # リレーション
    portfolio: Mapped["Portfolio"] = relationship()  # type: ignore[name-defined]
    stock: Mapped["Stock"] = relationship()  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<Trade(stock_id={self.stock_id}, type={self.trade_type}, price={self.price})>"


class TradePlan(Base):
    """売買プラン"""

    __tablename__ = "trade_plans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True, comment="ユーザー紐付け（エージェント生成時はNULL）")
    signal_id: Mapped[int | None] = mapped_column(ForeignKey("signals.id", ondelete="SET NULL"), nullable=True, comment="元シグナルID")
    plan_type: Mapped[str] = mapped_column(String(4), nullable=False, comment="buy / sell")
    entry_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="エントリー価格")
    target_price_1: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="利確目標1")
    target_price_2: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="利確目標2")
    target_price_3: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="利確目標3")
    stop_loss_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="損切りライン")
    position_size: Mapped[int | None] = mapped_column(nullable=True, comment="推奨ポジションサイズ(株数)")
    risk_reward_ratio: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True, comment="リスクリワード比")
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False, comment="active/executed/cancelled")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True, comment="メモ")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # リレーション
    stock: Mapped["Stock"] = relationship()  # type: ignore[name-defined]
    user: Mapped["User | None"] = relationship()  # type: ignore[name-defined]
    signal: Mapped["Signal | None"] = relationship()  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<TradePlan(stock_id={self.stock_id}, type={self.plan_type}, status={self.status})>"
