# Cotomo ブランドデザインシステム

Cotomoブランドの実行可能スタイルガイド。すべてのMarpスライドでブランドの一貫性を保つための定義集。

---

## 1. CSS変数定義

スライドの `<style>` ブロックにコピペして使用する。すべての変数は `--co-` プレフィックスで統一。

```html
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');

:root {
  /* ── 背景色 ── */
  --co-bg-primary:   #F3FBF8;   /* 薄ミントグリーン（メイン背景） */
  --co-bg-secondary: #F9FFFC;   /* ほぼ白のミント */
  --co-bg-warm:      #FFFBF5;   /* 暖かみのあるオフホワイト */
  --co-bg-white:     #FFFFFF;   /* 純白 */

  /* ── テキスト色 ── */
  --co-text-primary:   #484848; /* メインテキスト */
  --co-text-secondary: #6b6b6b; /* サブテキスト */
  --co-text-muted:     #1B1B1B; /* 最高コントラスト（見出し等） */

  /* ── ブランドカラー ── */
  --co-brand:       #40B287;    /* ブランドグリーン */
  --co-brand-light: #6CC7A5;    /* 薄グリーン */

  /* ── 装飾バブル色 ── */
  --co-bubble-green:  #6CC7A5;
  --co-bubble-yellow: #D1C45C;
  --co-bubble-pink:   #DA76D7;

  /* ── アクセント色 ── */
  --co-accent-blue:    #298BBF;
  --co-accent-magenta: #B131AE;
  --co-accent-purple:  #9D69E5;
  --co-accent-orange:  #D26737;

  /* ── タイポグラフィ ── */
  --co-font-family:   'Noto Sans JP', sans-serif;
  --co-font-display:    80px;   /* 特大数字・KPI */
  --co-font-heading:    44px;   /* h1・スライドタイトル */
  --co-font-subheading: 32px;   /* h2・セクション見出し */
  --co-font-body:       24px;   /* 本文 */
  --co-font-caption:    18px;   /* 注釈・URL */

  /* ── 余白 ── */
  --co-space-xs:  8px;
  --co-space-sm: 16px;
  --co-space-md: 24px;
  --co-space-lg: 40px;
  --co-space-xl: 64px;

  /* ── 角丸 ── */
  --co-radius-sm:   8px;
  --co-radius-md:  16px;
  --co-radius-pill: 999px;

  /* ── シャドウ ── */
  --co-shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
  --co-shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);

  /* ── 区切り線 ── */
  --co-divider-color: #BBBBBB;
}
</style>
```

---

## 2. section ベーススタイル

全スライド共通の基本設定。フロントマターの直後に配置する。

```html
<style>
section {
  font-family: var(--co-font-family);
  font-size: var(--co-font-body);
  color: var(--co-text-primary);
  background: var(--co-bg-primary);
  padding: var(--co-space-xl);
  line-height: 1.6;
}

h1 {
  font-size: var(--co-font-heading);
  font-weight: 700;
  color: var(--co-text-muted);
  margin-bottom: var(--co-space-md);
}

h2 {
  font-size: var(--co-font-subheading);
  font-weight: 700;
  color: var(--co-text-muted);
  margin-bottom: var(--co-space-sm);
}

p, li {
  font-size: var(--co-font-body);
  color: var(--co-text-primary);
}

strong {
  color: var(--co-text-muted);
}
</style>
```

---

## 3. コンポーネント定義

### 3.1 カード `.co-card` + `.co-card-grid-{2,3,4}`

白背景のカードコンポーネント。情報をグルーピングして表示する。

**CSS定義:**

```html
<style>
.co-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: var(--co-radius-md);
  padding: var(--co-space-lg);
  box-shadow: var(--co-shadow-sm);
}

.co-card-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--co-space-md);
}

.co-card-grid-3 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: var(--co-space-md);
}

.co-card-grid-4 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: var(--co-space-sm);
}
</style>
```

**HTML使用例:**

```html
<div class="co-card-grid-3">
  <div class="co-card">
    <h3>機能A</h3>
    <p>説明テキスト</p>
  </div>
  <div class="co-card">
    <h3>機能B</h3>
    <p>説明テキスト</p>
  </div>
  <div class="co-card">
    <h3>機能C</h3>
    <p>説明テキスト</p>
  </div>
</div>
```

---

### 3.2 バッジ `.co-badge`

CTAボタン風の丸角バッジ。キーワードやラベルの強調に使用。

**CSS定義:**

```html
<style>
.co-badge {
  display: inline-block;
  background: var(--co-brand);
  color: #FFFFFF;
  font-size: var(--co-font-caption);
  font-weight: 700;
  padding: var(--co-space-xs) var(--co-space-md);
  border-radius: var(--co-radius-pill);
}
</style>
```

