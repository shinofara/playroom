import type {
  DashboardSummary,
  MarketOverview,
  PaginatedResponse,
  ScreeningCriteria,
  Signal,
  Stock,
  StockFundamental,
  StockPrice,
  TechnicalIndicator,
  TodayActions,
  TradePlan,
  Portfolio,
  PortfolioItem,
  Transaction,
  Watchlist,
} from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

// 汎用フェッチ関数
const fetcher = async <T>(path: string, options?: RequestInit): Promise<T> => {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API Error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
};

// SWR用フェッチャー
export const swrFetcher = <T>(path: string): Promise<T> => fetcher<T>(path);

// ダッシュボード
export const fetchDashboardSummary = () =>
  fetcher<DashboardSummary>("/dashboard/summary");

export const fetchMarketOverview = () =>
  fetcher<MarketOverview>("/dashboard/market");

// 銘柄
export const fetchStocks = (params?: Record<string, string>) => {
  const query = params ? `?${new URLSearchParams(params)}` : "";
  return fetcher<PaginatedResponse<Stock>>(`/stocks${query}`);
};

export const fetchStock = (code: string) =>
  fetcher<Stock>(`/stocks/${code}`);

export const fetchStockPrices = (code: string, params?: Record<string, string>) => {
  const query = params ? `?${new URLSearchParams(params)}` : "";
  return fetcher<StockPrice[]>(`/stocks/${code}/prices${query}`);
};

export const fetchStockFundamentals = (code: string) =>
  fetcher<StockFundamental>(`/stocks/${code}/fundamentals`);

export const fetchStockTechnicals = (code: string) =>
  fetcher<TechnicalIndicator[]>(`/stocks/${code}/technicals`);

export const fetchStockSignals = (code: string) =>
  fetcher<Signal[]>(`/stocks/${code}/signals`);

export const fetchStockPlan = (code: string) =>
  fetcher<TradePlan>(`/stocks/${code}/plan`);

// シグナル
export const fetchBuySignals = () =>
  fetcher<Signal[]>("/signals/buy");

export const fetchSellSignals = () =>
  fetcher<Signal[]>("/signals/sell");

// スクリーニング
export const executeScreening = (criteria: ScreeningCriteria) =>
  fetcher<PaginatedResponse<Stock & { score?: number }>>("/screening", {
    method: "POST",
    body: JSON.stringify(criteria),
  });

// ポートフォリオ
export const fetchPortfolio = () =>
  fetcher<Portfolio & { items: PortfolioItem[] }>("/portfolio");

export const addPortfolioItem = (data: {
  stock_id: number;
  quantity: number;
  avg_purchase_price: number;
}) =>
  fetcher<PortfolioItem>("/portfolio/items", {
    method: "POST",
    body: JSON.stringify(data),
  });

export const deletePortfolioItem = (id: number) =>
  fetcher<void>(`/portfolio/items/${id}`, { method: "DELETE" });

export const fetchTransactions = () =>
  fetcher<Transaction[]>("/portfolio/transactions");

export const addTransaction = (data: {
  stock_id: number;
  transaction_type: "buy" | "sell";
  quantity: number;
  price: number;
  commission?: number;
  transaction_date: string;
  notes?: string;
}) =>
  fetcher<Transaction>("/portfolio/transactions", {
    method: "POST",
    body: JSON.stringify(data),
  });

// ウォッチリスト
export const fetchWatchlists = () =>
  fetcher<Watchlist[]>("/watchlists");

export const createWatchlist = (name: string) =>
  fetcher<Watchlist>("/watchlists", {
    method: "POST",
    body: JSON.stringify({ name }),
  });

export const addWatchlistItem = (watchlistId: number, stockId: number) =>
  fetcher<void>(`/watchlists/${watchlistId}/items`, {
    method: "POST",
    body: JSON.stringify({ stock_id: stockId }),
  });

export const deleteWatchlistItem = (watchlistId: number, itemId: number) =>
  fetcher<void>(`/watchlists/${watchlistId}/items/${itemId}`, {
    method: "DELETE",
  });

// エージェント
export const fetchTodayActions = () =>
  fetcher<TodayActions>("/agent/today-actions");

export const triggerPipeline = () =>
  fetcher<{ status: string; message: string }>("/agent/run-pipeline", {
    method: "POST",
  });

export const fetchPipelineStatus = () =>
  fetcher<{ status: string; message?: string }>("/agent/pipeline-status");
