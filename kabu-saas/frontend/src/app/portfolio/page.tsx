"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { HoldingCard } from "@/components/portfolio/HoldingCard";
import { TradeForm } from "@/components/portfolio/TradeForm";
import { PortfolioChart } from "@/components/charts/PortfolioChart";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { useSWRFetch } from "@/hooks/useSWRFetch";
import type { Portfolio, PortfolioItem } from "@/types";

// 金額フォーマット
const formatYen = (value: number) =>
  `¥${new Intl.NumberFormat("ja-JP").format(Math.round(value))}`;

export default function PortfolioPage() {
  const [dialogOpen, setDialogOpen] = useState(false);
  const { data: portfolio, isLoading, mutate } =
    useSWRFetch<Portfolio & { items: PortfolioItem[] }>("/portfolio");

  if (isLoading) {
    return <LoadingSpinner message="ポートフォリオを読み込み中..." />;
  }

  const items = portfolio?.items ?? [];
  const totalCost = items.reduce((sum, item) => sum + item.quantity * item.avg_purchase_price, 0);
  const totalValue = items.reduce(
    (sum, item) => sum + (item.current_price ? item.quantity * item.current_price : item.quantity * item.avg_purchase_price),
    0
  );
  const totalPnl = totalValue - totalCost;
  const totalPnlPct = totalCost > 0 ? (totalPnl / totalCost) * 100 : 0;

  return (
    <div className="space-y-6">
      {/* サマリー */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-slate-500">投資元本</p>
            <p className="text-xl font-bold mt-1">{formatYen(totalCost)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-slate-500">評価額合計</p>
            <p className="text-xl font-bold mt-1">{formatYen(totalValue)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-slate-500">含み損益</p>
            <p className={`text-xl font-bold mt-1 ${totalPnl >= 0 ? "text-green-600" : "text-red-600"}`}>
              {totalPnl >= 0 ? "+" : ""}{formatYen(totalPnl)}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-slate-500">損益率</p>
            <p className={`text-xl font-bold mt-1 ${totalPnlPct >= 0 ? "text-green-600" : "text-red-600"}`}>
              {totalPnlPct >= 0 ? "+" : ""}{totalPnlPct.toFixed(2)}%
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 保有銘柄一覧 */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>保有銘柄</CardTitle>
            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
              <DialogTrigger asChild>
                <Button size="sm">取引を記録</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>取引登録</DialogTitle>
                </DialogHeader>
                <TradeForm
                  onSuccess={() => {
                    setDialogOpen(false);
                    mutate();
                  }}
                />
              </DialogContent>
            </Dialog>
          </CardHeader>
          <CardContent className="space-y-3">
            {items.length === 0 ? (
              <p className="text-sm text-slate-400 text-center py-4">保有銘柄がありません</p>
            ) : (
              items.map((item) => <HoldingCard key={item.id} item={item} />)
            )}
          </CardContent>
        </Card>

        {/* セクター配分チャート */}
        <Card>
          <CardHeader>
            <CardTitle>セクター別配分</CardTitle>
          </CardHeader>
          <CardContent>
            <PortfolioChart items={items} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
