# レイアウトパターンライブラリ

AIが「都度CSSを書く」のではなく「パターンを選択する」ためのカタログ。
各パターンにはコピペ可能なHTMLスニペットを含む。

---

## CSS定義（全レイアウトクラス）

スライドの `<style>` セクションに以下をまとめて貼り付ける。
色・サイズはすべてCSS変数 `--co-*` を参照し、ハードコード値は使用しない。

```html
<style>
/* ======================================================
   レイアウトパターン CSS定義
   ====================================================== */

/* --- A: 中央寄せ --- */
.layout-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  height: 100%;
  position: relative;
  z-index: 1;
}

/* --- A: 機能紹介2カラム --- */
.feature-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  height: 100%;
  width: 100%;
  padding: 1.5rem 2.5rem;
  position: relative;
  z-index: 1;
}
.feature-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
}
.feature-col-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--co-text-muted, #1B1B1B);
  text-align: center;
  line-height: 1.5;
  margin: 0;
}
.feature-col-screen {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}
.feature-col-screen img.screen-img {
  max-height: 340px;
  width: auto;
  border-radius: 20px;
  filter: drop-shadow(0 4px 20px rgba(0, 0, 0, 0.1));
  position: relative;
  z-index: 2;
}
.feature-col-screen .glow {
  position: absolute;
  width: 200px;
  height: 200px;
  opacity: 0.5;
  z-index: 0;
}
.feature-tag { position: absolute; z-index: 3; text-align: center; }
.feature-tag-sm { font-size: 11px; font-weight: 700; color: #FFFFFF; }
.feature-tag-lg { font-size: 20px; font-weight: 700; color: #FFFFFF; }

/* --- A: ユーザー数ハイライト --- */
.stat-users {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  position: relative;
  z-index: 1;
}
.stat-users .stat-huge {
  font-size: 120px;
  font-weight: 900;
  font-style: italic;
  color: var(--co-text-primary, #484848);
  line-height: 1;
}
.stat-users .stat-sub {
  font-size: 38px;
  font-weight: 700;
  color: var(--co-text-primary, #484848);
  margin-top: 0.3rem;
}

/* --- A: 累計KPI+キャラクター装飾 --- */
.stat-chattime {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  position: relative;
  z-index: 1;
}
.stat-chattime .stat-title {
  font-size: var(--co-font-body, 24px);
  font-weight: 700;
  color: #575757;
}
.stat-chattime .stat-number-row {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.2rem;
}
.stat-chattime .stat-num {
  font-size: 110px;
  font-weight: 900;
  font-style: italic;
  color: #575757;
  line-height: 1;
}
.stat-chattime .stat-unit-lg { font-size: 64px; font-weight: 700; color: #575757; }
.stat-chattime .stat-unit-sm { font-size: 44px; font-weight: 700; color: #575757; }
.stat-chattime .stat-card {
  background: #FFFFFF;
  border-radius: 20px;
  padding: 1rem 2.5rem;
  margin-top: 1.5rem;
  box-shadow: var(--co-shadow-sm, 0 2px 8px rgba(0,0,0,0.08));
  font-size: var(--co-font-caption, 18px);
  color: #575757;
}
.stat-chattime .stat-card .pink { color: #DD82DA; font-weight: 700; }
.char-illust { position: absolute; z-index: 0; }
.char-illust img { width: 100%; height: 100%; object-fit: contain; }

/* --- A: CTA --- */
.cta-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  position: relative;
  z-index: 1;
  gap: 0.5rem;
}
.cta-layout .cta-heading { font-size: 36px; font-weight: 900; color: #575757; margin: 0; line-height: 1.4; }
.cta-layout .cta-brand { font-size: 20px; color: #545454; margin-top: 1rem; }
.cta-layout .cta-divider { width: 60px; height: 1px; background: var(--co-divider-color, #BBB); margin: 0.8rem auto; }
.cta-layout .cta-url { font-size: var(--co-font-caption, 18px); color: var(--co-text-secondary, #6b6b6b); }

.huge-number {
  font-size: 110px;
  font-weight: 900;
  color: var(--co-brand, #40B287);
  letter-spacing: 0.03em;
  line-height: 1.1;
  margin: 0.3em 0 0.15em;
  text-align: center;
}

/* --- A: プロダクト紹介 --- */
.product-split {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  width: 100%;
  padding: 2rem 3rem;
  position: relative;
  z-index: 1;
}

.product-left {
  flex: 0 0 45%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  padding-left: 1rem;
}

.product-left .product-catchphrase {
  font-size: 38px;
  font-weight: 900;
  color: var(--co-text-primary, #484848);
  line-height: 1.5;
  margin: 0 0 1.5rem;
}

.product-left .product-logo {
  height: 64px;
  margin-bottom: 0.8rem;
}

.product-left .product-subtitle {
  font-size: var(--co-font-body, 24px);
  font-weight: 400;
  color: var(--co-text-secondary, #6b6b6b);
  margin: 0;
}

.product-right {
  flex: 0 0 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-right .product-mockup {
  max-height: 480px;
  width: auto;
  filter: drop-shadow(0 8px 32px rgba(0, 0, 0, 0.15));
}

/* --- B: テキスト中心 --- */
.layout-text {
  display: flex;
  flex-direction: column;
  gap: var(--co-spacing-md, 1.5rem);
  padding: var(--co-spacing-lg, 2rem) var(--co-spacing-xl, 3rem);
}

.layout-steps {
  display: flex;
  flex-direction: column;
  gap: var(--co-spacing-md, 1.5rem);
  padding: var(--co-spacing-lg, 2rem) var(--co-spacing-xl, 3rem);
  counter-reset: step;
}

.layout-steps .step {
  display: flex;
  align-items: flex-start;
  gap: var(--co-spacing-md, 1.5rem);
  counter-increment: step;
}

.layout-steps .step::before {
  content: counter(step);
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: var(--co-color-primary, #00B894);
  color: var(--co-color-on-primary, #fff);
  font-weight: bold;
  font-size: var(--co-font-size-lg, 1.2rem);
  flex-shrink: 0;
}

/* --- C: 分割レイアウト --- */
.layout-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--co-spacing-lg, 2rem);
  height: 100%;
  align-items: start;
  padding: var(--co-spacing-lg, 2rem);
}

.layout-2col-wide {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: var(--co-spacing-lg, 2rem);
  height: 100%;
  align-items: start;
  padding: var(--co-spacing-lg, 2rem);
}

.layout-img-text {
  display: grid;
  grid-template-columns: 2fr 3fr;
  gap: var(--co-spacing-lg, 2rem);
  height: 100%;
  align-items: center;
  padding: var(--co-spacing-lg, 2rem);
}

.layout-text-img {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: var(--co-spacing-lg, 2rem);
  height: 100%;
  align-items: center;
  padding: var(--co-spacing-lg, 2rem);
}

.layout-top-bottom {
  display: grid;
  grid-template-rows: auto 1fr;
  gap: var(--co-spacing-md, 1.5rem);
  height: 100%;
  padding: var(--co-spacing-lg, 2rem);
}

/* --- D: カード/グリッド --- */
.layout-cards {
  display: grid;
  gap: var(--co-spacing-md, 1.5rem);
  padding: var(--co-spacing-md, 1.5rem);
  height: 100%;
  align-items: stretch;
}

.layout-cards.cols-2 {
  grid-template-columns: 1fr 1fr;
}

.layout-cards.cols-3 {
  grid-template-columns: 1fr 1fr 1fr;
}

.layout-cards.cols-4 {
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
}

.layout-cards .card {
  background: var(--co-color-surface, #fff);
  border: 1px solid var(--co-color-border, #e0e0e0);
  border-radius: var(--co-radius-md, 12px);
  padding: var(--co-spacing-md, 1.5rem);
  display: flex;
  flex-direction: column;
  gap: var(--co-spacing-sm, 0.75rem);
}

.layout-cards .card h3 {
  margin: 0;
  color: var(--co-color-primary, #00B894);
  font-size: var(--co-font-size-lg, 1.2rem);
}

.layout-cards .card .icon {
  font-size: 2rem;
  margin-bottom: var(--co-spacing-xs, 0.5rem);
}

/* --- E: 数値ハイライト --- */
.layout-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  height: 100%;
  gap: var(--co-spacing-md, 1.5rem);
}

.layout-stat .stat-number {
  font-size: var(--co-font-size-hero, 5rem);
  font-weight: bold;
  color: var(--co-color-primary, #00B894);
  line-height: 1;
}

.layout-stat .stat-unit {
  font-size: var(--co-font-size-xl, 2rem);
  color: var(--co-color-text-secondary, #666);
}

.layout-stat .stat-label {
  font-size: var(--co-font-size-lg, 1.2rem);
  color: var(--co-color-text-secondary, #666);
}

.layout-stat-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--co-spacing-lg, 2rem);
  height: 100%;
  align-items: center;
  padding: var(--co-spacing-lg, 2rem);
}

.layout-stat-row .stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--co-spacing-sm, 0.75rem);
}

.layout-stat-row .stat-number {
  font-size: var(--co-font-size-xxl, 3rem);
  font-weight: bold;
  color: var(--co-color-primary, #00B894);
  line-height: 1;
}

.layout-stat-row .stat-label {
  font-size: var(--co-font-size-base, 1rem);
  color: var(--co-color-text-secondary, #666);
}

.layout-stat-compare {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: var(--co-spacing-lg, 2rem);
  height: 100%;
  align-items: center;
  justify-items: center;
  padding: var(--co-spacing-lg, 2rem);
}

.layout-stat-compare .arrow {
  font-size: var(--co-font-size-xxl, 3rem);
  color: var(--co-color-primary, #00B894);
}

/* --- F: 引用/強調 --- */
.layout-quote {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  height: 100%;
  padding: var(--co-spacing-xl, 3rem);
}

.layout-quote blockquote {
  font-size: var(--co-font-size-xl, 2rem);
  font-style: italic;
  border: none;
  color: var(--co-color-text, #333);
  max-width: 80%;
  line-height: 1.6;
}

.layout-quote .cite {
  margin-top: var(--co-spacing-md, 1.5rem);
  font-size: var(--co-font-size-base, 1rem);
  color: var(--co-color-text-secondary, #666);
  font-style: normal;
}

.layout-emphasis {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  height: 100%;
  gap: var(--co-spacing-lg, 2rem);
  padding: var(--co-spacing-xl, 3rem);
}

.layout-emphasis .negative {
  font-size: var(--co-font-size-xl, 2rem);
  color: var(--co-color-text-secondary, #666);
  text-decoration: line-through;
}

.layout-emphasis .positive {
  font-size: var(--co-font-size-xxl, 3rem);
  font-weight: bold;
  color: var(--co-color-primary, #00B894);
}

.layout-emphasis .highlight-box {
  background: var(--co-color-accent-bg, #E8F8F5);
  border-left: 4px solid var(--co-color-primary, #00B894);
  border-radius: var(--co-radius-sm, 8px);
  padding: var(--co-spacing-md, 1.5rem) var(--co-spacing-lg, 2rem);
  max-width: 80%;
  text-align: left;
  font-size: var(--co-font-size-lg, 1.2rem);
}

/* --- G: CTA/クロージング --- */
.layout-cta {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  height: 100%;
  gap: var(--co-spacing-md, 1.5rem);
}

.layout-cta .badge {
  display: inline-block;
  padding: var(--co-spacing-xs, 0.5rem) var(--co-spacing-md, 1.5rem);
  border-radius: 999px;
  background: var(--co-color-primary, #00B894);
  color: var(--co-color-on-primary, #fff);
  font-weight: bold;
  font-size: var(--co-font-size-sm, 0.9rem);
}

.layout-cta-qr {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--co-spacing-xl, 3rem);
  height: 100%;
  align-items: center;
  padding: var(--co-spacing-xl, 3rem);
}

.layout-cta-qr .qr-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--co-spacing-sm, 0.75rem);
}

.layout-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--co-spacing-lg, 2rem);
  height: 100%;
  align-items: start;
  padding: var(--co-spacing-lg, 2rem);
}

.layout-summary .next-steps {
  background: var(--co-color-accent-bg, #E8F8F5);
  border-radius: var(--co-radius-md, 12px);
  padding: var(--co-spacing-md, 1.5rem);
}
</style>
```

