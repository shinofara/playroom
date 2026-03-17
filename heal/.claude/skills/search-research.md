---
name: search-research
description: Healmateの検索機能を使って好みに合う女性をリサーチする
user_invocable: true
---

# 検索リサーチスキル

Healmateの検索機能を使い、ユーザーの好みに合う相手を効率的にリサーチする。

## 手順

1. `.claude/knowledge/user_preferences.md` の好み基準を読み込む
2. Playwright MCPで `https://my.healmate.jp/search` にアクセス
3. 検索条件を設定:
   - 年齢: 27〜38歳
   - 地域: 東京都、神奈川県
   - メイン写真あり
4. 検索結果を巡回し、候補をリストアップ
5. 有望な候補のプロフィール詳細を取得（profile-fetchスキルと連携）
6. スコアリングして優先順位を付ける

## スコアリング基準
`.claude/knowledge/user_preferences.md` に準拠

## 出力

- 候補一覧をスコア付きテーブルで表示
- 上位候補のプロフィール要約を添える
- いいね送信の推奨を提示
- `data/likes/research_YYYYMMDD.json` に保存
