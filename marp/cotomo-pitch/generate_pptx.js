/**
 * Cotomo 1分ピッチ PPTX生成スクリプト（PptxGenJS版）
 * Anthropic PPTX Skill準拠
 */
const pptxgen = require("pptxgenjs");
const path = require("path");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3" × 7.5"
pres.author = "Starley Inc.";
pres.title = "Cotomo 1分ピッチ";

const IMG = path.join(__dirname, "images");
const img = (name) => path.join(IMG, name);

// --- ブランドカラー（#なし） ---
const C = {
  bgLight: "F3FBF8",
  white: "FFFFFF",
  textPrimary: "484848",
  textSecondary: "6b6b6b",
  textDark: "575757",
  brand: "40B287",
  bubbleGreen: "6CC7A5",
  bubbleYellow: "D1C45C",
  bubblePink: "DA76D7",
  accentPink: "DD82DA",
};

/** 装飾バブル */
function addBubble(slide, x, y, w, h, color, opacity = 0.35) {
  slide.addShape(pres.shapes.OVAL, {
    x, y, w, h,
    fill: { color, transparency: Math.round((1 - opacity) * 100) },
    line: { type: "none" },
  });
}

// =================================================================
// S1: タイトル
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.bgLight });
  s.addImage({ path: img("bg-characters.png"), x: 0, y: 0, w: 13.3, h: 7.5, sizing: { type: "cover", w: 13.3, h: 7.5 } });
  addBubble(s, -0.5, -0.8, 3, 3, C.bubbleGreen);
  addBubble(s, 10, 5, 2.5, 2.5, C.bubblePink);
  s.addImage({ path: img("cotomo-logo.png"), x: 4.8, y: 1.8, h: 0.9 });
  s.addText("Cotomo 1分ピッチ", {
    x: 1, y: 3.0, w: 11.3, h: 1.2,
    fontSize: 44, fontFace: "Noto Sans JP", bold: true,
    color: C.textPrimary, align: "center", valign: "middle",
  });
  s.addText("Starley株式会社 ｜ VPoE 篠原 祐貴", {
    x: 1, y: 4.3, w: 11.3, h: 0.6,
    fontSize: 22, fontFace: "Noto Sans JP", color: C.textSecondary, align: "center",
  });
  s.addImage({ path: img("starley-logo.png"), x: 0.4, y: 6.8, h: 0.3 });
}

// =================================================================
// S2: プロフィール
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.bgLight });
  addBubble(s, 10.5, -0.5, 2.5, 2.5, C.bubbleGreen);
  addBubble(s, -0.3, 5.5, 1.8, 1.8, C.bubblePink);

  s.addText("篠原 祐貴", {
    x: 0.8, y: 0.5, w: 8, h: 0.8,
    fontSize: 40, fontFace: "Noto Sans JP", bold: true, color: C.textPrimary, align: "left", margin: 0,
  });
  s.addText("Starley株式会社 VPoE", {
    x: 0.8, y: 1.3, w: 8, h: 0.5,
    fontSize: 22, fontFace: "Noto Sans JP", bold: true, color: C.brand, align: "left", margin: 0,
  });
  s.addText("ヤフーを経て、Schoo初代CTO、メドピア技術部長、マネーフォワードケッサイ取締役CTOを歴任。その後SpirのCRO兼CTO、LegalscapeのVPoEを務めるなど、一貫して技術組織の牽引とバリューの最大化に従事。", {
    x: 0.8, y: 2.0, w: 10.5, h: 1.2,
    fontSize: 16, fontFace: "Noto Sans JP", color: C.textSecondary, align: "left",
  });
  s.addText([
    { text: "現在はStarleyのVPoEとして、エンジニアリングが創出する価値の全体設計を担当。AIと人が共創する", options: { color: C.textSecondary } },
    { text: "「AIネイティブ」なプロダクト組織", options: { color: C.brand } },
    { text: "の実現をリードしています。", options: { color: C.textSecondary } },
  ], {
    x: 0.8, y: 3.4, w: 10.5, h: 1.2,
    fontSize: 16, fontFace: "Noto Sans JP", align: "left",
  });

  const careers = ["Yahoo!", "Schoo CTO", "メドピア", "MFケッサイ CTO", "Spir CRO/CTO", "Legalscape VPoE", "Starley VPoE"];
  let tx = 0.8;
  careers.forEach((c, i) => {
    const isCurrent = c === "Starley VPoE";
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: tx, y: 5.0, w: 1.6, h: 0.45,
      fill: { color: isCurrent ? "E8F8F0" : "F0F0F0" },
      line: { type: "none" }, rectRadius: 0.1,
    });
    s.addText(c, {
      x: tx, y: 5.0, w: 1.6, h: 0.45,
      fontSize: 13, fontFace: "Noto Sans JP", bold: true,
      color: isCurrent ? C.brand : C.textPrimary, align: "center", valign: "middle", margin: 0,
    });
    tx += 1.7;
  });
}