---

## カテゴリ A: タイトル/リード

### 中央1メッセージ（`title-center`）

**用途**: 表紙、セクション区切り、問いかけスライド
**配置**: テキストを縦横中央に配置

```html
<!-- レイアウト: title-center -->
<div class="layout-center">

# スライドタイトル

</div>
```

---

### 中央メッセージ + サブテキスト（`title-center-sub`）

**用途**: 表紙（発表者名・日付付き）、セクション導入
**配置**: メインタイトルとサブテキストを中央配置

```html
<!-- レイアウト: title-center-sub -->
<div class="layout-center">

# メインタイトル

社名 ｜ 肩書 登壇者名

</div>
```

---

### ロゴ + タイトル（`title-logo`）

**用途**: ブランド紹介、会社紹介の表紙
**配置**: ロゴ画像とタイトルを中央縦並び

```html
<!-- レイアウト: title-logo -->
<div class="layout-center">

![w:200](./images/logo.png)

# プロダクト名

キャッチコピーやサブタイトル

</div>
```

---

### プロダクト紹介（`product-split`）

**用途**: プロダクトのキャッチコピー + アプリ画面モックアップの分割表示
**配置**: 左にキャッチコピー・ロゴ・サブタイトル、右にアプリ画面mockup

```html
<!-- レイアウト: product-split -->

![bg cover](./images/bg-characters.png)

<div class="bubble bubble-green" style="width:280px;height:280px;top:-70px;left:-50px;"></div>
<div class="bubble bubble-yellow" style="width:200px;height:200px;bottom:-40px;left:30%;"></div>
<div class="bubble bubble-pink" style="width:180px;height:180px;top:60px;right:-30px;"></div>

<div class="product-split">
  <div class="product-left">
    <p class="product-catchphrase">キャッチコピー</p>
    <img src="./images/cotomo-logo.png" class="product-logo">
    <p class="product-subtitle">プロダクトのサブタイトル</p>
  </div>
  <div class="product-right">
    <img src="./images/app-mockup.png" class="product-mockup">
  </div>
</div>
```

