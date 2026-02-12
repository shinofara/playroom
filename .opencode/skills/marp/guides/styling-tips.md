# Marp スタイリング Tips

> **注意**: Cotomoブランドの資料を作成する場合は、まず `cotomo-brand.md`（カラー・タイポ・コンポーネント）と `layout-patterns.md`（レイアウトカタログ）を参照してください。このファイルはブランドに依存しない汎用テクニックです。

テーマ共通で使えるスタイリングのテクニック集。

## フォント設定

### 日本語フォントの指定

```html
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');

section {
  font-family: 'Noto Sans JP', sans-serif;
}
</style>
```

### フォントサイズの調整

```html
<style>
section {
  font-size: 28px;    /* 本文のベースサイズ */
}
h1 {
  font-size: 48px;
}
h2 {
  font-size: 36px;
}
</style>
```

## レイアウト

### 2カラムレイアウト

```html
<style>
.columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}
</style>

<div class="columns">
<div>

### 左カラム

- 内容A
- 内容B

</div>
<div>

### 右カラム

- 内容C
- 内容D

</div>
</div>
```

### 3カラムレイアウト

```html
<style>
.three-columns {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1.5rem;
}
</style>
```

## 背景

### グラデーション背景

```html
<!-- _backgroundImage: linear-gradient(135deg, #667eea 0%, #764ba2 100%) -->
<!-- _color: white -->
```

### 半透明オーバーレイ付き背景画像

```html
<style scoped>
section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
}
</style>

![bg](./images/photo.png)

# 背景画像の上にテキスト
```

## 強調表現

### ハイライトボックス

```html
<style>
.highlight {
  background: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: 1rem;
  border-radius: 4px;
}
</style>

<div class="highlight">

**重要**: ここに強調したい内容を記載

</div>
```

### バッジ風ラベル

```html
<style>
.badge {
  display: inline-block;
  padding: 0.2rem 0.8rem;
  border-radius: 999px;
  font-size: 0.8em;
  font-weight: bold;
}
.badge-new { background: #00b894; color: white; }
.badge-wip { background: #fdcb6e; color: #2d3436; }
.badge-done { background: #6c5ce7; color: white; }
</style>

<span class="badge badge-new">NEW</span> 新機能の紹介
```

## 画像の配置パターン

### 背景画像のサイズ・位置

```markdown
![bg](image.png)              <!-- 全面表示 -->
![bg contain](image.png)      <!-- 収まるように表示 -->
![bg cover](image.png)        <!-- 覆うように表示 -->
![bg fit](image.png)          <!-- フィット -->
![bg auto](image.png)         <!-- 原寸 -->
![bg 80%](image.png)          <!-- 80%サイズ -->
```

### 複数背景画像（分割表示）

```markdown
![bg](image1.png)
![bg](image2.png)
```

2枚指定すると左右に分割表示される。3枚なら3分割。

### 画像に影を付ける

```html
<style>
img[alt~="shadow"] {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-radius: 8px;
}
</style>

![shadow w:500](./images/screenshot.png)
```

## 表のスタイリング

```html
<style>
table {
  width: 100%;
  font-size: 0.9em;
}
th {
  background: #2d3436;
  color: white;
}
tr:nth-child(even) {
  background: #f5f5f5;
}
</style>
```

## アニメーション・トランジション

Marp単体ではスライド間のアニメーションはサポートしていないが、HTML出力時に以下で簡易的なトランジションを追加できる：

```yaml
---
marp: true
transition: fade
---
```

利用可能なトランジション: `fade`, `slide`, `cover`, `none`

※ HTMLプレビュー時のみ有効。PDF/PPTXでは無視される。

## ページ番号のカスタマイズ

### 表紙のページ番号を非表示

```html
<!-- _paginate: false -->
```

### ページ番号のスタイル変更

```html
<style>
section::after {
  font-size: 0.6em;
  color: #999;
}
</style>
```

## ベストプラクティス

1. **1スライド1メッセージ**: 詰め込みすぎない
2. **箇条書きは5項目以内**: 多い場合はスライドを分割
3. **コードは短く**: 15行以上のコードはAppendixへ
4. **統一感**: 色・フォント・余白を全スライドで揃える
5. **画像は高解像度**: ぼやけた画像は避ける
6. **コントラスト**: 背景と文字のコントラスト比を十分に確保する
