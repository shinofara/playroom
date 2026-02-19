"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { OrderRecommendation } from "@/types";

type Props = {
  readonly recommendation: OrderRecommendation;
  readonly onClick?: () => void;
};

const formatYen = (value: number) =>
  `\u00a5${new Intl.NumberFormat("ja-JP").format(Math.round(value))}`;

export const ActionCard = ({ recommendation: rec, onClick }: Props) => {
  const isBuy = rec.action === "buy";
  const orderLabel = rec.order_type === "market" ? "成行" : "指値";

  return (
    <Card
      className="cursor-pointer hover:shadow-md transition-shadow"
      onClick={onClick}
    >
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base">
            <span className="text-slate-500 text-sm mr-1">{rec.stock_code}</span>
            {rec.stock_name}
          </CardTitle>
          <div className="flex gap-1">
            <Badge variant={isBuy ? "default" : "destructive"}>
              {isBuy ? "買い" : "売り"}
            </Badge>
            <Badge variant="outline">{orderLabel}</Badge>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        {/* 価格・数量 */}
        <div className="grid grid-cols-3 gap-2 text-sm mb-3">
          <div>
            <p className="text-slate-400 text-xs">注文価格</p>
            <p className="font-bold">{formatYen(rec.price)}</p>
          </div>
          <div>
            <p className="text-slate-400 text-xs">数量</p>
            <p className="font-bold">{rec.quantity}株</p>
          </div>
          <div>
            <p className="text-slate-400 text-xs">スコア</p>
            <p className={`font-bold ${isBuy ? "text-green-600" : "text-red-600"}`}>
              {Number(rec.score).toFixed(1)}
            </p>
          </div>
        </div>

        {/* 利確・損切り */}
        {(rec.take_profit_1 || rec.stop_loss) && (
          <div className="flex gap-3 text-xs text-slate-500 border-t pt-2">
            {rec.take_profit_1 && (
              <span>利確1: {formatYen(rec.take_profit_1)}</span>
            )}
            {rec.stop_loss && (
              <span className="text-red-500">損切: {formatYen(rec.stop_loss)}</span>
            )}
            {rec.risk_reward_ratio && (
              <span>RR: {Number(rec.risk_reward_ratio).toFixed(1)}</span>
            )}
          </div>
        )}

        {/* 主な理由（先頭2件） */}
        {rec.reasons.length > 0 && (
          <div className="mt-2 space-y-0.5">
            {rec.reasons.slice(0, 2).map((r, i) => (
              <p key={i} className="text-xs text-slate-500 truncate">
                {r.indicator}: {r.description}
              </p>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};