---

### 機能紹介2カラム（`feature-2col`）

**用途**: プロダクトの主要機能を2カラムでスクリーンショット付きで紹介。各カラムにタイトル＋スクリーンショット＋グローエフェクト＋機能タグ
**配置**: 左右対称の2カラム、各カラムにアプリ画面とグロー装飾

```html
<!-- レイアウト: feature-2col -->
<div class="feature-2col">
  <div class="feature-col">
    <p class="feature-col-title">左カラムタイトル<br><strong>サブタイトル</strong></p>
    <div class="feature-col-screen">
      <img src="./images/glow-orange.png" class="glow" style="top:-20px;left:-10px;">
      <img src="./images/glow-blue.png" class="glow" style="bottom:-20px;right:20px;">
      <img src="./images/feature-settings.png" class="screen-img">
      <div class="feature-tag" style="bottom:180px;left:10px;">
        <div class="feature-tag-sm">ラベル</div>
        <div class="feature-tag-lg">機能名</div>
      </div>
    </div>
  </div>
  <div class="feature-col">
    <p class="feature-col-title">右カラムタイトル<br><strong>サブタイトル</strong></p>
    <div class="feature-col-screen">
      <img src="./images/glow-pink.png" class="glow" style="top:-10px;right:-20px;">
      <img src="./images/glow-green.png" class="glow" style="bottom:20px;left:-10px;">
      <img src="./images/feature-characters.png" class="screen-img">
    </div>
  </div>
</div>
```

