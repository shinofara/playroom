"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { addTransaction } from "@/lib/api";

type Props = {
  readonly onSuccess?: () => void;
};

export const TradeForm = ({ onSuccess }: Props) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const formData = new FormData(e.currentTarget);
    try {
      await addTransaction({
        stock_id: Number(formData.get("stock_id")),
        transaction_type: formData.get("transaction_type") as "buy" | "sell",
        quantity: Number(formData.get("quantity")),
        price: Number(formData.get("price")),
        commission: Number(formData.get("commission") || 0),
        transaction_date: formData.get("transaction_date") as string,
        notes: (formData.get("notes") as string) || undefined,
      });
      onSuccess?.();
      (e.target as HTMLFormElement).reset();
    } catch (err) {
      setError(err instanceof Error ? err.message : "取引の登録に失敗しました");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="stock_id">銘柄ID</Label>
          <Input id="stock_id" name="stock_id" type="number" required placeholder="例: 1" />
        </div>
        <div className="space-y-2">
          <Label htmlFor="transaction_type">売買区分</Label>
          <Select name="transaction_type" defaultValue="buy">
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="buy">買い</SelectItem>
              <SelectItem value="sell">売り</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2">
          <Label htmlFor="quantity">数量</Label>
          <Input id="quantity" name="quantity" type="number" required placeholder="例: 100" />
        </div>
        <div className="space-y-2">
          <Label htmlFor="price">約定単価</Label>
          <Input id="price" name="price" type="number" step="0.01" required placeholder="例: 1500" />
        </div>
        <div className="space-y-2">
          <Label htmlFor="commission">手数料</Label>
          <Input id="commission" name="commission" type="number" step="0.01" defaultValue="0" />
        </div>
        <div className="space-y-2">
          <Label htmlFor="transaction_date">約定日</Label>
          <Input id="transaction_date" name="transaction_date" type="date" required />
        </div>
      </div>
      <div className="space-y-2">
        <Label htmlFor="notes">メモ</Label>
        <Textarea id="notes" name="notes" placeholder="取引メモ（任意）" rows={2} />
      </div>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <Button type="submit" disabled={loading} className="w-full">
        {loading ? "登録中..." : "取引を登録"}
      </Button>
    </form>
  );
};
