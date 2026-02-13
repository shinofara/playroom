#!/usr/bin/env python3
"""Cotomo ピッチデッキ PPTX ビルダー (テンプレートベース)

Cotomo_template.pptx をベースに、ピッチデッキの全15スライドを生成する。
テンプレートの固定スライド (S1=product-hero, S2=company-info, S3=feature-2col, S9=cta) はそのまま利用し、
テンプレートスライド (S4-S8) を複製・編集してピッチ内容を挿入する。

使い方:
    python build_from_template.py
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

# ===== パス設定 =====
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = BASE_DIR / ".claude" / "skills" / "pptx" / "scripts"
TEMPLATE_UNPACKED = Path("/tmp/cotomo-template-unpacked")
TEMPLATE_PPTX = BASE_DIR / ".claude" / "skills" / "pptx" / "templates" / "Cotomo_template.pptx"
WORK_DIR = Path("/tmp/cotomo-pitch-work")
OUTPUT_PPTX = Path(__file__).resolve().parent / "cotomo-pitch.pptx"


def copy_template():
    """テンプレートを作業ディレクトリにコピーする"""
    if WORK_DIR.exists():
        shutil.rmtree(WORK_DIR)
    shutil.copytree(TEMPLATE_UNPACKED, WORK_DIR)
    print(f"テンプレートをコピー: {WORK_DIR}")


def duplicate_slide(source_name: str) -> tuple[str, str, int]:
    """スライドを複製し、(新ファイル名, rId, sldId) を返す

    add_slide.py は presentation.xml の sldIdLst を更新しないため、
    複製後に自分で sldId エントリを追加して次回呼び出し時にIDが重複しないようにする。
    """
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "add_slide.py"), str(WORK_DIR), source_name],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"エラー: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"{source_name} の複製に失敗")

    lines = result.stdout.strip().split("\n")
    # "Created slide10.xml from slide4.xml"
    new_name = lines[0].split()[1]
    # 'Add to presentation.xml <p:sldIdLst>: <p:sldId id="265" r:id="rId16"/>'
    id_match = re.search(r'id="(\d+)"', lines[1])
    rid_match = re.search(r'r:id="(rId\d+)"', lines[1])
    slide_id = int(id_match.group(1))
    rid = rid_match.group(1)

    # presentation.xml の sldIdLst にエントリを追加（次回のID計算に必要）
    _add_sld_id_entry(slide_id, rid)

    print(f"  複製: {source_name} → {new_name} (id={slide_id}, {rid})")
    return new_name, rid, slide_id


def _add_sld_id_entry(slide_id: int, rid: str):
    """presentation.xml の sldIdLst に sldId エントリを追加する"""
    pres_path = WORK_DIR / "ppt" / "presentation.xml"
    content = pres_path.read_text(encoding="utf-8")
    new_entry = f'    <p:sldId id="{slide_id}" r:id="{rid}"/>'
    content = content.replace(
        "</p:sldIdLst>",
        f"{new_entry}\n  </p:sldIdLst>",
    )
    pres_path.write_text(content, encoding="utf-8")


def edit_presentation_xml(slide_order: list[tuple[int, str]]):
    """presentation.xml のスライド順序を書き換える"""
    pres_path = WORK_DIR / "ppt" / "presentation.xml"
    content = pres_path.read_text(encoding="utf-8")

    sld_entries = "\n".join(
        f'    <p:sldId id="{sid}" r:id="{rid}"/>'
        for sid, rid in slide_order
    )
    new_sld_list = f"  <p:sldIdLst>\n{sld_entries}\n  </p:sldIdLst>"

    content = re.sub(
        r"<p:sldIdLst>.*?</p:sldIdLst>",
        new_sld_list,
        content,
        flags=re.DOTALL,
    )
    pres_path.write_text(content, encoding="utf-8")
    print(f"presentation.xml 更新: {len(slide_order)} スライド")


def replace_text_in_slide(slide_name: str, replacements: list[tuple[str, str]]):
    """スライドXML内のテキストを置換する"""
    slide_path = WORK_DIR / "ppt" / "slides" / slide_name
    content = slide_path.read_text(encoding="utf-8")
    for old, new in replacements:
        content = content.replace(old, new)
    slide_path.write_text(content, encoding="utf-8")


def remove_image_placeholder(slide_name: str):
    """S4テンプレートの画像プレースホルダー（グレー矩形 + "image" ラベル）を削除する"""
    slide_path = WORK_DIR / "ppt" / "slides" / slide_name
    content = slide_path.read_text(encoding="utf-8")

    # Shape 7 (gray rect, id=9): グレー画像プレースホルダー背景
    content = re.sub(
        r'<p:sp>\s*<p:nvSpPr>\s*<p:cNvPr id="9" name="Shape 7"/>.*?</p:sp>',
        "",
        content,
        flags=re.DOTALL,
    )
    # Text 8 (id=10): "image" テキストラベル
    content = re.sub(
        r'<p:sp>\s*<p:nvSpPr>\s*<p:cNvPr id="10" name="Text 8"/>.*?</p:sp>',
        "",
        content,
        flags=re.DOTALL,
    )
    slide_path.write_text(content, encoding="utf-8")


def edit_s6_texts(slide_name: str, title: str, rows: list[tuple[str, str, str]]):
    """S6 (bg-accent-list) テンプレートのテキストを編集する

    rows は [(前テキスト, 強調テキスト, 後テキスト)] × 3
    """
    slide_path = WORK_DIR / "ppt" / "slides" / slide_name
    content = slide_path.read_text(encoding="utf-8")

    # タイトル
    content = content.replace(
        "<a:t>スライドタイトル</a:t>",
        f"<a:t>{title}</a:t>",
        1,
    )

    # テキスト行を検索・置換 (各行は "テキストテキスト" + "強調テキスト" + "テキスト" の3つ組)
    # 最初のセット (Text 3 / id=6)
    old_texts = [
        ("テキストテキスト", "強調テキスト", "テキスト"),
        ("テキストテキスト", "強調テキスト", "テキスト"),
        ("テキストテキスト", "強調テキスト", "テキスト"),
    ]

    for i, ((old_pre, old_acc, old_post), (new_pre, new_acc, new_post)) in enumerate(
        zip(old_texts, rows)
    ):
        # 各行のテキストを順番に置換（1回ずつ）
        content = content.replace(f"<a:t>{old_pre}</a:t>", f"<a:t>{new_pre}</a:t>", 1)
        content = content.replace(f"<a:t>{old_acc}</a:t>", f"<a:t>{new_acc}</a:t>", 1)
        content = content.replace(f"<a:t>{old_post}</a:t>", f"<a:t>{new_post}</a:t>", 1)

    slide_path.write_text(content, encoding="utf-8")


def edit_s7_texts(
    slide_name: str,
    title: str,
    heading1: str,
    body1: list[str],
    heading2: str,
    body2: list[str],
):
    """S7 (bg-heading-body) テンプレートのテキストを編集する"""
    slide_path = WORK_DIR / "ppt" / "slides" / slide_name
    content = slide_path.read_text(encoding="utf-8")

    content = content.replace(
        "<a:t>スライドタイトル</a:t>", f"<a:t>{title}</a:t>", 1
    )
    content = content.replace("<a:t>見出し1</a:t>", f"<a:t>{heading1}</a:t>", 1)
    content = content.replace("<a:t>見出し2</a:t>", f"<a:t>{heading2}</a:t>", 1)

    # 本文テキスト（各セクション2行ずつ）
    old_body = "本文テキスト本文テキスト本文テキスト本文テキスト"
    for i, text in enumerate(body1):
        content = content.replace(f"<a:t>{old_body}</a:t>", f"<a:t>{text}</a:t>", 1)
    for i, text in enumerate(body2):
        content = content.replace(f"<a:t>{old_body}</a:t>", f"<a:t>{text}</a:t>", 1)

    # 残りの本文プレースホルダーをクリア
    content = content.replace(f"<a:t>{old_body}</a:t>", "<a:t></a:t>")

    slide_path.write_text(content, encoding="utf-8")


def edit_s8_texts(
    slide_name: str,
    title: str,
    cards: list[tuple[str, str]],
):
    """S8 (bg-card-grid) テンプレートのテキストを編集する

    cards は [(コンテンツ, 強調テキスト)] × 4
    """
    slide_path = WORK_DIR / "ppt" / "slides" / slide_name
    content = slide_path.read_text(encoding="utf-8")

    content = content.replace(
        "<a:t>スライドタイトル</a:t>", f"<a:t>{title}</a:t>", 1
    )

    for i, (card_text, accent_text) in enumerate(cards, 1):
        content = content.replace(
            f"<a:t>コンテンツ{i}</a:t>", f"<a:t>{card_text}</a:t>", 1
        )
    # 強調テキストの置換（各カードに1つずつ）
    for _, accent_text in cards:
        content = content.replace(
            "<a:t>強調テキスト</a:t>", f"<a:t>{accent_text}</a:t>", 1
        )

    slide_path.write_text(content, encoding="utf-8")


def run_clean():
    """clean.py を実行する"""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "clean.py"), str(WORK_DIR)],
        capture_output=True, text=True,
    )
    print(f"クリーンアップ: {result.stdout.strip()}")
    if result.returncode != 0:
        print(f"  警告: {result.stderr}", file=sys.stderr)


def run_pack():
    """pack.py を実行して PPTX を生成する"""
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "office" / "pack.py"),
            str(WORK_DIR),
            str(OUTPUT_PPTX),
            "--original",
            str(TEMPLATE_PPTX),
        ],
        capture_output=True, text=True,
    )
    print(f"パック: {result.stdout.strip()}")
    if result.returncode != 0:
        print(f"  エラー: {result.stderr}", file=sys.stderr)
        raise RuntimeError("PPTX パッキングに失敗")


def main():
    print("=" * 60)
    print("Cotomo ピッチデッキ PPTX ビルド")
    print("=" * 60)

    # Step 1: テンプレートをコピー
    copy_template()

    # Step 2: スライド複製
    print("\nスライド複製:")

    # S4 (title-image-1) × 3
    title_slide, title_rid, title_id = duplicate_slide("slide4.xml")
    pitch_title_slide, pitch_title_rid, pitch_title_id = duplicate_slide("slide4.xml")
    kikitakoto_slide, kikitakoto_rid, kikitakoto_id = duplicate_slide("slide4.xml")

    # S6 (bg-accent-list) × 4
    users_slide, users_rid, users_id = duplicate_slide("slide6.xml")
    chattime_slide, chattime_rid, chattime_id = duplicate_slide("slide6.xml")
    aichar_slide, aichar_rid, aichar_id = duplicate_slide("slide6.xml")
    dl_slide, dl_rid, dl_id = duplicate_slide("slide6.xml")

    # S7 (bg-heading-body) × 2
    profile_slide, profile_rid, profile_id = duplicate_slide("slide7.xml")
    shijou_slide, shijou_rid, shijou_id = duplicate_slide("slide7.xml")

    # S8 (bg-card-grid) × 1
    mitsu_slide, mitsu_rid, mitsu_id = duplicate_slide("slide8.xml")

    # S9 (cta) × 1
    help_cta_slide, help_cta_rid, help_cta_id = duplicate_slide("slide9.xml")

    # Step 3: スライド順序を設定
    # オリジナルスライドの rId マッピング:
    #   slide1 (product-hero):  id=256, rId2
    #   slide2 (company-info):  id=257, rId3
    #   slide3 (feature-2col):  id=258, rId4
    #   slide9 (cta):           id=264, rId10
    print("\nスライド順序設定:")
    slide_order = [
        (title_id, title_rid),          # 1. タイトル
        (profile_id, profile_rid),      # 2. 自己紹介
        (257, "rId3"),                  # 3. 会社情報 (固定)
        (256, "rId2"),                  # 4. プロダクト紹介 (固定)
        (258, "rId4"),                  # 5. 機能紹介 (固定)
        (users_id, users_rid),          # 6. ユーザー数
        (chattime_id, chattime_rid),    # 7. おしゃべり時間
        (264, "rId10"),                 # 8. CTA (固定)
        (pitch_title_id, pitch_title_rid),  # 9. ピッチ本題タイトル
        (mitsu_id, mitsu_rid),          # 10. 3つだけ覚えて
        (kikitakoto_id, kikitakoto_rid),  # 11. 聞いたことありますか
        (aichar_id, aichar_rid),        # 12. AIキャラクター市場
        (dl_id, dl_rid),                # 13. 200万+ DL
        (shijou_id, shijou_rid),        # 14. 市場の成長
        (help_cta_id, help_cta_rid),    # 15. 助けてください CTA
    ]
    edit_presentation_xml(slide_order)

    # Step 4: 各スライドのコンテンツ編集
    print("\nコンテンツ編集:")

    # --- Slide 1: タイトル (S4 ベース) ---
    print("  Slide 1: タイトル")
    replace_text_in_slide(title_slide, [
        ("スライドタイトル", "Cotomo 1分ピッチ"),
        ("サブテキストサブテキストサブテキストサブテキスト",
         "Starley株式会社 ｜ VPoE 篠原 祐貴"),
    ])
    remove_image_placeholder(title_slide)

    # --- Slide 2: 自己紹介 (S7 ベース) ---
    print("  Slide 2: 自己紹介")
    edit_s7_texts(
        profile_slide,
        title="自己紹介",
        heading1="篠原 祐貴 ─ Starley株式会社 VPoE",
        body1=[
            "ヤフーを経て、Schoo初代CTO、メドピア技術部長、MFケッサイ取締役CTOを歴任",
            "AIと人が共創する「AIネイティブ」なプロダクト組織の実現をリード",
        ],
        heading2="キャリア",
        body2=[
            "Yahoo! → Schoo CTO → メドピア → MFケッサイ CTO",
            "→ Spir CRO/CTO → Legalscape VPoE → Starley VPoE",
        ],
    )

    # --- Slide 3-5: 固定スライド（編集不要） ---
    print("  Slide 3-5: 固定スライド（会社情報・プロダクト・機能紹介）")

    # --- Slide 6: ユーザー数 (S6 ベース) ---
    print("  Slide 6: ユーザー数")
    edit_s6_texts(
        users_slide,
        title="ユーザー数",
        rows=[
            ("累計", "200万", "ダウンロード"),
            ("", "ユーザー突破！", ""),
            ("おしゃべりAI", "Cotomo", "が急成長中"),
        ],
    )

    # --- Slide 7: おしゃべり時間 (S6 ベース) ---
    print("  Slide 7: おしゃべり時間")
    edit_s6_texts(
        chattime_slide,
        title="全ユーザー累計おしゃべり時間",
        rows=[
            ("", "250万時間", ""),
            ("リリースから", "1.5年", "で"),
            ("約", "285年分", "のおしゃべり！"),
        ],
    )

    # --- Slide 8: CTA 固定 ---
    print("  Slide 8: CTA（固定）")

    # --- Slide 9: ピッチ本題タイトル (S4 ベース) ---
    print("  Slide 9: ピッチ本題タイトル")
    replace_text_in_slide(pitch_title_slide, [
        ("スライドタイトル", "Cotomo 1分ピッチ"),
        ("サブテキストサブテキストサブテキストサブテキスト", ""),
    ])
    remove_image_placeholder(pitch_title_slide)

    # --- Slide 10: 3つだけ覚えて (S8 ベース) ---
    print("  Slide 10: 3つだけ覚えて")
    edit_s8_texts(
        mitsu_slide,
        title="3つだけ、覚えてください。",
        cards=[
            ("Cotomo", "おしゃべりAI"),
            ("AIキャラクター市場", "新しいエンタメ"),
            ("採用", "Designer &amp; Engineer"),
            ("", ""),
        ],
    )

    # --- Slide 11: 聞いたことありますか (S4 ベース) ---
    print("  Slide 11: 聞いたことありますか")
    replace_text_in_slide(kikitakoto_slide, [
        ("スライドタイトル", "聞いたこと、ありますか？"),
        ("サブテキストサブテキストサブテキストサブテキスト",
         "AIキャラクターとおしゃべりできるアプリ Cotomo"),
    ])
    remove_image_placeholder(kikitakoto_slide)

    # --- Slide 12: AIキャラクター市場 (S6 ベース) ---
    print("  Slide 12: AIキャラクター市場")
    edit_s6_texts(
        aichar_slide,
        title="",
        rows=[
            ("AIキャラクターという", "", ""),
            ("", "新しいエンタメ市場", "が、"),
            ("世界的に、", "静かに立ち上がっている。", ""),
        ],
    )

    # --- Slide 13: 200万+ DL (S6 ベース) ---
    print("  Slide 13: 200万+ DL")
    edit_s6_texts(
        dl_slide,
        title="",
        rows=[
            ("リリース直後に", "", ""),
            ("", "200万+ DL", ""),
            ("日本では、", "今が一番大事なタイミング", "だ。"),
        ],
    )

    # --- Slide 14: 市場の成長 (S7 ベース) ---
    print("  Slide 14: 市場の成長")
    edit_s7_texts(
        shijou_slide,
        title="",
        heading1="市場の成長と一緒にいるフェーズだ。",
        body1=["成された市場に乗るのではなく、市場を作りにいっている"],
        heading2="乗るのではない。作る。",
        body2=["Cotomoは、日本発でこの市場を作りにいっています"],
    )

    # --- Slide 15: 助けてください CTA (S9 ベース) ---
    print("  Slide 15: 助けてください CTA")
    replace_text_in_slide(help_cta_slide, [
        ("<a:t>今すぐ</a:t>", "<a:t>一緒に作る側として、</a:t>"),
        ("<a:t>おしゃべり！</a:t>", "<a:t>助けてください。</a:t>"),
    ])

    # Step 5: クリーンアップ
    print("\nクリーンアップ:")
    run_clean()

    # Step 6: パッキング
    print("\nPPTX生成:")
    run_pack()

    print(f"\n✓ 生成完了: {OUTPUT_PPTX}")


if __name__ == "__main__":
    main()