---

### ユーザー数ハイライト（`stat-users`）

**用途**: ユーザー数などの大きな数値をイタリック太字で中央にインパクト表示
**配置**: 特大数値＋サブテキストを中央縦並び。背景白

```html
<!-- レイアウト: stat-users -->
<!--
_backgroundColor: #FFFFFF
-->
<div class="stat-users">
  <div class="stat-huge">200<span style="font-size:64px;font-style:normal;">万</span></div>
  <div class="stat-sub">ユーザー突破！</div>
</div>
```

---

### 累計KPI + キャラクター装飾（`stat-chattime`）

**用途**: 利用時間等のKPIをキャラクターイラスト付きで表示。ピンクのアクセント色で強調テキスト
**配置**: 中央にKPI＋補足カード、周囲にキャラクターイラスト＋グロー装飾。背景白

```html
<!-- レイアウト: stat-chattime -->
<!--
_backgroundColor: #FFFFFF
-->
<div class="char-illust" style="width:180px;height:180px;top:40px;left:40px;">
  <img src="./images/char-boy.png">
</div>
<div class="char-illust" style="width:160px;height:160px;bottom:30px;left:120px;">
  <img src="./images/char-girl-purple.png">
</div>
<div class="char-illust" style="width:170px;height:170px;bottom:40px;right:60px;">
  <img src="./images/char-girl-green.png">
</div>
<div class="bubble bubble-yellow" style="width:260px;height:260px;bottom:-40px;left:30%;opacity:0.40;"></div>

<div class="stat-chattime">
  <div class="stat-title">指標ラベル</div>
  <div class="stat-number-row">
    <span class="stat-num">数値</span>
    <span class="stat-unit-lg">万</span>
    <span class="stat-unit-sm">単位</span>
  </div>
  <div class="stat-card">
    補足テキスト <span class="pink">強調部分</span>
  </div>
</div>
```

