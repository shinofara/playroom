"use client";

import { useState, useCallback } from "react";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { StockTable } from "@/components/stocks/StockTable";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { useSWRFetch } from "@/hooks/useSWRFetch";
import type { Stock, PaginatedResponse } from "@/types";

export default function StocksPage() {
  const [search, setSearch] = useState("");
  const [market, setMarket] = useState<string>("all");
  const [sortBy, setSortBy] = useState("code");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  // クエリパラメータ構築
  const params = new URLSearchParams();
  if (search) params.set("search", search);
  if (market !== "all") params.set("market", market);
  params.set("sort_by", sortBy);
  params.set("sort_order", sortOrder);

  const { data, isLoading } = useSWRFetch<PaginatedResponse<Stock>>(
    `/stocks?${params.toString()}`
  );

  // ソート切り替え
  const handleSort = useCallback((column: string) => {
    setSortOrder((prev) => (sortBy === column && prev === "asc" ? "desc" : "asc"));
    setSortBy(column);
  }, [sortBy]);

  return (
    <div className="space-y-4">
      {/* フィルタバー */}
      <div className="flex flex-col sm:flex-row gap-3">
        <Input
          placeholder="銘柄名・コードで検索..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="sm:max-w-xs"
        />
        <Select value={market} onValueChange={setMarket}>
          <SelectTrigger className="sm:max-w-[180px]">
            <SelectValue placeholder="市場" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">全市場</SelectItem>
            <SelectItem value="プライム">プライム</SelectItem>
            <SelectItem value="スタンダード">スタンダード</SelectItem>
            <SelectItem value="グロース">グロース</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* テーブル */}
      {isLoading ? (
        <LoadingSpinner message="銘柄一覧を読み込み中..." />
      ) : (
        <>
          <p className="text-sm text-slate-500">
            {data?.total ?? 0}件の銘柄
          </p>
          <StockTable
            stocks={data?.items ?? []}
            onSort={handleSort}
            sortBy={sortBy}
            sortOrder={sortOrder}
          />
        </>
      )}
    </div>
  );
}
