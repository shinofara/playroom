"""スクリーニングプリセットモデル"""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ScreeningPreset(Base):
    """スクリーニングプリセット"""

    __tablename__ = "screening_presets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="プリセット名")
    conditions: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, comment="フィルタ条件")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<ScreeningPreset(name={self.name})>"
