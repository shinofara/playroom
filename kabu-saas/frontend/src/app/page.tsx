"use client";

import { useState, useCallback } from "react";
import { useSWRFetch } from "@/hooks/useSWRFetch";
import { triggerPipeline } from "@/lib/api";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { AgentStatusBar } from "@/components/agent/AgentStatusBar";
import { ActionList } from "@/components/agent/ActionList";
import { StockDetailDrawer } from "@/components/agent/StockDetailDrawer";
import type { TodayActions, OrderRecommendation } from "@/types";

export default function AgentPage() {
  const { data, isLoading, mutate } = useSWRFetch<TodayActions>("/agent/today-actions");
  const [selectedRec, setSelectedRec] = useState<OrderRecommendation | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  const handleRunPipeline = useCallback(async () => {
    setIsRunning(true);
    try {
      await triggerPipeline();
      // 定期的にステータスを更新
      const poll = setInterval(async () => {
        const updated = await mutate();
        if (updated && updated.pipeline_status !== "running") {
          clearInterval(poll);
          setIsRunning(false);
        }
      }, 5000);
    } catch {
      setIsRunning(false);
    }
  }, [mutate]);

  if (isLoading) {
    return <LoadingSpinner message="エージェントデータを読み込み中..." />;
  }

  const pipelineRunning = isRunning || data?.pipeline_status === "running";

  return (
    <div className="space-y-6">
      {/* ヘッダー */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">売買エージェント</h1>
        <p className="text-sm text-slate-500 mt-1">
          {data?.summary ?? "分析パイプラインを実行して推奨アクションを取得してください。"}
        </p>
      </div>

      {/* パイプライン状態 */}
      <AgentStatusBar
        pipelineStatus={data?.pipeline_status ?? "not_run"}
        lastRun={data?.pipeline_last_run ?? null}
        onRunPipeline={handleRunPipeline}
        isRunning={pipelineRunning}
      />

      {/* 買い推奨 */}
      <ActionList
        title="買い推奨"
        recommendations={data?.buy_recommendations ?? []}
        onCardClick={setSelectedRec}
        emptyMessage="買い推奨はありません"
      />

      {/* 売り推奨 */}
      <ActionList
        title="売り推奨"
        recommendations={data?.sell_recommendations ?? []}
        onCardClick={setSelectedRec}
        emptyMessage="売り推奨はありません"
      />

      {/* 銘柄詳細ドロワー */}
      <StockDetailDrawer
        recommendation={selectedRec}
        open={selectedRec !== null}
        onClose={() => setSelectedRec(null)}
      />
    </div>
  );
}