**HTML使用例:**

```html
<span class="co-badge">音声AI</span>
<span class="co-badge">新機能</span>
```

---

### 3.3 特大数値 `.co-stat`

KPIや印象的な数字をdisplayサイズで表示する。

**CSS定義:**

```html
<style>
.co-stat {
  font-size: var(--co-font-display);
  font-weight: 700;
  color: var(--co-brand);
  line-height: 1.1;
}

.co-stat .co-stat-unit {
  font-size: var(--co-font-subheading);
  color: var(--co-text-secondary);
  margin-left: var(--co-space-xs);
}

.co-stat .co-stat-label {
  display: block;
  font-size: var(--co-font-body);
  font-weight: 400;
  color: var(--co-text-secondary);
  margin-top: var(--co-space-xs);
}
</style>
```

**HTML使用例:**

```html
<div class="co-stat">
  500<span class="co-stat-unit">万</span>
  <span class="co-stat-label">累計ダウンロード数</span>
</div>
```

---

### 3.4 テキスト強調 `.co-accent`

本文中のキーワードをブランドグリーンで強調する。

**CSS定義:**

```html
<style>
.co-accent {
  color: var(--co-brand);
  font-weight: 700;
}
</style>
```

**HTML使用例:**

```html
<p>Cotomoは<span class="co-accent">自然な会話</span>を実現するAIです。</p>
```

---

### 3.5 対比テキスト `.co-contrast`

「Xではない。Yだ。」型の対比表現を視覚的に表現する。

**CSS定義:**

```html
<style>
.co-contrast {
  text-align: center;
  padding: var(--co-space-lg) 0;
}

.co-contrast .co-contrast-before {
  font-size: var(--co-font-subheading);
  color: var(--co-text-secondary);
  text-decoration: line-through;
  text-decoration-color: var(--co-text-secondary);
}

.co-contrast .co-contrast-after {
  font-size: var(--co-font-heading);
  color: var(--co-brand);
  font-weight: 700;
  margin-top: var(--co-space-sm);
}
</style>
```

**HTML使用例:**

```html
<div class="co-contrast">
  <div class="co-contrast-before">ただのチャットボットではない。</div>
  <div class="co-contrast-after">会話を楽しむAI。</div>
</div>
```

---

### 3.6 区切り線 `.co-divider`

セクション間の視覚的な区切り。

**CSS定義:**

```html
<style>
.co-divider {
  border: none;
  border-top: 1px solid var(--co-divider-color);
  margin: var(--co-space-lg) 0;
}
</style>
```

**HTML使用例:**

```html
<hr class="co-divider">
```

---

### 3.7 引用ブロック `.co-quote`

引用やユーザーの声を表示する。

**CSS定義:**

```html
<style>
.co-quote {
  border-left: 4px solid var(--co-brand);
  padding: var(--co-space-md) var(--co-space-lg);
  background: rgba(255, 255, 255, 0.7);
  border-radius: 0 var(--co-radius-sm) var(--co-radius-sm) 0;
  font-size: var(--co-font-body);
  color: var(--co-text-primary);
  font-style: italic;
}

.co-quote .co-quote-author {
  display: block;
  font-size: var(--co-font-caption);
  font-style: normal;
  color: var(--co-text-secondary);
  margin-top: var(--co-space-sm);
}
</style>
```

**HTML使用例:**

```html
<div class="co-quote">
  「毎日話しかけてしまう。友達みたいな存在。」
  <span class="co-quote-author">--- 20代女性ユーザー</span>
</div>
```

---

### 3.8 ロゴ `.co-logo`

ロゴ画像の配置。スライド上部やフッター向け。

**CSS定義:**

```html
<style>
.co-logo {
  display: block;
}

.co-logo img {
  height: 48px;
  width: auto;
  object-fit: contain;
}

.co-logo-center {
  text-align: center;
}

.co-logo-center img {
  height: 80px;
}
</style>
```

**HTML使用例:**

```html
<!-- ヘッダー配置 -->
<div class="co-logo">
  <img src="./images/cotomo-logo.png" alt="Cotomo">
</div>

<!-- 中央配置（表紙向け） -->
<div class="co-logo co-logo-center">
  <img src="./images/cotomo-logo.png" alt="Cotomo">
</div>
```

---

### 3.9 QRコード `.co-qr`

QRコードとURL表示の組み合わせ。

**CSS定義:**

```html
<style>
.co-qr {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--co-space-sm);
}

.co-qr img {
  width: 160px;
  height: 160px;
  border-radius: var(--co-radius-sm);
  box-shadow: var(--co-shadow-sm);
}

.co-qr .co-qr-url {
  font-size: var(--co-font-caption);
  color: var(--co-text-secondary);
}
</style>
```

