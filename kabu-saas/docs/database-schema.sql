-- =============================================================================
-- Kabu SaaS データベーススキーマ定義
-- PostgreSQL 16
-- =============================================================================

-- 拡張機能の有効化
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- users（ユーザー）
-- 当面は1ユーザーだが、マルチユーザー対応を前提に設計
-- =============================================================================
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    username        VARCHAR(50) NOT NULL UNIQUE,
    email           VARCHAR(100) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE users IS 'ユーザーマスタ';
COMMENT ON COLUMN users.username IS 'ユーザー名（一意）';
COMMENT ON COLUMN users.email IS 'メールアドレス（一意）';
COMMENT ON COLUMN users.password_hash IS 'bcryptハッシュ化パスワード';
COMMENT ON COLUMN users.is_active IS '有効フラグ';

-- =============================================================================
-- user_settings（ユーザー設定）
-- スコアリング重み、デフォルト利確/損切り率等をJSONBで柔軟に保持
-- =============================================================================
CREATE TABLE user_settings (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    setting_key     VARCHAR(50) NOT NULL,
    setting_value   JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_user_settings_user_key UNIQUE (user_id, setting_key)
);

COMMENT ON TABLE user_settings IS 'ユーザー個別設定';
COMMENT ON COLUMN user_settings.setting_key IS '設定キー（scoring_weights, default_take_profit, default_stop_loss等）';
COMMENT ON COLUMN user_settings.setting_value IS '設定値（JSONB形式）';

CREATE INDEX idx_user_settings_user_id ON user_settings(user_id);

