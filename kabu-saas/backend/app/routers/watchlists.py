"""ウォッチリストAPIルーター"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.watchlist import Watchlist, WatchlistItem
from app.schemas.watchlist import (
    WatchlistCreate,
    WatchlistItemCreate,
    WatchlistItemResponse,
    WatchlistItemUpdate,
    WatchlistResponse,
    WatchlistUpdate,
)

router = APIRouter()


@router.get("", response_model=list[WatchlistResponse])
async def list_watchlists(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[WatchlistResponse]:
    """ウォッチリスト一覧取得"""
    result = await db.execute(
        select(Watchlist).where(Watchlist.user_id == current_user.id)
    )
    return [WatchlistResponse.model_validate(w) for w in result.scalars().all()]


@router.post("", response_model=WatchlistResponse, status_code=status.HTTP_201_CREATED)
async def create_watchlist(
    request: WatchlistCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> WatchlistResponse:
    """ウォッチリスト作成"""
    watchlist = Watchlist(user_id=current_user.id, name=request.name)
    db.add(watchlist)
    await db.flush()
    return WatchlistResponse.model_validate(watchlist)


@router.put("/{watchlist_id}", response_model=WatchlistResponse)
async def update_watchlist(
    watchlist_id: int,
    request: WatchlistUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> WatchlistResponse:
    """ウォッチリスト更新"""
    result = await db.execute(
        select(Watchlist).where(Watchlist.id == watchlist_id, Watchlist.user_id == current_user.id)
    )
    watchlist = result.scalar_one_or_none()
    if not watchlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ウォッチリストが見つかりません")

    if request.name is not None:
        watchlist.name = request.name
    return WatchlistResponse.model_validate(watchlist)


@router.delete("/{watchlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_watchlist(
    watchlist_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    """ウォッチリスト削除"""
    result = await db.execute(
        select(Watchlist).where(Watchlist.id == watchlist_id, Watchlist.user_id == current_user.id)
    )
    watchlist = result.scalar_one_or_none()
    if not watchlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ウォッチリストが見つかりません")
    await db.delete(watchlist)


@router.post("/{watchlist_id}/items", response_model=WatchlistItemResponse, status_code=status.HTTP_201_CREATED)
async def add_watchlist_item(
    watchlist_id: int,
    request: WatchlistItemCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> WatchlistItemResponse:
    """ウォッチリストに銘柄追加"""
    result = await db.execute(
        select(Watchlist).where(Watchlist.id == watchlist_id, Watchlist.user_id == current_user.id)
    )
    watchlist = result.scalar_one_or_none()
    if not watchlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ウォッチリストが見つかりません")

    item = WatchlistItem(
        watchlist_id=watchlist_id,
        stock_id=request.stock_id,
        memo=request.memo,
        alert_enabled=request.alert_enabled or False,
    )
    db.add(item)
    await db.flush()
    return WatchlistItemResponse.model_validate(item)


@router.put("/{watchlist_id}/items/{item_id}", response_model=WatchlistItemResponse)
async def update_watchlist_item(
    watchlist_id: int,
    item_id: int,
    request: WatchlistItemUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> WatchlistItemResponse:
    """ウォッチリスト項目更新"""
    result = await db.execute(
        select(Watchlist).where(Watchlist.id == watchlist_id, Watchlist.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ウォッチリストが見つかりません")

    item_result = await db.execute(
        select(WatchlistItem).where(WatchlistItem.id == item_id, WatchlistItem.watchlist_id == watchlist_id)
    )
    item = item_result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="項目が見つかりません")

    if request.memo is not None:
        item.memo = request.memo
    if request.alert_enabled is not None:
        item.alert_enabled = request.alert_enabled
    return WatchlistItemResponse.model_validate(item)


@router.delete("/{watchlist_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_watchlist_item(
    watchlist_id: int,
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    """ウォッチリストから銘柄削除"""
    result = await db.execute(
        select(Watchlist).where(Watchlist.id == watchlist_id, Watchlist.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ウォッチリストが見つかりません")

    item_result = await db.execute(
        select(WatchlistItem).where(WatchlistItem.id == item_id, WatchlistItem.watchlist_id == watchlist_id)
    )
    item = item_result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="項目が見つかりません")
    await db.delete(item)
