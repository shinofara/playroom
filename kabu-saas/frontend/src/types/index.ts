// 銘柄マスタ
export type Stock = {
  readonly id: number;
  readonly code: string;
  readonly name: string;
  readonly sector: string;
  readonly market: string;
  readonly is_active: boolean;
  readonly created_at: string;
  readonly updated_at: string;
};

// 株価日足
export type StockPrice = {
  readonly id: number;
  readonly stock_id: number;
  readonly date: string;
  readonly open: number;
  readonly high: number;
  readonly low: number;
  readonly close: number;
  readonly volume: number;
  readonly adjusted_close: number;
};

// ファンダメンタルデータ
export type StockFundamental = {
  readonly id: number;
  readonly stock_id: number;
  readonly date: string;
  readonly per: number | null;
  readonly pbr: number | null;
  readonly dividend_yield: number | null;
  readonly roe: number | null;
  readonly eps: number | null;
  readonly bps: number | null;
  readonly market_cap: number | null;
  readonly revenue: number | null;
  readonly operating_income: number | null;
};

// テクニカル指標
export type TechnicalIndicator = {
  readonly id: number;
  readonly stock_id: number;
  readonly date: string;
  readonly sma_5: number | null;
  readonly sma_25: number | null;
  readonly sma_75: number | null;
  readonly sma_200: number | null;
  readonly ema_12: number | null;
  readonly ema_26: number | null;
  readonly rsi_14: number | null;
  readonly macd_line: number | null;
  readonly macd_signal: number | null;
  readonly macd_histogram: number | null;
  readonly bb_upper_2: number | null;
  readonly bb_middle: number | null;
  readonly bb_lower_2: number | null;
  readonly volume_sma_25: number | null;
};

// シグナル
export type Signal = {
  readonly id: number;
  readonly stock_id: number;
  readonly stock?: Stock;
  readonly date: string;
  readonly signal_type: "buy" | "sell";
  readonly score: number;
  readonly technical_score: number;
  readonly fundamental_score: number;
  readonly reasons: SignalReason[];
  readonly created_at: string;
};

export type SignalReason = {
  readonly indicator: string;
  readonly description: string;
  readonly score: number;
};

// ポートフォリオ
export type Portfolio = {
  readonly id: number;
  readonly user_id: number;
  readonly name: string;
  readonly total_investment: number;
  readonly created_at: string;
};

// 保有銘柄
export type PortfolioItem = {
  readonly id: number;
  readonly portfolio_id: number;
  readonly stock_id: number;
  readonly stock?: Stock;
  readonly quantity: number;
  readonly avg_purchase_price: number;
  readonly current_price?: number;
  readonly unrealized_pnl?: number;
  readonly unrealized_pnl_pct?: number;
  readonly created_at: string;
  readonly updated_at: string;
};

// 取引履歴
export type Transaction = {
  readonly id: number;
  readonly portfolio_item_id: number;
  readonly stock_id: number;
  readonly stock?: Stock;
  readonly transaction_type: "buy" | "sell";
  readonly quantity: number;
  readonly price: number;
  readonly commission: number;
  readonly transaction_date: string;
  readonly notes: string | null;
  readonly created_at: string;
};

// ウォッチリスト
export type Watchlist = {
  readonly id: number;
  readonly user_id: number;
  readonly name: string;
  readonly created_at: string;
  readonly items?: WatchlistItem[];
};

// ウォッチリスト項目
export type WatchlistItem = {
  readonly id: number;
  readonly watchlist_id: number;
  readonly stock_id: number;
  readonly stock?: Stock;
  readonly memo: string | null;
  readonly alert_enabled: boolean;
  readonly added_at: string;
};

// ダッシュボードサマリー（バックエンドAPI準拠）
export type DashboardSummary = {
  readonly total_assets: number;
  readonly total_profit_loss: number;
  readonly daily_change: number;
  readonly buy_signal_count: number;
  readonly sell_signal_count: number;
};

// マーケット概況（バックエンドAPI準拠）
export type MarketOverview = {
  readonly nikkei225: number;
  readonly nikkei225_change: number;
  readonly topix: number;
  readonly topix_change: number;
  readonly usd_jpy: number;
  readonly usd_jpy_change: number;
};

// スクリーニング条件
export type ScreeningCriteria = {
  readonly market?: string;
  readonly sector?: string;
  readonly price_min?: number;
  readonly price_max?: number;
  readonly per_min?: number;
  readonly per_max?: number;
  readonly pbr_min?: number;
  readonly pbr_max?: number;
  readonly dividend_yield_min?: number;
  readonly rsi_min?: number;
  readonly rsi_max?: number;
  readonly min_volume?: number;
  readonly min_score?: number;
  readonly sort_by?: string;
  readonly sort_order?: "asc" | "desc";
};

// 売買プラン
export type TradePlan = {
  readonly stock: Stock;
  readonly entry_price: number;
  readonly take_profit_levels: TakeProfitLevel[];
  readonly stop_loss_price: number;
  readonly stop_loss_pct: number;
  readonly position_size: number;
  readonly risk_reward_ratio: number;
  readonly score: number;
};

export type TakeProfitLevel = {
  readonly level: number;
  readonly price: number;
  readonly pct: number;
};

// APIレスポンス
export type PaginatedResponse<T> = {
  readonly items: T[];
  readonly total: number;
  readonly page: number;
  readonly per_page: number;
};

// エージェント: 注文推奨
export type OrderRecommendation = {
  readonly stock_code: string;
  readonly stock_name: string;
  readonly action: "buy" | "sell";
  readonly order_type: "market" | "limit";
  readonly price: number;
  readonly quantity: number;
  readonly score: number;
  readonly reasons: SignalReason[];
  readonly take_profit_1: number | null;
  readonly take_profit_2: number | null;
  readonly take_profit_3: number | null;
  readonly stop_loss: number | null;
  readonly risk_reward_ratio: number | null;
};

// エージェント: 今日のアクション
export type TodayActions = {
  readonly date: string;
  readonly pipeline_status: "not_run" | "running" | "completed" | "failed";
  readonly pipeline_last_run: string | null;
  readonly buy_recommendations: OrderRecommendation[];
  readonly sell_recommendations: OrderRecommendation[];
  readonly summary: string;
};
