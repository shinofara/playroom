"""ユーザー・設定モデル"""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    """ユーザー"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="ユーザー名")
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, comment="メールアドレス")
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False, comment="パスワードハッシュ")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # リレーション
    portfolios: Mapped[list["Portfolio"]] = relationship(back_populates="user", lazy="selectin")  # type: ignore[name-defined]
    watchlists: Mapped[list["Watchlist"]] = relationship(back_populates="user", lazy="selectin")  # type: ignore[name-defined]
    settings: Mapped[list["UserSetting"]] = relationship(back_populates="user", lazy="selectin")

    def __repr__(self) -> str:
        return f"<User(username={self.username})>"


class UserSetting(Base):
    """ユーザー設定"""

    __tablename__ = "user_settings"
    __table_args__ = (
        UniqueConstraint("user_id", "setting_key", name="uq_user_settings_user_key"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    setting_key: Mapped[str] = mapped_column(String(50), nullable=False, comment="設定キー")
    setting_value: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, comment="設定値")

    # リレーション
    user: Mapped["User"] = relationship(back_populates="settings")

    def __repr__(self) -> str:
        return f"<UserSetting(user_id={self.user_id}, key={self.setting_key})>"
