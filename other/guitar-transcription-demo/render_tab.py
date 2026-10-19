#!/usr/bin/env python3
"""
把 guitar-transcription-demo 生成的 MusicXML 直接渲染成吉他六线谱 SVG/PNG。
不依赖浏览器或 MuseScore，纯 Python + cairosvg。
"""

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_musicxml(path: str):
    tree = ET.parse(path)
    root = tree.getroot()

    measures_data = []
    for measure in root.iter("measure"):
        measure_num = measure.get("number", "?")
        notes_in_measure = []
        current_chord = None

        for note in measure.iter("note"):
            is_chord = note.find("chord") is not None
            is_rest = note.find("rest") is not None
            duration_el = note.find("duration")
            duration = int(duration_el.text) if duration_el is not None else 0

            if is_rest:
                item = {"type": "rest", "duration": duration}
            else:
                string_el = note.find(".//string")
                fret_el = note.find(".//fret")
                string_num = int(string_el.text) if string_el is not None else None
                fret = int(fret_el.text) if fret_el is not None else None
                item = {
                    "type": "note",
                    "duration": duration,
                    "string": string_num,
                    "fret": fret,
                }

            if is_chord:
                if current_chord is not None:
                    current_chord["items"].append(item)
            else:
                if current_chord is not None:
                    notes_in_measure.append(current_chord)
                current_chord = {"type": "chord", "duration": duration, "items": [item]}

        if current_chord is not None:
            notes_in_measure.append(current_chord)

        measures_data.append({
            "number": measure_num,
            "notes": [c for c in notes_in_measure if not (len(c["items"]) == 1 and c["items"][0]["type"] == "rest")],
        })

    return measures_data


def render_svg(measures_data, max_measures=50, measures_per_row=4,
               measure_width=220, string_spacing=12, title="Guitar Tab"):
    measures_data = measures_data[:max_measures]

    margin_x = 20
    margin_y = 30
    row_height = string_spacing * 6 + 50  # 6 strings + top/bottom margin
    total_rows = (len(measures_data) + measures_per_row - 1) // measures_per_row
    width = margin_x * 2 + measures_per_row * measure_width
    height = margin_y * 2 + total_rows * row_height

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{margin_x}" y="22" font-family="sans-serif" font-size="14" fill="#333">{title} — Guitar Tab Preview (first {len(measures_data)} measures)</text>',
    ]

    for idx, m in enumerate(measures_data):
        row = idx // measures_per_row
        col = idx % measures_per_row
        mx = margin_x + col * measure_width
        my = margin_y + 30 + row * row_height

        # 小节号
        svg_parts.append(f'<text x="{mx + 4}" y="{my - 6}" font-family="sans-serif" font-size="10" fill="#666">{m["number"]}</text>')

        # 6 根弦
        for s in range(6):
            sy = my + s * string_spacing
            svg_parts.append(f'<line x1="{mx}" y1="{sy}" x2="{mx + measure_width}" y2="{sy}" stroke="#333" stroke-width="1"/>')

        # 小节竖线
        svg_parts.append(f'<line x1="{mx}" y1="{my}" x2="{mx}" y2="{my + 5 * string_spacing}" stroke="#333" stroke-width="1.5"/>')
        svg_parts.append(f'<line x1="{mx + measure_width}" y1="{my}" x2="{mx + measure_width}" y2="{my + 5 * string_spacing}" stroke="#333" stroke-width="1.5"/>')

        # 音符/和弦
        notes = m["notes"]
        if notes:
            usable_width = measure_width - 20
            step = usable_width / max(len(notes), 1)
            for i, chord in enumerate(notes):
                cx = mx + 12 + i * step
                for item in chord["items"]:
                    if item["type"] == "note":
                        string_num = item["string"]  # 1=high E (top), 6=low E (bottom)
                        sy = my + (string_num - 1) * string_spacing
                        fret = item["fret"]
                        # 白底覆盖弦线
                        svg_parts.append(f'<rect x="{cx - 8}" y="{sy - 7}" width="16" height="14" fill="white"/>')
                        svg_parts.append(f'<text x="{cx}" y="{sy + 4}" font-family="sans-serif" font-size="11" fill="#000" text-anchor="middle">{fret}</text>')

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def main():
    parser = argparse.ArgumentParser(description="MusicXML 吉他六线谱 -> SVG/PNG")
    parser.add_argument("input", help="输入 MusicXML 文件")
    parser.add_argument("--output", "-o", default="tab_preview.svg", help="输出 SVG/PNG 路径")
    parser.add_argument("--max-measures", type=int, default=50, help="最多渲染多少小节")
    parser.add_argument("--measures-per-row", type=int, default=4, help="每行几小节")
    parser.add_argument("--title", default="Guitar Tab", help="标题")
    args = parser.parse_args()

    measures = parse_musicxml(args.input)
    svg = render_svg(
        measures,
        max_measures=args.max_measures,
        measures_per_row=args.measures_per_row,
        title=args.title,
    )

    output_path = Path(args.output)
    if output_path.suffix.lower() == ".png":
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(output_path), scale=2.0)
    else:
        output_path.write_text(svg, encoding="utf-8")

    print(f"已生成：{output_path.resolve()}（{min(args.max_measures, len(measures))}/{len(measures)} 小节）")


if __name__ == "__main__":
    main()
