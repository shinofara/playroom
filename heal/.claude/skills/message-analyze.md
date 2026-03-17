---
name: message-analyze
description: マッチング中の相手とのメッセージ履歴を分析し、返信案を提案する
user_invocable: true
---

# メッセージ分析スキル

マッチング中の相手とのメッセージ履歴を取得・分析し、最適な返信を提案する。

## 手順

1. `.claude/knowledge/target_profiles.md` からマッチング中の相手を確認
2. Playwright MCPで `https://my.healmate.jp/talklist` にアクセス
3. 対象のメッセージスレッドを開いて会話履歴を取得
4. 分析:
   - 会話の温度感（盛り上がり度）
   - 相手の返信速度・文量
   - 話題の流れ
   - 次に振るべき話題の提案
5. 返信案を生成

## 返信作成ガイドライン
- 相手の文量に合わせる（長すぎない）
- 相手の質問には必ず答える
- 新しい話題か深掘りのどちらかを含める
- デートに誘うタイミングの判断

## 出力

- 会話分析レポート
- 返信案2〜3パターン
- `data/messages/{code}_YYYYMMDD.json` に保存
- `.claude/knowledge/target_profiles.md` のステータスを更新
