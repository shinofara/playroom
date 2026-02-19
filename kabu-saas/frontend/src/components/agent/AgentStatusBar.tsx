"use client";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

type Props = {
  readonly pipelineStatus: string;
  readonly lastRun: string | null;
  readonly onRunPipeline: () => void;
  readonly isRunning: boolean;
};

const statusConfig: Record<string, { label: string; variant: "default" | "secondary" | "destructive" | "outline" }> = {
  not_run: { label: "未実行", variant: "outline" },
  running: { label: "実行中...", variant: "secondary" },
  completed: { label: "完了", variant: "default" },
  failed: { label: "失敗", variant: "destructive" },
};

export const AgentStatusBar = ({ pipelineStatus, lastRun, onRunPipeline, isRunning }: Props) => {
  const config = statusConfig[pipelineStatus] ?? statusConfig.not_run;

  return (
    <div className="flex items-center justify-between bg-slate-50 border border-slate-200 rounded-lg px-4 py-3">
      <div className="flex items-center gap-3">
        <span className="text-sm font-medium text-slate-700">分析パイプライン</span>
        <Badge variant={config.variant}>{config.label}</Badge>
        {lastRun && (
          <span className="text-xs text-slate-400">
            最終実行: {new Date(lastRun).toLocaleString("ja-JP")}
          </span>
        )}
      </div>
      <Button
        size="sm"
        onClick={onRunPipeline}
        disabled={isRunning}
      >
        {isRunning ? "実行中..." : "パイプライン実行"}
      </Button>
    </div>
  );
};
