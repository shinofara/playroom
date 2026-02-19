"use client";

import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { Badge } from "@/components/ui/badge";
import { StockChart } from "@/components/charts/StockChart";
import { IndicatorChart } from "@/components/charts/IndicatorChart";
import { useSWRFetch } from "@/hooks/useSWRFetch";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import type { OrderRecommendation, StockPrice, TechnicalIndicator } from "@/types";

type Props = {
  readonly recommendation: OrderRecommendation | null;
  readonly open: boolean;
  readonly onClose: () => void;
};

const formatYen = (value: number) =>
  `\u00a5${new Intl.NumberFormat("ja-JP").format(Math.round(value))}`;

export const StockDetailDrawer = ({ recommendation: rec, open, onClose }: Props) => {
  const code = rec?.stock_code ?? null;
  const { data: prices, isLoading: pricesLoading } = useSWRFetch<StockPrice[]>(
    code ? `/stocks/${code}/prices?days=90` : null,
  );
  const { data: technicals, isLoading: techLoading } = useSWRFetch<TechnicalIndicator[]>(
    code ? `/stocks/${code}/technicals` : null,
  );

  return (
    <Sheet open={open} onOpenChange={(v) => !v && onClose()}>
      <SheetContent className="w-full sm:max-w-2xl overflow-y-auto">
        {rec && (
          <>
            <SheetHeader>
              <SheetTitle className="flex items-center gap-2">
                <span className="text-slate-400">{rec.stock_code}</span>
                {rec.stock_name}
                <Badge variant={rec.action === "buy" ? "default" : "destructive"}>
                  {rec.action === "buy" ? "買い推奨" : "売り推奨"}
                </Badge>
              </SheetTitle>
            </SheetHeader>

            {/* 注文詳細 */}
            <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
              <div className="bg-slate-50 rounded-lg p-3">
                <p className="text-slate-400 text-xs">注文種別</p>
                <p className="font-bold">{rec.order_type === "market" ? "成行注文" : "指値注文"}</p>
              </div>
              <div className="bg-slate-50 rounded-lg p-3">
                <p className="text-slate-400 text-xs">注文価格</p>
                <p className="font-bold">{formatYen(rec.price)}</p>
              </div>
              <div className="bg-slate-50 rounded-lg p-3">
                <p className="text-slate-400 text-xs">数量</p>
                <p className="font-bold">{rec.quantity}株</p>
              </div>
              <div className="bg-slate-50 rounded-lg p-3">
                <p className="text-slate-400 text-xs">スコア</p>
                <p className={`font-bold ${rec.action === "buy" ? "text-green-600" : "text-red-600"}`}>
                  {Number(rec.score).toFixed(1)}点
                </p>
              </div>
            </div>

            {/* 利確・損切りライン */}
            {(rec.take_profit_1 || rec.stop_loss) && (
              <div className="mt-4 bg-slate-50 rounded-lg p-3">
                <p className="text-xs font-medium text-slate-500 mb-2">利確・損切りライン</p>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  {rec.take_profit_1 && (
                    <div>
                      <span className="text-slate-400">利確1:</span>{" "}
                      <span className="text-green-600 font-medium">{formatYen(rec.take_profit_1)}</span>
                    </div>
                  )}
                  {rec.take_profit_2 && (
                    <div>
                      <span className="text-slate-400">利確2:</span>{" "}
                      <span className="text-green-600 font-medium">{formatYen(rec.take_profit_2)}</span>
                    </div>
                  )}
                  {rec.take_profit_3 && (
                    <div>
                      <span className="text-slate-400">利確3:</span>{" "}
                      <span className="text-green-600 font-medium">{formatYen(rec.take_profit_3)}</span>
                    </div>
                  )}
                  {rec.stop_loss && (
                    <div>
                      <span className="text-slate-400">損切:</span>{" "}
                      <span className="text-red-600 font-medium">{formatYen(rec.stop_loss)}</span>
                    </div>
                  )}
                  {rec.risk_reward_ratio && (
                    <div>
                      <span className="text-slate-400">RR比:</span>{" "}
                      <span className="font-medium">{Number(rec.risk_reward_ratio).toFixed(2)}</span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* シグナル理由 */}
            {rec.reasons.length > 0 && (
              <div className="mt-4">
                <p className="text-xs font-medium text-slate-500 mb-2">シグナル理由</p>
                <div className="space-y-1">
                  {rec.reasons.map((r, i) => (
                    <div key={i} className="flex justify-between text-sm bg-slate-50 rounded px-3 py-1.5">
                      <span className="text-slate-600">{r.indicator}: {r.description}</span>
                      <span className={`font-medium ${r.score > 0 ? "text-green-600" : "text-red-600"}`}>
                        {r.score > 0 ? "+" : ""}{r.score.toFixed(1)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* チャート */}
            <div className="mt-4">
              <p className="text-xs font-medium text-slate-500 mb-2">株価チャート（90日）</p>
              {pricesLoading ? (
                <LoadingSpinner message="チャートを読み込み中..." />
              ) : prices && prices.length > 0 ? (
                <StockChart prices={prices} />
              ) : (
                <p className="text-sm text-slate-400 text-center py-4">チャートデータがありません</p>
              )}
            </div>

            {technicals && technicals.length > 0 && (
              <div className="mt-4">
                <p className="text-xs font-medium text-slate-500 mb-2">テクニカル指標</p>
                {techLoading ? (
                  <LoadingSpinner message="テクニカル指標を読み込み中..." />
                ) : (
                  <IndicatorChart indicators={technicals} />
                )}
              </div>
            )}
          </>
        )}
      </SheetContent>
    </Sheet>
  );
};
