"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

// ナビゲーション項目定義
const navItems = [
  { href: "/", label: "売買エージェント", icon: "🤖" },
  { href: "/stocks", label: "銘柄一覧", icon: "📈" },
  { href: "/signals", label: "シグナル", icon: "🔔" },
  { href: "/screening", label: "スクリーニング", icon: "🔍" },
  { href: "/portfolio", label: "ポートフォリオ", icon: "💼" },
  { href: "/watchlist", label: "ウォッチリスト", icon: "⭐" },
] as const;

export const Sidebar = () => {
  const pathname = usePathname();

  return (
    <aside className="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0 bg-slate-900 text-white">
      {/* ロゴ */}
      <div className="flex items-center h-16 px-6 border-b border-slate-700">
        <Link href="/" className="text-xl font-bold tracking-tight">
          Kabu Agent
        </Link>
      </div>

      {/* ナビゲーション */}
      <nav className="flex-1 px-3 py-4 space-y-1">
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
    </aside>
  );
};
