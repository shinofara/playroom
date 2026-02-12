---
name: marp
description: Marp（Markdown Presentation Ecosystem）を使ってスライドを作成・プレビュー・エクスポートする。スライド作成やプレゼン準備の依頼時に使用する。
argument-hint: "[操作] [資料名] (例: create my-talk, preview my-talk, export my-talk pdf)"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Marp スライドスキル

Markdownでプレゼンテーションスライドを作成し、HTML/PDF/PPTXにエクスポートします。

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

## 操作

ユーザーの指示に応じて以下の操作を実行してください。引数は `$ARGUMENTS` で渡されます。

### 1. スライド作成（create）

1. `marp/<資料名>/` ディレクトリを作成
2. テンプレート選択:
   - Cotomo関連 → `.opencode/skills/marp/templates/cotomo-base.md` をコピー
   - その他 → 適切なテンプレートを選択
3. **必須**: `.opencode/skills/marp/guides/cotomo-brand.md` を読み、CSS変数とコンポーネント定義を確認
4. **必須**: `.opencode/skills/marp/guides/layout-patterns.md` を読み、各スライドに使うパターンを選択
5. 各スライドに `<!-- レイアウト: {パターン識別子} -->` コメントを付与
6. 制約ルールに従いコンテンツを記述
7. セルフチェック:
   - [ ] 色の直接指定（#XXXXXX）が残っていないか
   - [ ] 5段階以外のフォントサイズが使われていないか
   - [ ] 定義済みコンポーネント以外のクラスが作られていないか
   - [ ] アクセントカラーが3色以上のスライドがないか

### 2. プレビュー（preview）

スライドをブラウザでプレビューします。

```bash
npx @marp-team/marp-cli --preview marp/<資料名>/<資料名>.md
```

### 3. ウォッチモード（watch）

ファイル変更を検知してリアルタイムプレビューします。

```bash
npx @marp-team/marp-cli -w --preview marp/<資料名>/<資料名>.md
```

### 4. エクスポート（export）

指定フォーマットにエクスポートします。出力先は各資料ディレクトリ内の `out/` です。

```bash
# HTML
npx @marp-team/marp-cli marp/<資料名>/<資料名>.md -o marp/<資料名>/out/<資料名>.html

# PDF
npx @marp-team/marp-cli marp/<資料名>/<資料名>.md --pdf -o marp/<資料名>/out/<資料名>.pdf

# PPTX
npx @marp-team/marp-cli marp/<資料名>/<資料名>.md --pptx -o marp/<資料名>/out/<資料名>.pptx
```

### 5. 一覧（list）

既存の資料を `marp/` 配下から一覧表示します。

## ナレッジ

`.opencode/skills/marp/knowledge/` に会社・人物などの参照情報があります。自己紹介や会社紹介スライドの作成時に参照してください。

| ナレッジ | ファイル | 内容 |
|----------|---------|------|
| Starley | `knowledge/starley.md` | 会社概要・プロダクト・メンバー情報 |

## Marp記法リファレンス

### フロントマター（必須）

```yaml
---
marp: true
theme: default    # default | gaia | uncover
paginate: true
size: 16:9
header: 'ヘッダー'
footer: 'フッター'
---
```

### スライド区切り

`---` で次のスライドに切り替え。

### ローカルディレクティブ（スライド単位）

```html
<!-- _class: lead -->        <!-- タイトルスライド -->
<!-- _backgroundColor: #1a1a2e -->
<!-- _color: white -->
<!-- _paginate: false -->    <!-- ページ番号非表示 -->
```

### 画像

```markdown
![通常の画像](./images/image.png)
![bg](./images/bg.png)               <!-- 背景画像 -->
![bg left](./images/side.png)        <!-- 左半分に画像 -->
![bg right:40%](./images/side.png)   <!-- 右40%に画像 -->
![bg fit](./images/image.png)        <!-- フィット -->
![bg blur](./images/image.png)       <!-- ぼかし背景 -->
![w:300](./images/image.png)         <!-- 幅指定 -->
![h:200](./images/image.png)         <!-- 高さ指定 -->
```

### カスタムCSS

```html
<style>
section {
  font-family: 'Noto Sans JP', sans-serif;
}
h1 {
  color: #2d3436;
}
</style>
```

### テーマ別クラス

| テーマ | 利用可能クラス |
|--------|--------------|
| default | (なし) |
| gaia | `lead`, `invert` |
| uncover | `lead`, `invert` |

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

`.opencode/skills/marp/templates/` にテンプレートがあります。スライド作成時に用途に応じて選択してください。

| テンプレート | ファイル | 用途 |
|-------------|---------|------|
| cotomo-base **（推奨）** | `templates/cotomo-base.md` | Cotomoブランド資料（ブランドCSS・レイアウト内蔵） |
| default | `templates/default.md` | 汎用プレゼン |
| tech-talk | `templates/tech-talk.md` | 技術発表・LT・勉強会（gaiaテーマ） |
| proposal | `templates/proposal.md` | 提案・企画資料（uncoverテーマ） |

## ガイドライン

`.opencode/skills/marp/guides/` にテーマ別ガイドラインとTipsがあります。スライド作成・スタイリング時に参照してください。

| ガイド | ファイル | 内容 | 参照 |
|--------|---------|------|------|
| Cotomoブランド | `guides/cotomo-brand.md` | CSS変数・コンポーネント定義・Do's/Don'ts | **必須参照** |
| レイアウトパターン | `guides/layout-patterns.md` | レイアウトクラス定義・パターンカタログ | **必須参照** |
| Gaiaテーマ | `guides/theme-gaia.md` | クラス・配色・推奨スタイル | 任意 |
| Uncoverテーマ | `guides/theme-uncover.md` | クラス・配色・レイアウト例 | 任意 |
| スタイリングTips | `guides/styling-tips.md` | CSS・レイアウト・画像配置テクニック | 任意 |