---

### CTA + QR（`cta-layout`）

**用途**: プロダクトへの誘導。ロゴ＋CTAメッセージ＋区切り線＋ブランド名＋QRコード
**配置**: 全要素を中央縦並び。背景白にカラフルなblob装飾

```html
<!-- レイアウト: cta-layout -->
<!--
_backgroundColor: #FFFFFF
-->
<div class="cta-layout">
  <img src="./images/cotomo-logo.png" style="height:56px;margin-bottom:0.5rem;">
  <p class="cta-heading">CTAメッセージ</p>
  <div class="cta-divider"></div>
  <p class="cta-brand">おしゃべりAI コトモ</p>
  <div class="qr-section" style="margin-top:0.8rem;">
    <img src="./images/qr-code.png" style="height:100px;">
    <div>
      <p class="cta-url">https://cotomo.ai/</p>
    </div>
  </div>
</div>
```

---

### 目次/アジェンダ（`title-toc`）

**用途**: 目次、アジェンダ、発表の構成紹介
**配置**: 見出しと番号付きリスト

```html
<!-- レイアウト: title-toc -->
<div class="layout-text">

# アジェンダ

1. はじめに
2. 背景・課題
3. 提案内容
4. デモ
5. まとめ

</div>
```

---

## カテゴリ B: テキスト中心

### 見出し + 箇条書き（`text-heading-list`）

**用途**: 情報伝達、ポイント列挙
**配置**: 上部に見出し、下部に箇条書き

```html
<!-- レイアウト: text-heading-list -->
<div class="layout-text">

# 主要な発見

- ユーザーの80%がモバイルからアクセス
- 平均セッション時間は3分
- リテンション率が前月比15%向上
- NPS スコアが業界平均を上回る

</div>
```

---

### 見出し + 段落テキスト（`text-heading-paragraph`）

**用途**: 説明、ストーリーテリング、背景情報
**配置**: 見出しの下に本文段落

```html
<!-- レイアウト: text-heading-paragraph -->
<div class="layout-text">

# 背景

私たちのチームは、ユーザー体験を根本から見直すプロジェクトに取り組んできました。
従来のアプローチでは解決できなかった課題に対し、新しい技術スタックを導入することで
大幅な改善を実現しました。

</div>
```

---

### 見出し + 箇条書き + 注釈（`text-heading-list-note`）

**用途**: 補足情報付きのポイント列挙
**配置**: 見出し、箇条書き、下部に注釈

```html
<!-- レイアウト: text-heading-list-note -->
<div class="layout-text">

# 導入要件

- Node.js 20 以上
- Docker 環境
- AWS アカウント（本番環境用）

<small style="color: var(--co-color-text-secondary, #666);">
※ 開発環境ではDockerのみで動作可能です
</small>

</div>
```

---

### ステップ/タイムライン（`text-steps`）

**用途**: プロセス説明、手順、ロードマップ
**配置**: 番号付きステップを縦に配置

```html
<!-- レイアウト: text-steps -->
<div class="layout-text">

# 導入ステップ

<div class="layout-steps">
<div class="step">
<div>

**環境構築**
リポジトリのクローンと依存関係のインストール

</div>
</div>
<div class="step">
<div>

**設定ファイルの作成**
`.env` と `config.yaml` を環境に合わせて編集

</div>
</div>
<div class="step">
<div>

**デプロイ**
CI/CDパイプラインを通じて本番環境にデプロイ

</div>
</div>
</div>

</div>
```