// =================================================================
// S3: 会社紹介
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.bgLight });
  addBubble(s, -0.5, -0.6, 2.8, 2.8, C.bubbleYellow);
  addBubble(s, 10.5, 5.5, 2, 2, C.bubbleGreen);
  s.addImage({ path: img("starley-logo.png"), x: 4.5, y: 2.5, h: 0.7 });
  s.addText("2023年4月創業 ｜ AI関連プロダクトの企画・開発", {
    x: 1, y: 4.0, w: 11.3, h: 0.7,
    fontSize: 26, fontFace: "Noto Sans JP", color: C.textSecondary, align: "center",
  });
}

// =================================================================
// S4: プロダクト紹介
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.bgLight });
  s.addImage({ path: img("bg-characters.png"), x: 0, y: 0, w: 13.3, h: 7.5, sizing: { type: "cover", w: 13.3, h: 7.5 } });
  addBubble(s, -0.5, -0.7, 3, 3, C.bubbleGreen);
  addBubble(s, 4, 5.5, 2.2, 2.2, C.bubbleYellow);
  addBubble(s, 10.5, 0.6, 2, 2, C.bubblePink);

  s.addText([
    { text: "だれと、", options: { breakLine: true } },
    { text: "おしゃべりする？" },
  ], {
    x: 0.8, y: 1.5, w: 5, h: 2,
    fontSize: 38, fontFace: "Noto Sans JP", bold: true, color: C.textPrimary, align: "left", margin: 0,
  });
  s.addImage({ path: img("cotomo-logo.png"), x: 0.8, y: 3.8, h: 0.7 });
  s.addText("おしゃべりAI コトモ", {
    x: 0.8, y: 4.8, w: 5, h: 0.5,
    fontSize: 24, fontFace: "Noto Sans JP", color: C.textSecondary, align: "left", margin: 0,
  });
  s.addImage({ path: img("app-mockup.png"), x: 6.5, y: 0.8, h: 5.5 });
}

// =================================================================
// S5: 機能紹介（2カラム）
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.bgLight });

  // 左カラム
  s.addText([
    { text: "声、アイコン、性格をカスタマイズして", options: { breakLine: true } },
    { text: "AIキャラを作成", options: { bold: true } },
  ], {
    x: 0.5, y: 0.3, w: 5.5, h: 0.8,
    fontSize: 16, fontFace: "Noto Sans JP", bold: true, color: "1B1B1B", align: "center",
  });

  // 右カラム
  s.addText([
    { text: "他のユーザーが作成したキャラと出会う", options: { breakLine: true } },
    { text: "プラットフォーム", options: { bold: true } },
  ], {
    x: 7, y: 0.3, w: 5.5, h: 0.8,
    fontSize: 16, fontFace: "Noto Sans JP", bold: true, color: "1B1B1B", align: "center",
  });

  // グロー装飾
  s.addImage({ path: img("glow-orange.png"), x: 0.3, y: 1.2, w: 2.5 });
  s.addImage({ path: img("glow-blue.png"), x: 3, y: 4.5, w: 2.5 });
  s.addImage({ path: img("glow-pink.png"), x: 8, y: 1, w: 2.2 });
  s.addImage({ path: img("glow-green.png"), x: 7.5, y: 4, w: 2.2 });

  // スクリーンショット
  s.addImage({ path: img("feature-settings.png"), x: 1.3, y: 1.3, h: 5 });
  s.addImage({ path: img("feature-characters.png"), x: 7.5, y: 1.3, h: 5 });

  // 機能タグ（左カラム）
  const tags = [
    ["ハイクオリティな", "声", 0.5, 3.0],
    ["作り込める", "性格", 4.5, 4.5],
    ["自由に設定", "アイコン", 4.5, 2.0],
  ];
  tags.forEach(([sm, lg, tx, ty]) => {
    s.addText(sm, { x: tx, y: ty, w: 1.5, h: 0.3, fontSize: 11, fontFace: "Noto Sans JP", bold: true, color: C.white, margin: 0 });
    s.addText(lg, { x: tx, y: ty + 0.25, w: 1.5, h: 0.4, fontSize: 20, fontFace: "Noto Sans JP", bold: true, color: C.white, margin: 0 });
  });
  s.addText("キャラを", { x: 11, y: 4.5, w: 1.5, h: 0.3, fontSize: 11, fontFace: "Noto Sans JP", bold: true, color: C.white, margin: 0 });
  s.addText("公開", { x: 11, y: 4.75, w: 1.5, h: 0.4, fontSize: 20, fontFace: "Noto Sans JP", bold: true, color: C.white, margin: 0 });
}

