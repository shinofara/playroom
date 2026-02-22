# Cotomo Sentry 運用ガイド

> **「VPoTが一人で見ている」から「チーム全員で品質を守る」へ**
>
> このドキュメントは、Cotomoのエラー監視ツール Sentry の運用ルールを定めるものである。
> 属人的な監視体制を脱却し、5名のエンジニア全員で持続可能に回す仕組みを構築する。

---

## 目次

1. [現状の課題と変革の目的](#1-現状の課題と変革の目的)
2. [Sentryの位置づけ](#2-sentryの位置づけ)
3. [プロジェクト構成](#3-プロジェクト構成)
4. [当番制（Sentry Duty）](#4-当番制sentry-duty)
5. [トリアージ基準](#5-トリアージ基準)
6. [アラートルール設計](#6-アラートルール設計)
7. [Slack連携](#7-slack連携)
8. [日常オペレーション](#8-日常オペレーション)
9. [リリースとの連携](#9-リリースとの連携)
10. [Issue管理](#10-issue管理)
11. [ノイズ対策](#11-ノイズ対策)
12. [スプリントへの組み込み](#12-スプリントへの組み込み)
13. [オンボーディング](#13-オンボーディング)
14. [メトリクスと振り返り](#14-メトリクスと振り返り)
15. [導入ロードマップ](#15-導入ロードマップ)

---

## 1. 現状の課題と変革の目的

### 現状

- VPoTが Slack で Sentry のアラートに反応し、Issue化して人に投げたり自分で解決している
- 対応可能なエンジニアは VPoT・VPoE を含め5名いるが、実質 VPoT 一人がSentryを監視している
- 他のメンバーは Sentry に対する当事者意識が薄い

### なぜこれが問題か

- **バス係数が1**: VPoTが休暇・体調不良・退職した瞬間に、200万ユーザのサービスのエラー検知能力がゼロになる
- **経営リソースの無駄遣い**: VPoTを「アラート仕分け係」として使っている。戦略的な仕事に集中すべき立場
- **バーンアウトリスク**: 「自分がやらなければ」という責任感で一人が抱え込むパターンは、半年〜1年で破綻する
- **スケーラビリティの限界**: 200万ユーザは「1人で見れる」規模の最終段階。ユーザ成長がそのまま品質劣化に直結する

### 変革の目的

VPoTの役割を「日常監視者」から「エスカレーション先・最終判断者」に再定義し、チーム全員で品質を守る体制を構築する。

---

## 2. Sentryの位置づけ

Sentryは「エラーが出たら見るもの」ではない。**プロダクトの健康状態を映す鏡**である。

### 原則

- Sentry のエラー状況はチーム全員が共有すべきプロダクト品質の指標
- エラー対応は「コスト」ではなく「投資」。早期対応はユーザリテンション向上に直結する
- 「見なかったことにする」と「判断して無視する」は全く違う
- 問題は「エラーが出ること」ではなく「エラーに気づかないこと」「エラーを放置すること」

---

## 3. プロジェクト構成

### コンポーネントごとにプロジェクトを分離する

```
sentry-org: cotomo
├── project: audrey-brain             # コア会話AI
├── project: audrey-long-term-memory  # 記憶・永続化
├── project: cotomo-admin-2           # 管理画面
├── project: cotomo-api               # APIサーバ（該当する場合）
└── project: cotomo-client            # クライアントアプリ（該当する場合）
```

**理由**:
- オーナーシップの明確化（どのプロジェクトのエラーは誰が見るか）
- アラート閾値をプロジェクトごとに調整可能（管理画面とコアAIでは重要度が違う）
- ノイジーなエラーが他プロジェクトの重要エラーを埋もれさせない
- サンプリングレートを個別設定可能

### Ownership Rules（自動アサイン）

```yaml
# Sentry Ownership Rules
path:audrey-brain/*              #core-ai
path:audrey-long-term-memory/*   #core-ai
path:cotomo-admin-2/*            #admin
url:*/api/v1/*                   #platform
```

エラー発生時に自動でチームにアサインされ、VPoTが手動で振り分ける必要がなくなる。

---

## 4. 当番制（Sentry Duty）

### 基本構造: 週次ローテーション + Primary/Secondary 体制

| 役割 | 責務 |
|------|------|
| **Primary（1名）** | Sentryの日次チェック、トリアージ、軽微なものは自分で対応 |
| **Secondary（1名）** | Primary不在時のバックアップ、判断に迷った時の相談相手 |
| **残り3名** | 通常開発に集中。ただし自分がデプロイしたコードに起因するエラーは自分で対応 |

### ローテーションスケジュール（5名: A, B, C, D, E）

```
Week 1: Primary=A, Secondary=B
Week 2: Primary=B, Secondary=C
Week 3: Primary=C, Secondary=D
Week 4: Primary=D, Secondary=E
Week 5: Primary=E, Secondary=A
（以降ループ）
```

5週で一巡。各メンバーは5週に1回 Primary、1回 Secondary を担当。

### VPoTの位置づけ

- VPoTもローテーションに入る。ただし特別扱いはしない
- VPoTがOn-Callでない週にちゃんと他のメンバーが回せることが、制度の成功指標
- 移行完了後、VPoTは月1回のレビューのみ

### Primary の期待値

- 営業時間中、Slackの Sentry アラートチャンネルを30分以内に確認する
- **毎日2回**（朝会前 10:00 + 夕方 17:00）Sentryダッシュボードを確認（各15〜30分）
- P0エラーは15分以内に Ack（「見ました、対応します」）を返す
- 新規 Issue をトリアージし、結果を Slack に報告する

### 引き継ぎ

- 毎週月曜の朝に15分の引き継ぎを実施
- 前週の当番が「未解決のエラー」「注意すべき傾向」「対応したこと」を共有
- Slackスレッドで「今週のSentry当番サマリー」を投稿

### 負荷への配慮

- **On-Call 週は通常の開発タスクの割り当てを50%削減する**。これをやらないと誰もやりたがらなくなる
- On-Call対応のログを残し、評価に反映する

---

## 5. トリアージ基準

### 優先度定義

| 優先度 | 定義 | 対応基準 | 例 |
|--------|------|---------|-----|
| **P0** | ユーザ影響が広範囲、コア機能障害、データ損失・セキュリティ | 15分以内に着手 | 会話ができない、課金エラー |
| **P1** | 一部ユーザに影響、非コア機能障害、パフォーマンス劣化 | 当日中に着手 | 設定画面が開けない、レスポンス劣化 |
| **P2** | 影響が限定的、エッジケース、軽微なUX問題 | バックログに積み、スプリント内で検討 | 少数ユーザの表示崩れ |
| **P3 (Ignore)** | 外部起因、対応済み（修正リリース待ち）、期待されたエラー | Sentry上でIgnore/Archiveし理由をコメント | BOTアクセス、Rate limiting |

### 判断フローチャート

```
新規Issue発見
  │
  ├─ ユーザ影響あり？（エラー率上昇 or 主要機能の障害）
  │   ├─ YES → P0: 即座に対応開始。#sentry-critical に投稿。
  │   │         関係者にメンション。必要に応じてVPoTにエスカレーション
  │   └─ NO ↓
  │
  ├─ 再現性あり？（複数ユーザ or 複数回発生）
  │   ├─ YES → P1: GitHub Issue 作成。担当者アサイン。当日中に着手
  │   └─ NO ↓
  │
  ├─ 既知の問題 or 外部要因？
  │   ├─ YES → P3: Sentry で Ignore/Archive し、備考を残す
  │   └─ NO ↓
  │
  └─ P2: バックログに積む。次スプリント以降で検討
```

### 優先度スコアリング（迷ったとき用）

```
影響ユーザ数 × エラーの深刻度 × 発生頻度 = 優先度スコア

- 影響ユーザ数: 全体(3) / 多数(2) / 少数(1)
- 深刻度:       データ損失・セキュリティ(3) / 機能不全(2) / UX劣化(1)
- 頻度:         常時(3) / 頻繁(2) / 稀(1)

スコア 7以上 → P0、4-6 → P1、3以下 → P2
```

### エスカレーション基準

| 状況 | エスカレーション先 |
|------|-------------------|
| P0で30分以内に原因特定できない | VPoT |
| P0で1時間以内に解決の見通しが立たない | VPoT + VPoE |
| 同一Issueが3スプリント連続で未解決 | スプリントレトロで議論 |

**迷ったら上げる。** 上げすぎて怒られることはない、上げなくて大事になることはある。

---

## 6. アラートルール設計

### 3層アラート

**Layer 1: P0（即時対応）**
```yaml
条件:
  - 新規Issue AND 影響ユーザ数 > 100人/1時間
  - エラー率が直近1時間で200%以上増加
  - 特定の致命的エラー（会話不成立、課金関連）
  - Crash free session rate が 99.5% を下回った
通知先: #sentry-critical（@channel メンション）
期待対応: 30分以内にAcknowledge
```

**Layer 2: P1（当日対応）**
```yaml
条件:
  - 新規Issue AND 発生回数 > 50回/1時間
  - 既存Issueが再発（Regression）
  - エラー率が直近1時間で150%以上増加
通知先: #sentry-alerts（当番メンション）
期待対応: 当日中にトリアージ
```

**Layer 3: P2（週次レビュー）**
```yaml
条件:
  - 上記に該当しない新規Issue
  - 低頻度の既存エラー
対応: 週次の棚卸し会で確認。Slackには流さない
```

### Sentry Alert Rules 設定例

```
Alert Rule: "Critical Error Spike"
  When: number of events in an issue is more than 100 in 1 hour
  Filter: issue.isUnhandled is true
  Action: Send Slack notification to #sentry-critical

Alert Rule: "Regression Detected"
  When: A regression event occurs
  Action: Send Slack notification to #sentry-alerts

Alert Rule: "New High-Volume Issue"
  When: A new issue is created AND event count > 50 in 1 hour
  Action: Send Slack notification to #sentry-alerts

Alert Rule: "Deploy Regression"
  When: Crash free session rate drops below 99.5% for release
  Action: Send Slack notification to #sentry-critical
```

---

## 7. Slack連携

### チャンネル設計

| チャンネル | 用途 | 通知設定 |
|-----------|------|---------|
| `#sentry-critical` | P0アラートのみ。ここが鳴ったら全員注目 | `@channel` メンション。全員通知ON |
| `#sentry-alerts` | P1アラート。当番が日常的にチェック | `@sentry-duty` メンション（当番のユーザーグループ） |
| `#sentry-triage` | 当番のトリアージ結果報告・議論用（人間が書く） | メンションなし |
| `#sentry-noise` | 既知・低優先度のアラート退避先 | 通知OFF推奨。アーカイブ目的 |

### 目安

- `#sentry-critical` は週0〜2回が理想
- `#sentry-alerts` は1日3〜5件が理想
- これを大幅に超える場合はアラートルールかノイズフィルタの見直しが必要

---

## 8. 日常オペレーション

### 朝のSentryチェックフロー（Primary当番）

1. Sentryの「Issues」画面を `is:unresolved firstSeen:-24h` で開く
2. 新規Issueを1件ずつ確認し、トリアージフローに従って分類
3. 結果を `#sentry-triage` に投稿

### トリアージ報告テンプレート（Slack投稿用）

```
【Sentryトリアージ報告】
日付: YYYY-MM-DD
当番: @名前

■ 新規Issue
- [Issue名](Sentryリンク) | P0/P1/P2/P3 | 担当: @名前 or 未アサイン
  概要: 一行で何が起きているか
  対応: 即時対応中 / チケット作成済み / Ignore済み

■ 継続対応中
- [Issue名](Sentryリンク) | 進捗メモ

■ 本日の所感
（任意。ノイズが多い、特定の傾向がある、等）
```

### デプロイ後のSentry確認

デプロイした本人が、デプロイ後15分〜30分で Sentry を確認する。自分のデプロイで新規エラーが出ていないかをチェック。これにより「自分で気づいて報告する」のが自然な流れになる。

---

## 9. リリースとの連携

### Sentry Release の活用

CI/CDパイプラインに以下を組み込み、デプロイとSentryリリースを紐付ける。

```bash
# develop → main マージ時のCI/CDに追加

export SENTRY_ORG=cotomo
export SENTRY_PROJECT=audrey-brain  # プロジェクトごとに実行
export VERSION=$(git rev-parse --short HEAD)

# リリースの作成とコミット紐付け
sentry-cli releases new "$VERSION"
sentry-cli releases set-commits "$VERSION" --auto

# デプロイ実行後
sentry-cli releases deploys "$VERSION" new -e production
sentry-cli releases finalize "$VERSION"
```

### 効果

- **Release Health**: セッションベースのクラッシュ率が自動計測される
- **Release比較**: 前リリースと比較してエラー率が上がったか一目で分かる
- **Deploy Marker**: グラフにデプロイタイミングが縦線で表示される
- **Suspect Commits**: エラーを引き起こした可能性のあるコミットとコミッターが自動表示される

### リリースPRチェックリストへの追加

既存のリリースPRチェックリストに以下を追加する:

```markdown
## リリース後チェック
- [ ] デプロイ後30分: Sentryで新規エラーの確認完了
- [ ] デプロイ後30分: 主要メトリクス（エラー率、レスポンスタイム）に異常なし
- [ ] 翌営業日: Sentry当番による24時間後チェック完了
```

---

## 10. Issue管理

### アクションの使い分け

| アクション | いつ使うか | 例 |
|-----------|-----------|---|
| **Resolve** | 修正コードをデプロイした時 | バグ修正PRマージ後 |
| **Resolve in Next Release** | 修正がmainに入ったがまだデプロイされていない時 | develop→mainマージ直後 |
| **Ignore (Until condition)** | 一定条件まで無視したい時 | 「100回以上再発したら再通知」 |
| **Merge** | 同一原因の複数Issueをまとめる時 | 同じバグが異なるスタックトレースで出ている |
| **Archive** | 対応不要と判断した時 | サードパーティ由来、ユーザ環境依存 |

### Saved Search（よく使う検索条件）

```
"要トリアージ":     is:unresolved !has:assignee age:-7d
"放置Issue":       is:unresolved has:assignee age:+30d
"高頻度未対応":     is:unresolved times_seen:>100 !has:assignee
"今週のRegression": is:regression firstSeen:-7d
```

### 週次棚卸し会（15〜30分）

```
アジェンダ:
1. 直近1週間の新規Issue確認（Unresolved, First Seen: 7d）
2. 高頻度Issueの確認（Sort by Events, Last 7 days）
3. Assigneeなしの古いIssueの処理（Assign or Archive）
4. Regressionの確認
5. アラートルールの調整が必要か
```

---

## 11. ノイズ対策

ノイズが多いと誰も見なくなり、Sentryが無意味になる。3層で対策する。

### Layer 1: SDK側（送信前フィルタ）

```python
sentry_sdk.init(
    dsn="...",
    before_send=before_send,
    ignore_errors=[
        ConnectionResetError,
        BrokenPipeError,
    ],
)

def before_send(event, hint):
    exc_type = hint.get("exc_info", [None])[0]

    # ユーザのネットワーク切断（モバイルでは日常的）
    if exc_type and issubclass(exc_type, (ConnectionError, TimeoutError)):
        return None

    # Bot/クローラからのエラーを除外
    user_agent = event.get("request", {}).get("headers", {}).get("User-Agent", "")
    if is_bot(user_agent):
        return None

    return event
```

### Layer 2: Sentry Inbound Filters

```
Settings > [Project] > Inbound Filters:
✅ Filter legacy browsers
✅ Filter known web crawlers
✅ Filter localhost events
```

### Layer 3: Fingerprinting Rules

```yaml
# 外部APIのタイムアウトを1つのIssueにまとめる
error.type:TimeoutError message:"External API *" -> external-api-timeout

# サードパーティライブラリのエラーをまとめる
module:third_party.* -> third-party-error-{{ module }}
```

### 月次ノイズレビュー

「Top 20 高頻度Issue」を確認し:
- 修正可能 → チケット化して対応
- 修正不可能 → `before_send` でフィルタまたは Archive
- 判断保留 → Ignore (Until 1 month) で1ヶ月後に再確認

---

## 12. スプリントへの組み込み

### 「割り込み枠」と「計画枠」の二本立て

#### 割り込み枠（P0/P1）

- スプリントのベロシティの **15〜20%をバッファとして確保**
- P0は即時対応（スプリント計画外で着手してよい）
- P1は当番がチケット化し、スタンドアップで共有 → その場でアサイン

#### 計画枠（P2）

- 当番がバックログにチケットを作成（Sentryリンク + 再現手順 + 影響範囲）
- スプリントプランニングで他のストーリーと一緒に優先度を判断
- **毎スプリント1〜2件は必ずピックアップ**するルール。放置すると溜まる一方

#### チケットのラベル

- `source:sentry` のラベルを付けて追跡可能にする

---

## 13. オンボーディング

### Phase 1: ペアトリアージ（1〜2週間）

- VPoTと1名がペアでSentryを見る時間を毎日30分設ける
- VPoTが「自分はこう考えてこう判断する」を声に出しながらトリアージする（Think Aloud）
- 全メンバーが最低1回は経験する

### Phase 2: ランブック整備

VPoTの暗黙知を形式知化する。最低限以下を文書化:

- Sentryダッシュボードの見方（どの画面を見るか、どの数字に注目するか）
- トリアージの判断基準（P0/P1/P2/P3の具体的な閾値）
- **よくあるエラーパターンと対応方法（Top 10〜20）**
- エスカレーション基準（「これはVPoTに聞くべき」の明確な線引き）
- 対応フローチャート

### Phase 3: シャドウ当番（2〜4週間）

- 正式ローテーション開始前に「シャドウ期間」を設ける
- 新Primaryが判断し、経験者がレビューする
- 「間違えても大丈夫」という安全な環境で実践経験を積む

### ジュニアメンバーへの段階的導入

1. **「見るだけ当番」** から始める: 対応しなくていいから、Sentryを開いて気になったエラーを1つSlackに投稿するだけ
2. **ペアで当番**: 先輩と一緒に Primary を担当する
3. **Secondary として独り立ち**: バックアップ役から始める
4. **Primary として独り立ち**: ここまで来ればフルローテーション参加

### 心理的安全性

- **「判断を間違えても大丈夫」** を明示的に伝える。大騒ぎして大したことなかった方が、スルーして大事になるより100倍マシ
- 自分のデプロイで壊した場合の自己申告を称賛する文化を作る
- エラー報告への最初のリアクションは必ず「報告ありがとう」から始める
- 「なんでこんなバグ出したの？」は絶対にNG。「どうすれば防げるか一緒に考えましょう」

---

## 14. メトリクスと振り返り

### 週次メトリクス（当番が金曜に集計）

| メトリクス | 内容 |
|-----------|------|
| 新規Issue数 | 今週の新規 |
| 解決Issue数 | 今週の解決 |
| 未解決Issue数 | 累積 |
| P0/P1発生件数 | 今週 |
| 平均解決時間 | P0/P1の検知→解決リードタイム |
| 影響ユーザTop3 | 最も影響ユーザ数が多かったIssue |

### スプリントレトロへの組み込み

スプリントレトロのアジェンダに **「Sentry振り返り」を固定枠（5〜10分）** で入れる:

- 今週ノイズが多かったものはあるか → Alert Rule調整
- 繰り返し発生しているIssueはあるか → 根本対応の優先度を上げる
- 当番の負荷は適切か → ローテーション調整

### 評価への組み込み

- **「運用貢献」カテゴリ**を評価制度に設ける
- 当番での対応品質、再発防止策の実施、ランブック整備、知識共有を評価対象とする
- **障害の発生件数で評価しない**（「何もデプロイしない」が最適解になる）
- ポジティブフィードバック: 週次振り返りで当番の貢献を具体的に感謝する

---

## 15. 導入ロードマップ

### Week 0（宣言と準備）

- [ ] VPoT/VPoEからチームに「Sentry運用体制を変える」ことを宣言
- [ ] 変更の目的を明確に伝える
- [ ] Sentryの現状棚卸し（未解決Issue数、主要エラーパターンの整理）
- [ ] ローテーションスケジュールのドラフト作成

### Week 1〜2（オンボーディング + 技術基盤）

- [ ] Sentryプロジェクト分離 + Ownership Rules設定（半日）
- [ ] アラートルール3層設計 + Slackチャンネル整備（半日）
- [ ] Inbound Filters + before_send フィルタ設定（半日）
- [ ] VPoTによるペアトリアージを全員に実施（各メンバー2〜3回）
- [ ] ランブックのドラフト作成
- [ ] トリアージ基準の合意形成

### Week 3〜4（シャドウ期間）

- [ ] 最初の2名がシャドウPrimaryとして実践（VPoTがレビュアー）
- [ ] CI/CDにSentry Release統合（1日）
- [ ] ランブックの加筆・修正
- [ ] 残りメンバーもシャドウを経験

### Week 5〜6（正式ローテーション開始）

- [ ] Primary/Secondary体制で正式にローテーション開始
- [ ] VPoTは日常監視から離脱（エスカレーション先としてのみ機能）
- [ ] 週次の振り返り会を開始

### Week 7〜8（安定化と改善）

- [ ] ローテーションの負荷感をヒアリング
- [ ] リリースPRチェックリストの更新
- [ ] 評価制度への正式な組み込みを検討

### Month 3以降（自律運用）

- [ ] チームが自律的にローテーションを回している状態
- [ ] VPoTは月1回のレビューのみ
- [ ] 新メンバー加入時のオンボーディングプロセスが確立
- [ ] 月次ダッシュボードの構築（任意）

---

## Appendix: パフォーマンスモニタリング（発展）

### サンプリングレートの設計

200万ユーザ規模では全トランザクション送信はコスト面で非現実的。

```python
sentry_sdk.init(
    dsn="...",
    traces_sample_rate=0.01,  # 本番は1%から開始
    traces_sampler=traces_sampler,
)

def traces_sampler(sampling_context):
    name = sampling_context.get("transaction_context", {}).get("name", "")

    if "/health" in name or "/readiness" in name:
        return 0        # ヘルスチェックは送らない
    if "/payment" in name or "/subscription" in name:
        return 0.5      # 課金関連は高めにサンプリング
    if "/conversation" in name or "/chat" in name:
        return 0.05     # コア会話APIは少し高め
    return 0.01         # デフォルト
```

### Enhanced Context

```python
sentry_sdk.set_user({"id": user_id})

sentry_sdk.set_context("conversation", {
    "session_id": session_id,
    "turn_count": turn_count,
    "model_version": model_version,
})

sentry_sdk.set_tag("environment", "production")
sentry_sdk.set_tag("region", "ap-northeast-1")
```

エラー発生時に「どのユーザの、どの会話の、何ターン目で」発生したかが即座に分かる。

---

> *完璧な仕組みを作ろうとしないこと。まず回し始めて、痛みを感じたところを直していく。*
> *最も重要なのは Week 0 で動き出すこと。*