**HTML使用例:**

```html
<div class="co-qr">
  <img src="./images/qr-code.png" alt="QRコード">
  <span class="co-qr-url">https://cotomo.ai</span>
</div>
```

---

### 3.10 装飾バブル `.bubble`

スライドに有機的な装飾を加える円形バブル。

**CSS定義:**

```html
<style>
.bubble {
  position: absolute;
  border-radius: 50%;
  z-index: 0;
}

.bubble-green  { background: var(--co-bubble-green); }
.bubble-yellow { background: var(--co-bubble-yellow); }
.bubble-pink   { background: var(--co-bubble-pink); }

/* サイズプリセット */
.bubble-sm { width: 150px; height: 150px; }
.bubble-md { width: 220px; height: 220px; }
.bubble-lg { width: 320px; height: 320px; }
</style>
```

**HTML使用例:**

```html
<div class="bubble bubble-green bubble-lg" style="top: -80px; right: -60px; opacity: 0.35;"></div>
<div class="bubble bubble-yellow bubble-sm" style="bottom: -40px; left: -30px; opacity: 0.30;"></div>
<div class="bubble bubble-pink bubble-md" style="top: 60%; right: -50px; opacity: 0.35;"></div>
```

---

## 4. 共通スライドコンポーネント

`cotomo-base.md` テンプレートに定義済み。すべてのCotomo資料で共通して使う冒頭スライド群。

### 4.1 タイトルスライド

| クラス | 用途 |
|--------|------|
| `.title-logo` | プロダクトロゴ（中央、高さ80px） |
| `.title-sub` | サブテキスト（社名 ｜ 肩書 登壇者名） |
| `.company-logo-corner` | 会社ロゴ（左下隅、控えめ表示） |

### 4.2 プロフィールスライド

| クラス | 用途 |
|--------|------|
| `.profile` | プロフィール全体のコンテナ |
| `.profile-main` | メインコンテンツ領域 |
| `.profile-name` | 氏名（40px、太字） |
| `.profile-title` | 会社名・肩書（ブランドグリーン） |
| `.profile-bio` | 経歴説明文（caption サイズ） |
| `.profile-career` | キャリアタグのコンテナ（flex wrap） |
| `.career-tag` | 各経歴のタグ（白背景カード風） |

### 4.3 会社紹介スライド

| クラス | 用途 |
|--------|------|
| `.company-logo` | 会社ロゴ（中央、高さ64px） |

---

## 5. 装飾バブルルール

バブルはスライドに柔らかな印象を与える装飾要素。以下のルールを厳守する。

### 個数制限

- 1スライドあたり **最大3個**
- 0個でも問題ない（すべてのスライドに必須ではない）

### サイズ

| サイズ | 範囲 | クラス |
|--------|------|--------|
| 小 | 150-180px | `.bubble-sm` |
| 中 | 200-250px | `.bubble-md` |
| 大 | 280-350px | `.bubble-lg` |

### 不透明度

- **opacity: 0.30 〜 0.40** の範囲のみ
- コンテンツの可読性を妨げないこと

### 配置

- スライド端から **はみ出す** ように配置する
- `top`, `left`, `right`, `bottom` にマイナス値を使用
- コンテンツ領域と重なる場合は `z-index: 0` でコンテンツの背面に配置

### 推奨 色の組み合わせパターン

| パターン | 組み合わせ |
|----------|------------|
| 基本 | 緑1 + 黄1 |
| 華やか | 緑1 + 黄1 + ピンク1 |
| シンプル | 緑1のみ |
| アクティブ | ピンク1 + 黄1 |

---

## 6. Do's / Don'ts

### Do's

- CSS変数（`var(--co-*)`）を使って色・サイズを指定する
- タイポグラフィは5段階（display / heading / subheading / body / caption）のみ使用する
- 定義済みコンポーネント（`.co-*`）を優先して使う
- 背景色は定義済み4種（primary / secondary / warm / white）から選ぶ
- バブルはスライド端からはみ出すように配置する
- カードの角丸は `var(--co-radius-md)` (16px) を使う

### Don'ts

- 色を直接指定しない（例: `color: #40B287;` ではなく `color: var(--co-brand);`）
- 定義外のフォントサイズを使わない（例: `font-size: 36px;` は不可、`var(--co-font-subheading)` を使う）
- 未定義のクラス名を作成しない（`.co-*` 以外のカスタムクラスは避ける）
- バブルを5個以上配置しない
- バブルの opacity を 0.5 以上にしない
- ブランド外の色を導入しない
- `font-family` を上書きしない（常に Noto Sans JP）
