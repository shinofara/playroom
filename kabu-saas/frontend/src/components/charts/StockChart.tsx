"use client";

import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import type { StockPrice, TechnicalIndicator } from "@/types";

type Props = {
  readonly prices: StockPrice[];
  readonly technicals?: TechnicalIndicator[];
  readonly showSMA?: boolean;
  readonly showBB?: boolean;
};

// 株価チャートデータの結合
const mergeData = (prices: StockPrice[], technicals?: TechnicalIndicator[]) =>
  prices.map((p) => {
    const tech = technicals?.find((t) => t.date === p.date);
    return {
      date: p.date,
      open: p.open,
      high: p.high,
      low: p.low,
      close: p.close,
      volume: p.volume,
      sma_25: tech?.sma_25,
      sma_75: tech?.sma_75,
      bb_upper_2: tech?.bb_upper_2,
      bb_lower_2: tech?.bb_lower_2,
    };
  });

// 日付フォーマット
const formatDate = (dateStr: string) => {
  const d = new Date(dateStr);
  return `${d.getMonth() + 1}/${d.getDate()}`;
};

// 価格フォーマット
const formatPrice = (value: number) =>
  new Intl.NumberFormat("ja-JP").format(value);

// カスタムローソク足（簡易版 - 棒グラフで表現）
const CandlestickBar = (props: Record<string, unknown>) => {
  const { x, y, width, height, payload } = props as {
    x: number; y: number; width: number; height: number;
    payload: { open: number; close: number; high: number; low: number };
  };
  const isUp = payload.close >= payload.open;
  const color = isUp ? "#22c55e" : "#ef4444";

  return (
    <g>
      <rect
        x={x}
        y={y}
        width={width}
        height={Math.max(height, 1)}
        fill={color}
        stroke={color}
      />
    </g>
  );
};

export const StockChart = ({ prices, technicals, showSMA = true, showBB = false }: Props) => {
  const data = mergeData(prices, technicals);

  if (data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        データがありません
      </div>
    );
  }

  return (
    <div className="w-full space-y-2">
      {/* 株価チャート */}
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart data={data} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis
            dataKey="date"
            tickFormatter={formatDate}
            tick={{ fontSize: 11, fill: "#94a3b8" }}
            interval="preserveStartEnd"
          />
          <YAxis
            domain={["auto", "auto"]}
            tickFormatter={formatPrice}
            tick={{ fontSize: 11, fill: "#94a3b8" }}
            width={70}
          />
          <Tooltip
            formatter={(value) => formatPrice(Number(value))}
            labelFormatter={(label) => String(label)}
          />

          {/* ローソク足の代替: 終値の棒グラフ */}
          <Bar
            dataKey="close"
            shape={<CandlestickBar />}
            isAnimationActive={false}
          />

          {/* 移動平均線 */}
          {showSMA && (
            <>
              <Line
                type="monotone"
                dataKey="sma_25"
                stroke="#f59e0b"
                dot={false}
                strokeWidth={1.5}
                name="SMA25"
                connectNulls
              />
              <Line
                type="monotone"
                dataKey="sma_75"
                stroke="#8b5cf6"
                dot={false}
                strokeWidth={1.5}
                name="SMA75"
                connectNulls
              />
            </>
          )}

          {/* ボリンジャーバンド */}
          {showBB && (
            <>
              <Line
                type="monotone"
                dataKey="bb_upper_2"
                stroke="#94a3b8"
                dot={false}
                strokeWidth={1}
                strokeDasharray="5 5"
                name="BB+2σ"
                connectNulls
              />
              <Line
                type="monotone"
                dataKey="bb_lower_2"
                stroke="#94a3b8"
                dot={false}
                strokeWidth={1}
                strokeDasharray="5 5"
                name="BB-2σ"
                connectNulls
              />
            </>
          )}
        </ComposedChart>
      </ResponsiveContainer>

      {/* 出来高チャート */}
      <ResponsiveContainer width="100%" height={100}>
        <ComposedChart data={data} margin={{ top: 0, right: 10, left: 10, bottom: 0 }}>
          <XAxis dataKey="date" hide />
          <YAxis hide />
          <Bar dataKey="volume" fill="#cbd5e1" isAnimationActive={false} />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};
