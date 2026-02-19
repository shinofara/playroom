"""ポートフォリオモデル"""

from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Portfolio(Base, TimestampMixin):
    """ポートフォリオ"""

    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="ポートフォリオ名")
    total_investment: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), default=0, nullable=False, comment="総投資額"
    )

    # リレーション
    user: Mapped["User"] = relationship(back_populates="portfolios")  # type: ignore[name-defined]
    holdings: Mapped[list["PortfolioHolding"]] = relationship(back_populates="portfolio", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Portfolio(name={self.name})>"


class PortfolioHolding(Base, TimestampMixin):
    """保有銘柄"""

    __tablename__ = "portfolio_holdings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, comment="保有数量")
    avg_purchase_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, comment="平均取得単価"
    )

    # リレーション
    portfolio: Mapped["Portfolio"] = relationship(back_populates="holdings")
    stock: Mapped["Stock"] = relationship()  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<PortfolioHolding(stock_id={self.stock_id}, quantity={self.quantity})>"
