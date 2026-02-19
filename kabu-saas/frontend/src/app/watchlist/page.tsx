"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { useSWRFetch } from "@/hooks/useSWRFetch";
import { createWatchlist, deleteWatchlistItem } from "@/lib/api";
import type { Watchlist } from "@/types";
import Link from "next/link";

export default function WatchlistPage() {
  const { data: watchlists, isLoading, mutate } = useSWRFetch<Watchlist[]>("/watchlists");
  const [newListName, setNewListName] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [creating, setCreating] = useState(false);

  const handleCreateWatchlist = async () => {
    if (!newListName.trim()) return;
    setCreating(true);
    try {
      await createWatchlist(newListName.trim());
      setNewListName("");
      setDialogOpen(false);
      mutate();
    } catch {
      // エラー処理
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteItem = async (watchlistId: number, itemId: number) => {
    try {
      await deleteWatchlistItem(watchlistId, itemId);
      mutate();
    } catch {
      // エラー処理
    }
  };

  if (isLoading) {
    return <LoadingSpinner message="ウォッチリストを読み込み中..." />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-slate-800">ウォッチリスト</h2>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button size="sm">新規作成</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>ウォッチリストを作成</DialogTitle>
            </DialogHeader>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label>リスト名</Label>
                <Input
                  value={newListName}
                  onChange={(e) => setNewListName(e.target.value)}
                  placeholder="例: 高配当銘柄"
                />
              </div>
              <Button onClick={handleCreateWatchlist} disabled={creating} className="w-full">
                {creating ? "作成中..." : "作成"}
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {(watchlists ?? []).length === 0 ? (
        <Card>
          <CardContent className="py-8">
            <p className="text-sm text-slate-400 text-center">ウォッチリストがありません</p>
          </CardContent>
        </Card>
      ) : (
        (watchlists ?? []).map((wl) => (
          <Card key={wl.id}>
            <CardHeader>
              <CardTitle>{wl.name}</CardTitle>
            </CardHeader>
            <CardContent>
              {(wl.items ?? []).length === 0 ? (
                <p className="text-sm text-slate-400 text-center py-4">銘柄が登録されていません</p>
              ) : (
                <div className="rounded-md border">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>コード</TableHead>
                        <TableHead>銘柄名</TableHead>
                        <TableHead>セクター</TableHead>
                        <TableHead>アラート</TableHead>
                        <TableHead>メモ</TableHead>
                        <TableHead className="w-[80px]" />
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {(wl.items ?? []).map((item) => (
                        <TableRow key={item.id}>
                          <TableCell className="font-mono text-sm">{item.stock?.code ?? "-"}</TableCell>
                          <TableCell>
                            <Link
                              href={`/stocks/${item.stock?.code ?? item.stock_id}`}
                              className="font-medium hover:text-blue-600"
                            >
                              {item.stock?.name ?? `ID: ${item.stock_id}`}
                            </Link>
                          </TableCell>
                          <TableCell>
                            <Badge variant="outline" className="text-xs">
                              {item.stock?.sector ?? "-"}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            <Badge variant={item.alert_enabled ? "default" : "secondary"} className="text-xs">
                              {item.alert_enabled ? "ON" : "OFF"}
                            </Badge>
                          </TableCell>
                          <TableCell className="text-sm text-slate-500 max-w-[200px] truncate">
                            {item.memo ?? "-"}
                          </TableCell>
                          <TableCell>
                            <Button
                              variant="ghost"
                              size="sm"
                              className="text-red-500 hover:text-red-700"
                              onClick={() => handleDeleteItem(wl.id, item.id)}
                            >
                              削除
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              )}
            </CardContent>
          </Card>
        ))
      )}
    </div>
  );
}
