"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { SignalList } from "@/components/signals/SignalList";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { useSWRFetch } from "@/hooks/useSWRFetch";
import type { Signal } from "@/types";

export default function SignalsPage() {
  const { data: buySignals, isLoading: buyLoading } = useSWRFetch<Signal[]>("/signals/buy");
  const { data: sellSignals, isLoading: sellLoading } = useSWRFetch<Signal[]>("/signals/sell");

  if (buyLoading || sellLoading) {
    return <LoadingSpinner message="シグナルを読み込み中..." />;
  }

  // スコア順にソート（降順）
  const sortedBuy = [...(buySignals ?? [])].sort((a, b) => b.score - a.score);
  const sortedSell = [...(sellSignals ?? [])].sort((a, b) => b.score - a.score);

  return (
    <div className="space-y-4">
      <Tabs defaultValue="buy">
        <TabsList>
          <TabsTrigger value="buy">
            買いシグナル ({sortedBuy.length})
          </TabsTrigger>
          <TabsTrigger value="sell">
            売りシグナル ({sortedSell.length})
          </TabsTrigger>
        </TabsList>
        <TabsContent value="buy" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>買いシグナル一覧</CardTitle>
            </CardHeader>
            <CardContent>
              <SignalList signals={sortedBuy} />
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="sell" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>売りシグナル一覧</CardTitle>
            </CardHeader>
            <CardContent>
              <SignalList signals={sortedSell} />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
