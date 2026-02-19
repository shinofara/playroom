"use client";

import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/", label: "ダッシュボード", icon: "📊" },
  { href: "/stocks", label: "銘柄一覧", icon: "📈" },
  { href: "/signals", label: "シグナル", icon: "🔔" },
  { href: "/portfolio", label: "ポートフォリオ", icon: "💼" },
  { href: "/screening", label: "スクリーニング", icon: "🔍" },
  { href: "/watchlist", label: "ウォッチリスト", icon: "⭐" },
  { href: "/plans", label: "売買プラン", icon: "📋" },
] as const;

export const Header = () => {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 bg-white border-b border-slate-200 md:pl-64">
      <div className="flex items-center justify-between h-16 px-4 sm:px-6">
        {/* モバイルメニュー */}
        <Sheet>
          <SheetTrigger asChild>
            <button className="md:hidden p-2 rounded-md hover:bg-slate-100">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </SheetTrigger>
          <SheetContent side="left" className="w-64 p-0 bg-slate-900">
            <div className="flex items-center h-16 px-6 border-b border-slate-700">
              <span className="text-xl font-bold text-white tracking-tight">Kabu SaaS</span>
            </div>
            <nav className="px-3 py-4 space-y-1">
              {navItems.map((item) => {
                const isActive =
                  item.href === "/"
                    ? pathname === "/"
                    : pathname.startsWith(item.href);
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                      isActive
                        ? "bg-slate-700 text-white"
                        : "text-slate-300 hover:bg-slate-800 hover:text-white"
                    )}
                  >
                    <span className="text-lg">{item.icon}</span>
                    {item.label}
                  </Link>
                );
              })}
            </nav>
          </SheetContent>
        </Sheet>

        {/* ページタイトル */}
        <h1 className="text-lg font-semibold text-slate-800 md:text-xl">
          {navItems.find((item) =>
            item.href === "/"
              ? pathname === "/"
              : pathname.startsWith(item.href)
          )?.label ?? "Kabu SaaS"}
        </h1>

        {/* 右側アクション */}
        <div className="flex items-center gap-2">
          <span className="text-sm text-slate-500">
            {new Date().toLocaleDateString("ja-JP")}
          </span>
        </div>
      </div>
    </header>
  );
};