-- =============================================================================
-- stocks（銘柄マスタ）
-- 東証上場銘柄の基本情報を管理
-- =============================================================================
CREATE TABLE stocks (
    id              SERIAL PRIMARY KEY,
    ticker_code     VARCHAR(10) NOT NULL UNIQUE,
    name            VARCHAR(100) NOT NULL,
    name_en         VARCHAR(100),
    sector          VARCHAR(50),
    market          VARCHAR(20),
    market_cap      BIGINT,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE stocks IS '銘柄マスタ（東証上場銘柄）';
COMMENT ON COLUMN stocks.ticker_code IS '銘柄コード（例: "7203.T"）';
COMMENT ON COLUMN stocks.name IS '銘柄名（日本語）';
COMMENT ON COLUMN stocks.name_en IS '銘柄名（英語）';
COMMENT ON COLUMN stocks.sector IS '業種・セクター';
COMMENT ON COLUMN stocks.market IS '市場区分（プライム/スタンダード/グロース）';
COMMENT ON COLUMN stocks.market_cap IS '時価総額（円）';
COMMENT ON COLUMN stocks.is_active IS '上場中フラグ（上場廃止時にFALSE）';

CREATE INDEX idx_stocks_market ON stocks(market) WHERE is_active = TRUE;
CREATE INDEX idx_stocks_sector ON stocks(sector) WHERE is_active = TRUE;
CREATE INDEX idx_stocks_ticker_code ON stocks(ticker_code);

-- =============================================================================
-- stock_prices（株価データ）
-- 日足の株価データを保持（過去5年分）
-- =============================================================================
CREATE TABLE stock_prices (
    id              SERIAL PRIMARY KEY,
    stock_id        INTEGER NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    date            DATE NOT NULL,
    open            DECIMAL(10, 2) NOT NULL,
    high            DECIMAL(10, 2) NOT NULL,
    low             DECIMAL(10, 2) NOT NULL,
    close           DECIMAL(10, 2) NOT NULL,
    volume          BIGINT NOT NULL DEFAULT 0,
    adjusted_close  DECIMAL(10, 2),

    CONSTRAINT uq_stock_prices_stock_date UNIQUE (stock_id, date)
);

COMMENT ON TABLE stock_prices IS '株価日足データ';
COMMENT ON COLUMN stock_prices.open IS '始値';
COMMENT ON COLUMN stock_prices.high IS '高値';
COMMENT ON COLUMN stock_prices.low IS '安値';
COMMENT ON COLUMN stock_prices.close IS '終値';
COMMENT ON COLUMN stock_prices.volume IS '出来高';
COMMENT ON COLUMN stock_prices.adjusted_close IS '調整後終値（分割・配当調整済み）';

CREATE INDEX idx_stock_prices_stock_date_desc ON stock_prices(stock_id, date DESC);
CREATE INDEX idx_stock_prices_date ON stock_prices(date DESC);

-- =============================================================================
-- technical_indicators（テクニカル指標）
-- 各銘柄の日次テクニカル分析結果を保持
-- =============================================================================
CREATE TABLE technical_indicators (
    id              SERIAL PRIMARY KEY,
    stock_id        INTEGER NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    date            DATE NOT NULL,

    -- 移動平均線（SMA）
    sma_5           DECIMAL(10, 2),
    sma_25          DECIMAL(10, 2),
    sma_75          DECIMAL(10, 2),
    sma_200         DECIMAL(10, 2),

    -- 指数移動平均線（EMA）
    ema_12          DECIMAL(10, 2),
    ema_26          DECIMAL(10, 2),

    -- RSI
    rsi_14          DECIMAL(5, 2),

    -- MACD
    macd            DECIMAL(10, 4),
    macd_signal     DECIMAL(10, 4),
    macd_histogram  DECIMAL(10, 4),

    -- ボリンジャーバンド（20日, 2σ）
    bollinger_upper DECIMAL(10, 2),
    bollinger_middle DECIMAL(10, 2),
    bollinger_lower DECIMAL(10, 2),

    -- 出来高指標
    volume_sma_25   BIGINT,
    volume_ratio    DECIMAL(5, 2),

    CONSTRAINT uq_technical_indicators_stock_date UNIQUE (stock_id, date)
);

COMMENT ON TABLE technical_indicators IS 'テクニカル指標（日次計算結果）';
COMMENT ON COLUMN technical_indicators.sma_5 IS '5日単純移動平均線';
COMMENT ON COLUMN technical_indicators.sma_25 IS '25日単純移動平均線';
COMMENT ON COLUMN technical_indicators.sma_75 IS '75日単純移動平均線';
COMMENT ON COLUMN technical_indicators.sma_200 IS '200日単純移動平均線';
COMMENT ON COLUMN technical_indicators.ema_12 IS '12日指数移動平均線';
COMMENT ON COLUMN technical_indicators.ema_26 IS '26日指数移動平均線';
COMMENT ON COLUMN technical_indicators.rsi_14 IS '14日RSI（相対力指数）';
COMMENT ON COLUMN technical_indicators.macd IS 'MACDライン（EMA12 - EMA26）';
COMMENT ON COLUMN technical_indicators.macd_signal IS 'MACDシグナルライン（9日EMA）';
COMMENT ON COLUMN technical_indicators.macd_histogram IS 'MACDヒストグラム';
COMMENT ON COLUMN technical_indicators.bollinger_upper IS 'ボリンジャーバンド上限（+2σ）';
COMMENT ON COLUMN technical_indicators.bollinger_middle IS 'ボリンジャーバンド中央（20日SMA）';
COMMENT ON COLUMN technical_indicators.bollinger_lower IS 'ボリンジャーバンド下限（-2σ）';
COMMENT ON COLUMN technical_indicators.volume_sma_25 IS '出来高25日移動平均';
COMMENT ON COLUMN technical_indicators.volume_ratio IS '出来高比率（当日出来高 / 25日平均）';

CREATE INDEX idx_technical_indicators_stock_date_desc ON technical_indicators(stock_id, date DESC);
CREATE INDEX idx_technical_indicators_date ON technical_indicators(date DESC);

-- =============================================================================
-- fundamental_data（ファンダメンタルデータ）
-- 各銘柄のファンダメンタル指標を日次で保持
-- =============================================================================
CREATE TABLE fundamental_data (
    id              SERIAL PRIMARY KEY,
    stock_id        INTEGER NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    date            DATE NOT NULL,

    per             DECIMAL(10, 2),
    pbr             DECIMAL(10, 2),
    dividend_yield  DECIMAL(5, 2),
    roe             DECIMAL(5, 2),
    eps             DECIMAL(10, 2),
    bps             DECIMAL(10, 2),
    market_cap      BIGINT,
    revenue         BIGINT,
    operating_income BIGINT,

    CONSTRAINT uq_fundamental_data_stock_date UNIQUE (stock_id, date)
);

COMMENT ON TABLE fundamental_data IS 'ファンダメンタルデータ（日次）';
COMMENT ON COLUMN fundamental_data.per IS '株価収益率（PER）';
COMMENT ON COLUMN fundamental_data.pbr IS '株価純資産倍率（PBR）';
COMMENT ON COLUMN fundamental_data.dividend_yield IS '配当利回り（%）';
COMMENT ON COLUMN fundamental_data.roe IS '自己資本利益率 ROE（%）';
COMMENT ON COLUMN fundamental_data.eps IS '1株当たり利益（EPS）';
COMMENT ON COLUMN fundamental_data.bps IS '1株当たり純資産（BPS）';
COMMENT ON COLUMN fundamental_data.market_cap IS '時価総額（円）';
COMMENT ON COLUMN fundamental_data.revenue IS '売上高（円）';
COMMENT ON COLUMN fundamental_data.operating_income IS '営業利益（円）';

CREATE INDEX idx_fundamental_data_stock_date_desc ON fundamental_data(stock_id, date DESC);
CREATE INDEX idx_fundamental_data_date ON fundamental_data(date DESC);

-- =============================================================================
-- signals（シグナル）
-- 買い/売りシグナルの検出結果とスコアリング
-- =============================================================================
CREATE TABLE signals (
    id                  SERIAL PRIMARY KEY,
    stock_id            INTEGER NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    date                DATE NOT NULL,
    signal_type         VARCHAR(4) NOT NULL CHECK (signal_type IN ('buy', 'sell')),
    score               DECIMAL(5, 2) NOT NULL CHECK (score >= 0 AND score <= 100),
    technical_score     DECIMAL(5, 2) CHECK (technical_score >= 0 AND technical_score <= 100),
    fundamental_score   DECIMAL(5, 2) CHECK (fundamental_score >= 0 AND fundamental_score <= 100),
    reason              JSONB NOT NULL DEFAULT '[]',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE signals IS '買い/売りシグナル';
COMMENT ON COLUMN signals.signal_type IS 'シグナル種別（buy: 買い, sell: 売り）';
COMMENT ON COLUMN signals.score IS '総合スコア（0-100）';
COMMENT ON COLUMN signals.technical_score IS 'テクニカルスコア（0-100）';
COMMENT ON COLUMN signals.fundamental_score IS 'ファンダメンタルスコア（0-100）';
COMMENT ON COLUMN signals.reason IS 'シグナル理由の詳細（JSON配列）';

CREATE INDEX idx_signals_date_type_score ON signals(date DESC, signal_type, score DESC);
CREATE INDEX idx_signals_stock_date_desc ON signals(stock_id, date DESC);
CREATE INDEX idx_signals_signal_type ON signals(signal_type);

-- =============================================================================
-- portfolios（ポートフォリオ）
-- ユーザーのポートフォリオ情報
-- =============================================================================
CREATE TABLE portfolios (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name            VARCHAR(50) NOT NULL,
    description     TEXT,
    total_investment DECIMAL(14, 2) NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE portfolios IS 'ポートフォリオ';
COMMENT ON COLUMN portfolios.name IS 'ポートフォリオ名';
COMMENT ON COLUMN portfolios.description IS '説明';
COMMENT ON COLUMN portfolios.total_investment IS '総投資額（円）';

CREATE INDEX idx_portfolios_user_id ON portfolios(user_id);

-- =============================================================================
-- portfolio_holdings（保有銘柄）
-- ポートフォリオ内の個別銘柄保有情報
-- =============================================================================
CREATE TABLE portfolio_holdings (
    id                  SERIAL PRIMARY KEY,
    portfolio_id        INTEGER NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
    stock_id            INTEGER NOT NULL REFERENCES stocks(id) ON DELETE RESTRICT,
    quantity            INTEGER NOT NULL CHECK (quantity > 0),
    avg_cost            DECIMAL(10, 2) NOT NULL,
    current_price       DECIMAL(10, 2),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_portfolio_holdings_portfolio_stock UNIQUE (portfolio_id, stock_id)
);

COMMENT ON TABLE portfolio_holdings IS 'ポートフォリオ保有銘柄';
COMMENT ON COLUMN portfolio_holdings.quantity IS '保有数量（株数）';
COMMENT ON COLUMN portfolio_holdings.avg_cost IS '平均取得単価（円）';
COMMENT ON COLUMN portfolio_holdings.current_price IS '現在価格（直近終値から更新）';

CREATE INDEX idx_portfolio_holdings_portfolio_id ON portfolio_holdings(portfolio_id);
CREATE INDEX idx_portfolio_holdings_stock_id ON portfolio_holdings(stock_id);

-- =============================================================================
-- trades（取引履歴）
-- 売買取引の記録
-- =============================================================================
CREATE TABLE trades (
    id              SERIAL PRIMARY KEY,
    portfolio_id    INTEGER NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
    stock_id        INTEGER NOT NULL REFERENCES stocks(id) ON DELETE RESTRICT,
    trade_type      VARCHAR(4) NOT NULL CHECK (trade_type IN ('buy', 'sell')),
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    price           DECIMAL(10, 2) NOT NULL,
    commission      DECIMAL(8, 2) NOT NULL DEFAULT 0,
    trade_date      DATE NOT NULL,
    notes           TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE trades IS '取引履歴';
COMMENT ON COLUMN trades.trade_type IS '取引種別（buy: 買い, sell: 売り）';
COMMENT ON COLUMN trades.quantity IS '取引数量（株数）';
COMMENT ON COLUMN trades.price IS '約定単価（円）';
COMMENT ON COLUMN trades.commission IS '手数料（円）';
COMMENT ON COLUMN trades.trade_date IS '約定日';
COMMENT ON COLUMN trades.notes IS '取引メモ';

CREATE INDEX idx_trades_portfolio_id ON trades(portfolio_id);
CREATE INDEX idx_trades_stock_id ON trades(stock_id);
CREATE INDEX idx_trades_trade_date_desc ON trades(trade_date DESC);
CREATE INDEX idx_trades_portfolio_date ON trades(portfolio_id, trade_date DESC);

-- =============================================================================
-- trade_plans（売買プラン）
-- エントリーポイント・利確/損切りライン・ポジションサイズの計画
-- =============================================================================
CREATE TABLE trade_plans (
    id                  SERIAL PRIMARY KEY,
    stock_id            INTEGER NOT NULL REFERENCES stocks(id) ON DELETE RESTRICT,
    user_id             INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    entry_price         DECIMAL(10, 2) NOT NULL,
    target_price        DECIMAL(10, 2) NOT NULL,
    stop_loss_price     DECIMAL(10, 2) NOT NULL,
    position_size       INTEGER NOT NULL CHECK (position_size > 0),
    risk_reward_ratio   DECIMAL(5, 2),
    status              VARCHAR(10) NOT NULL DEFAULT 'active'
                        CHECK (status IN ('active', 'executed', 'cancelled', 'expired')),
    reason              TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE trade_plans IS '売買プラン';
COMMENT ON COLUMN trade_plans.entry_price IS 'エントリー価格（推奨購入価格）';
COMMENT ON COLUMN trade_plans.target_price IS '利確目標価格';
COMMENT ON COLUMN trade_plans.stop_loss_price IS '損切り価格';
COMMENT ON COLUMN trade_plans.position_size IS 'ポジションサイズ（株数）';
COMMENT ON COLUMN trade_plans.risk_reward_ratio IS 'リスクリワード比';
COMMENT ON COLUMN trade_plans.status IS 'ステータス（active/executed/cancelled/expired）';
COMMENT ON COLUMN trade_plans.reason IS 'プラン根拠の説明';

CREATE INDEX idx_trade_plans_stock_id ON trade_plans(stock_id);
CREATE INDEX idx_trade_plans_user_id ON trade_plans(user_id);
CREATE INDEX idx_trade_plans_status ON trade_plans(status) WHERE status = 'active';

-- =============================================================================
-- watchlists（ウォッチリスト）
-- ユーザーの注目銘柄リスト
-- =============================================================================
CREATE TABLE watchlists (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name            VARCHAR(50) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE watchlists IS 'ウォッチリスト';
COMMENT ON COLUMN watchlists.name IS 'ウォッチリスト名';

CREATE INDEX idx_watchlists_user_id ON watchlists(user_id);

-- =============================================================================
-- watchlist_items（ウォッチリスト項目）
-- ウォッチリスト内の個別銘柄
-- =============================================================================
CREATE TABLE watchlist_items (
    id              SERIAL PRIMARY KEY,
    watchlist_id    INTEGER NOT NULL REFERENCES watchlists(id) ON DELETE CASCADE,
    stock_id        INTEGER NOT NULL REFERENCES stocks(id) ON DELETE RESTRICT,
    memo            TEXT,
    alert_enabled   BOOLEAN NOT NULL DEFAULT TRUE,
    added_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_watchlist_items_watchlist_stock UNIQUE (watchlist_id, stock_id)
);

COMMENT ON TABLE watchlist_items IS 'ウォッチリスト項目';
COMMENT ON COLUMN watchlist_items.memo IS '銘柄メモ';
COMMENT ON COLUMN watchlist_items.alert_enabled IS 'アラート有効フラグ';

CREATE INDEX idx_watchlist_items_watchlist_id ON watchlist_items(watchlist_id);
CREATE INDEX idx_watchlist_items_stock_id ON watchlist_items(stock_id);

-- =============================================================================
-- screening_presets（スクリーニング条件プリセット）
-- ユーザーが保存したスクリーニング条件
-- =============================================================================
CREATE TABLE screening_presets (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name            VARCHAR(100) NOT NULL,
    conditions      JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE screening_presets IS 'スクリーニング条件プリセット';
COMMENT ON COLUMN screening_presets.name IS 'プリセット名';
COMMENT ON COLUMN screening_presets.conditions IS 'スクリーニング条件（JSONB）';

/*
  conditions の構造例:
  {
    "market": ["プライム", "スタンダード"],
    "sector": ["情報・通信業"],
    "price_min": 500,
    "price_max": 5000,
    "per_max": 15,
    "pbr_max": 1.0,
    "dividend_yield_min": 3.0,
    "roe_min": 10,
    "rsi_min": 20,
    "rsi_max": 70,
    "volume_min": 100000,
    "score_min": 60,
    "sort_by": "score",
    "sort_order": "desc"
  }
*/

CREATE INDEX idx_screening_presets_user_id ON screening_presets(user_id);

-- =============================================================================
-- data_collection_logs（データ収集ログ）
-- バッチジョブの実行履歴（運用監視用）
-- =============================================================================
CREATE TABLE data_collection_logs (
    id              SERIAL PRIMARY KEY,
    job_name        VARCHAR(50) NOT NULL,
    status          VARCHAR(10) NOT NULL CHECK (status IN ('running', 'success', 'failed', 'partial')),
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at     TIMESTAMPTZ,
    total_count     INTEGER DEFAULT 0,
    success_count   INTEGER DEFAULT 0,
    error_count     INTEGER DEFAULT 0,
    error_details   JSONB DEFAULT '[]'
);

COMMENT ON TABLE data_collection_logs IS 'データ収集ジョブ実行ログ';
COMMENT ON COLUMN data_collection_logs.job_name IS 'ジョブ名（collect_prices, collect_fundamentals, calculate_technicals, detect_signals）';
COMMENT ON COLUMN data_collection_logs.status IS '実行ステータス';
COMMENT ON COLUMN data_collection_logs.total_count IS '処理対象件数';
COMMENT ON COLUMN data_collection_logs.success_count IS '成功件数';
COMMENT ON COLUMN data_collection_logs.error_count IS 'エラー件数';
COMMENT ON COLUMN data_collection_logs.error_details IS 'エラー詳細（JSON配列）';

CREATE INDEX idx_data_collection_logs_job_started ON data_collection_logs(job_name, started_at DESC);

-- =============================================================================
-- updated_at トリガー関数
-- =============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- updated_at 自動更新トリガーを各テーブルに設定
CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_user_settings_updated_at
    BEFORE UPDATE ON user_settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_stocks_updated_at
    BEFORE UPDATE ON stocks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_portfolios_updated_at
    BEFORE UPDATE ON portfolios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_portfolio_holdings_updated_at
    BEFORE UPDATE ON portfolio_holdings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_trade_plans_updated_at
    BEFORE UPDATE ON trade_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_watchlists_updated_at
    BEFORE UPDATE ON watchlists
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_screening_presets_updated_at
    BEFORE UPDATE ON screening_presets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- 初期データ: デフォルトユーザー
-- パスワードは 'admin123' のbcryptハッシュ（本番では変更すること）
-- =============================================================================
-- INSERT INTO users (username, email, password_hash)
-- VALUES ('admin', 'admin@kabu-saas.local', '$2b$12$placeholder_hash_change_me');
