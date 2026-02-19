"""設定スキーマ"""

from typing import Any

from pydantic import BaseModel


class SettingsResponse(BaseModel):
    """設定レスポンス"""

    settings: dict[str, Any]


class SettingsUpdate(BaseModel):
    """設定更新リクエスト"""

    settings: dict[str, Any]