---

## カテゴリ C: 分割レイアウト

### 2カラム均等（`split-2col`）

**用途**: 比較、対照、2つの視点
**配置**: 左右均等に2カラム

```html
<!-- レイアウト: split-2col -->
# 比較：プランA vs プランB

<div class="layout-2col">
<div>

### プランA

- 低コスト
- 導入が簡単
- スケーラビリティに制限

</div>
<div>

### プランB

- 高機能
- カスタマイズ性が高い
- 初期投資が必要

</div>
</div>
```

---

### 2カラム非対称（`split-2col-wide`）

**用途**: メインコンテンツ + 補足情報
**配置**: 左6:右4の非対称カラム

```html
<!-- レイアウト: split-2col-wide -->
# アーキテクチャ概要

<div class="layout-2col-wide">
<div>

### システム構成

メインのアプリケーションはマイクロサービスアーキテクチャを採用。
各サービスはKubernetes上で独立してデプロイ可能。

- API Gateway
- 認証サービス
- ビジネスロジック
- データストア

</div>
<div>

### 技術スタック

- **言語**: Go, TypeScript
- **DB**: PostgreSQL
- **キャッシュ**: Redis
- **インフラ**: AWS EKS

</div>
</div>
```

---

### 左画像 + 右テキスト（`split-img-left`）

**用途**: スクリーンショット付き説明、ビジュアル+テキスト
**配置**: 左に画像、右にテキスト

```html
<!-- レイアウト: split-img-left -->
# 新しいダッシュボード

<div class="layout-img-text">
<div>

![w:100%](./images/dashboard.png)

</div>
<div>

### 主な改善点

- リアルタイムデータ表示
- カスタマイズ可能なウィジェット
- ダークモード対応
- モバイルレスポンシブ

</div>
</div>
```

---

### 右画像 + 左テキスト（`split-img-right`）

**用途**: テキスト説明+ビジュアル補足
**配置**: 左にテキスト、右に画像

```html
<!-- レイアウト: split-img-right -->
# ユーザーフロー

<div class="layout-text-img">
<div>

### 操作手順

1. ホーム画面でメニューを開く
2. 「新規作成」をタップ
3. テンプレートを選択
4. 内容を入力して保存

直感的なUIで迷わず操作できます。

</div>
<div>

![w:100%](./images/user-flow.png)

</div>
</div>
```

---

### 上下分割（`split-top-bottom`）

**用途**: 見出し+メインコンテンツ、図表+説明
**配置**: 上部と下部に分割

```html
<!-- レイアウト: split-top-bottom -->
<div class="layout-top-bottom">
<div>

# 月次売上推移

![w:90%](./images/chart.png)

</div>
<div>

**分析**: 7月以降、新機能リリースに伴い売上が30%増加。特にエンタープライズプランの契約が好調。

</div>
</div>
```

---

## カテゴリ D: カード/グリッド

### 2カード横並び（`card-2`）

**用途**: 2つの概念・サービスの紹介
**配置**: 2枚のカードを横に並べる

```html
<!-- レイアウト: card-2 -->
# サービスラインナップ

<div class="layout-cards cols-2">
<div class="card">

### Basic

- 月額 ¥980
- 基本機能
- メールサポート

</div>
<div class="card">

### Pro

- 月額 ¥2,980
- 全機能
- 優先サポート

</div>
</div>
```

---

### 3カード横並び（`card-3`）

**用途**: 3つの特徴・プラン・ステージ
**配置**: 3枚のカードを横に並べる

```html
<!-- レイアウト: card-3 -->
# 3つの強み

<div class="layout-cards cols-3">
<div class="card">

### スピード

高速なレスポンスで
ストレスフリーな体験

</div>
<div class="card">

### セキュリティ

エンタープライズグレードの
セキュリティ対策

</div>
<div class="card">

### スケーラビリティ

負荷に応じた
自動スケーリング

</div>
</div>
```

---

### 4カード（2x2）（`card-4-grid`）

**用途**: 4つの要素をグリッド表示
**配置**: 2行2列のグリッド

