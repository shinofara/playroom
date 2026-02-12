---
marp: true
theme: default
paginate: false
size: 16:9
transition: fade
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap');

/* ===== グローバル ===== */
section {
  font-family: 'Noto Sans JP', sans-serif;
  background-color: #F3FBF8;
  color: #484848;
  font-size: 32px;
  letter-spacing: 0.02em;
  position: relative;
  overflow: hidden;
}

h1 {
  font-weight: 900;
  color: #484848;
  line-height: 1.4;
  font-size: 44px;
}

h2 {
  font-weight: 400;
  color: #6b6b6b;
  font-size: 26px;
  margin-top: 1.2rem;
}

/* ===== 装飾バブル ===== */
.bubble {
  position: absolute;
  border-radius: 50%;
  opacity: 0.35;
  z-index: 0;
}
.bubble-green {
  background: #6CC7A5;
}
.bubble-yellow {
  background: #D1C45C;
}
.bubble-pink {
  background: #DA76D7;
}

/* ===== cotomo ロゴ画像 ===== */
.cotomo-logo-img {
  height: 56px;
  margin: 1.5rem 0;
}

/* ===== 3ワードカード ===== */
.three-cards {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 2.5rem;
}
.three-cards .card {
  background: rgba(255, 255, 255, 0.85);
  border-radius: 16px;
  padding: 1rem 1.8rem;
  font-size: 22px;
  font-weight: 700;
  color: #484848;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

/* ===== 特大数字 ===== */
.huge-number {
  font-size: 110px;
  font-weight: 900;
  color: #40B287;
  letter-spacing: 0.03em;
  line-height: 1.1;
  margin: 0.3em 0 0.15em;
  text-align: center;
}

/* ===== アクセントテキスト（cotomoグリーン） ===== */
.accent {
  color: #40B287;
}

/* ===== 対比ライン ===== */
.contrast-line {
  font-size: 36px;
  font-weight: 900;
  color: #40B287;
  margin-top: 1.5rem;
}

/* ===== CTA バッジ ===== */
.cta-badge {
  display: inline-block;
  padding: 0.5rem 2rem;
  background: #40B287;
  border-radius: 999px;
  font-size: 26px;
  font-weight: 700;
  color: #FFFFFF;
  margin-top: 2rem;
  letter-spacing: 0.06em;
}

/* ===== 中央寄せレイアウト ===== */
.center-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  position: relative;
  z-index: 1;
}

/* ===== 区切り線（ブランド準拠） ===== */
.divider {
  width: 60px;
  height: 2px;
  background: #BBBBBB;
  margin: 1rem auto;
}

/* ===== QRセクション ===== */
.qr-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  margin-top: 1.5rem;
}
.qr-section img {
  height: 120px;
}
.qr-section .url {
  font-family: 'Open Sans', sans-serif;
  font-size: 20px;
  color: #6b6b6b;
}

/* ===== タイトルスライド ===== */
.title-logo {
  height: 80px;
  margin-bottom: 1rem;
}

.title-sub {
  font-size: 22px;
  font-weight: 400;
  color: #6b6b6b;
  margin-top: 0.5rem;
}

/* ===== 自己紹介スライド ===== */
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
  color: #484848;
  margin: 0 0 0.3rem;
  line-height: 1.3;
}

.profile-title {
  font-size: 22px;
  font-weight: 700;
  color: #40B287;
  margin: 0 0 1.2rem;
}

