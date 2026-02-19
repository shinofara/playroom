"use client";

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";
import type { PortfolioItem } from "@/types";

type Props = {
  readonly items: PortfolioItem[];
};

// セクター別の配色
const COLORS = [
  "#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6",
  "#ec4899", "#14b8a6", "#f97316", "#6366f1", "#84cc16",
];

// セクター別に集計
const aggregateBySector = (items: PortfolioItem[]) => {
  const sectorMap = new Map<string, number>();
  items.forEach((item) => {
    const sector = item.stock?.sector ?? "不明";
    const value = item.quantity * item.avg_purchase_price;
    sectorMap.set(sector, (sectorMap.get(sector) ?? 0) + value);
  });
  return Array.from(sectorMap.entries()).map(([name, value]) => ({ name, value }));
};

const formatYen = (value: number) =>
  `¥${new Intl.NumberFormat("ja-JP").format(Math.round(value))}`;

export const PortfolioChart = ({ items }: Props) => {
  const data = aggregateBySector(items);

  if (data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        保有銘柄がありません
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={100}
          dataKey="value"
          nameKey="name"
          label={({ name, percent }) => `${name ?? ""} ${((percent ?? 0) * 100).toFixed(1)}%`}
          labelLine
        >
          {data.map((_, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(value) => formatYen(Number(value))} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};
