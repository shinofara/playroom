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


def build_title_slide(slide_name: str):
    """S1 (product-hero) の複製をカスタムタイトルスライドに書き換える

    背景画像 (bg-characters) と装飾バブルを保持しつつ、
    フォンモックアップを除去し、中央にタイトル・ロゴ・スピーカー情報を配置する。
    slide1.xml の rels: rId1=bg-characters, rId9=Cotomo logo icon
    """
    slide_path = WORK_DIR / "ppt" / "slides" / slide_name
    # スライドサイズ: 9144000 × 5143500 EMU
    xml = '''<?xml version="1.0" encoding="utf-8"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld name="Title">
    <p:bg>
      <p:bgPr>
        <a:solidFill>
          <a:srgbClr val="FFFFFF"/>
        </a:solidFill>
      </p:bgPr>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="2" name="Shape 0"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="-72161" y="0"/>
            <a:ext cx="9286875" cy="5214938"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="EFF6F2"/></a:solidFill>
          <a:ln/>
        </p:spPr>
      </p:sp>
      <p:pic>
        <p:nvPicPr>
          <p:cNvPr id="3" name="Image 0" descr="bg-characters"/>
          <p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>
          <p:nvPr/>
        </p:nvPicPr>
        <p:blipFill>
          <a:blip r:embed="rId1"/>
          <a:srcRect l="0" r="8" t="0" b="16279"/>
          <a:stretch/>
        </p:blipFill>
        <p:spPr>
          <a:xfrm>
            <a:off x="-72885" y="-376131"/>
            <a:ext cx="9277499" cy="5214938"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        </p:spPr>
      </p:pic>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="4" name="Bubble Yellow"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm rot="2321545">
            <a:off x="-663091" y="3942119"/>
            <a:ext cx="2392446" cy="2268699"/>
          </a:xfrm>
          <a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="D1C45C"><a:alpha val="40000"/></a:srgbClr></a:solidFill>
          <a:ln/>
        </p:spPr>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="5" name="Bubble Green"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm rot="2321545">
            <a:off x="-927779" y="261282"/>
            <a:ext cx="2326682" cy="2206336"/>
          </a:xfrm>
          <a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="6CC7A5"><a:alpha val="40000"/></a:srgbClr></a:solidFill>
          <a:ln/>
        </p:spPr>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="6" name="Bubble Pink"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm rot="2321545">
            <a:off x="7100721" y="-675699"/>
            <a:ext cx="3086356" cy="2926717"/>
          </a:xfrm>
          <a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="DA76D7"><a:alpha val="40000"/></a:srgbClr></a:solidFill>
          <a:ln/>
        </p:spPr>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="7" name="Center Card"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="1572000" y="800000"/>
            <a:ext cx="6000000" cy="3500000"/>
          </a:xfrm>
          <a:prstGeom prst="roundRect">
            <a:avLst><a:gd name="adj" fmla="val 6000"/></a:avLst>
          </a:prstGeom>
          <a:solidFill><a:srgbClr val="FFFFFF"><a:alpha val="75000"/></a:srgbClr></a:solidFill>
          <a:ln/>
        </p:spPr>
      </p:sp>
      <p:pic>
        <p:nvPicPr>
          <p:cNvPr id="8" name="Cotomo Logo"/>
          <p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>
          <p:nvPr/>
        </p:nvPicPr>
        <p:blipFill>
          <a:blip r:embed="rId9"/>
          <a:srcRect l="0" r="0" t="0" b="0"/>
          <a:stretch/>
        </p:blipFill>
        <p:spPr>
          <a:xfrm>
            <a:off x="4082000" y="950000"/>
            <a:ext cx="980000" cy="980000"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        </p:spPr>
      </p:pic>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="9" name="Brand Text"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="2572000" y="1980000"/>
            <a:ext cx="4000000" cy="320000"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:noFill/>
          <a:ln/>
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/>
          <a:lstStyle/>
          <a:p>
            <a:pPr algn="ctr" indent="0" marL="0">
              <a:lnSpc><a:spcPts val="2200"/></a:lnSpc>
              <a:buNone/>
            </a:pPr>
            <a:r>
              <a:rPr lang="en-US" sz="1200" spc="400" kern="0" dirty="0">
                <a:solidFill><a:srgbClr val="6b6b6b"><a:alpha val="99000"/></a:srgbClr></a:solidFill>
                <a:latin typeface="Noto Sans JP" pitchFamily="34" charset="0"/>
                <a:ea typeface="Noto Sans JP" pitchFamily="34" charset="-122"/>
                <a:cs typeface="Noto Sans JP" pitchFamily="34" charset="-120"/>
              </a:rPr>
              <a:t>おしゃべりAI コトモ</a:t>
            </a:r>
            <a:endParaRPr lang="en-US" sz="1200" dirty="0"/>
          </a:p>
        </p:txBody>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="10" name="Line Left"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="2800000" y="2120000"/>
            <a:ext cx="1200000" cy="0"/>
          </a:xfrm>
          <a:prstGeom prst="line"><a:avLst/></a:prstGeom>
          <a:noFill/>
          <a:ln w="6350"><a:solidFill><a:srgbClr val="BBBBBB"/></a:solidFill></a:ln>
        </p:spPr>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="11" name="Line Right"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="5144000" y="2120000"/>
            <a:ext cx="1200000" cy="0"/>
          </a:xfrm>
          <a:prstGeom prst="line"><a:avLst/></a:prstGeom>
          <a:noFill/>
          <a:ln w="6350"><a:solidFill><a:srgbClr val="BBBBBB"/></a:solidFill></a:ln>
        </p:spPr>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="12" name="Title"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="1572000" y="2300000"/>
            <a:ext cx="6000000" cy="800000"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:noFill/>
          <a:ln/>
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/>
          <a:lstStyle/>
          <a:p>
            <a:pPr algn="ctr" indent="0" marL="0">
              <a:lnSpc><a:spcPts val="4000"/></a:lnSpc>
              <a:buNone/>
            </a:pPr>
            <a:r>
              <a:rPr lang="en-US" sz="2800" b="1" spc="300" kern="0" dirty="0">
                <a:solidFill><a:srgbClr val="484848"><a:alpha val="99000"/></a:srgbClr></a:solidFill>
                <a:latin typeface="Noto Sans JP" pitchFamily="34" charset="0"/>
                <a:ea typeface="Noto Sans JP" pitchFamily="34" charset="-122"/>
                <a:cs typeface="Noto Sans JP" pitchFamily="34" charset="-120"/>
              </a:rPr>
              <a:t>Cotomo 1&#x5206;&#x30D4;&#x30C3;&#x30C1;</a:t>
            </a:r>
            <a:endParaRPr lang="en-US" sz="2800" dirty="0"/>
          </a:p>
        </p:txBody>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="13" name="Speaker"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="1572000" y="3200000"/>
            <a:ext cx="6000000" cy="400000"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:noFill/>
          <a:ln/>
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/>
          <a:lstStyle/>
          <a:p>
            <a:pPr algn="ctr" indent="0" marL="0">
              <a:lnSpc><a:spcPts val="2400"/></a:lnSpc>
              <a:buNone/>
            </a:pPr>
            <a:r>
              <a:rPr lang="en-US" sz="1400" spc="200" kern="0" dirty="0">
                <a:solidFill><a:srgbClr val="6b6b6b"><a:alpha val="99000"/></a:srgbClr></a:solidFill>
                <a:latin typeface="Noto Sans JP" pitchFamily="34" charset="0"/>
                <a:ea typeface="Noto Sans JP" pitchFamily="34" charset="-122"/>
                <a:cs typeface="Noto Sans JP" pitchFamily="34" charset="-120"/>
              </a:rPr>
              <a:t>Starley&#x682A;&#x5F0F;&#x4F1A;&#x793E; &#xFF5C; VPoE &#x7BC0;&#x539F; &#x7950;&#x8CB4;</a:t>
            </a:r>
            <a:endParaRPr lang="en-US" sz="1400" dirty="0"/>
          </a:p>
        </p:txBody>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="14" name="Starley Logo"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="300000" y="4700000"/>
            <a:ext cx="2000000" cy="300000"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:noFill/>
          <a:ln/>
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/>
          <a:lstStyle/>
          <a:p>
            <a:pPr algn="l" indent="0" marL="0">
              <a:lnSpc><a:spcPts val="1600"/></a:lnSpc>
              <a:buNone/>
            </a:pPr>
            <a:r>
              <a:rPr lang="en-US" sz="900" spc="200" kern="0" dirty="0">
                <a:solidFill><a:srgbClr val="999999"><a:alpha val="70000"/></a:srgbClr></a:solidFill>
                <a:latin typeface="Noto Sans JP" pitchFamily="34" charset="0"/>
                <a:ea typeface="Noto Sans JP" pitchFamily="34" charset="-122"/>
                <a:cs typeface="Noto Sans JP" pitchFamily="34" charset="-120"/>
              </a:rPr>
              <a:t>Starley&#x682A;&#x5F0F;&#x4F1A;&#x793E;</a:t>
            </a:r>
            <a:endParaRPr lang="en-US" sz="900" dirty="0"/>
          </a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr>
    <a:masterClrMapping/>
  </p:clrMapOvr>
</p:sld>'''
    slide_path.write_text(xml, encoding="utf-8")


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

    # S1 (product-hero) × 1 → タイトルスライド
    title_slide, title_rid, title_id = duplicate_slide("slide1.xml")

    # S4 (title-image-1) × 2
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

    # --- Slide 1: タイトル (S1 ベースのカスタムレイアウト) ---
    print("  Slide 1: タイトル")
    build_title_slide(title_slide)

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
