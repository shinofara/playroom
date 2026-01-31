# シニアプロダクトエンジニア / Senior Product Engineer

## いま私たちがこのポジションで実現したいこと（日本語）

Starleyは、**「人とAIの新たな関係をデザインする」**ことをミッションに、音声会話型おしゃべりAIアプリ **「Cotomo（コトモ）」** を開発・運営しています。

Cotomoは **「話したいことも、話せないことも。」** をテーマに、ユーザーに寄り添う自然な会話を通じて、日々の孤独感やストレスを少しでも軽くすることをコンセプトにしています。私たちはAIを単なる「業務効率化のためのツール」としてだけではなく、**人と相互にコミュニケーションできる可能性のある存在**として捉えています。

そのために、会話の内容だけでなく、**会話のテンポ、感情、間合い、声の揺らぎ**といった体験の細部まで丁寧に設計し、改善を続けています。目指すのは、いわゆる"話せるAI"に留まらず、"心に届くAI"です。

Cotomoは **200万以上ダウンロード** され、ユーザー数・トラフィックが伸び続けています。いま私たちは、**会話品質の改善と安定運用を両立しながら、体験を継続的に進化させるフェーズ**にいます。

このポジションでは、いわゆる「バックエンド」だけに閉じず、**音声×リアルタイム×LLM** の体験を成立させるために必要な領域（API、会話用WebSocketサーバ、Promptチューニング、モデル選定、クラウド基盤、運用・体制）を横断し、**技術的な意思決定と実装・運用の推進をリード**していただきます。Engineeringを「価値を形にする営み」と捉え、ユーザーの体験に直結する論点を技術で前に進める役割です。

---

## ポジションの特徴（まず知ってほしいこと）

- **200万DL超**のプロダクトで、増え続けるユーザー・トラフィックに向き合う（品質改善と安定稼働を止めない）
- **音声×リアルタイム**の会話体験を支える：WebSocketを中心に、低レイテンシ/再接続/状態管理など、**テンポや間合いを含む体験**に直結する課題が多い
- **Prompt改善を「運用」する**：一度の調整で終わらせず、評価・再現性・変更管理を含めた改善サイクルを回す（"心に届く"会話品質を積み上げる）
- **モデル選定〜統合まで**をプロダクト要件から考える（ASR/LLM/音声合成などを組み合わせ、品質・コスト・レイテンシ・運用性の最適解を探る）
- **Google Cloud中心の基盤と運用**：観測性、障害対応、キャパシティ、セキュリティまで含めて“持続的に価値提供できる仕組み”を作る
- チーム横断で、プロダクトの状況に応じて優先度の高い課題を掴み、**意思決定→実装→運用改善**までやり切る

## チーム・開発組織について

- Starleyのエンジニアは、**海外比率70%超**の多様なチームです（バックグラウンドの幅が広く、前提や視点の違いを踏まえた設計・意思決定が求められます）。
- 一方で、**エンジニア間の公用語は日本語**です。日々の業務上のコミュニケーション（会話・読み書き）は日本語が中心になります。
- 英語での技術的コミュニケーションができる方は歓迎しますが、プロダクト開発を前に進めるうえで、日本語での協業が基本となります。

---

## 業務内容

Cotomoおよび新規プロダクトの「会話体験」を支えるシステムを、設計〜実装〜運用まで一気通貫でリードしていただきます。担当領域は固定せず、プロダクトの状況に応じて優先度の高い課題に向き合います。

- **Cotomoアプリが利用するAPI** の設計・実装・運用（プロダクト要求と将来のスケールを踏まえた設計）
- **会話用WebSocketサーバ（会話のためのAgent的機能を含む）** の設計・実装・運用  
  - 低レイテンシ、セッション管理、ストリーミング、再接続、状態管理 など
- 会話品質を支える **Agent的機能** の設計・実装  
  - 会話の状態・文脈の扱い、ツール実行、ガードレール設計 など
- **Promptチューニング** と改善サイクルの設計・運用  
  - 品質評価、再現性、変更管理
- **モデル選定・統合**（ASR/LLM/音声合成等）  
  - 品質・コスト・レイテンシ・運用性のバランスを踏まえたシステム設計
- **Google Cloud を始めとしたクラウド基盤**の設計・改善  
  - セキュリティ、ネットワーク、データ、実行基盤、CI/CD など
- 増え続けるユーザー・トラフィックに対して、持続的に価値提供し続けるための **システム基盤 / 運用基盤 / 体制** の整備  
  - 監視、アラート、インシデント対応、SLOの検討、キャパシティ計画、運用改善
