"""ファンダメンタルデータモデル"""

from datetime import date
from decimal import Decimal

from sqlalchemy import BigInteger, Date, ForeignKey, Index, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class FundamentalData(Base):
    """ファンダメンタルデータ"""

    __tablename__ = "fundamental_data"
    __table_args__ = (
        UniqueConstraint("stock_id", "date", name="uq_fundamental_data_stock_date"),
        Index("ix_fundamental_data_stock_date_desc", "stock_id", "date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, comment="取得日")
    per: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="PER")
    pbr: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="PBR")
    dividend_yield: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True, comment="配当利回り(%)")
    roe: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True, comment="ROE(%)")
    eps: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="EPS")
    bps: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="BPS")
    market_cap: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="時価総額")
    revenue: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="売上高")
    operating_income: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="営業利益")

    # リレーション
    stock: Mapped["Stock"] = relationship(back_populates="fundamentals")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<FundamentalData(stock_id={self.stock_id}, date={self.date})>"
