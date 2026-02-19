"use client";

import { SignalCard } from "./SignalCard";
import type { Signal } from "@/types";

type Props = {
  readonly signals: Signal[];
  readonly title?: string;
};

export const SignalList = ({ signals, title }: Props) => (
  <div className="space-y-3">
    {title && <h3 className="text-lg font-semibold text-slate-800">{title}</h3>}
    {signals.length === 0 ? (
      <p className="text-sm text-slate-400 py-4 text-center">シグナルはありません</p>
    ) : (
      signals.map((signal) => <SignalCard key={signal.id} signal={signal} />)
    )}
  </div>
);
