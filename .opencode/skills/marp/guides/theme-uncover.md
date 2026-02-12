# Uncover テーマ ガイドライン

Marp組み込みテーマ `uncover` の使い方と設計指針。

## 特徴

- モダンでミニマルなデザイン
- 白基調のクリーンな配色
- ビジネス・社内資料向き
- 読みやすさ重視

## フロントマター

```yaml
---
marp: true
theme: uncover
paginate: true
size: 16:9
---
```

## 利用可能クラス

### `lead`

タイトルスライドやセクション区切り用。中央寄せレイアウト。

```html
<!-- _class: lead -->

# セクションタイトル
```

### `invert`

配色を反転（ダーク背景 + ライトテキスト）。

```html
<!-- _class: invert -->

# ダーク背景のスライド
```

### 組み合わせ

```html
<!-- _class: lead invert -->
```

## 配色のカスタマイズ

Uncoverの基本カラーを上書きする場合：

```html
<style>
:root {
  --color-background: #fafafa;
  --color-foreground: #2d3436;
  --color-highlight: #0984e3;
  --color-dimmed: #b2bec3;
}
</style>
```

## 推奨スタイル

- **余白を活かす**: 情報を詰め込みすぎない。1スライド1メッセージ
- **図表**: シンプルな表やチャートとの相性が良い
- **画像**: 明るい画像が映える。`bg left` / `bg right` で片側配置が効果的
- **フォント**: デフォルトのサンセリフ体がそのまま適合する
- **色**: アクセントカラーは1色に絞る

## 画像レイアウト例

### 左に画像、右にテキスト

```markdown
![bg left:40%](./images/photo.png)

# テキスト内容

- ポイント1
- ポイント2
```

### 右に画像、左にテキスト

```markdown
![bg right:45%](./images/chart.png)

# データの説明

結果をここに記載
```

## 使用例

```markdown
---
marp: true
theme: uncover
paginate: true
---

<!-- _class: lead -->

# 四半期レビュー

事業部名 / 2026 Q1

---

# 売上推移

![bg right:50%](./images/chart.png)

- Q1: 前年比120%
- 新規顧客: 15社
- 継続率: 95%

---

<!-- _class: lead invert -->

# Next Quarter
```
