"""ウォッチリストモデル"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Watchlist(Base):
    """ウォッチリスト"""

    __tablename__ = "watchlists"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="リスト名")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # リレーション
    user: Mapped["User"] = relationship(back_populates="watchlists")  # type: ignore[name-defined]
    items: Mapped[list["WatchlistItem"]] = relationship(back_populates="watchlist", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Watchlist(name={self.name})>"


class WatchlistItem(Base):
    """ウォッチリスト項目"""

    __tablename__ = "watchlist_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    watchlist_id: Mapped[int] = mapped_column(ForeignKey("watchlists.id", ondelete="CASCADE"), nullable=False)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    memo: Mapped[str | None] = mapped_column(Text, nullable=True, comment="メモ")
    alert_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="アラート有効フラグ")
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # リレーション
    watchlist: Mapped["Watchlist"] = relationship(back_populates="items")
    stock: Mapped["Stock"] = relationship()  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<WatchlistItem(watchlist_id={self.watchlist_id}, stock_id={self.stock_id})>"