.profile-bio {
  font-size: 18px;
  color: #6b6b6b;
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
  border-radius: 8px;
  padding: 0.3rem 0.8rem;
  font-size: 16px;
  font-weight: 500;
  color: #484848;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}
</style>

<!-- レイアウト: title-logo -->
<!--
_backgroundColor: #F3FBF8
-->

<div class="center-content">

<div class="bubble bubble-green" style="width:300px;height:300px;top:-80px;right:-60px;"></div>
<div class="bubble bubble-yellow" style="width:200px;height:200px;bottom:-40px;left:-40px;"></div>

<img src="./images/cotomo-logo.png" class="title-logo">

# Cotomo 1分ピッチ

<div class="title-sub">Starley株式会社 ｜ VPoE 篠原 祐貴</div>

</div>

---

<!-- レイアウト: split-2col-wide -->
<!--
_backgroundColor: #F3FBF8
-->

<div class="bubble bubble-green" style="width:220px;height:220px;top:-50px;right:-40px;"></div>
<div class="bubble bubble-pink" style="width:160px;height:160px;bottom:-30px;left:-30px;"></div>

<div class="profile">
<div class="profile-main">

<div class="profile-name">篠原 祐貴</div>
<div class="profile-title">Starley株式会社 VPoE</div>

<p class="profile-bio">ヤフーを経て、Schoo初代CTO、メドピア技術部長、マネーフォワードケッサイ取締役CTOを歴任。その後SpirのCRO兼CTO、LegalscapeのVPoEを務めるなど、一貫して技術組織の牽引とバリューの最大化に従事。</p>

<p class="profile-bio">現在はStarleyのVPoEとして、エンジニアリングが創出する価値の全体設計を担当。AIと人が共創する<span class="accent">「AIネイティブ」なプロダクト組織</span>の実現をリードしています。</p>

<div class="profile-career">
  <span class="career-tag">Yahoo!</span>
  <span class="career-tag">Schoo CTO</span>
  <span class="career-tag">メドピア</span>
  <span class="career-tag">MFケッサイ CTO</span>
  <span class="career-tag">Spir CRO/CTO</span>
  <span class="career-tag">Legalscape VPoE</span>
  <span class="career-tag accent">Starley VPoE</span>
</div>

</div>
</div>

---

<!-- レイアウト: title-center-sub -->
<!--
_backgroundColor: #F3FBF8
-->

<div class="center-content">

<div class="bubble bubble-yellow" style="width:250px;height:250px;top:-60px;left:-50px;"></div>
<div class="bubble bubble-green" style="width:180px;height:180px;bottom:-30px;right:-40px;"></div>

<img src="./images/starley-logo.svg" style="height:64px; margin-bottom:1.5rem;">

## 2023年4月創業 ｜ AI関連プロダクトの企画・開発

</div>

---

<!--
_backgroundColor: #F3FBF8
-->

<div class="center-content">

<div class="bubble bubble-green" style="width:300px;height:300px;top:-80px;right:-60px;"></div>
<div class="bubble bubble-yellow" style="width:200px;height:200px;bottom:-40px;left:-40px;"></div>
<div class="bubble bubble-pink" style="width:180px;height:180px;bottom:60px;right:100px;"></div>

# 3つだけ、覚えてください。

<div class="three-cards">
  <div class="card"><span class="accent">Cotomo</span></div>
  <div class="card">AIキャラクター市場</div>
  <div class="card">採用</div>
</div>

</div>

<!-- スピーカーノート: 最初に、これだけ覚えていてください。Cotomo。AIキャラクターという新しいエンタメ市場。そして、デザイナとエンジニアを本気で募集しています。これだけ覚えてもらえれば大丈夫です。 -->

---

<!--
_backgroundColor: #F3FBF8
-->

<div class="center-content">

<div class="bubble bubble-green" style="width:250px;height:250px;top:-60px;left:-50px;"></div>
<div class="bubble bubble-pink" style="width:160px;height:160px;bottom:40px;right:-30px;"></div>

<img src="./images/cotomo-logo.png" class="cotomo-logo-img">

# 聞いたこと、ありますか？

</div>

<!-- スピーカーノート: ひとつだけ聞かせてください。Cotomoという、AIキャラクターとおしゃべりできるアプリを、聞いたことあるかも？という人、どれくらいいますか？（挙手を促す）ありがとうございます。 -->

---

<!--
_backgroundColor: #F3FBF8
-->

<div class="center-content">

<div class="bubble bubble-yellow" style="width:280px;height:280px;top:-70px;right:-50px;"></div>
<div class="bubble bubble-green" style="width:200px;height:200px;bottom:-50px;left:80px;"></div>
<div class="bubble bubble-pink" style="width:150px;height:150px;top:100px;left:-30px;"></div>

# AIキャラクターという<br>新しいエンタメ市場が、<br>世界的に、<span class="accent">静かに立ち上がっている。</span>

</div>

<!-- スピーカーノート: まだ知らない人のほうが多いですよね。でも実は今、AIキャラクターと話し、自分の言葉で物語や体験が変わっていく——そんな新しいエンタメ市場が、世界的に静かに立ち上がっています。 -->

---

<!--
_backgroundColor: #F3FBF8
-->

<div class="center-content">

<div class="bubble bubble-green" style="width:350px;height:350px;top:-100px;left:-80px;"></div>
<div class="bubble bubble-yellow" style="width:200px;height:200px;bottom:-40px;right:-40px;"></div>

<div class="huge-number">1,000,000+ DL</div>

## 日本では、今が一番大事なタイミングだ。

</div>

<!-- スピーカーノート: リリース直後に100万、200万ダウンロードに到達するプロダクトも出てきていて、日本では、今が一番大事なタイミングです。 -->

---

<!--
_backgroundColor: #F3FBF8
-->

<div class="center-content">

<div class="bubble bubble-pink" style="width:260px;height:260px;top:-60px;right:-40px;"></div>
<div class="bubble bubble-green" style="width:220px;height:220px;bottom:-60px;left:-50px;"></div>

# 市場の成長と<br>一緒にいるフェーズだ。

<div class="contrast-line">乗るのではない。作る。</div>

</div>

<!-- スピーカーノート: Cotomoは、日本発でこの市場を作りにいっています。成された市場に乗るのではなく、市場の成長と一緒にいるフェーズです。だから正直に言うと—— -->

---

<!--
_backgroundColor: #F3FBF8
-->

<div class="center-content">

<div class="bubble bubble-green" style="width:300px;height:300px;top:-80px;left:-60px;"></div>
<div class="bubble bubble-yellow" style="width:240px;height:240px;bottom:-60px;right:-50px;"></div>
<div class="bubble bubble-pink" style="width:160px;height:160px;top:60px;right:40px;"></div>

# 一緒に作る側として、<br>ぜひ<span class="accent">助けてください。</span>

<div class="cta-badge">Designer & Engineer 募集</div>

<div class="qr-section">
  <img src="./images/qr-code.png">
  <div>
    <img src="./images/cotomo-logo.png" style="height:36px;">
    <div class="url" style="font-size:18px;color:#6b6b6b;margin-top:4px;">https://cotomo.ai/</div>
  </div>
</div>

</div>

<!-- スピーカーノート: フルコミットできるデザイナとエンジニアが、本当に必要です。今しかできないこの挑戦を、一緒に作る側として、ぜひ助けてください。 -->
