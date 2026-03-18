# AI時代のプロダクト開発組織戦略（ChatGPT対話ログ整理）

## 発端
- Slackチャンネル C0AH6RN73F0 にて eruma が議題提起（2026-03-15）
- 「次の議題として、AI 時代のプロダクト開発組織の理想系を一度議論したいです！」
- shinofara に叩き台を依頼

## 背景・現状の課題
- Unityチーム（業務委託4名＋EM1名＋デザイナ1名）とAIチーム（PE3名＋AI/ML3名＋PdM1名）が分離
- UnityとAPI開発の連携遅延（EMが開発も兼務、APIが遅れUnityが詰まる）
- AIチームがユーザ体験をイメージできず、CRUD的API設計になりがち
- ユーザに価値を届けるインターフェース体験の解像度が低い

## 組織戦略の方向性

### Project制の導入
- 一人1PJ原則でオーナーシップを明確化
- PJサイズは2〜6週間、1四半期以内に完了
- PJタイプ: UX/UI変更系 / サーバ側改善 / OPS基盤整備

### 管理・運用デザイン
- Kanban + Linear Cycle（Weekly）で運用
- スクラムは不採用。リズムだけ取り入れる
- PJ意思決定オーナーはPO兼CEO（丸橋）
- 週1回の全体PJレビュー会（30〜45分）

### PJテンプレート（Starley Project Template v2）
モダンアジャイル（2025年版）のベストプラクティスをベースに設計：
1. **Why** — どんな「問題」を解決したいのか？
   - Problem（問題）→ Cause（原因）→ Goal/Value Hypothesis（価値仮説）
2. **What** — 何をもって成功とするのか？
   - 成果（Outcome）、検証方法、Deliverables
3. **Who** — 誰が責任を持つのか？
   - PO/PdM/Designer/PE/Unity/QA/EM の責任を簡潔に
4. **Learnings / Next Steps** — 何を学び、どう次に活かすか？
   - What worked / What didn't / What's next

### PEの役割再定義
- EMから指示を受けるのではなく、能動的にFigmaを読み、Designerの意図を汲み取る
- UnityエンジニアとコミュニケーションしながらAPIのあるべきを描く
- API利用者（Unityエンジニア）に「苦労ではなく価値」を届ける責任
- API実装だけでなく、Unity結合支援・体験着地までが責任範囲

### EMの理想的役割
- 指示・管理ではなく「隙間を埋め、接続し、踏み込む支援」
- PdM/Designer/PE/Unity Engineersが自律的に連携できる状態を目指す
- チームの価値最大化のためのインパクトを見つけて解決する触媒

### 大きな開発プロセスの流れ
1. PdM → POの間で企画デザイン
2. PdM → Designerの間で体験デザイン
3. このタイミングからPEを巻き込みPJ化
   → PEが「仕様の受け手」ではなく「体験を共に作る当事者」に

## Unityチーム体制（最新）
- 石原さん（週2日）
- せとさん（週3日）
- 田村さん（週4日・新規）
- 新規メンバー（週5日・10月15日週から）
- オフショア: Unityエンジニア（ミドル）1名、テスター1名、ブリッジ0.25人月

## AI時代の開発文化

### DiscoverとDeliveryの融合
- 分けて考えるのではなく、永遠にDiscoverを小さくやり続ける
- ToCエンタメではDiscoverが困難。作って試して撤退をAIで高速化
- AIにより「試すコスト」が劇的に下がった

### 能動性が最重要
- AIが生産性を加速 → 問題・負債も同じ速度で増加
- 負債回収も全員が能動的にチャレンジしないと増える速度に負ける
- 「気づいたら何かする」が文化の根幹

### 「気づいたら何かする」文化
- Devinに投げる / LinearでIssue化 / Slackで共有
- 1回で解決できなくてもOK。気づいて動くことが最も価値がある
- 完璧より即行動

## 3ヶ月フェーズ設計（AsIs → ToBe）

