"""銘柄・株価モデル"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, Date, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Stock(Base, TimestampMixin):
    """銘柄マスタ"""

    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, comment="銘柄コード（例: 7203.T）")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="銘柄名")
    sector: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="業種")
    market: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="市場区分")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="上場中フラグ")

    # リレーション
    prices: Mapped[list["StockPrice"]] = relationship(back_populates="stock", lazy="selectin")
    fundamentals: Mapped[list[FundamentalData]] = relationship(back_populates="stock", lazy="selectin")
    technical_indicators: Mapped[list[TechnicalIndicator]] = relationship(back_populates="stock", lazy="selectin")
    signals: Mapped[list[Signal]] = relationship(back_populates="stock", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Stock(code={self.code}, name={self.name})>"


class StockPrice(Base):
    """株価日足データ"""

    __tablename__ = "stock_prices"
    __table_args__ = (
        UniqueConstraint("stock_id", "date", name="uq_stock_prices_stock_date"),
        Index("ix_stock_prices_stock_date_desc", "stock_id", "date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, comment="日付")
    open: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="始値")
    high: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="高値")
    low: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="安値")
    close: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="終値")
    volume: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="出来高")
    adjusted_close: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="調整後終値")

    # リレーション
    stock: Mapped["Stock"] = relationship(back_populates="prices")

    def __repr__(self) -> str:
        return f"<StockPrice(stock_id={self.stock_id}, date={self.date}, close={self.close})>"
