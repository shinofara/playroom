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

/* ===== Productスライド（PPTX再現） ===== */
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
  color: #484848;
  line-height: 1.5;
  margin: 0 0 1.5rem;
}

.product-left .product-logo {
  height: 64px;
  margin-bottom: 0.8rem;
}

.product-left .product-subtitle {
  font-size: 24px;
  font-weight: 400;
  color: #6b6b6b;
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

/* ===== 機能紹介スライド（PPTX slide2再現） ===== */
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
  color: #1B1B1B;
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

.feature-tag {
  position: absolute;
  z-index: 3;
  text-align: center;
}

.feature-tag-sm {
  font-size: 11px;
  font-weight: 700;
  color: #FFFFFF;
}

.feature-tag-lg {
  font-size: 20px;
  font-weight: 700;
  color: #FFFFFF;
}

/* ===== ユーザー数スライド（PPTX slide3再現） ===== */
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
  color: #484848;
  line-height: 1;
  margin: 0;
}

.stat-users .stat-sub {
  font-size: 38px;
  font-weight: 700;
  color: #484848;
  margin-top: 0.3rem;
}

/* ===== 累計おしゃべり時間スライド（PPTX slide4再現） ===== */
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
  font-size: 24px;
  font-weight: 700;
  color: #575757;
  margin-bottom: 0.5rem;
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

.stat-chattime .stat-unit-lg {
  font-size: 64px;
  font-weight: 700;
  color: #575757;
}

.stat-chattime .stat-unit-sm {
  font-size: 44px;
  font-weight: 700;
  color: #575757;
}

.stat-chattime .stat-card {
  background: #FFFFFF;
  border-radius: 20px;
  padding: 1rem 2.5rem;
  margin-top: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  font-size: 18px;
  color: #575757;
  font-weight: 500;
  line-height: 1.6;
}

.stat-chattime .stat-card .pink {
  color: #DD82DA;
  font-weight: 700;
}

.char-illust {
  position: absolute;
  z-index: 0;
}

.char-illust img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* ===== CTAスライド（PPTX slide5再現） ===== */
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

.cta-layout .cta-heading {
  font-size: 36px;
  font-weight: 900;
  color: #575757;
  margin: 0;
  line-height: 1.4;
}

.cta-layout .cta-brand {
  font-size: 20px;
  font-weight: 400;
  color: #545454;
  margin-top: 1rem;
}

.cta-layout .cta-divider {
  width: 60px;
  height: 1px;
  background: #BBBBBB;
  margin: 0.8rem auto;
}

.cta-layout .cta-url {
  font-size: 18px;
  color: #6b6b6b;
}
</style>

<!-- レイアウト: title-logo -->
<!--
_backgroundColor: #F3FBF8
-->

![bg cover](./images/bg-characters.png)

<div class="company-logo-corner">
  <img src="./images/starley-logo.svg" alt="Starley">
</div>

<div class="center-content">

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

<!-- レイアウト: product-split（PPTX再現） -->
<!--
_backgroundColor: #F3FBF8
-->

![bg cover](./images/bg-characters.png)

<div class="bubble bubble-green" style="width:280px;height:280px;top:-70px;left:-50px;"></div>
<div class="bubble bubble-yellow" style="width:200px;height:200px;bottom:-40px;left:30%;"></div>
<div class="bubble bubble-pink" style="width:180px;height:180px;top:60px;right:-30px;"></div>

<div class="product-split">
  <div class="product-left">
    <p class="product-catchphrase">だれと、<br>おしゃべりする？</p>
    <img src="./images/cotomo-logo.png" class="product-logo">
    <p class="product-subtitle">おしゃべりAI コトモ</p>
  </div>
  <div class="product-right">
    <img src="./images/app-mockup.png" class="product-mockup">
  </div>
</div>

---

<!-- S5: 機能紹介（PPTX slide2再現） -->
<!--
_backgroundColor: #F3FBF8
-->

<div class="feature-2col">
  <div class="feature-col">
    <p class="feature-col-title">声、アイコン、性格をカスタマイズして<br><strong>AIキャラを作成</strong></p>
    <div class="feature-col-screen">
      <img src="./images/glow-orange.png" class="glow" style="top:-20px;left:-10px;">
      <img src="./images/glow-blue.png" class="glow" style="bottom:-20px;right:20px;">
      <img src="./images/feature-settings.png" class="screen-img">
      <div class="feature-tag" style="bottom:180px;left:10px;">
        <div class="feature-tag-sm">ハイクオリティな</div>
        <div class="feature-tag-lg">声</div>
      </div>
      <div class="feature-tag" style="bottom:80px;right:10px;">
        <div class="feature-tag-sm">作り込める</div>
        <div class="feature-tag-lg">性格</div>
      </div>
      <div class="feature-tag" style="top:30px;right:10px;">
        <div class="feature-tag-sm">自由に設定</div>
        <div class="feature-tag-lg">アイコン</div>
      </div>
    </div>
  </div>
  <div class="feature-col">
    <p class="feature-col-title">他のユーザーが作成したキャラと出会う<br><strong>プラットフォーム</strong></p>
    <div class="feature-col-screen">
      <img src="./images/glow-pink.png" class="glow" style="top:-10px;right:-20px;">
      <img src="./images/glow-green.png" class="glow" style="bottom:20px;left:-10px;">
      <img src="./images/feature-characters.png" class="screen-img">
      <div class="feature-tag" style="bottom:60px;right:20px;">
        <div class="feature-tag-sm">キャラを</div>
        <div class="feature-tag-lg">公開</div>
      </div>
    </div>
  </div>
</div>

---

<!-- S6: ユーザー数（PPTX slide3再現） -->
<!--
_backgroundColor: #FFFFFF
-->

<div class="stat-users">
  <div class="stat-huge">200<span style="font-size:64px;font-style:normal;">万</span></div>
  <div class="stat-sub">ユーザー突破！</div>
</div>

---

<!-- S7: 累計おしゃべり時間（PPTX slide4再現） -->
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
  <div class="stat-title">全ユーザー累計おしゃべり時間</div>
  <div class="stat-number-row">
    <span class="stat-num">250</span>
    <span class="stat-unit-lg">万</span>
    <span class="stat-unit-sm">時間</span>
  </div>
  <div class="stat-card">
    リリースから<span class="pink">1.5年</span>で、約<span class="pink">285年分</span>のおしゃべり時間！
  </div>
</div>

---

<!-- S8: CTA（PPTX slide5再現） -->
<!--
_backgroundColor: #FFFFFF
-->

<img src="./images/blob-red.png" style="position:absolute;width:300px;top:-60px;right:-60px;opacity:0.8;z-index:0;">
<img src="./images/blob-pink.png" style="position:absolute;width:120px;bottom:80px;left:60px;opacity:0.7;z-index:0;">

<div class="cta-layout">
  <img src="./images/cotomo-logo.png" style="height:56px;margin-bottom:0.5rem;">
  <p class="cta-heading">今すぐ<br>おしゃべり！</p>
  <div class="cta-divider"></div>
  <p class="cta-brand">おしゃべりAI コトモ</p>
  <div class="qr-section" style="margin-top:0.8rem;">
    <img src="./images/qr-code.png" style="height:100px;">
    <div>
      <p class="cta-url">https://cotomo.ai/</p>
    </div>
  </div>
</div>

---

<!-- レイアウト: title-center -->
<!--
_backgroundColor: #F3FBF8
-->

![bg cover](./images/bg-characters.png)

<div class="center-content">

# Cotomo 1分ピッチ

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

<div class="huge-number">200万+ DL</div>

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
