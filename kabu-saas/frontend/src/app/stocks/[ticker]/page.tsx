"use client";

import { use } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { StockChart } from "@/components/charts/StockChart";
import { IndicatorChart } from "@/components/charts/IndicatorChart";
import { SignalList } from "@/components/signals/SignalList";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { useSWRFetch } from "@/hooks/useSWRFetch";
import type { Stock, StockPrice, TechnicalIndicator, StockFundamental, Signal } from "@/types";

// 金額フォーマット
const formatValue = (value: number | null | undefined, suffix = "") =>
  value != null ? `${new Intl.NumberFormat("ja-JP", { maximumFractionDigits: 2 }).format(value)}${suffix}` : "-";

// ファンダメンタル指標行
const FundamentalRow = ({ label, value, unit = "" }: { label: string; value: number | null | undefined; unit?: string }) => (
  <div className="flex justify-between py-2 border-b border-slate-100 last:border-0">
    <span className="text-sm text-slate-500">{label}</span>
    <span className="text-sm font-medium">{formatValue(value, unit)}</span>
  </div>
);

export default function StockDetailPage({ params }: { params: Promise<{ ticker: string }> }) {
  const { ticker } = use(params);

  const { data: stock, isLoading: stockLoading } = useSWRFetch<Stock>(`/stocks/${ticker}`);
  const { data: prices } = useSWRFetch<StockPrice[]>(`/stocks/${ticker}/prices`);
  const { data: technicals } = useSWRFetch<TechnicalIndicator[]>(`/stocks/${ticker}/technicals`);
  const { data: fundamentals } = useSWRFetch<StockFundamental>(`/stocks/${ticker}/fundamentals`);
  const { data: signals } = useSWRFetch<Signal[]>(`/stocks/${ticker}/signals`);

  if (stockLoading) {
    return <LoadingSpinner message="銘柄情報を読み込み中..." />;
  }

  if (!stock) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-500">銘柄が見つかりません: {ticker}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 銘柄ヘッダ */}
      <div className="flex items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">{stock.name}</h2>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-slate-500 font-mono">{stock.code}</span>
            <Badge variant="outline">{stock.sector}</Badge>
            <Badge variant="secondary">{stock.market}</Badge>
          </div>
        </div>
      </div>

      {/* チャートタブ */}
      <Card>
        <CardHeader>
          <CardTitle>チャート</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="price">
            <TabsList>
              <TabsTrigger value="price">株価</TabsTrigger>
              <TabsTrigger value="rsi">RSI</TabsTrigger>
              <TabsTrigger value="macd">MACD</TabsTrigger>
            </TabsList>
            <TabsContent value="price">
              <StockChart
                prices={prices ?? []}
                technicals={technicals ?? []}
                showSMA
                showBB
              />
            </TabsContent>
            <TabsContent value="rsi">
              <IndicatorChart technicals={technicals ?? []} type="rsi" />
            </TabsContent>
            <TabsContent value="macd">
              <IndicatorChart technicals={technicals ?? []} type="macd" />
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* 詳細情報 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* ファンダメンタル */}
        <Card>
          <CardHeader>
            <CardTitle>ファンダメンタル指標</CardTitle>
          </CardHeader>
          <CardContent>
            <FundamentalRow label="PER" value={fundamentals?.per} unit="倍" />
            <FundamentalRow label="PBR" value={fundamentals?.pbr} unit="倍" />
            <FundamentalRow label="配当利回り" value={fundamentals?.dividend_yield} unit="%" />
            <FundamentalRow label="ROE" value={fundamentals?.roe} unit="%" />
            <FundamentalRow label="EPS" value={fundamentals?.eps} unit="円" />
            <FundamentalRow label="BPS" value={fundamentals?.bps} unit="円" />
            <FundamentalRow
              label="時価総額"
              value={fundamentals?.market_cap ? fundamentals.market_cap / 100000000 : null}
              unit="億円"
            />
          </CardContent>
        </Card>

        {/* シグナル */}
        <Card>
          <CardHeader>
            <CardTitle>売買シグナル</CardTitle>
          </CardHeader>
          <CardContent>
            {signals && signals.length > 0 ? (
              <SignalList signals={signals.slice(0, 5)} />
            ) : (
              <p className="text-sm text-slate-400 text-center py-4">シグナルなし</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
