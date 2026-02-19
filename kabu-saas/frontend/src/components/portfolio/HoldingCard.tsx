"use client";

import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import type { PortfolioItem } from "@/types";

type Props = {
  readonly item: PortfolioItem;
};

const formatYen = (value: number) =>
  `¥${new Intl.NumberFormat("ja-JP").format(Math.round(value))}`;

export const HoldingCard = ({ item }: Props) => {
  const totalCost = item.quantity * item.avg_purchase_price;
  const currentValue = item.current_price ? item.quantity * item.current_price : null;
  const pnl = item.unrealized_pnl ?? (currentValue ? currentValue - totalCost : null);
  const pnlPct = item.unrealized_pnl_pct ?? (pnl && totalCost > 0 ? (pnl / totalCost) * 100 : null);
  const isPositive = (pnl ?? 0) >= 0;

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div>
            <Link
              href={`/stocks/${item.stock?.code ?? item.stock_id}`}
              className="font-semibold text-slate-800 hover:text-blue-600"
            >
              {item.stock?.name ?? `銘柄ID: ${item.stock_id}`}
            </Link>
            <p className="text-sm text-slate-500 mt-0.5">
              {item.stock?.code} | {item.quantity}株 | 取得単価 {formatYen(item.avg_purchase_price)}
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-slate-500">取得コスト: {formatYen(totalCost)}</p>
            {currentValue != null && (
              <p className="font-bold">評価額: {formatYen(currentValue)}</p>
            )}
            {pnl != null && pnlPct != null && (
              <p className={`text-sm font-medium ${isPositive ? "text-green-600" : "text-red-600"}`}>
                {isPositive ? "+" : ""}{formatYen(pnl)} ({isPositive ? "+" : ""}{pnlPct.toFixed(2)}%)
              </p>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
