"""シグナルモデル"""

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, DateTime, ForeignKey, Index, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Signal(Base):
    """買い/売りシグナル"""

    __tablename__ = "signals"
    __table_args__ = (
        Index("ix_signals_date_type_score", "date", "signal_type", "score"),
        Index("ix_signals_stock_date_desc", "stock_id", "date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, comment="シグナル発生日")
    signal_type: Mapped[str] = mapped_column(String(10), nullable=False, comment="buy / sell")
    score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, comment="総合スコア(0-100)")
    technical_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True, comment="テクニカルスコア")
    fundamental_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True, comment="ファンダメンタルスコア")
    reasons: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True, comment="シグナル理由の詳細")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # リレーション
    stock: Mapped["Stock"] = relationship(back_populates="signals")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<Signal(stock_id={self.stock_id}, type={self.signal_type}, score={self.score})>"