```html
<!-- レイアウト: card-4-grid -->
# 主要機能

<div class="layout-cards cols-4">
<div class="card">

### ダッシュボード

データを一目で把握

</div>
<div class="card">

### レポート

自動レポート生成

</div>
<div class="card">

### アラート

異常検知の即時通知

</div>
<div class="card">

### API

外部連携が容易

</div>
</div>
```

---

### 見出し + 3カード（`card-3-headed`）

**用途**: セクション見出し付きの3要素紹介
**配置**: 上部に見出し、下部に3カード

```html
<!-- レイアウト: card-3-headed -->
<div class="layout-top-bottom">
<div>

# なぜ選ばれるのか

多くのお客様に選ばれる3つの理由

</div>
<div>

<div class="layout-cards cols-3">
<div class="card">

### 実績

導入企業 500社以上

</div>
<div class="card">

### サポート

24/365 対応体制

</div>
<div class="card">

### コスト

業界最安水準

</div>
</div>

</div>
</div>
```

---

### アイコン付きカード（`card-icon`）

**用途**: ビジュアルアクセント付きの特徴紹介
**配置**: 各カードにアイコン（絵文字）を配置

```html
<!-- レイアウト: card-icon -->
# プラットフォーム対応

<div class="layout-cards cols-3">
<div class="card">
<div class="icon">🌐</div>

### Web

モダンブラウザ対応
PWA サポート

</div>
<div class="card">
<div class="icon">📱</div>

### Mobile

iOS / Android
ネイティブアプリ

</div>
<div class="card">
<div class="icon">🖥️</div>

### Desktop

Windows / macOS
Electronアプリ

</div>
</div>
```

---

## カテゴリ E: 数値ハイライト

### 単一KPI（`stat-single`）

**用途**: インパクトのある1つの数値を大きく表示
**配置**: 特大の数値を中央に配置

```html
<!-- レイアウト: stat-single -->
<div class="layout-stat">

<div class="stat-number">98<span class="stat-unit">%</span></div>
<div class="stat-label">顧客満足度</div>

</div>
```

---

### 3KPI横並び（`stat-3`）

**用途**: 複数の主要指標を並べて表示
**配置**: 3つのKPIを横に均等配置

```html
<!-- レイアウト: stat-3 -->
# 主要指標

<div class="layout-stat-row">
<div class="stat-item">
<div class="stat-number">1.2M</div>
<div class="stat-label">月間アクティブユーザー</div>
</div>
<div class="stat-item">
<div class="stat-number">99.9%</div>
<div class="stat-label">稼働率</div>
</div>
<div class="stat-item">
<div class="stat-number">4.8</div>
<div class="stat-label">アプリ評価（5段階）</div>
</div>
</div>
```

---

### KPI + 説明文（`stat-explained`）

**用途**: 数値の背景や文脈を添えて表示
**配置**: 大きな数値と説明テキスト

```html
<!-- レイアウト: stat-explained -->
<div class="layout-stat">

<div class="stat-number">3x</div>
<div class="stat-label">開発速度の向上</div>

従来の手動テスト工程をCI/CDに置き換えた結果、
リリースサイクルが月1回から週3回に改善しました。

</div>
```

---

### Before/After 数値（`stat-compare`）

**用途**: 改善効果、ビフォーアフターの数値比較
**配置**: 左にBefore、中央に矢印、右にAfter

```html
<!-- レイアウト: stat-compare -->
# レスポンス時間の改善

<div class="layout-stat-compare">
<div class="stat-item">
<div class="stat-label">Before</div>
<div class="stat-number">1.8s</div>
</div>
<div class="arrow">→</div>
<div class="stat-item">
<div class="stat-label">After</div>
<div class="stat-number" style="color: var(--co-color-primary, #00B894);">0.3s</div>
</div>
</div>
```

---

## カテゴリ F: 引用/強調

### 大引用（`quote-large`）

**用途**: インパクトのある引用、メッセージ
**配置**: 引用テキストを中央に大きく表示

```html
<!-- レイアウト: quote-large -->
<div class="layout-quote">

> 最も重要なのは、ユーザーが何を言うかではなく、何をするかだ。

</div>
```

---

### 引用 + 出典（`quote-cited`）

