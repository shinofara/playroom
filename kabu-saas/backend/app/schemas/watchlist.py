"""ウォッチリストスキーマ"""

from datetime import datetime

from pydantic import BaseModel


class WatchlistResponse(BaseModel):
    """ウォッチリストレスポンス"""

    id: int
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}


class WatchlistCreate(BaseModel):
    """ウォッチリスト作成リクエスト"""

    name: str


class WatchlistUpdate(BaseModel):
    """ウォッチリスト更新リクエスト"""

    name: str | None = None


class WatchlistItemResponse(BaseModel):
    """ウォッチリスト項目レスポンス"""

    id: int
    watchlist_id: int
    stock_id: int
    memo: str | None = None
    alert_enabled: bool
    added_at: datetime

    model_config = {"from_attributes": True}


class WatchlistItemCreate(BaseModel):
    """ウォッチリスト項目追加リクエスト"""

    stock_id: int
    memo: str | None = None
    alert_enabled: bool | None = False


class WatchlistItemUpdate(BaseModel):
    """ウォッチリスト項目更新リクエスト"""

    memo: str | None = None
    alert_enabled: bool | None = None