// =================================================================
// S6: ユーザー数
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.white });
  s.addText([
    { text: "200", options: { fontSize: 120, bold: true, italic: true, color: C.textPrimary } },
    { text: "万", options: { fontSize: 64, bold: true, color: C.textPrimary } },
  ], {
    x: 1, y: 2.0, w: 11.3, h: 2.5,
    fontFace: "Noto Sans JP", align: "center", valign: "middle",
  });
  s.addText("ユーザー突破！", {
    x: 1, y: 4.5, w: 11.3, h: 0.8,
    fontSize: 38, fontFace: "Noto Sans JP", bold: true, color: C.textPrimary, align: "center",
  });
}

// =================================================================
// S7: 累計おしゃべり時間
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.white });

  // キャラクターイラスト
  s.addImage({ path: img("char-boy.png"), x: 0.4, y: 0.4, h: 2 });
  s.addImage({ path: img("char-girl-purple.png"), x: 1.2, y: 5, h: 1.8 });
  s.addImage({ path: img("char-girl-green.png"), x: 10.5, y: 4.8, h: 1.9 });

  addBubble(s, 3.5, 5, 3, 3, C.bubbleYellow, 0.40);

  s.addText("全ユーザー累計おしゃべり時間", {
    x: 2, y: 1.5, w: 9.3, h: 0.6,
    fontSize: 24, fontFace: "Noto Sans JP", bold: true, color: C.textDark, align: "center",
  });
  s.addText([
    { text: "250", options: { fontSize: 110, bold: true, italic: true, color: C.textDark } },
    { text: "万", options: { fontSize: 64, bold: true, color: C.textDark } },
    { text: "時間", options: { fontSize: 44, bold: true, color: C.textDark } },
  ], {
    x: 2, y: 2.2, w: 9.3, h: 2.5,
    fontFace: "Noto Sans JP", align: "center", valign: "middle",
  });

  // 補足カード
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 2.5, y: 4.8, w: 8.3, h: 1.1,
    fill: { color: C.white }, line: { type: "none" },
    shadow: { type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.06 },
    rectRadius: 0.2,
  });
  s.addText([
    { text: "リリースから", options: { color: C.textDark } },
    { text: "1.5年", options: { color: C.accentPink, bold: true } },
    { text: "で、約", options: { color: C.textDark } },
    { text: "285年分", options: { color: C.accentPink, bold: true } },
    { text: "のおしゃべり時間！", options: { color: C.textDark } },
  ], {
    x: 2.8, y: 5.0, w: 7.8, h: 0.7,
    fontSize: 18, fontFace: "Noto Sans JP", align: "center", valign: "middle",
  });
}

// =================================================================
// S8: CTA
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.white });
  s.addImage({ path: img("blob-red.png"), x: 10, y: -0.5, w: 3.5 });
  s.addImage({ path: img("blob-pink.png"), x: 0.5, y: 5.5, w: 1.5 });

  s.addImage({ path: img("cotomo-logo.png"), x: 5.2, y: 1.2, h: 0.6 });
  s.addText([
    { text: "今すぐ", options: { breakLine: true } },
    { text: "おしゃべり！" },
  ], {
    x: 1, y: 2.2, w: 11.3, h: 1.2,
    fontSize: 36, fontFace: "Noto Sans JP", bold: true, color: C.textDark, align: "center",
  });

  // 区切り線
  s.addShape(pres.shapes.LINE, {
    x: 5.8, y: 3.8, w: 1.6, h: 0,
    line: { color: "BBBBBB", width: 1 },
  });

  s.addText("おしゃべりAI コトモ", {
    x: 1, y: 4.2, w: 11.3, h: 0.5,
    fontSize: 20, fontFace: "Noto Sans JP", color: "545454", align: "center",
  });
  s.addImage({ path: img("qr-code.png"), x: 5.2, y: 5.0, h: 1.3 });
  s.addText("https://cotomo.ai/", {
    x: 7, y: 5.3, w: 3, h: 0.4,
    fontSize: 18, fontFace: "Noto Sans JP", color: C.textSecondary, align: "left", margin: 0,
  });
}

