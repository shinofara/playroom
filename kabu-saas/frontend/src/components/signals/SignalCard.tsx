"use client";

import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import type { Signal } from "@/types";

type Props = {
  readonly signal: Signal;
};

// スコアに応じた色分け
const getScoreColor = (score: number) => {
  if (score >= 80) return "text-green-700 bg-green-100";
  if (score >= 60) return "text-blue-700 bg-blue-100";
  if (score >= 40) return "text-yellow-700 bg-yellow-100";
  return "text-red-700 bg-red-100";
};

const getSignalLabel = (type: "buy" | "sell") =>
  type === "buy" ? "買い" : "売り";

const getSignalColor = (type: "buy" | "sell") =>
  type === "buy" ? "default" : "destructive";

export const SignalCard = ({ signal }: Props) => (
  <Card className="hover:shadow-md transition-shadow">
    <CardContent className="p-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Badge variant={getSignalColor(signal.signal_type)}>
            {getSignalLabel(signal.signal_type)}
          </Badge>
          <Link
            href={`/stocks/${signal.stock?.code ?? signal.stock_id}`}
            className="font-semibold text-slate-800 hover:text-blue-600"
          >
            {signal.stock?.name ?? `銘柄ID: ${signal.stock_id}`}
          </Link>
          <span className="text-sm text-slate-500">{signal.stock?.code}</span>
        </div>
        <div className={`px-3 py-1 rounded-full text-sm font-bold ${getScoreColor(signal.score)}`}>
          {signal.score.toFixed(1)}
        </div>
      </div>
      {signal.reasons.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1">
          {signal.reasons.slice(0, 3).map((reason, i) => (
            <span key={i} className="text-xs text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
              {reason.indicator}: {reason.description}
            </span>
          ))}
        </div>
      )}
      <p className="mt-1 text-xs text-slate-400">{signal.date}</p>
    </CardContent>
  </Card>
);
