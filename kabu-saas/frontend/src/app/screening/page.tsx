"use client";

import { useState, type FormEvent } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { StockTable } from "@/components/stocks/StockTable";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { executeScreening } from "@/lib/api";
import type { Stock, ScreeningCriteria, PaginatedResponse } from "@/types";

export default function ScreeningPage() {
  const [results, setResults] = useState<PaginatedResponse<Stock & { score?: number }> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData(e.currentTarget);
    const criteria: ScreeningCriteria = {
      market: formData.get("market") as string || undefined,
      per_min: formData.get("per_min") ? Number(formData.get("per_min")) : undefined,
      per_max: formData.get("per_max") ? Number(formData.get("per_max")) : undefined,
      pbr_min: formData.get("pbr_min") ? Number(formData.get("pbr_min")) : undefined,
      pbr_max: formData.get("pbr_max") ? Number(formData.get("pbr_max")) : undefined,
      dividend_yield_min: formData.get("dividend_yield_min") ? Number(formData.get("dividend_yield_min")) : undefined,
      rsi_min: formData.get("rsi_min") ? Number(formData.get("rsi_min")) : undefined,
      rsi_max: formData.get("rsi_max") ? Number(formData.get("rsi_max")) : undefined,
      min_volume: formData.get("min_volume") ? Number(formData.get("min_volume")) : undefined,
      min_score: formData.get("min_score") ? Number(formData.get("min_score")) : undefined,
    };

    try {
      const data = await executeScreening(criteria);
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "スクリーニングに失敗しました");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
      {/* フィルタパネル */}
      <Card className="lg:col-span-1">
        <CardHeader>
          <CardTitle>条件指定</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label>市場</Label>
              <Select name="market">
                <SelectTrigger>
                  <SelectValue placeholder="全市場" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">全市場</SelectItem>
                  <SelectItem value="プライム">プライム</SelectItem>
                  <SelectItem value="スタンダード">スタンダード</SelectItem>
                  <SelectItem value="グロース">グロース</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>PER</Label>
              <div className="flex gap-2 items-center">
                <Input name="per_min" type="number" step="0.1" placeholder="下限" className="w-full" />
                <span className="text-slate-400">〜</span>
                <Input name="per_max" type="number" step="0.1" placeholder="上限" className="w-full" />
              </div>
            </div>

            <div className="space-y-2">
              <Label>PBR</Label>
              <div className="flex gap-2 items-center">
                <Input name="pbr_min" type="number" step="0.01" placeholder="下限" className="w-full" />
                <span className="text-slate-400">〜</span>
                <Input name="pbr_max" type="number" step="0.01" placeholder="上限" className="w-full" />
              </div>
            </div>

            <div className="space-y-2">
              <Label>配当利回り（%以上）</Label>
              <Input name="dividend_yield_min" type="number" step="0.1" placeholder="例: 3.0" />
            </div>

            <div className="space-y-2">
              <Label>RSI</Label>
              <div className="flex gap-2 items-center">
                <Input name="rsi_min" type="number" step="1" placeholder="下限" className="w-full" />
                <span className="text-slate-400">〜</span>
                <Input name="rsi_max" type="number" step="1" placeholder="上限" className="w-full" />
              </div>
            </div>

            <div className="space-y-2">
              <Label>最低出来高</Label>
              <Input name="min_volume" type="number" placeholder="例: 100000" />
            </div>

            <div className="space-y-2">
              <Label>最低スコア</Label>
              <Input name="min_score" type="number" step="1" placeholder="例: 60" />
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "検索中..." : "スクリーニング実行"}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* 結果テーブル */}
      <div className="lg:col-span-3">
        <Card>
          <CardHeader>
            <CardTitle>
              スクリーニング結果
              {results && <span className="text-sm font-normal text-slate-500 ml-2">{results.total}件</span>}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <LoadingSpinner message="スクリーニング中..." />
            ) : error ? (
              <p className="text-sm text-red-600 text-center py-4">{error}</p>
            ) : results ? (
              <StockTable stocks={results.items} />
            ) : (
              <p className="text-sm text-slate-400 text-center py-8">
                条件を指定してスクリーニングを実行してください
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
