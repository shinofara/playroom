"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { useSWRFetch } from "@/hooks/useSWRFetch";
import type { TradePlan } from "@/types";

// 金額フォーマット
const formatYen = (value: number) =>
  `¥${new Intl.NumberFormat("ja-JP").format(Math.round(value))}`;

// スコアバッジの色
const getScoreBadge = (score: number) => {
  if (score >= 80) return "default";
  if (score >= 60) return "secondary";
  return "outline";
};

export default function PlansPage() {
  const { data: plans, isLoading } = useSWRFetch<TradePlan[]>("/trade-plans");

  if (isLoading) {
    return <LoadingSpinner message="売買プランを読み込み中..." />;
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>売買プラン一覧</CardTitle>
        </CardHeader>
        <CardContent>
          {(plans ?? []).length === 0 ? (
            <p className="text-sm text-slate-400 text-center py-8">
              売買プランがありません
            </p>
          ) : (
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>銘柄</TableHead>
                    <TableHead className="text-right">エントリー価格</TableHead>
                    <TableHead className="text-right">利確（1段階目）</TableHead>
                    <TableHead className="text-right">損切り</TableHead>
                    <TableHead className="text-right">リスクリワード比</TableHead>
                    <TableHead className="text-right">ポジションサイズ</TableHead>
                    <TableHead className="text-center">スコア</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {(plans ?? []).map((plan, i) => (
                    <TableRow key={i}>
                      <TableCell>
                        <Link
                          href={`/stocks/${plan.stock.code}`}
                          className="font-medium hover:text-blue-600"
                        >
                          {plan.stock.name}
                        </Link>
                        <span className="text-xs text-slate-400 ml-2">{plan.stock.code}</span>
                      </TableCell>
                      <TableCell className="text-right font-mono">
                        {formatYen(plan.entry_price)}
                      </TableCell>
                      <TableCell className="text-right">
                        {plan.take_profit_levels.length > 0 ? (
                          <span className="text-green-600 font-mono">
                            {formatYen(plan.take_profit_levels[0].price)}
                            <span className="text-xs ml-1">(+{plan.take_profit_levels[0].pct.toFixed(1)}%)</span>
                          </span>
                        ) : (
                          "-"
                        )}
                      </TableCell>
                      <TableCell className="text-right">
                        <span className="text-red-600 font-mono">
                          {formatYen(plan.stop_loss_price)}
                          <span className="text-xs ml-1">({plan.stop_loss_pct.toFixed(1)}%)</span>
                        </span>
                      </TableCell>
                      <TableCell className="text-right font-bold">
                        {plan.risk_reward_ratio.toFixed(2)}
                      </TableCell>
                      <TableCell className="text-right font-mono">
                        {plan.position_size}株
                      </TableCell>
                      <TableCell className="text-center">
                        <Badge variant={getScoreBadge(plan.score)}>
                          {plan.score.toFixed(1)}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