- プロダクトマネージャー・デザイナー等と協業し、技術面から意思決定を支え、継続的なプロダクト改善を推進

---

## 具体的な役割と期待（Seniorとして）

「手を動かす」だけでなく、**技術と運用の意思決定を担い、チームの出力を上げる**ことを期待します。

- **技術的な意思決定**：複数の選択肢から、体験品質・コスト・運用負荷・開発速度のバランスを取り、納得度の高い判断をする
- **アーキテクチャ設計・進化**：いま必要な現実解を取りつつ、将来のスケールや変更に耐える構造へ段階的に改善する
- **信頼性・運用の設計**：観測性（ログ/メトリクス/トレース）、アラート、障害対応の進め方、再発防止などを仕組みとして整える
- **チーム横断の推進**：PM/デザイン/ML/基盤など関係者を巻き込み、論点整理と合意形成を行い、実装・運用まで前に進める
- **改善サイクルの定着**：Prompt/モデル/リアルタイム基盤など、不確実性が高い領域でも検証→学習→改善が回る状態を作る

---

## 技術的な面白さ・チャレンジ

- **リアルタイム音声対話**ならではの難しさに正面から取り組む  
  - レイテンシ、途切れ、再接続、順序、ストリーミング、状態の整合性などが体験に直結します
- **スケールと信頼性の両立**  
  - 200万DL規模のプロダクトとして、安定稼働を維持しながら改善を止めないための設計・運用が必要です
- **LLM/音声モデルを“プロダクトとして運用する”**  
  - Promptやモデルの改善を、属人的な調整で終わらせず、評価・再現性・変更管理を含めた改善サイクルとして回します（LLMOpsに近い領域）
- **コスト最適化と体験品質のトレードオフ**  
  - 推論・ストリーミング・インフラの設計を通じて、品質/レイテンシ/コスト/運用性の最適点を探索します
- **障害対応をプロダクトの強さに変える**  
  - 事後対応に留めず、原因特定しやすい観測性や、再発防止まで含めた運用設計を積み上げます

---

## 求める人物像

- 役割範囲を限定せず、プロダクト価値最大化のために「今、効く」課題を自ら見つけてリードできる方
- 技術的な正しさだけでなく、ユーザー体験・運用・コスト・開発速度のバランスを踏まえて意思決定できる方
- 不確実性の高い領域（モデル、プロンプト、リアルタイム性、スケール）に対して、検証と改善のサイクルを回せる方
- チームでの成果にこだわり、オープンなコミュニケーションで周囲を巻き込める方

---

## 必須要件（Required）

- バックエンドシステムの設計・実装・運用における **実務経験7年以上（目安）**
- 成長フェーズ、または新規立ち上げフェーズで、技術面の中心として意思決定・推進を担った経験
- RDB（PostgreSQL/MySQL等）およびNoSQLを含むデータストアの活用経験
- 大規模トラフィック、または高負荷システムの開発・運用経験
- AWS / GCP / Azure 等のクラウドプラットフォームでの実践的な運用経験
- **エンジニア間の公用語は日本語**です。日本語での業務コミュニケーション能力（会話・読み書き）
- **AI支援開発ツール**（例：Devin / Cursor Pro / Claude Code Max / Codex / OpenCode 等）を日々の開発プロセスに取り入れ、継続的に改善してきた経験（個人プロジェクトでの利用も可）

---

## 歓迎要件（Preferred）

- WebSocket / WebRTC 等のリアルタイム通信技術に関する設計・運用経験
- 機械学習モデルの本番運用経験、または LLM 等深層学習モデルの調整・評価に関わった経験
- Promptチューニングや評価設計、改善サイクル運用（いわゆるLLMOpsに近い領域）の経験
- Google Cloud（GCP）でのアーキテクチャ設計・運用経験
- 観測性（ログ/メトリクス/トレース）、SLO設計、インシデント対応体制の整備経験
- 英語での技術的コミュニケーション能力
- 成長期スタートアップでの開発・運用経験
- 音声認識・自然言語処理・音声合成に関する知識および実務経験

---

## 給与・待遇

- **850万円以上**
- 業績・貢献度に応じたストックオプション制度

---

## 働き方

- 働き方：原則出社  
- ただし、明確な制度として固定されているわけではありません。家庭の事情や看病など、何らかの事情で出社が難しい日・期間がある場合は、事前に相談のうえリモート勤務も可能です（「この日だけ」といった単発の相談も含みます）。
- VISAサポートあり（条件あり）

---

## Tech Stack（利用技術）

※プロダクト状況に応じて更新します。現時点の主な利用技術です。

