"""銘柄マスタ収集モジュール

東証上場銘柄のマスタデータを管理する。
初期データは主要銘柄を手動登録し、週次で更新を行う。
"""

import logging

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stock import Stock

logger = logging.getLogger(__name__)

# 初期登録する主要銘柄リスト（東証プライムの代表銘柄）
INITIAL_STOCKS: list[dict[str, str]] = [
    {"code": "7203.T", "name": "トヨタ自動車", "sector": "輸送用機器", "market": "プライム"},
    {"code": "6758.T", "name": "ソニーグループ", "sector": "電気機器", "market": "プライム"},
    {"code": "9984.T", "name": "ソフトバンクグループ", "sector": "情報・通信業", "market": "プライム"},
    {"code": "6861.T", "name": "キーエンス", "sector": "電気機器", "market": "プライム"},
    {"code": "8306.T", "name": "三菱UFJフィナンシャル・グループ", "sector": "銀行業", "market": "プライム"},
    {"code": "9432.T", "name": "日本電信電話", "sector": "情報・通信業", "market": "プライム"},
    {"code": "6501.T", "name": "日立製作所", "sector": "電気機器", "market": "プライム"},
    {"code": "7741.T", "name": "HOYA", "sector": "精密機器", "market": "プライム"},
    {"code": "6098.T", "name": "リクルートホールディングス", "sector": "サービス業", "market": "プライム"},
    {"code": "4063.T", "name": "信越化学工業", "sector": "化学", "market": "プライム"},
    {"code": "8035.T", "name": "東京エレクトロン", "sector": "電気機器", "market": "プライム"},
    {"code": "6902.T", "name": "デンソー", "sector": "輸送用機器", "market": "プライム"},
    {"code": "4519.T", "name": "中外製薬", "sector": "医薬品", "market": "プライム"},
    {"code": "6594.T", "name": "日本電産", "sector": "電気機器", "market": "プライム"},
    {"code": "7974.T", "name": "任天堂", "sector": "その他製品", "market": "プライム"},
    {"code": "6367.T", "name": "ダイキン工業", "sector": "機械", "market": "プライム"},
    {"code": "9433.T", "name": "KDDI", "sector": "情報・通信業", "market": "プライム"},
    {"code": "4568.T", "name": "第一三共", "sector": "医薬品", "market": "プライム"},
    {"code": "8058.T", "name": "三菱商事", "sector": "卸売業", "market": "プライム"},
    {"code": "8001.T", "name": "伊藤忠商事", "sector": "卸売業", "market": "プライム"},
    {"code": "2914.T", "name": "日本たばこ産業", "sector": "食料品", "market": "プライム"},
    {"code": "6920.T", "name": "レーザーテック", "sector": "電気機器", "market": "プライム"},
    {"code": "6723.T", "name": "ルネサスエレクトロニクス", "sector": "電気機器", "market": "プライム"},
    {"code": "7267.T", "name": "本田技研工業", "sector": "輸送用機器", "market": "プライム"},
    {"code": "4661.T", "name": "オリエンタルランド", "sector": "サービス業", "market": "プライム"},
    {"code": "4502.T", "name": "武田薬品工業", "sector": "医薬品", "market": "プライム"},
    {"code": "6981.T", "name": "村田製作所", "sector": "電気機器", "market": "プライム"},
    {"code": "3382.T", "name": "セブン&アイ・ホールディングス", "sector": "小売業", "market": "プライム"},
    {"code": "9983.T", "name": "ファーストリテイリング", "sector": "小売業", "market": "プライム"},
    {"code": "6857.T", "name": "アドバンテスト", "sector": "電気機器", "market": "プライム"},
]


async def seed_initial_stocks(db: AsyncSession) -> int:
    """初期銘柄データを登録する"""
    logger.info("初期銘柄データ登録開始")

    count = 0
    for stock_data in INITIAL_STOCKS:
        stmt = pg_insert(Stock).values(
            code=stock_data["code"],
            name=stock_data["name"],
            sector=stock_data["sector"],
            market=stock_data["market"],
            is_active=True,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["code"],
            set_={
                "name": stmt.excluded.name,
                "sector": stmt.excluded.sector,
                "market": stmt.excluded.market,
            },
        )
        await db.execute(stmt)
        count += 1

    await db.commit()
    logger.info(f"初期銘柄データ登録完了: {count}件")
    return count


async def get_active_stock_count(db: AsyncSession) -> int:
    """アクティブな銘柄数を取得する"""
    result = await db.execute(
        select(Stock).where(Stock.is_active.is_(True))
    )
    return len(result.scalars().all())
