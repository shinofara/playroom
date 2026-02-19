"""認証スキーマ"""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """ユーザー登録リクエスト"""

    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    """ログインリクエスト"""

    email: str
    password: str


class TokenResponse(BaseModel):
    """トークンレスポンス"""

    access_token: str
    refresh_token: str
    token_type: str


class UserResponse(BaseModel):
    """ユーザーレスポンス"""

    id: int
    username: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}