- 言語: **Python / Rust / TypeScript**
- リアルタイム・通信: **WebSocket / WebRTC**
- データストア・検索: **PostgreSQL / Elasticsearch**
- クラウド: **Google Cloud (GCP) / AWS / Azure**
- 分析・データ基盤: **BigQuery / Dataform**
- ML/推論・開発基盤: **PyTorch / Transformers / DeepSpeed / vLLM / NVIDIA Triton / Weights & Biases**
- クライアント/周辺: **Unity**
- 監視・運用: **Sentry**
- コラボレーション: **Slack / GitHub**
- AI開発支援: **Devin / Cursor Pro / Claude Code Max / Codex / OpenCode**（利用は人により異なります。より良いツールが出れば積極的に試し、AIで生産性を高め続けることに向き合っています）

---

## 選考プロセス（参考）

※状況により変更となる場合があります。

- 書類選考
- コーディングテスト（LLM利用が必要なレベル）
- 面談/面接（複数回）
- オファー面談

---

# Senior Product Engineer

## Why we’re hiring / What we want to achieve

Starley’s mission is to **design a new relationship between people and AI**. We develop and operate **Cotomo**, a voice-based AI conversation app.

Cotomo is built around the theme **“Even the things you want to say, and the things you can’t.”** Our concept is to ease everyday loneliness and stress through natural conversations that stay close to the user. We see AI not only as a tool for “workflow efficiency,” but as an entity that can **communicate interactively with people**.

To achieve this, we continuously design and improve not only what is said, but also the details of the experience—**conversation tempo, emotion, pauses, and even subtle fluctuations in the voice**. Our goal is not just a “talkable AI,” but an AI that can “reach the heart.”

Cotomo has been downloaded **over 2 million times**. As our users and traffic continue to grow, we are in a phase where we must **keep improving conversation quality while maintaining stable, reliable operations**—and continuously evolve the experience.

In this role, you won’t be limited to “backend” work. You will lead technical decision-making and execution across the domains required to make a voice, real-time, LLM-driven product work in production: APIs, a conversation-oriented WebSocket server, prompt tuning, model selection, cloud infrastructure, and sustainable operations/team practices. We see engineering as the work of “shaping value into reality,” and you will push forward technical decisions that directly impact user experience.

---

## What makes this role unique

- Work on a **2M+ download** product, tackling ever-growing users and traffic without slowing down improvements
- Build a **voice + real-time** conversation experience: low latency, reconnections, state management—problems that directly affect the experience, including tempo and pauses
- Operate a **prompt improvement loop** with evaluation, reproducibility, and change management (not “one-off” tuning) to steadily build “heart-reaching” conversation quality
- Make product-driven decisions on **model selection and integration** (ASR / LLM / speech synthesis), balancing quality, cost, latency, and operability
- Improve cloud infrastructure and operations (centered on **Google Cloud**) including observability, incident response, capacity planning, and security
- Drive **end-to-end execution** across teams: decision-making → implementation → operational improvements

## Team & Engineering Communication

- Our engineering team is highly diverse, with **70%+ of engineers based overseas**. You’ll work with teammates with different backgrounds and perspectives, and we value clear reasoning and shared context in decision-making.
- At the same time, **Japanese is the working language within the engineering team**. Most day-to-day communication (spoken and written) is conducted in Japanese.
- English technical communication is a plus, but Japanese collaboration is the default for moving product development forward.

---

## Responsibilities

You will lead the end-to-end design, implementation, and operation of systems that support the “conversation experience” of Cotomo and new products. Your scope is not fixed; you will tackle the highest-priority problems as the product evolves.

- Design, implement, and operate **APIs used by the Cotomo app** (with product requirements and future scale in mind)
- Design, implement, and operate a **conversation WebSocket server (including agent-like capabilities)**  
  - low latency, session management, streaming, reconnection, state management, etc.
- Design and implement **agent-like capabilities** that support conversation quality  
  - handling conversation state/context, tool execution, guardrail design, etc.
- Run **prompt tuning** and build an improvement cycle  
  - quality evaluation, reproducibility, change management
- **Select and integrate models** (ASR/LLM/speech synthesis, etc.)  
  - system design balancing quality, cost, latency, and operability
- Design and improve **cloud infrastructure** (including Google Cloud and others)  
  - security, networking, data, runtime platform, CI/CD, etc.
- Build **system foundations / operational foundations / team structures** so we can keep delivering value sustainably as users and traffic grow  
  - monitoring, alerting, incident response, SLO considerations, capacity planning, operational improvements
