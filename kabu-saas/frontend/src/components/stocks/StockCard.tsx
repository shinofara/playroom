"use client";

import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Stock } from "@/types";

type Props = {
  readonly stock: Stock;
  readonly price?: number;
  readonly change?: number;
  readonly changePct?: number;
};

export const StockCard = ({ stock, price, change, changePct }: Props) => {
  const isPositive = (change ?? 0) >= 0;

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div>
            <Link
              href={`/stocks/${stock.code}`}
              className="font-semibold text-slate-800 hover:text-blue-600"
            >
              {stock.name}
            </Link>
            <div className="flex items-center gap-2 mt-1">
              <span className="text-sm text-slate-500">{stock.code}</span>
              <Badge variant="outline" className="text-xs">
                {stock.sector}
              </Badge>
            </div>
          </div>
          {price != null && (
            <div className="text-right">
              <p className="text-lg font-bold">
                ¥{new Intl.NumberFormat("ja-JP").format(price)}
              </p>
              {change != null && changePct != null && (
                <p className={`text-sm font-medium ${isPositive ? "text-green-600" : "text-red-600"}`}>
                  {isPositive ? "+" : ""}{change.toFixed(0)} ({isPositive ? "+" : ""}{changePct.toFixed(2)}%)
                </p>
              )}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
