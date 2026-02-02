# Ops Standard（運用の約束）v0.1

この文書は、Starley / Cotomo のプロダクト開発チームが「価値を守る（ユーザが使える状態を維持する）」ための運用の約束です。

- 文体は「〜しよう / 〜としよう」で統一しよう
- 迷ったら「P1を見逃さない」方向に倒そう（あとで下げてもよい）

---

## 1. 目的
- ユーザが使えない状態を最短で解消しよう
- 「どこを見るか」「どこで宣言するか」「誰に助けを求めるか」をそろえよう

## 2. 対象
- プロダクト運用に関わる全員（正社員・業務委託をふくむ）
- 本番リリース後の確認、障害対応、オンコール運用

---

## 3. 障害（Incident）の考え方

### 3.1 一時的でも、コア価値がこわれたら障害として扱おう
- 「原因が外部」でも同じように扱おう（クラウド、決済、認証など）
- まずは復旧しよう（原因調査は復旧のあとでよい）

### 3.2 優先順位（P1）を決めよう
現時点の Starley では、次を **P1（最優先）** としよう。

#### P1（最優先で直そう）
1. **全員が使えないようなインフラ・APIなどの問題**
2. **課金に関する問題**
3. **コア体験の会話が、システム起因で止まること**（特に課金しているケース）

---

## 4. 見る場所（入口）

### 4.1 インフラ（GCP Monitoring）
- Slack（インフラ/基盤アラート）: `#cotomo-alert-production`
- Dashboard:
  - https://console.cloud.google.com/monitoring/dashboards/builder/0cdb568f-5c0f-4e5b-b2e6-36001557fc80?project=starley-mate-production

### 4.2 アプリ（Sentry）
- Sentry の Issue Alert 通知は、Slack の `#cotomo-error-server-production` に流そう
- ここには **障害ではない通知も流れる**前提で運用しよう

---

## 5. どこで話すか（チャンネル運用）

### 5.1 対応の会話は error-server に集めよう
- `#cotomo-alert-production` は「インフラ通知の入口」として使おう
- `#cotomo-error-server-production` は「Sentry通知 + 障害対応の司令塔」として使おう

インフラ側（alert）でP1を見つけたときも、対応の会話は error-server 側に寄せよう（リンクを貼ろう）。

---

## 6. Sentry通知の扱い（トリアージしよう）

`#cotomo-error-server-production` に Sentry Issue Alert が来たら、まず分類しよう。

1) **P1（最優先）**
- 課金に関する問題の疑いがある
- 会話停止（特に課金ユーザ）の疑いがある
- 全体影響に近いエラー急増の疑いがある

2) **要対応（非P1）**
- 影響は限定的だが放置しない（継続している、増えている、特定顧客影響など）

3) **情報（FYI）**
- 単発、既知、影響が小さい

> 目的は「通知をゼロにする」ことではなく、P1を見逃さないことにしよう。

---

## 7. P1が起きたときの動き方

### 7.1 まずP1宣言しよう（error-server）
`#cotomo-error-server-production` に投稿しよう。

```text
[P1] 発生
- 種別: (全員が使えない / 課金 / 会話停止)
- 入口: (alert-production / sentry)
- 影響: (全員 / 課金ユーザ / 一部)
- 兆候リンク: (Monitoring / Sentry URL)
- まずやること: (ロールバック / 設定戻し / 暫定回避 / 調査)
```

### 7.2 まず復旧しよう（価値毀損を止めよう）
- 原因調査より、復旧を先にしよう
- 迷ったら「戻す」を選びやすくしよう（revert、一部戻し、設定戻し、機能停止など）

### 7.3 復旧は観測で確認しよう
- GCP Monitoring と Sentry で「落ち着いた」ことを確認してから復旧宣言しよう

```text
[P1] 復旧（暫定/完全）
- 対応: (何をしたか)
- 確認:
  - Sentry: (対象エラーが落ちた/0になった、リンク)
  - Monitoring: (5xx/latencyが戻った、リンク)
- 次: (恒久対応 / 再発防止の宿題)
```

### 7.4 あとで仕組みを直そう（ブレームレスでいこう）
- 人を責めないで、仕組みを直そう
- 「気をつける」ではなく、次のどれかで塞ごう
  - アラート条件の調整
  - ダッシュボード整備
  - リリース後確認項目の追加
  - ロールバック容易化

---

## 8. エスカレーション
- 困ったら `@team-backend` でエスカレーションしよう
- 「P1かも」と思った時点で呼んでよい（あとで下げよう）

---

## 9. Weekly オンコール担当スケジュール（育てよう）

### 9.1 ローテーション
1. @Yu-Hsing Hsieh
2. @yuki shinohara
3. @Siwat Pruksapanya
4. @Jacky Ye
5. @Goro / 藤吾郎

> 交代のタイミング（例：毎週月曜10:00JST）は、運用しながら決めよう。

### 9.2 有給・不在のとき
- 不在が分かったら早めに相談して、当番を入れ替えよう
- 入れ替えが決まったら、`#cotomo-error-server-production` で共有しよう

---

## 10. リリース後の確認との関係
- ProductionでReleaseを実行した人は、リリース後確認（T+25 / T+45）で次を見よう
  - `#cotomo-alert-production`（インフラ）
  - `#cotomo-error-server-production`（Sentry + 司令塔）
  - GCP Monitoring Dashboard
  - Sentry

---

## 11. （別件）Slack通知が来ないときの切り分け（メモ）
- まず「どの通知が」「どのチャンネルに」来ないかをはっきりさせよう
- GCP Monitoring は `#cotomo-alert-production` を前提に確認しよう
- Sentry Issue Alert は `#cotomo-error-server-production` を前提に確認しよう