- Collaborate with product managers and designers, support decisions from a technical perspective, and drive continuous product improvement

---

## Expectations as a Senior Engineer

Beyond hands-on implementation, we expect you to **own technical and operational decision-making** and raise the team’s overall output.

- **Technical decision-making**: choose approaches with a balanced view of experience quality, cost, operational load, and development speed
- **Architecture evolution**: deliver practical solutions now while improving the system step-by-step toward scalable, change-tolerant designs
- **Reliability & operations**: build observability (logs/metrics/traces), alerting, incident-response practices, and a repeatable path to prevention
- **Cross-team execution**: align stakeholders (PM/design/ML/platform), clarify trade-offs, and drive delivery through implementation and operations
- **Sustainable improvement loops**: create an environment where validation → learning → iteration works even in uncertain areas (prompts/models/real-time/scale)

---

## Engineering challenges you’ll work on

- Tackling **real-time voice conversation** constraints head-on  
  - latency, interruptions, reconnections, ordering, streaming, and state consistency directly impact UX
- Balancing **scale and reliability**  
  - maintain stable operations at the scale of a 2M+ download product while continuing to ship improvements
- Running LLM/voice models **as a product in production**  
  - building an improvement loop with evaluation, reproducibility, and change management (LLMOps-adjacent)
- Navigating trade-offs between **cost optimization and experience quality**  
  - inference/streaming/infrastructure design to find the best balance
- Turning incident response into product strength  
  - improving observability and operational practices so issues are easier to diagnose and prevent

---

## Who we’re looking for

- Someone who can proactively find and lead “what matters now” to maximize product value, without limiting their scope
- Someone who can make decisions with a balanced view of user experience, operations, cost, and development speed—not only technical correctness
- Someone who can run a cycle of validation and improvement in uncertain domains (models, prompts, real-time, scale)
- Someone who values team outcomes and can involve others through open communication

---

## Required Experience

- **7+ years** (guideline) of hands-on experience designing, implementing, and operating backend systems
- Experience owning technical decision-making and execution as a core engineer in a growth phase or a product launch phase
- Experience using data stores including relational databases (PostgreSQL/MySQL, etc.) and NoSQL
- Experience developing and operating systems that handle large-scale traffic or high load
- Practical experience operating systems on cloud platforms such as AWS / GCP / Azure
- **Japanese is the working language within the engineering team.** Fluency in Japanese for daily work communication (spoken and written)
- Experience continuously improving your workflow with **AI-assisted development tools** (e.g., Devin / Cursor Pro / Claude Code Max / Codex / OpenCode) (personal projects are acceptable)

---

## Preferred Experience

- Design/operations experience with real-time communication technologies such as WebSocket / WebRTC
- Production experience operating ML models, or experience related to tuning/evaluating deep learning models such as LLMs
- Experience with prompt tuning, evaluation design, and operating improvement cycles (an LLMOps-adjacent area)
- Architecture/operations experience on Google Cloud (GCP)
- Experience building observability (logs/metrics/traces), SLO design, and incident-response processes
- Technical communication skills in English
- Development/operations experience in a fast-growing startup environment
- Knowledge or experience in speech recognition, natural language processing, or speech synthesis

---

## Compensation

- **8,500,000 JPY and above**
- Performance-based stock options

---

## Work Style

- Work style: Primarily in-office  
- However, this is not yet a clearly formalized policy. If there are days or a period when coming to the office is difficult due to circumstances such as family matters or caregiving, remote work may be possible upon prior consultation (including one-off requests such as “just this day”).
- VISA sponsorship available (conditions apply)

---

## Tech Stack

*This list evolves over time; below are the main technologies we use today.*

- Languages: **Python / Rust / TypeScript**
- Real-time / Communication: **WebSocket / WebRTC**
- Data stores / Search: **PostgreSQL / Elasticsearch**
- Cloud: **Google Cloud (GCP) / AWS / Azure**
- Analytics / Data platform: **BigQuery / Dataform**
- ML / Inference & Dev: **PyTorch / Transformers / DeepSpeed / vLLM / NVIDIA Triton / Weights & Biases**
- Client / Adjacent: **Unity**
- Observability: **Sentry**
- Collaboration: **Slack / GitHub**
- AI development tools: **Devin / Cursor Pro / Claude Code Max / Codex / OpenCode** (usage may vary by individual. We actively try better tools as they emerge and continuously focus on improving productivity with AI)

---

## Interview Process (example)

*The process may change depending on the situation.*

- Document screening
- Coding test (LLM usage expected)
- Interviews (multiple rounds)
- Offer meeting
