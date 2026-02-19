"""データ収集ログモデル"""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DataCollectionLog(Base):
    """データ収集ジョブ実行ログ"""

    __tablename__ = "data_collection_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    job_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="ジョブ名")
    status: Mapped[str] = mapped_column(
        String(10), nullable=False, comment="running/success/failed/partial"
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    total_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="処理対象件数")
    success_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="成功件数")
    error_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="エラー件数")
    error_details: Mapped[list[Any] | None] = mapped_column(JSONB, nullable=True, comment="エラー詳細")

    def __repr__(self) -> str:
        return f"<DataCollectionLog(job={self.job_name}, status={self.status})>"
