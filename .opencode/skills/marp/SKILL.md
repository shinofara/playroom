---
name: marp
description: Marp（Markdown Presentation Ecosystem）を使ってスライドを作成・プレビュー・エクスポートするスキル
---

# marp

Markdown記法でプレゼンテーションスライドを作成し、HTML/PDF/PPTXにエクスポートします。

## 概要

このスキルは [Marp](https://marp.app/) を使い、Markdownファイルからスライドを生成します。`npx @marp-team/marp-cli` を使用するため、グローバルインストールは不要です。

## ディレクトリ構成

資料ごとにディレクトリを分けて管理します。

```
marp/
├── <資料名>/
│   ├── <資料名>.md        # スライドソース
│   ├── images/            # 画像素材（必要に応じて）
│   └── out/               # エクスポート出力先（gitignore済み）
│       ├── <資料名>.html
│       ├── <資料名>.pdf
│       └── <資料名>.pptx
└── <別の資料名>/
    ├── <別の資料名>.md
    └── out/
```

## スライドの作成

新しいスライドを作成する際は、テンプレートを参考にしてください。

```
.opencode/skills/marp/templates/default.md
```

### Marp Markdownの基本ルール

1. **フロントマター**: ファイル先頭に `marp: true` を必ず含める
2. **スライド区切り**: `---` で新しいスライドに切り替える
3. **ディレクティブ**: `<!-- directive: value -->` でスライド単位の設定が可能

### よく使うディレクティブ

| ディレクティブ | 説明 | 例 |
|---------------|------|-----|
| `theme` | テーマ設定 | `theme: default`, `theme: gaia`, `theme: uncover` |
| `paginate` | ページ番号表示 | `paginate: true` |
| `header` | ヘッダーテキスト | `header: 'プレゼンタイトル'` |
| `footer` | フッターテキスト | `footer: '© 2026'` |
| `size` | スライドサイズ | `size: 16:9`（デフォルト）, `size: 4:3` |
| `backgroundColor` | 背景色 | `backgroundColor: '#fff'` |
| `backgroundImage` | 背景画像 | `backgroundImage: url('bg.png')` |
| `class` | CSSクラス | `class: lead`（タイトルスライド用） |
| `color` | 文字色 | `color: '#333'` |
| `math` | 数式レンダリング | `math: mathjax` |

### スライド内マークダウン記法

```markdown
# 見出し（スライドタイトル）

- 箇条書き
  - ネスト可能

**太字** / *斜体* / ~~取り消し~~

![画像](./images/image.png)

![bg](./images/background.png)          <!-- 背景画像 -->
![bg left](./images/side-image.png)     <!-- 左半分に画像 -->
![bg right:40%](./images/image.png)     <!-- 右40%に画像 -->
![bg fit](./images/image.png)           <!-- フィットさせる -->

> 引用テキスト

| 列1 | 列2 |
|-----|-----|
| A   | B   |
```

## コマンド

### プレビュー（ブラウザで確認）

```bash
npx @marp-team/marp-cli --preview marp/<資料名>/<資料名>.md
```

### HTMLエクスポート

```bash
npx @marp-team/marp-cli marp/<資料名>/<資料名>.md -o marp/<資料名>/out/<資料名>.html
```

### PDFエクスポート

```bash
npx @marp-team/marp-cli marp/<資料名>/<資料名>.md --pdf -o marp/<資料名>/out/<資料名>.pdf
```

### PPTXエクスポート

```bash
npx @marp-team/marp-cli marp/<資料名>/<資料名>.md --pptx -o marp/<資料名>/out/<資料名>.pptx
```

### ウォッチモード（リアルタイムプレビュー）

```bash
npx @marp-team/marp-cli -w --preview marp/<資料名>/<資料名>.md
```

## 組み込みテーマ

Marpには3つの組み込みテーマがあります：

| テーマ | 説明 |
|--------|------|
| `default` | シンプルなデフォルトテーマ |
| `gaia` | 暗めの配色、プレゼン向き |
| `uncover` | モダンでミニマルなデザイン |

各テーマには `lead` や `invert` などのクラスが用意されています：

```yaml
---
marp: true
theme: gaia
class: lead
---
```

## ワークフロー

1. **ディレクトリ作成**: `marp/<資料名>/` ディレクトリを作成
2. **テンプレート選択**: Cotomo関連 → `cotomo-base.md`、その他 → 適切なテンプレート
3. **スタイルガイド確認**: `cotomo-brand.md` を読み、制約を把握
4. **スライド構成設計**: 各スライドの「役割」を決定
5. **パターン選択**: `layout-patterns.md` から各スライドのレイアウトを選択
6. **コンテンツ記述**: パターンのHTMLスニペットにコンテンツを記入
7. **プレビュー**: `npx @marp-team/marp-cli --preview` で確認
8. **セルフチェック**: 制約ルールに照らして検証
9. **エクスポート**: 必要なフォーマットに変換

## 制約ルール（MUST）

### CSSの記述
- 色は必ずCSS変数（`--co-*`）を参照する。16進数カラーの直接指定は禁止
- フォントサイズは5段階（display/heading/subheading/body/caption）のみ
- 新規CSSクラスの作成は原則禁止。`cotomo-brand.md`・`layout-patterns.md` の定義済みクラスで対応する

### レイアウト
- 各スライドのレイアウトは `layout-patterns.md` から選択する
- 選択したパターンをコメントで記録する（例: `<!-- レイアウト: stat-single -->`）

### カラー
- アクセントカラーは1スライドあたり最大2色
- バブル装飾は1スライドあたり最大3個

### セルフチェック
- CSS変数の直接値（`#XXXXXX`）が残っていないか
- 定義済みコンポーネント以外のクラスが使われていないか

## ブランド画像素材

`.claude/skills/marp/images/` にCotomo関連のロゴ・素材画像を管理しています。スライドで使用する際は、各資料の `images/` ディレクトリにコピーして使ってください。

```
.claude/skills/marp/images/Cotomo_to_oshaberi_sozai/
├── Cotomo_App_icon.png                              # アプリアイコン（レインボー角丸）
├── default/
│   ├── cotomo_logo_logo_style01.png                 # 横型ロゴ（アイコン+テキスト横並び）
│   └── cotomo_logo_logo_style02.png                 # 縦型ロゴ（アイコン上+テキスト下）
├── background_black/
│   ├── cotomo_logo_logo_style01_font_white.png      # 横型・白文字（暗い背景用）
│   └── cotomo_logo_logo_style02_font_white.png      # 縦型・白文字（暗い背景用）
├── monotone_black/
│   ├── cotomo_logo_logo_style01_black.png           # 横型・黒モノトーン
│   └── cotomo_logo_logo_style02_black.png           # 縦型・黒モノトーン
└── monotone_white/
    ├── cotomo_logo_logo_style01_white.png           # 横型・白モノトーン
    └── cotomo_logo_logo_style02_white.png           # 縦型・白モノトーン
```

### ロゴ使い分け

| 背景 | 推奨ロゴ |
|------|---------|
| 明るい背景（`#F3FBF8` 等） | `default/cotomo_logo_logo_style01.png` |
| 暗い背景（gaia等） | `background_black/cotomo_logo_logo_style01_font_white.png` |
| モノクロ印刷 | `monotone_black/cotomo_logo_logo_style01_black.png` |

## テンプレート

`.opencode/skills/marp/templates/` にテンプレートがあります。

| テンプレート | ファイル | 用途 |
|-------------|---------|------|
| cotomo-base **（推奨）** | `templates/cotomo-base.md` | Cotomoブランド資料（ブランドCSS・レイアウト内蔵） |
| default | `templates/default.md` | 汎用プレゼン |
| tech-talk | `templates/tech-talk.md` | 技術発表・LT・勉強会（gaiaテーマ） |
| proposal | `templates/proposal.md` | 提案・企画資料（uncoverテーマ） |

## ガイドライン

`.opencode/skills/marp/guides/` にテーマ別ガイドラインとTipsがあります。

| ガイド | ファイル | 内容 | 参照 |
|--------|---------|------|------|
| Cotomoブランド | `guides/cotomo-brand.md` | CSS変数・コンポーネント定義・Do's/Don'ts | **必須参照** |
| レイアウトパターン | `guides/layout-patterns.md` | レイアウトクラス定義・パターンカタログ | **必須参照** |
| Gaiaテーマ | `guides/theme-gaia.md` | クラス・配色・推奨スタイル | 任意 |
| Uncoverテーマ | `guides/theme-uncover.md` | クラス・配色・レイアウト例 | 任意 |
| スタイリングTips | `guides/styling-tips.md` | CSS・レイアウト・画像配置テクニック | 任意 |

## ナレッジ

`.opencode/skills/marp/knowledge/` に会社・人物などの参照情報を管理しています。スライド作成時に自己紹介や会社紹介が必要な場合に参照してください。

| ナレッジ | ファイル | 内容 |
|----------|---------|------|
| Starley | `knowledge/starley.md` | 会社概要・プロダクト・メンバー情報 |

## 注意事項

- PDFエクスポートにはChrome/Chromiumが必要です
- 画像は `marp/<資料名>/images/` に配置し、スライドからは `./images/` で参照します
- カスタムCSSは `<style>` タグでスライド内に直接記述できます
- `marp/**/out/` は `.gitignore` に追加済みです