// =================================================================
// S9: 本題タイトル
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.bgLight });
  s.addImage({ path: img("bg-characters.png"), x: 0, y: 0, w: 13.3, h: 7.5, sizing: { type: "cover", w: 13.3, h: 7.5 } });
  s.addText("Cotomo 1分ピッチ", {
    x: 1, y: 2.8, w: 11.3, h: 1.2,
    fontSize: 44, fontFace: "Noto Sans JP", bold: true, color: C.textPrimary, align: "center",
  });
}

// =================================================================
// S10: 3つだけ覚えてください
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.bgLight });
  addBubble(s, 8.5, -0.8, 3.3, 3.3, C.bubbleGreen);
  addBubble(s, -0.4, 5.5, 2.2, 2.2, C.bubbleYellow);
  addBubble(s, 8, 4.5, 2, 2, C.bubblePink);

  s.addText("3つだけ、覚えてください。", {
    x: 1, y: 1.5, w: 11.3, h: 1.2,
    fontSize: 44, fontFace: "Noto Sans JP", bold: true, color: C.textPrimary, align: "center",
  });

  const cards = [
    ["Cotomo", C.brand], ["AIキャラクター市場", C.textPrimary], ["採用", C.textPrimary],
  ];
  let cx = 2.5;
  cards.forEach(([label, color]) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: cx, y: 3.5, w: 2.6, h: 0.8,
      fill: { color: "FAFAFA" }, line: { type: "none" },
      shadow: { type: "outer", blur: 4, offset: 1, color: "000000", opacity: 0.04 },
      rectRadius: 0.15,
    });
    s.addText(label, {
      x: cx, y: 3.5, w: 2.6, h: 0.8,
      fontSize: 22, fontFace: "Noto Sans JP", bold: true, color, align: "center", valign: "middle", margin: 0,
    });
    cx += 2.9;
  });

  s.addNotes("最初に、これだけ覚えていてください。Cotomo。AIキャラクターという新しいエンタメ市場。そして、デザイナとエンジニアを本気で募集しています。これだけ覚えてもらえれば大丈夫です。");
}

// =================================================================
// S11: 聞いたこと、ありますか？
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.bgLight });
  addBubble(s, -0.5, -0.6, 2.8, 2.8, C.bubbleGreen);
  addBubble(s, 10.5, 4, 1.8, 1.8, C.bubblePink);

  s.addImage({ path: img("cotomo-logo.png"), x: 5.2, y: 2.2, h: 0.6 });
  s.addText("聞いたこと、ありますか？", {
    x: 1, y: 3.2, w: 11.3, h: 1.2,
    fontSize: 44, fontFace: "Noto Sans JP", bold: true, color: C.textPrimary, align: "center",
  });

  s.addNotes("ひとつだけ聞かせてください。Cotomoという、AIキャラクターとおしゃべりできるアプリを、聞いたことあるかも？という人、どれくらいいますか？（挙手を促す）ありがとうございます。");
}

// =================================================================
// S12: 新しいエンタメ市場
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.bgLight });
  addBubble(s, 8.5, -0.7, 3, 3, C.bubbleYellow);
  addBubble(s, 0.8, 5.5, 2.2, 2.2, C.bubbleGreen);
  addBubble(s, -0.3, 1, 1.7, 1.7, C.bubblePink);

  s.addText([
    { text: "AIキャラクターという\n新しいエンタメ市場が、\n世界的に、", options: { color: C.textPrimary, breakLine: false } },
    { text: "静かに立ち上がっている。", options: { color: C.brand } },
  ], {
    x: 1, y: 1.5, w: 11.3, h: 4,
    fontSize: 40, fontFace: "Noto Sans JP", bold: true, align: "center",
  });

  s.addNotes("まだ知らない人のほうが多いですよね。でも実は今、AIキャラクターと話し、自分の言葉で物語や体験が変わっていく——そんな新しいエンタメ市場が、世界的に静かに立ち上がっています。");
}

