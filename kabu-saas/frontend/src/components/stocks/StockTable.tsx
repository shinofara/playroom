"use client";

import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { Stock } from "@/types";

type StockWithPrice = Stock & {
  readonly price?: number;
  readonly change?: number;
  readonly change_pct?: number;
  readonly score?: number;
};

type Props = {
  readonly stocks: StockWithPrice[];
  readonly onSort?: (column: string) => void;
  readonly sortBy?: string;
  readonly sortOrder?: "asc" | "desc";
};

const formatPrice = (value: number | undefined) =>
  value != null ? `¥${new Intl.NumberFormat("ja-JP").format(value)}` : "-";

const SortIcon = ({ active, order }: { active: boolean; order: "asc" | "desc" }) => (
  <span className={`ml-1 ${active ? "text-blue-600" : "text-slate-300"}`}>
    {order === "asc" ? "▲" : "▼"}
  </span>
);

export const StockTable = ({ stocks, onSort, sortBy, sortOrder = "asc" }: Props) => {
  const handleSort = (column: string) => onSort?.(column);

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead
              className="cursor-pointer hover:bg-slate-50"
              onClick={() => handleSort("code")}
            >
              コード
              {sortBy === "code" && <SortIcon active order={sortOrder} />}
            </TableHead>
            <TableHead>銘柄名</TableHead>
            <TableHead>セクター</TableHead>
            <TableHead>市場</TableHead>
            <TableHead
              className="text-right cursor-pointer hover:bg-slate-50"
              onClick={() => handleSort("price")}
            >
              株価
              {sortBy === "price" && <SortIcon active order={sortOrder} />}
            </TableHead>
            <TableHead className="text-right">前日比</TableHead>
            <TableHead
              className="text-right cursor-pointer hover:bg-slate-50"
              onClick={() => handleSort("score")}
            >
              スコア
              {sortBy === "score" && <SortIcon active order={sortOrder} />}
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {stocks.length === 0 ? (
            <TableRow>
              <TableCell colSpan={7} className="text-center py-8 text-slate-400">
                銘柄が見つかりません
              </TableCell>
            </TableRow>
          ) : (
            stocks.map((stock) => {
              const isPositive = (stock.change ?? 0) >= 0;
              return (
                <TableRow key={stock.id} className="hover:bg-slate-50">
                  <TableCell className="font-mono text-sm">{stock.code}</TableCell>
                  <TableCell>
                    <Link
                      href={`/stocks/${stock.code}`}
                      className="font-medium text-slate-800 hover:text-blue-600"
                    >
                      {stock.name}
                    </Link>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline" className="text-xs">
                      {stock.sector}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-sm text-slate-500">{stock.market}</TableCell>
                  <TableCell className="text-right font-mono">
                    {formatPrice(stock.price)}
                  </TableCell>
                  <TableCell className="text-right">
                    {stock.change != null && stock.change_pct != null ? (
                      <span className={`text-sm font-medium ${isPositive ? "text-green-600" : "text-red-600"}`}>
                        {isPositive ? "+" : ""}{stock.change_pct.toFixed(2)}%
                      </span>
                    ) : (
                      "-"
                    )}
                  </TableCell>
                  <TableCell className="text-right">
                    {stock.score != null ? (
                      <span className="font-bold">{stock.score.toFixed(1)}</span>
                    ) : (
                      "-"
                    )}
                  </TableCell>
                </TableRow>
              );
            })
          )}
        </TableBody>
      </Table>
    </div>
  );
};