### AsIs（現在）
- AI活用は始まっているが「道具としての利用」に留まる
- 気づいてもスルー、Project外に意識が向かない
- 指示・タスクドリブンな動きが残る

### Phase 1: Awareness（Week 1〜3）
- テーマ: 気づいて動くことを当たり前にする
- #noticedチャンネル開設、ロールモデルが先行投稿
- 称賛文化の導入

### Phase 2: Activation（Week 4〜6）
- テーマ: 動きがチームで循環する
- Devin→Linear→Slack自動連携
- "Noticed of the Week"選出
- 職種横断の投げ合い促進

### Phase 3: Autonomy（Week 7〜10）
- テーマ: AIと共に自律的に動くチーム
- 各自がAIワークフローを最適化
- EMの介入不要で改善が自走
- 評価に能動性を反映

### ToBe（3ヶ月後）
- 全員が能動的にAIをフル活用し自律的に動く
- PJタスク・サイドタスク・改善をローカル/リモートでフル活用
- Devinリクエスト・Issue化が日常的に活発

## Output ×3 戦略（3ヶ月目標）

### Output = Execution Speed × Parallelism × Judgment Quality

### VPoEがやるべき3つ
1. **価値の言語化** — 全員の意思決定と行動が価値ベースに揃う
2. **仕組みのデザイン** — 努力ではなく仕組みが組織を自走させる
3. **Seniorを価値ドライバーに** — レバレッジを最大化

## エンジニアの価値定義

### Starley版
「技術とAIを用いて、ユーザ・チーム・未来のために"より良い状態"を継続的に作り出すこと」

### レベル別
- **Junior**: Execution × Learning（タスク遂行の正確性、AI活用で速度向上）
- **Mid**: Collaboration × Problem Solving（利用者理解、自走改善）
- **Senior**: Judgment × Leverage（何を作るべきかの判断、チームOutput向上）

### 本質
- 課題解決は手段。本質は「状態を良くし続けること」
- AI時代では「解く力」より「選ぶ力・疑う力・気づく力」がシフト

## VPoE（shinofara）の役割定義

### Starley版VPoE
「Engineeringが生み出す価値全体をデザインし、最大化する責任者」

### Engineeringの定義
- 職能ではなく「価値を形にする営み」
- エンジニア・デザイナー・PdM・AIすべてに共有されるもの

### 就任スピーチ（採用版）
> VPoEという肩書きはつきましたが、やりたいことはシンプルで、"みんなでより良いチームをつくる"ということです。
> 僕が考えるEngineeringは、コードを書くことでも、技術を管理することでもなくて、価値を形にする——僕たち全員の営みそのものだと思っています。
> そして今、その営みの中心にはAIがいます。人とAIが一緒に考え、動き、学んでいく。それが当たり前の世界で、僕はその"共創の仕組み"をつくっていきたい。

## 参考記事・知見
- Kent Beck講演（Findy）: Effort→Output→Outcome→Impactの価値の道筋
- Duolingo Handbook: Take the Long View / Raise the Bar / Ship It / Show Don't Tell / Make It Fun
- DORA 2025: AI導入＋仕組み・文化整備が必須。再作業率(rework rate)が新指標
- Battery Ventures「AI時代のPM」: Build-first文化、役割境界の曖昧化、成果指標の変革
- Anton Sten: Executionが容易になった時代はTaste（判断・見極め）が差別化要因
- PMBOK第8版: 価値(Value)への焦点、原則とプロセスの融合
- 「課題解決は本質か」: エンジニアの本質は課題を疑い選び技術でより良い状態を実装し続けること

## Agent向け引き継ぎ情報（AGENT_CONTEXT概要）
- 価値定義、文化原則、レベル別期待、意思決定フレーム、採用判断基準を含むドキュメントをGitHub管理へ移行予定
- 採用検討トリガー: ボトルネック存在 / 高価値機会の逸失 / Senior飽和 / システム最適化済み
