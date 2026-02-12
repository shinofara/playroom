---
marp: true
theme: default
paginate: false
size: 16:9
transition: fade
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');

/* ======================================================
   Cotomo ブランド CSS変数
   ====================================================== */
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

/* ======================================================
   section ベーススタイル
   ====================================================== */
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

/* ======================================================
   コンポーネント: カード (.co-card)
   ====================================================== */
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

/* ======================================================
   コンポーネント: バッジ (.co-badge)
   ====================================================== */
.co-badge {
  display: inline-block;
  background: var(--co-brand);
  color: #FFFFFF;
  font-size: var(--co-font-caption);
  font-weight: 700;
  padding: var(--co-space-xs) var(--co-space-md);
  border-radius: var(--co-radius-pill);
}

/* ======================================================
   コンポーネント: 特大数値 (.co-stat)
   ====================================================== */
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

/* ======================================================
   コンポーネント: テキスト強調 (.co-accent)
   ====================================================== */
.co-accent {
  color: var(--co-brand);
  font-weight: 700;
}

/* ======================================================
   コンポーネント: 対比テキスト (.co-contrast)
   ====================================================== */
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

/* ======================================================
   コンポーネント: 区切り線 (.co-divider)
   ====================================================== */
.co-divider {
  border: none;
  border-top: 1px solid var(--co-divider-color);
  margin: var(--co-space-lg) 0;
}

/* ======================================================
   コンポーネント: 引用ブロック (.co-quote)
   ====================================================== */
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

/* ======================================================
   コンポーネント: ロゴ (.co-logo)
   ====================================================== */
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

/* ======================================================
   コンポーネント: QRコード (.co-qr)
   ====================================================== */
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

/* ======================================================
   コンポーネント: 装飾バブル (.bubble)
   ====================================================== */
.bubble {
  position: absolute;
  border-radius: 50%;
  z-index: 0;
}

.bubble-green  { background: var(--co-bubble-green); }
.bubble-yellow { background: var(--co-bubble-yellow); }
.bubble-pink   { background: var(--co-bubble-pink); }

.bubble-sm { width: 150px; height: 150px; }
.bubble-md { width: 220px; height: 220px; }
.bubble-lg { width: 320px; height: 320px; }

/* ======================================================
   レイアウトパターン
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

/* ======================================================
   共通スライド: タイトル
   ====================================================== */
.title-logo {
  height: 80px;
  margin-bottom: 1rem;
}

.title-sub {
  font-size: var(--co-font-body);
  font-weight: 400;
  color: var(--co-text-secondary);
  margin-top: var(--co-space-sm);
}

.company-logo-corner {
  position: absolute;
  bottom: 28px;
  left: 40px;
  z-index: 2;
  opacity: 0.7;
}

.company-logo-corner img {
  height: 28px;
  width: auto;
}

/* ======================================================
   共通スライド: プロフィール
   ====================================================== */
.profile {
  display: flex;
  align-items: flex-start;
  gap: 2.5rem;
  width: 100%;
  max-width: 900px;
  position: relative;
  z-index: 1;
}

.profile-main {
  flex: 1;
}

.profile-name {
  font-size: 40px;
  font-weight: 900;
  color: var(--co-text-primary);
  margin: 0 0 0.3rem;
  line-height: 1.3;
}

.profile-title {
  font-size: var(--co-font-body);
  font-weight: 700;
  color: var(--co-brand);
  margin: 0 0 1.2rem;
}

.profile-bio {
  font-size: var(--co-font-caption);
  color: var(--co-text-secondary);
  line-height: 1.8;
  margin: 0;
}

.profile-career {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.profile-career .career-tag {
  display: inline-block;
  background: rgba(255, 255, 255, 0.85);
  border-radius: var(--co-radius-sm);
  padding: 0.3rem 0.8rem;
  font-size: 16px;
  font-weight: 500;
  color: var(--co-text-primary);
  box-shadow: var(--co-shadow-sm);
}

/* ======================================================
   共通スライド: 会社紹介
   ====================================================== */
.company-logo {
  height: 64px;
  margin-bottom: 1.5rem;
}
</style>

<!-- ======================================================
     スライド構成テンプレート
     title / profile / company は共通スライドです。
     内容を書き換えて使用してください。
     ====================================================== -->

<!-- ── S1: タイトル ── -->
<!-- レイアウト: title-logo -->

![bg cover](./images/bg-characters.png)

<div class="company-logo-corner">
  <img src="./images/starley-logo.svg" alt="Starley">
</div>

<div class="layout-center">

<img src="./images/cotomo-logo.png" class="title-logo">

# プレゼンテーションタイトル

<div class="title-sub">社名 ｜ 肩書 登壇者名</div>

</div>

---

<!-- ── S2: プロフィール ── -->
<!-- レイアウト: profile -->

<div class="bubble bubble-green bubble-md" style="top:-50px;right:-40px;opacity:0.35;"></div>
<div class="bubble bubble-pink bubble-sm" style="bottom:-30px;left:-30px;opacity:0.35;"></div>

<div class="profile">
<div class="profile-main">

<div class="profile-name">氏名</div>
<div class="profile-title">社名 肩書</div>

<p class="profile-bio">経歴やプロフィールの説明文。knowledge/starley.md を参照して記述。</p>

<div class="profile-career">
  <span class="career-tag">経歴1</span>
  <span class="career-tag">経歴2</span>
  <span class="career-tag co-accent">現職</span>
</div>

</div>
</div>

---

<!-- ── S3: 会社紹介 ── -->
<!-- レイアウト: title-center-sub -->

<div class="bubble bubble-yellow bubble-md" style="top:-60px;left:-50px;opacity:0.35;"></div>
<div class="bubble bubble-green bubble-sm" style="bottom:-30px;right:-40px;opacity:0.35;"></div>

<div class="layout-center">

<img src="./images/starley-logo.svg" class="company-logo">

## 創業年月 ｜ 事業内容

</div>

---

<!-- ── S4〜: 本編スライドをここに追加 ── -->
