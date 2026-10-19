#!/usr/bin/env python3
"""
把 guitar-transcription-demo 生成的 MusicXML 转成 VexFlow 六线谱 HTML。
只渲染前 N 小节，避免页面过长。
"""

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


DIVISIONS_PER_QUARTER = 480


def divisions_to_vexflow_duration(divs: int):
    """把 MusicXML divisions 转成 VexFlow  duration 字符串。"""
    if divs <= 0:
        return "16"
    # 支持附点：尝试无附点 -> 单附点 -> 双附点
    for dot_count in range(3):
        multiplier = (2 ** (dot_count + 1) - 1) / (2 ** dot_count)
        base = divs / multiplier
        if abs(base - 1920) < 1:
            return "w" + "d" * dot_count
        if abs(base - 960) < 1:
            return "h" + "d" * dot_count
        if abs(base - 480) < 1:
            return "q" + "d" * dot_count
        if abs(base - 240) < 1:
            return "8" + "d" * dot_count
        if abs(base - 120) < 1:
            return "16" + "d" * dot_count
        if abs(base - 60) < 1:
            return "32" + "d" * dot_count
    #  fallback：按最接近的
    if divs >= 960:
        return "h"
    if divs >= 480:
        return "q"
    if divs >= 240:
        return "8"
    return "16"


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
            "notes": notes_in_measure,
        })

    return measures_data


def build_html(measures_data, max_measures=50, title="Guitar Tab"):
    # 只取前 max_measures 小节
    measures_data = measures_data[:max_measures]

    js_measures = []
    for m in measures_data:
        notes_js = []
        for chord in m["notes"]:
            dur = divisions_to_vexflow_duration(chord["duration"])
            items = chord["items"]
            if len(items) == 1 and items[0]["type"] == "rest":
                notes_js.append(f"new VF.GhostNote({{duration: '{dur}'}})")
            else:
                positions = []
                for item in items:
                    if item["type"] == "note":
                        positions.append(f"{{str: {item['string']}, fret: {item['fret']}}}")
                if positions:
                    notes_js.append(f"new VF.TabNote({{positions: [{', '.join(positions)}], duration: '{dur}'}})")
        if notes_js:
            js_measures.append({"number": m["number"], "notes": notes_js})

    measures_json = "[\n"
    for m in js_measures:
        measures_json += f"  {{number: '{m['number']}', notes: [{', '.join(m['notes'])}]}},\n"
    measures_json += "]"

    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>
<script src="https://unpkg.com/vexflow@3.0.9/releases/vexflow-debug.js"></script>
<style>
  body {{ margin: 0; padding: 20px; font-family: sans-serif; background: #f8f8f8; }}
  h1 {{ font-size: 18px; margin-bottom: 10px; }}
  .row {{ display: flex; flex-wrap: wrap; gap: 0; margin-bottom: 10px; }}
  .measure {{ background: white; border: 1px solid #ddd; margin-right: -1px; }}
</style>
</head>
<body>
<h1>{title} — 吉他六线谱预览（前 {len(js_measures)} 小节）</h1>
<div id="sheet"></div>
<script>
var VF = Vex.Flow;
var measures = {measures_json};

var container = document.getElementById('sheet');
var measuresPerRow = 4;
var measureWidth = 280;
var measureHeight = 160;
var x = 10, y = 10;
var rowDiv = null;

measures.forEach(function(m, idx) {{
  if (idx % measuresPerRow === 0) {{
    rowDiv = document.createElement('div');
    rowDiv.className = 'row';
    container.appendChild(rowDiv);
    x = 10;
  }}

  var div = document.createElement('div');
  div.className = 'measure';
  div.style.width = measureWidth + 'px';
  div.style.height = measureHeight + 'px';
  rowDiv.appendChild(div);

  var renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);
  renderer.resize(measureWidth, measureHeight);
  var ctx = renderer.getContext();

  var stave = new VF.TabStave(x, y, measureWidth - 20);
  if (idx % measuresPerRow === 0) {{
    stave.addClef('tab').addTimeSignature('4/4');
  }}
  stave.setContext(ctx).draw();

  if (m.notes.length > 0) {{
    try {{
      VF.Formatter.FormatAndDraw(ctx, stave, m.notes);
    }} catch(e) {{
      console.error('measure', m.number, e);
    }}
  }}
}});
</script>
</body>
</html>'''
    return html


def main():
    parser = argparse.ArgumentParser(description="MusicXML 吉他六线谱 -> VexFlow HTML")
    parser.add_argument("input", help="输入 MusicXML 文件")
    parser.add_argument("--output", "-o", default="tab_preview.html", help="输出 HTML 路径")
    parser.add_argument("--max-measures", type=int, default=50, help="最多渲染多少小节")
    parser.add_argument("--title", default="Guitar Tab", help="页面标题")
    args = parser.parse_args()

    measures = parse_musicxml(args.input)
    html = build_html(measures, max_measures=args.max_measures, title=args.title)
    Path(args.output).write_text(html, encoding="utf-8")
    print(f"已生成：{args.output}（{min(args.max_measures, len(measures))}/{len(measures)} 小节）")


if __name__ == "__main__":
    main()
