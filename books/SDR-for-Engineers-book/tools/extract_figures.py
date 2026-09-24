#!/usr/bin/env python3
"""
extract_figures.py —— 从原书章节 PDF 中提取插图（v2）

原书排版特点（实测）：
- 插图全部是矢量图（无栅格），且常整图旋转 90° 横躺；
- 题注有时在图下方（正常横排），有时竖排在图右侧（旋转 90°，bbox 细长）。

策略：
1. cluster_drawings() 聚类，"锚图形"= 宽高任一向够大且另一向不太小；
2. 题注与锚图形匹配：图在题注上方（横排题注）或图在题注左侧（竖排题注）；
3. 从锚图形向外生长，吞掉间距 <=25pt 的碎片聚类；
4. 3x 渲染 PNG，命名 fig_<章2位><序2位>.png；
5. captions_<章>.tsv 记录 文件名/页码/英文题注 供翻译对照。

用法：
    python3 tools/extract_figures.py pdf/SDR4Engineers_CH01.pdf 1 images/
"""

import sys
import re
import fitz  # PyMuPDF
from pathlib import Path

CAPTION_RE = re.compile(r'^Figure\s+(\d+)\.(\d+)')
SEEK_UP = 420.0     # 横排题注：向上找图的最大距离
SEEK_LEFT = 40.0    # 竖排题注：向左找图的最大距离
GROW_GAP = 25.0     # 碎片吞并距离


def is_anchor(r):
    return (r.width >= 90 and r.height >= 50) or (r.width >= 40 and r.height >= 90)


def overlap_1d(a0, a1, b0, b1):
    return max(0, min(a1, b1) - max(a0, b0))


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    pdf_path, ch_num, out_dir = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    captions, fig_no = [], 0

    for pno in range(len(doc)):
        page = doc[pno]
        clusters = [fitz.Rect(c) for c in page.cluster_drawings()]
        clusters += [fitz.Rect(i["bbox"]) for i in page.get_image_info()
                     if fitz.Rect(i["bbox"]).width > 20 and fitz.Rect(i["bbox"]).height > 20]
        used = [False] * len(clusters)

        text_blocks = page.get_text("blocks")
        # 页眉文本块（页面最顶部），兜底裁剪时避开页眉装饰线
        header_bottom = 0.0
        for b in text_blocks:
            if b[1] < 75:
                header_bottom = max(header_bottom, b[3])

        for b in text_blocks:
            text = (b[4] or "").strip()
            if not CAPTION_RE.match(text):
                continue
            cap = fitz.Rect(b[:4])
            vertical_cap = cap.height > cap.width * 1.5  # 竖排题注

            # 候选锚图形
            best, best_d = None, 1e9
            for gi, g in enumerate(clusters):
                if used[gi] or not is_anchor(g):
                    continue
                if vertical_cap:
                    # 图在题注左侧
                    if g.x1 <= cap.x0 + 6 and cap.x0 - g.x1 <= SEEK_LEFT \
                       and overlap_1d(g.y0, g.y1, cap.y0, cap.y1) >= 30:
                        d = cap.x0 - g.x1
                    else:
                        continue
                else:
                    # 图在题注上方（或左上，跨栏图）
                    if g.y1 <= cap.y0 + 8 and cap.y0 - g.y1 <= SEEK_UP \
                       and g.x0 < cap.x1 + 20 and g.x1 > cap.x0 - 20:
                        d = cap.y0 - g.y1
                    else:
                        continue
                if d < best_d:
                    best, best_d = gi, d

            fig_no += 1
            name = f"fig_{ch_num:02d}{fig_no:02d}.png"
            if best is None:
                # 兜底：表格式插图（无大锚块）——题注上方、水平重叠的全部碎片外接矩形
                frags = [g for g in clusters
                         if g.y1 <= cap.y0 + 8 and cap.y0 - g.y1 <= SEEK_UP
                         and g.x0 < cap.x1 + 20 and g.x1 > cap.x0 - 20]
                if not frags:
                    print(f"  [p{pno+1}] ✗ 未匹配图形: {' '.join(text.split())[:60]}")
                    captions.append((None, pno + 1, text))
                    continue
                rect = fitz.Rect(frags[0])
                for g in frags[1:]:
                    rect |= g
                top = max(header_bottom + 2, rect.y0 - 4)
                rect = fitz.Rect(rect.x0 - 4, top, rect.x1 + 4, cap.y0 - 3)
                pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=rect, alpha=False)
                pix.save(out / name)
                captions.append((name, pno + 1, text))
                print(f"  [p{pno+1}] {name}  {rect.width:.0f}x{rect.height:.0f}pt  碎片兜底  {' '.join(text.split())[:40]}")
                continue

            # 从锚图形向外生长吞碎片
            rect = fitz.Rect(clusters[best])
            used[best] = True
            grown = True
            while grown:
                grown = False
                for gi, g in enumerate(clusters):
                    if used[gi]:
                        continue
                    inflated = fitz.Rect(rect) + (-GROW_GAP, -GROW_GAP, GROW_GAP, GROW_GAP)
                    if inflated.intersects(g):
                        rect |= g
                        used[gi] = True
                        grown = True

            # 题注下方留白裁掉（横排）；竖排题注在右侧，自然不含在内
            rect = fitz.Rect(max(0, rect.x0 - 4), max(0, rect.y0 - 4),
                             min(page.rect.x1, rect.x1 + 4), min(page.rect.y1, rect.y1 + 4))
            if not vertical_cap and cap.y0 > rect.y1:
                pass  # 已在上方，无需处理
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=rect, alpha=False)
            pix.save(out / name)
            captions.append((name, pno + 1, text))
            print(f"  [p{pno+1}] {name}  {rect.width:.0f}x{rect.height:.0f}pt"
                  f"  {'竖排' if vertical_cap else '横排'}  {' '.join(text.split())[:44]}")

    tsv = out / f"captions_{ch_num:02d}.tsv"
    with open(tsv, "w", encoding="utf-8") as f:
        for name, pno, text in captions:
            f.write(f"{name or '-'}\t{pno}\t{' '.join(text.split())}\n")
    print(f"\n✓ {len(captions)} 个题注，提取 {sum(1 for c in captions if c[0])} 张图 → {out}")


if __name__ == "__main__":
    main()
