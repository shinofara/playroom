import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Kabu SaaS - 日本株分析プラットフォーム",
  description: "日本株のテクニカル分析・ファンダメンタル分析を行い、買い時シグナルを検出する投資支援ツール",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-slate-50`}
      >
        <Sidebar />
        <div className="md:pl-64 min-h-screen flex flex-col">
          <Header />
          <main className="flex-1 p-4 sm:p-6">{children}</main>
          <Footer />
        </div>
      </body>
    </html>
  );
}