// =================================================================
// S13: 200万+ DL
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.bgLight });
  addBubble(s, -0.8, -1, 3.8, 3.8, C.bubbleGreen);
  addBubble(s, 10, 5.5, 2.2, 2.2, C.bubbleYellow);

  s.addText("200万+ DL", {
    x: 1, y: 1.8, w: 11.3, h: 2,
    fontSize: 110, fontFace: "Noto Sans JP", bold: true, color: C.brand, align: "center", valign: "middle",
  });
  s.addText("日本では、今が一番大事なタイミングだ。", {
    x: 1, y: 4.5, w: 11.3, h: 0.7,
    fontSize: 26, fontFace: "Noto Sans JP", color: C.textSecondary, align: "center",
  });

  s.addNotes("リリース直後に100万、200万ダウンロードに到達するプロダクトも出てきていて、日本では、今が一番大事なタイミングです。");
}

// =================================================================
// S14: 市場の成長と一緒にいるフェーズ
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.bgLight });
  addBubble(s, 9, -0.6, 2.8, 2.8, C.bubblePink);
  addBubble(s, -0.5, 5, 2.5, 2.5, C.bubbleGreen);

  s.addText([
    { text: "市場の成長と", options: { breakLine: true } },
    { text: "一緒にいるフェーズだ。" },
  ], {
    x: 1, y: 1.5, w: 11.3, h: 2.5,
    fontSize: 44, fontFace: "Noto Sans JP", bold: true, color: C.textPrimary, align: "center",
  });
  s.addText("乗るのではない。作る。", {
    x: 1, y: 4.3, w: 11.3, h: 0.8,
    fontSize: 36, fontFace: "Noto Sans JP", bold: true, color: C.brand, align: "center",
  });

  s.addNotes("Cotomoは、日本発でこの市場を作りにいっています。成された市場に乗るのではなく、市場の成長と一緒にいるフェーズです。だから正直に言うと——");
}

// =================================================================
// S15: 助けてください
// =================================================================
{
  const s = pres.addSlide({ bkgd: C.bgLight });
  addBubble(s, -0.6, -0.8, 3.3, 3.3, C.bubbleGreen);
  addBubble(s, 9, 5, 2.6, 2.6, C.bubbleYellow);
  addBubble(s, 8, 0.6, 1.8, 1.8, C.bubblePink);

  s.addText([
    { text: "一緒に作る側として、\nぜひ", options: { color: C.textPrimary } },
    { text: "助けてください。", options: { color: C.brand } },
  ], {
    x: 1, y: 0.8, w: 11.3, h: 2.5,
    fontSize: 44, fontFace: "Noto Sans JP", bold: true, align: "center",
  });

  // CTAバッジ
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 4.2, y: 3.5, w: 5, h: 0.7,
    fill: { color: C.brand }, line: { type: "none" }, rectRadius: 0.35,
  });
  s.addText("Designer & Engineer 募集", {
    x: 4.2, y: 3.5, w: 5, h: 0.7,
    fontSize: 26, fontFace: "Noto Sans JP", bold: true, color: C.white,
    align: "center", valign: "middle", margin: 0,
  });

  // QR + Cotomo
  s.addImage({ path: img("qr-code.png"), x: 4.5, y: 4.8, h: 1.5 });
  s.addImage({ path: img("cotomo-logo.png"), x: 6.5, y: 5.0, h: 0.4 });
  s.addText("https://cotomo.ai/", {
    x: 6.5, y: 5.5, w: 3, h: 0.4,
    fontSize: 18, fontFace: "Noto Sans JP", color: C.textSecondary, align: "left", margin: 0,
  });

  s.addNotes("フルコミットできるデザイナとエンジニアが、本当に必要です。今しかできないこの挑戦を、一緒に作る側として、ぜひ助けてください。");
}

// --- 保存 ---
const output = path.join(__dirname, "cotomo-pitch.pptx");
pres.writeFile({ fileName: output }).then(() => {
  console.log(`PPTX生成完了: ${output}`);
  console.log(`スライド数: 15`);
});
