# OpenCode 共通コンテキスト

このファイルは、`.opencode/agent/` 配下のすべてのエージェントが参照すべき共通情報を定義します。

---

## 採用関連ドキュメント

### 募集要項（Job Descriptions）

| 項目 | 値 |
|------|-----|
| 保存場所 | `docs/hr/career/` |
| 命名規則 | `YYYY-MM-<ポジション名>.md` |
| 形式 | Markdown（日本語・英語バイリンガル） |

#### 現在の募集要項一覧

```
docs/hr/career/
├── 2025-12-Lead Growth Product Manager.md
├── 2025-12-Product Designer.md
├── 2025-12-Team Lead, Machine Learning - Post-Training for AI Characters.md
├── 2025-12-プロダクトエンジニアProduct Engineer.md
├── 2025-12-プロダクトマネージャー - Product Manager, Communication AI.md
└── 2026-01-Senior-Product-Engineer.md
```

### 候補者評価レビュー（Candidate Reviews）

| 項目 | 値 |
|------|-----|
| 保存場所 | `docs/hr/reviews/` |
| 命名規則 | `YYYY-MM-DD_<候補者名>.md` |

---

## スキル一覧

| スキル名 | 説明 | パス |
|----------|------|------|
| gemini-drive | Google DriveファイルをGeminiで処理 | `.opencode/skills/gemini-drive/` |
| job-posting | 募集要項の作成 | `.opencode/skills/job-posting/` |
| marp | Marpでスライド作成・プレビュー・エクスポート | `.opencode/skills/marp/` |

---

## エージェント一覧

| エージェント名 | 用途 |
|---------------|------|
| engineer-job-post-writer | エンジニア向け募集要項の作成 |
| recruitment-spec-orchestrator | 募集要項作成の統括・調整 |
| resume-reviewer-gemini | レジュメの評価 |
| resume-batch-evaluator | 複数レジュメの一括評価 |
| resume-nogo-evaluator | 不採用判定の評価 |
| gemini-file-session | Geminiファイルセッション |
| obsidian-daily-note-refiner | ObsidianのDailyメモをDaily Noteに整理 |

---

## Obsidian（個人ノート）

| 項目 | 値 |
|------|-----|
| Vault ルート | `Obsidian/` |
| Dailyメモの保存場所（最新） | `Obsidian/daily/YYYY/MM/DD.md` |
| Daily Note（整理版）の保存場所（推奨） | `Obsidian/daily-note/YYYY/MM/DD.md` |

---

## 重要なパス

- **募集要項**: `docs/hr/career/`
- **候補者レビュー**: `docs/hr/reviews/`
- **スキル定義**: `.opencode/skills/`
- **エージェント定義**: `.opencode/agent/`
- **プロンプト**: `.opencode/skills/gemini-drive/prompts/`
- **Obsidian Vault**: `Obsidian/`
- **Obsidian Dailyメモ（最新）**: `Obsidian/daily/YYYY/MM/DD.md`
- **Obsidian Daily Note（整理版・推奨）**: `Obsidian/daily-note/YYYY/MM/DD.md`
