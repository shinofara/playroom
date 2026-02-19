"use client";

import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import type { TechnicalIndicator } from "@/types";

type Props = {
  readonly technicals: TechnicalIndicator[];
  readonly type: "rsi" | "macd";
};

const formatDate = (dateStr: string) => {
  const d = new Date(dateStr);
  return `${d.getMonth() + 1}/${d.getDate()}`;
};

// RSIチャート
const RSIChart = ({ data }: { data: TechnicalIndicator[] }) => (
  <ResponsiveContainer width="100%" height={200}>
    <ComposedChart data={data} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
      <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
      <XAxis
        dataKey="date"
        tickFormatter={formatDate}
        tick={{ fontSize: 10, fill: "#94a3b8" }}
        interval="preserveStartEnd"
      />
      <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: "#94a3b8" }} width={40} />
      <Tooltip />
      {/* 売られすぎ/買われすぎライン */}
      <ReferenceLine y={70} stroke="#ef4444" strokeDasharray="3 3" label="70" />
      <ReferenceLine y={30} stroke="#22c55e" strokeDasharray="3 3" label="30" />
      <Line
        type="monotone"
        dataKey="rsi_14"
        stroke="#6366f1"
        dot={false}
        strokeWidth={2}
        name="RSI(14)"
        connectNulls
      />
    </ComposedChart>
  </ResponsiveContainer>
);

// MACDチャート
const MACDChart = ({ data }: { data: TechnicalIndicator[] }) => (
  <ResponsiveContainer width="100%" height={200}>
    <ComposedChart data={data} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
      <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
      <XAxis
        dataKey="date"
        tickFormatter={formatDate}
        tick={{ fontSize: 10, fill: "#94a3b8" }}
        interval="preserveStartEnd"
      />
      <YAxis tick={{ fontSize: 10, fill: "#94a3b8" }} width={50} />
      <Tooltip />
      <ReferenceLine y={0} stroke="#94a3b8" />
      <Bar dataKey="macd_histogram" fill="#94a3b8" name="ヒストグラム" isAnimationActive={false} />
      <Line
        type="monotone"
        dataKey="macd_line"
        stroke="#3b82f6"
        dot={false}
        strokeWidth={2}
        name="MACD"
        connectNulls
      />
      <Line
        type="monotone"
        dataKey="macd_signal"
        stroke="#f97316"
        dot={false}
        strokeWidth={2}
        name="シグナル"
        connectNulls
      />
    </ComposedChart>
  </ResponsiveContainer>
);

export const IndicatorChart = ({ technicals, type }: Props) => {
  if (technicals.length === 0) {
    return (
      <div className="flex items-center justify-center h-48 text-slate-400">
        データがありません
      </div>
    );
  }

  return type === "rsi" ? <RSIChart data={technicals} /> : <MACDChart data={technicals} />;
};
