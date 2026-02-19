"use client";

import { ActionCard } from "./ActionCard";
import type { OrderRecommendation } from "@/types";

type Props = {
  readonly title: string;
  readonly recommendations: OrderRecommendation[];
  readonly onCardClick?: (rec: OrderRecommendation) => void;
  readonly emptyMessage?: string;
};

export const ActionList = ({ title, recommendations, onCardClick, emptyMessage }: Props) => {
  return (
    <section>
      <h2 className="text-lg font-semibold text-slate-800 mb-3">
        {title}
        {recommendations.length > 0 && (
          <span className="text-sm font-normal text-slate-400 ml-2">
            {recommendations.length}銘柄
          </span>
        )}
      </h2>
      {recommendations.length === 0 ? (
        <p className="text-sm text-slate-400 text-center py-6 bg-slate-50 rounded-lg">
          {emptyMessage ?? "該当する推奨はありません"}
        </p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {recommendations.map((rec) => (
            <ActionCard
              key={`${rec.stock_code}-${rec.action}`}
              recommendation={rec}
              onClick={() => onCardClick?.(rec)}
            />
          ))}
        </div>
      )}
    </section>
  );
};
