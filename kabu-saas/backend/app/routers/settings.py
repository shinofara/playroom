"""設定APIルーター"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User, UserSetting
from app.schemas.settings import SettingsResponse, SettingsUpdate

router = APIRouter()

# デフォルト設定値
DEFAULT_SETTINGS: dict[str, dict[str, Any]] = {
    "scoring_weights": {
        "value": {
            "sma_cross": 15,
            "rsi": 10,
            "macd": 15,
            "bollinger": 10,
            "volume": 10,
            "per": 10,
            "pbr": 10,
            "dividend_yield": 10,
            "roe": 10,
        }
    },
    "trade_defaults": {
        "value": {
            "take_profit_rates": [10, 20, 30],
            "stop_loss_rates": [5, 10],
        }
    },
}


@router.get("", response_model=SettingsResponse)
async def get_settings(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> SettingsResponse:
    """ユーザー設定取得"""
    result = await db.execute(
        select(UserSetting).where(UserSetting.user_id == current_user.id)
    )
    user_settings = {s.setting_key: s.setting_value for s in result.scalars().all()}

    # デフォルト値とマージ
    merged = {**DEFAULT_SETTINGS, **user_settings}
    return SettingsResponse(settings=merged)


@router.put("", response_model=SettingsResponse)
async def update_settings(
    request: SettingsUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> SettingsResponse:
    """ユーザー設定更新"""
    for key, value in request.settings.items():
        result = await db.execute(
            select(UserSetting).where(
                UserSetting.user_id == current_user.id,
                UserSetting.setting_key == key,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.setting_value = value
        else:
            db.add(UserSetting(
                user_id=current_user.id,
                setting_key=key,
                setting_value=value,
            ))

    await db.flush()

    # 更新後の設定を返却
    updated_result = await db.execute(
        select(UserSetting).where(UserSetting.user_id == current_user.id)
    )
    user_settings = {s.setting_key: s.setting_value for s in updated_result.scalars().all()}
    merged = {**DEFAULT_SETTINGS, **user_settings}
    return SettingsResponse(settings=merged)