**用途**: 出典付きの引用
**配置**: 引用テキスト + 出典情報

```html
<!-- レイアウト: quote-cited -->
<div class="layout-quote">

> シンプルであることは、複雑であることよりも難しい。

<div class="cite">— Steve Jobs, BusinessWeek, 1998</div>

</div>
```

---

### 対比強調（`emphasis-contrast`）

**用途**: 「XではなくY」形式の対比メッセージ
**配置**: 否定と肯定を上下に対比

```html
<!-- レイアウト: emphasis-contrast -->
<div class="layout-emphasis">

<div class="negative">たくさんの機能を作ること</div>
<div class="positive">ユーザーの課題を解決すること</div>

</div>
```

---

### ハイライトボックス（`emphasis-box`）

**用途**: 重要メッセージの強調、注意事項
**配置**: 枠線付きボックスで強調

```html
<!-- レイアウト: emphasis-box -->
<div class="layout-emphasis">

# 重要なお知らせ

<div class="highlight-box">

**2026年4月より新料金プランに移行します。**
既存のお客様は2026年9月まで現行プランをご利用いただけます。
詳細はサポートページをご確認ください。

</div>

</div>
```

---

## カテゴリ G: CTA/クロージング

### CTA + バッジ（`cta-badge`）

**用途**: アクション誘導、お知らせ
**配置**: バッジとCTAメッセージを中央に

```html
<!-- レイアウト: cta-badge -->
<div class="layout-cta">

<span class="badge">無料トライアル実施中</span>

# 今すぐ始めましょう

お申し込みは公式サイトから

**https://example.com/signup**

</div>
```

---

### CTA + QRコード（`cta-qr`）

**用途**: URLやアプリDLへの誘導
**配置**: 左にCTAテキスト、右にQRコード+ロゴ

```html
<!-- レイアウト: cta-qr -->
<div class="layout-cta-qr">
<div>

# アプリをダウンロード

App Store / Google Play で
「プロダクト名」を検索

**https://example.com/download**

</div>
<div class="qr-area">

![w:200](./images/qr-code.png)

![w:80](./images/logo.png)

</div>
</div>
```

---

### シンプルお礼（`closing-thanks`）

**用途**: プレゼン締めくくり、Q&A導入
**配置**: お礼メッセージを中央に

```html
<!-- レイアウト: closing-thanks -->
<div class="layout-center">

# ありがとうございました

ご質問・フィードバックをお待ちしております

</div>
```

---

### まとめ + Next Step（`closing-summary`）

**用途**: プレゼンの締め、要約+次のアクション
**配置**: 左にまとめ、右にNext Step

```html
<!-- レイアウト: closing-summary -->
# まとめ

<div class="layout-summary">
<div>

### 本日のポイント

- ポイント1の要約
- ポイント2の要約
- ポイント3の要約

</div>
<div class="next-steps">

### Next Steps

1. フィードバックの共有（今週中）
2. プロトタイプレビュー（来週）
3. 本番リリース判断（月末）

</div>
</div>
```

---

## パターン選択ガイド

| やりたいこと | 推奨パターン |
|-------------|-------------|
| プロダクトを紹介したい | `product-split` |
| 機能を紹介したい | `feature-2col` |
| ユーザー数をインパクトに | `stat-users` |
| KPI+キャラクター装飾 | `stat-chattime` |
| CTA+QRで誘導したい | `cta-layout` |
| 表紙を作りたい | `title-center-sub`, `title-logo` |
| セクション区切り | `title-center` |
| 目次を見せたい | `title-toc` |
| ポイントを列挙したい | `text-heading-list` |
| 手順を説明したい | `text-steps` |
| 2つを比較したい | `split-2col`, `stat-compare` |
| 画像付きで説明したい | `split-img-left`, `split-img-right` |
| 複数の特徴を並べたい | `card-3`, `card-icon` |
| 数値をインパクトに見せたい | `stat-single`, `stat-3` |
| 改善効果を見せたい | `stat-compare`, `stat-explained` |
| 印象的な一言を見せたい | `quote-large`, `emphasis-contrast` |
| 重要事項を強調したい | `emphasis-box` |
| アクションを促したい | `cta-badge`, `cta-qr` |
| プレゼンを締めたい | `closing-thanks`, `closing-summary` |
