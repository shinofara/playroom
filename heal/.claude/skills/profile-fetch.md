---
name: profile-fetch
description: 指定した相手のプロフィール詳細をPlaywright MCPで取得し保存する
user_invocable: true
---

# プロフィール取得スキル

指定した相手（コードまたは名前）のプロフィール詳細をPlaywright MCPで取得する。

## 手順

1. 引数でcodeまたは名前が指定された場合、そのプロフィールページに直接アクセス
   - URL: `https://my.healmate.jp/detail?code={code}`
2. 指定がない場合、お気に入りリストまたは検索結果から対象を選択
3. プロフィール詳細を構造化して取得:
   - 名前、年齢、地域、職業
   - 自己紹介文
   - 容姿・外見（身長、体型）
   - 基本プロフィール（血液型、学歴、収入）
   - 家族状況
   - 性格・プライベート（性格、MBTI、趣味、お酒、たばこ）
   - お相手に対して・希望
   - メッセージ付きいいねの内容
   - 写真の有無・枚数
4. スクリーンショットも撮影（写真確認用）

## 出力

- プロフィール要約を表示
- `data/profiles/{code}.json` に保存
- 必要に応じて `.claude/knowledge/target_profiles.md` に追記
