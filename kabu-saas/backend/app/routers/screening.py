"""スクリーニングAPIルーター"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.screening import ScreeningPreset
from app.models.user import User
from app.schemas.screening import ScreeningPresetCreate, ScreeningPresetResponse, ScreeningRequest, ScreeningResultResponse

router = APIRouter()


@router.post("", response_model=ScreeningResultResponse)
async def run_screening(
    request: ScreeningRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ScreeningResultResponse:
    """スクリーニング実行"""
    # TODO: Task #5 で実装
    return ScreeningResultResponse(items=[], total=0)


@router.get("/presets", response_model=list[ScreeningPresetResponse])
async def list_presets(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[ScreeningPresetResponse]:
    """プリセット一覧取得"""
    result = await db.execute(
        select(ScreeningPreset).where(ScreeningPreset.user_id == current_user.id)
    )
    return [ScreeningPresetResponse.model_validate(p) for p in result.scalars().all()]


@router.post("/presets", response_model=ScreeningPresetResponse, status_code=status.HTTP_201_CREATED)
async def create_preset(
    request: ScreeningPresetCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ScreeningPresetResponse:
    """プリセット保存"""
    preset = ScreeningPreset(
        user_id=current_user.id,
        name=request.name,
        conditions=request.conditions,
    )
    db.add(preset)
    await db.flush()
    return ScreeningPresetResponse.model_validate(preset)


@router.delete("/presets/{preset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_preset(
    preset_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    """プリセット削除"""
    result = await db.execute(
        select(ScreeningPreset).where(
            ScreeningPreset.id == preset_id,
            ScreeningPreset.user_id == current_user.id,
        )
    )
    preset = result.scalar_one_or_none()
    if not preset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="プリセットが見つかりません")
    await db.delete(preset)
