# システムアーキテクチャ設計書: Kabu SaaS

## 1. 全体構成図

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Docker Compose                              │
│                                                                     │
│  ┌──────────────────┐    ┌──────────────────┐   ┌───────────────┐  │
│  │   Frontend        │    │   Backend         │   │  PostgreSQL   │  │
│  │   (Next.js 14)    │───▶│   (FastAPI)       │──▶│  16           │  │
│  │   Port: 3000      │    │   Port: 8000      │   │  Port: 5432   │  │
│  │                    │    │                    │   │               │  │
│  │  ┌──────────────┐ │    │  ┌──────────────┐ │   │  ┌─────────┐ │  │
│  │  │ App Router   │ │    │  │ REST API     │ │   │  │ stocks  │ │  │
│  │  │ (RSC + CSR)  │ │    │  │ /api/*       │ │   │  │ prices  │ │  │
│  │  ├──────────────┤ │    │  ├──────────────┤ │   │  │ signals │ │  │
│  │  │ Recharts     │ │    │  │ SQLAlchemy   │ │   │  │ ...     │ │  │
│  │  │ shadcn/ui    │ │    │  │ 2.0 (Async)  │ │   │  └─────────┘ │  │
│  │  │ Tailwind CSS │ │    │  ├──────────────┤ │   │               │  │
│  │  └──────────────┘ │    │  │ APScheduler  │ │   └───────────────┘  │
│  │                    │    │  │ (定時タスク)  │ │                      │
│  └──────────────────┘    │  ├──────────────┤ │                      │
│                           │  │ Analysis     │ │                      │
│                           │  │ Engine       │ │                      │
│                           │  │ (pandas/ta)  │ │                      │
│                           │  └──────────────┘ │                      │
│                           │                    │                      │
│                           │  ┌──────────────┐ │   ┌───────────────┐  │
│                           │  │ Data          │ │   │  外部API       │  │
│                           │  │ Collector    │─│──▶│  (yfinance)   │  │
│                           │  └──────────────┘ │   └───────────────┘  │
│                           └──────────────────┘                      │
└─────────────────────────────────────────────────────────────────────┘
```

## 2. 技術スタック詳細

### 2.1 Backend

| 項目 | 技術 | バージョン | 用途 |
|------|------|------------|------|
| 言語 | Python | 3.12 | サーバーサイドロジック |
| フレームワーク | FastAPI | 0.115+ | REST API、自動ドキュメント生成 |
| ORM | SQLAlchemy | 2.0 | 非同期DB操作（asyncio対応） |
| マイグレーション | Alembic | 1.13+ | DBスキーマバージョン管理 |
| データ収集 | yfinance | 0.2+ | 日本株データ取得 |
| テクニカル分析 | pandas-ta | 0.3+ | テクニカル指標計算 |
| データ処理 | pandas | 2.2+ | データフレーム操作 |
| スケジューラ | APScheduler | 3.10+ | 定時データ収集・分析バッチ |
| 認証 | python-jose + passlib | - | JWT認証・パスワードハッシュ |
| バリデーション | Pydantic | 2.0+ | リクエスト/レスポンスモデル |
| テスト | pytest + pytest-asyncio | - | ユニットテスト・APIテスト |
| Linter/Formatter | ruff | - | コード品質管理 |
| 型チェック | mypy | - | 静的型解析 |
| DBドライバ | asyncpg | - | PostgreSQL非同期ドライバ |

### 2.2 Frontend

| 項目 | 技術 | バージョン | 用途 |
|------|------|------------|------|
| フレームワーク | Next.js | 14 (App Router) | SSR/CSRハイブリッドレンダリング |
| 言語 | TypeScript | 5.x | 型安全なフロントエンド開発 |
| スタイリング | Tailwind CSS | 3.x | ユーティリティファーストCSS |
| UIコンポーネント | shadcn/ui | - | 再利用可能なUIコンポーネント |
| チャート | Recharts | 2.x | 株価チャート・パフォーマンスグラフ |
| 軽量チャート | Lightweight Charts | 4.x | ローソク足チャート（TradingView風） |
| 状態管理 | Zustand | 5.x | グローバルステート管理 |
| HTTP Client | ky | 1.x | API通信 |
| フォーム | React Hook Form + Zod | - | フォームバリデーション |
| Linter | ESLint + Prettier | - | コード品質管理 |

### 2.3 Database

| 項目 | 技術 | 用途 |
|------|------|------|
| RDBMS | PostgreSQL 16 | メインデータストア |
| JSONB | PostgreSQL JSONB | スクリーニング条件・シグナル理由等の柔軟なデータ格納 |

### 2.4 インフラ

| 項目 | 技術 | 用途 |
|------|------|------|
| コンテナ | Docker + Docker Compose | 開発・実行環境の統一 |
| リバースプロキシ | - | 当面は不要（ローカル環境） |

## 3. ディレクトリ構成

```
kabu-saas/
├── docs/                           # ドキュメント
│   ├── product-requirements.md     # プロダクト要件書
│   ├── architecture.md             # アーキテクチャ設計書（本ファイル）
│   └── database-schema.sql         # DBスキーマ定義
│
├── backend/                        # Python FastAPI アプリケーション
│   ├── pyproject.toml              # Python プロジェクト設定（uv/poetry）
│   ├── alembic.ini                 # Alembic設定
│   ├── alembic/                    # DBマイグレーション
│   │   ├── env.py
│   │   └── versions/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPIアプリケーションエントリポイント
│   │   ├── config.py               # アプリケーション設定
│   │   ├── dependencies.py         # 共通依存性（DB session等）
│   │   │
│   │   ├── models/                 # SQLAlchemy モデル
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Baseモデル定義
│   │   │   ├── stock.py            # stocks, stock_prices
│   │   │   ├── technical.py        # technical_indicators
│   │   │   ├── fundamental.py      # fundamental_data
│   │   │   ├── signal.py           # signals
│   │   │   ├── portfolio.py        # portfolios, portfolio_holdings
│   │   │   ├── trade.py            # trades, trade_plans
│   │   │   ├── watchlist.py        # watchlists, watchlist_items
│   │   │   ├── screening.py        # screening_presets
│   │   │   └── user.py             # users, user_settings
│   │   │
│   │   ├── schemas/                # Pydantic スキーマ（リクエスト/レスポンス）
│   │   │   ├── __init__.py
│   │   │   ├── stock.py
│   │   │   ├── signal.py
│   │   │   ├── portfolio.py
│   │   │   ├── trade.py
│   │   │   ├── watchlist.py
│   │   │   ├── screening.py
│   │   │   ├── dashboard.py
│   │   │   ├── auth.py
│   │   │   └── settings.py
│   │   │
│   │   ├── routers/                # APIルーター
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # /api/auth/*
│   │   │   ├── stocks.py           # /api/stocks/*
│   │   │   ├── signals.py          # /api/signals/*
│   │   │   ├── screening.py        # /api/screening
│   │   │   ├── portfolio.py        # /api/portfolio/*
│   │   │   ├── watchlists.py       # /api/watchlists/*
│   │   │   ├── dashboard.py        # /api/dashboard/*
│   │   │   ├── data.py             # /api/data/*
│   │   │   └── settings.py         # /api/settings
│   │   │
│   │   ├── services/               # ビジネスロジック
│   │   │   ├── __init__.py
│   │   │   ├── stock_service.py
│   │   │   ├── signal_service.py
│   │   │   ├── portfolio_service.py
│   │   │   ├── screening_service.py
│   │   │   ├── watchlist_service.py
│   │   │   └── dashboard_service.py
│   │   │
│   │   ├── collectors/             # データ収集モジュール
│   │   │   ├── __init__.py
│   │   │   ├── price_collector.py  # 株価データ収集
│   │   │   ├── fundamental_collector.py  # ファンダメンタルデータ収集
│   │   │   └── master_collector.py # 銘柄マスタ収集
│   │   │
│   │   ├── analysis/               # 分析エンジン
│   │   │   ├── __init__.py
│   │   │   ├── technical.py        # テクニカル指標計算
│   │   │   ├── scoring.py          # スコアリングモデル
│   │   │   ├── signal_detector.py  # シグナル検出
│   │   │   └── trade_planner.py    # 売買プラン生成
│   │   │
│   │   └── scheduler/              # 定時タスク
│   │       ├── __init__.py
│   │       └── jobs.py             # スケジュールジョブ定義
│   │
│   └── tests/                      # テストコード
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_collectors/
│       ├── test_analysis/
│       ├── test_services/
│       └── test_routers/
│
├── frontend/                       # Next.js アプリケーション
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   │
│   ├── src/
│   │   ├── app/                    # App Router ページ
│   │   │   ├── layout.tsx          # ルートレイアウト
│   │   │   ├── page.tsx            # ダッシュボード（/）
│   │   │   ├── stocks/
│   │   │   │   └── [code]/
│   │   │   │       ├── page.tsx    # 銘柄詳細
│   │   │   │       └── plan/
│   │   │   │           └── page.tsx # 売買プラン
│   │   │   ├── screening/
│   │   │   │   └── page.tsx        # スクリーニング
│   │   │   ├── portfolio/
│   │   │   │   ├── page.tsx        # ポートフォリオ
│   │   │   │   └── history/
│   │   │   │       └── page.tsx    # 取引履歴
│   │   │   ├── watchlist/
│   │   │   │   └── page.tsx        # ウォッチリスト
│   │   │   └── settings/
│   │   │       └── page.tsx        # 設定
│   │   │
│   │   ├── components/             # UIコンポーネント
│   │   │   ├── ui/                 # shadcn/ui コンポーネント
│   │   │   ├── layout/             # レイアウトコンポーネント
│   │   │   │   ├── sidebar.tsx
│   │   │   │   ├── header.tsx
│   │   │   │   └── footer.tsx
│   │   │   ├── charts/             # チャートコンポーネント
│   │   │   │   ├── candlestick-chart.tsx
│   │   │   │   ├── line-chart.tsx
│   │   │   │   ├── volume-chart.tsx
│   │   │   │   └── donut-chart.tsx
│   │   │   ├── dashboard/          # ダッシュボード用
│   │   │   ├── stocks/             # 銘柄関連
│   │   │   ├── portfolio/          # ポートフォリオ関連
│   │   │   └── screening/          # スクリーニング関連
│   │   │
│   │   ├── lib/                    # ユーティリティ
│   │   │   ├── api.ts              # APIクライアント
│   │   │   └── utils.ts            # 共通ユーティリティ
│   │   │
│   │   ├── hooks/                  # カスタムフック
│   │   │   ├── use-stocks.ts
│   │   │   ├── use-portfolio.ts
│   │   │   └── use-signals.ts
│   │   │
│   │   ├── stores/                 # Zustand ストア
│   │   │   └── app-store.ts
│   │   │
│   │   └── types/                  # TypeScript 型定義
│   │       ├── stock.ts
│   │       ├── signal.ts
│   │       ├── portfolio.ts
│   │       └── api.ts
│   │
│   └── public/                     # 静的ファイル
│
├── docker-compose.yml              # Docker Compose 定義
├── Dockerfile.backend              # Backend用 Dockerfile
├── Dockerfile.frontend             # Frontend用 Dockerfile
└── .env.example                    # 環境変数テンプレート
```

## 4. API設計（RESTful APIエンドポイント一覧）

### 4.1 認証 API

| メソッド | エンドポイント | 説明 | 認証 |
|----------|----------------|------|------|
| POST | `/api/auth/register` | ユーザー登録 | 不要 |
| POST | `/api/auth/login` | ログイン（JWT発行） | 不要 |
| POST | `/api/auth/refresh` | トークンリフレッシュ | 必要 |
| GET | `/api/auth/me` | 現在のユーザー情報取得 | 必要 |

### 4.2 株価・銘柄 API

| メソッド | エンドポイント | 説明 | クエリパラメータ |
|----------|----------------|------|------------------|
| GET | `/api/stocks` | 銘柄一覧取得 | `market`, `sector`, `search`, `page`, `per_page` |
| GET | `/api/stocks/{code}` | 銘柄詳細取得 | - |
| GET | `/api/stocks/{code}/prices` | 株価履歴取得 | `from_date`, `to_date`, `interval` |
| GET | `/api/stocks/{code}/fundamentals` | ファンダメンタルデータ取得 | `from_date`, `to_date` |
| GET | `/api/stocks/{code}/technicals` | テクニカル指標取得 | `from_date`, `to_date` |
| GET | `/api/stocks/{code}/signals` | シグナル履歴取得 | `signal_type`, `from_date`, `to_date` |
| GET | `/api/stocks/{code}/plan` | 売買プラン取得 | - |

### 4.3 シグナル API

| メソッド | エンドポイント | 説明 | クエリパラメータ |
|----------|----------------|------|------------------|
| GET | `/api/signals/buy` | 買いシグナル一覧 | `min_score`, `date`, `limit` |
| GET | `/api/signals/sell` | 売りシグナル一覧 | `date`, `limit` |

### 4.4 スクリーニング API

| メソッド | エンドポイント | 説明 | ボディ |
|----------|----------------|------|--------|
| POST | `/api/screening` | スクリーニング実行 | フィルタ条件（JSONB） |
| GET | `/api/screening/presets` | プリセット一覧取得 | - |
| POST | `/api/screening/presets` | プリセット保存 | 名前 + 条件 |
| DELETE | `/api/screening/presets/{id}` | プリセット削除 | - |

### 4.5 ポートフォリオ API

| メソッド | エンドポイント | 説明 |
|----------|----------------|------|
| GET | `/api/portfolio` | ポートフォリオ取得 |
| PUT | `/api/portfolio` | ポートフォリオ更新（名前・投資額等） |
| GET | `/api/portfolio/holdings` | 保有銘柄一覧 |
| POST | `/api/portfolio/holdings` | 保有銘柄追加 |
| PUT | `/api/portfolio/holdings/{id}` | 保有銘柄更新 |
| DELETE | `/api/portfolio/holdings/{id}` | 保有銘柄削除 |
| GET | `/api/portfolio/performance` | パフォーマンス取得 |

### 4.6 取引 API

| メソッド | エンドポイント | 説明 | クエリパラメータ |
|----------|----------------|------|------------------|
| GET | `/api/trades` | 取引履歴取得 | `stock_code`, `trade_type`, `from_date`, `to_date`, `page`, `per_page` |
| POST | `/api/trades` | 取引記録追加 | - |

### 4.7 売買プラン API

| メソッド | エンドポイント | 説明 |
|----------|----------------|------|
| GET | `/api/trade-plans` | 売買プラン一覧 |
| POST | `/api/trade-plans` | 売買プラン作成 |
| PUT | `/api/trade-plans/{id}` | 売買プラン更新 |
| DELETE | `/api/trade-plans/{id}` | 売買プラン削除 |
| PUT | `/api/trade-plans/{id}/status` | ステータス変更（active/executed/cancelled） |

### 4.8 ウォッチリスト API

| メソッド | エンドポイント | 説明 |
|----------|----------------|------|
| GET | `/api/watchlists` | ウォッチリスト一覧取得 |
| POST | `/api/watchlists` | ウォッチリスト作成 |
| PUT | `/api/watchlists/{id}` | ウォッチリスト更新 |
| DELETE | `/api/watchlists/{id}` | ウォッチリスト削除 |
| POST | `/api/watchlists/{id}/items` | 銘柄追加 |
| PUT | `/api/watchlists/{id}/items/{item_id}` | 項目更新（メモ・アラート等） |
| DELETE | `/api/watchlists/{id}/items/{item_id}` | 銘柄削除 |

### 4.9 ダッシュボード API

| メソッド | エンドポイント | 説明 |
|----------|----------------|------|
| GET | `/api/dashboard/summary` | ダッシュボード全体サマリ |
| GET | `/api/dashboard/market` | マーケット概況（日経平均・TOPIX・為替） |

### 4.10 データ管理 API

| メソッド | エンドポイント | 説明 |
|----------|----------------|------|
| POST | `/api/data/collect` | データ収集の手動実行 |
| GET | `/api/data/status` | データ収集ジョブの状態確認 |
| GET | `/api/health` | ヘルスチェック |

### 4.11 設定 API

| メソッド | エンドポイント | 説明 |
|----------|----------------|------|
| GET | `/api/settings` | ユーザー設定取得 |
| PUT | `/api/settings` | ユーザー設定更新 |

## 5. データフロー図

### 5.1 データ収集フロー

```
[APScheduler: 毎日 18:00 JST]
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ master_collector │────▶│ yfinance API    │
│ (週次)           │     │ (銘柄マスタ取得) │
└─────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ price_collector  │────▶│ yfinance API    │
│ (日次)           │     │ (株価日足取得)   │
└─────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────────┐     ┌─────────────────┐
│ fundamental_collector│────▶│ yfinance API    │
│ (日次)               │     │ (指標取得)       │
└─────────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐
│ PostgreSQL      │
│ (stocks,        │
│  stock_prices,  │
│  fundamental_   │
│  data)          │
└─────────────────┘
```

### 5.2 分析・シグナル検出フロー

```
[APScheduler: データ収集完了後]
         │
         ▼
┌──────────────────────┐
│ technical.py          │
│ テクニカル指標計算     │
│ (SMA, EMA, RSI,      │
│  MACD, BB, Volume)    │
│                        │
│ 入力: stock_prices     │
│ 出力: technical_       │
│       indicators       │
└──────────────────────┘
         │
         ▼
┌──────────────────────┐
│ scoring.py            │
│ スコアリングモデル     │
│                        │
│ 入力: technical_       │
│       indicators +     │
│       fundamental_data │
│ 出力: 総合スコア       │
│       (0-100)          │
└──────────────────────┘
         │
         ▼
┌──────────────────────┐
│ signal_detector.py    │
│ シグナル検出           │
│                        │
│ 買い: スコア60以上     │
│ 売り: テクニカル悪化   │
│       + 保有銘柄チェック│
│                        │
│ 出力: signals テーブル │
└──────────────────────┘
         │
         ▼
┌──────────────────────┐
│ trade_planner.py      │
│ 売買プラン生成         │
│                        │
│ エントリーポイント計算  │
│ 利確/損切りライン計算   │
│ ポジションサイズ算出    │
│                        │
│ 出力: trade_plans      │
└──────────────────────┘
```

### 5.3 API リクエストフロー

```
[ブラウザ (Next.js)]
         │
         │  HTTP Request
         ▼
┌──────────────────────┐
│ FastAPI Router        │
│ (認証ミドルウェア)     │
│ JWT検証               │
└──────────────────────┘
         │
         ▼
┌──────────────────────┐
│ Pydantic Schema       │
│ リクエストバリデーション│
└──────────────────────┘
         │
         ▼
┌──────────────────────┐
│ Service Layer         │
│ ビジネスロジック       │
└──────────────────────┘
         │
         ▼
┌──────────────────────┐
│ SQLAlchemy (Async)    │
│ DB操作                │
└──────────────────────┘
         │
         ▼
┌──────────────────────┐
│ PostgreSQL            │
└──────────────────────┘
         │
         ▼
┌──────────────────────┐
│ Pydantic Schema       │
│ レスポンスシリアライズ  │
└──────────────────────┘
         │
         │  HTTP Response (JSON)
         ▼
[ブラウザ (Next.js)]
```

### 5.4 フロントエンドデータフロー

```
[Next.js App Router]
         │
    ┌────┴────┐
    ▼         ▼
[Server     [Client
 Components]  Components]
    │              │
    │         ┌────┴────┐
    │         ▼         ▼
    │    [Zustand    [React
    │     Store]     Hook Form]
    │         │         │
    └────┬────┘         │
         ▼              │
   [API Client (ky)]    │
         │              │
         ▼              │
   [FastAPI Backend]◀───┘
```

## 6. Docker Compose 構成

```yaml
# docker-compose.yml の概要

services:
  db:
    image: postgres:16-alpine
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]
    environment:
      POSTGRES_DB: kabu_saas
      POSTGRES_USER: kabu_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports: ["8000:8000"]
    depends_on: [db]
    environment:
      DATABASE_URL: postgresql+asyncpg://kabu_user:${DB_PASSWORD}@db:5432/kabu_saas
      SECRET_KEY: ${SECRET_KEY}
    volumes: [./backend:/app]

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports: ["3000:3000"]
    depends_on: [backend]
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    volumes: [./frontend:/app]

volumes:
  pgdata:
```

## 7. セキュリティ設計

### 7.1 認証フロー

```
1. POST /api/auth/login (email + password)
2. サーバー: bcryptでパスワード検証
3. サーバー: JWT (access_token + refresh_token) 発行
4. クライアント: access_tokenをAuthorizationヘッダに付与
5. サーバー: リクエストごとにJWT検証
6. access_token期限切れ時: refresh_tokenで新トークン取得
```

### 7.2 セキュリティ対策

| 対策 | 実装 |
|------|------|
| SQL Injection | SQLAlchemy ORMによるパラメータ化クエリ |
| XSS | Next.jsのデフォルトエスケーピング + CSP設定 |
| CORS | FastAPI CORSMiddleware（localhost:3000のみ許可） |
| パスワード | bcryptハッシュ化（salt rounds: 12） |
| トークン | JWT（HS256、access: 30分、refresh: 7日） |
| レートリミット | slowapi によるレート制限 |

## 8. スケジューラ設計

### 8.1 定時ジョブ一覧

| ジョブ名 | スケジュール | 説明 |
|----------|-------------|------|
| `collect_prices` | 毎日 18:00 JST | 全銘柄の日足株価データ収集 |
| `collect_fundamentals` | 毎日 18:30 JST | ファンダメンタルデータ収集 |
| `calculate_technicals` | 毎日 19:00 JST | テクニカル指標一括計算 |
| `detect_signals` | 毎日 19:30 JST | シグナル検出・スコアリング |
| `update_master` | 毎週日曜 10:00 JST | 銘柄マスタ更新 |

### 8.2 エラーハンドリング

- 各ジョブは個別銘柄の失敗時も他銘柄の処理を継続
- 最大3回リトライ（指数バックオフ）
- ジョブ実行結果をログに記録
- ヘルスチェックで直近のジョブ実行状況を返却
