#!/usr/bin/env python3
"""
MP3 -> MusicXML 吉他六线谱 Demo
================================
依赖：basic-pitch（自动扒谱）、music21（仅用于 pitch 工具函数）

用法：
    python transcribe.py input.mp3 --bpm 120 --output out.musicxml
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from music21 import pitch as m21_pitch


def _note_events_from_basic_pitch(audio_path: str):
    """用 basic-pitch 从音频提取音符事件。"""
    try:
        from basic_pitch.inference import predict
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "请先安装 basic-pitch：pip install -r requirements.txt"
        ) from exc

    # predict 返回 (model_output, midi_data, note_events)
    _, _, note_events = predict(audio_path)

    # note_events 格式：(start, end, pitch, confidence, ...) 长度可能是 4 或 5
    parsed = []
    for ev in note_events:
        if isinstance(ev, (list, tuple)):
            start, end, pitch, conf = ev[0], ev[1], ev[2], ev[3]
        else:
            start = ev.get("start_time_s")
            end = ev.get("end_time_s")
            pitch = ev.get("pitch_midi")
            conf = ev.get("confidence", 1.0)
        parsed.append((float(start), float(end), int(pitch), float(conf)))
    return parsed


# 吉他标准调弦，MIDI 音高编号
# MusicXML 的弦号约定：1 = 高音 E（最细），6 = 低音 E（最粗）
GUITAR_STRINGS = {
    1: {"name": "E", "midi": 64},  # ①弦 E4
    2: {"name": "B", "midi": 59},  # ②弦 B3
    3: {"name": "G", "midi": 55},  # ③弦 G3
    4: {"name": "D", "midi": 50},  # ④弦 D3
    5: {"name": "A", "midi": 45},  # ⑤弦 A2
    6: {"name": "E", "midi": 40},  # ⑥弦 E2
}
MAX_FRET = 24


def possible_positions(pitch: int):
    """返回某个音高在吉他上所有可行的（弦号，品）组合。"""
    candidates = []
    for string_num, info in GUITAR_STRINGS.items():
        fret = pitch - info["midi"]
        if 0 <= fret <= MAX_FRET:
            candidates.append((string_num, fret))
    # 按弦号排序：高音弦在前，低音弦在后
    candidates.sort(key=lambda x: x[0])
    return candidates


def choose_positions(notes, smoothing_weight: float = 2.0):
    """
    为每个 MIDI 音符选择（弦号，品）。
    简单启发式：最小化相邻音符的品位跳变，同时避免过高品位。
    """
    notes = sorted(notes, key=lambda x: x[0])
    current_fret = 5  # 默认手型位置
    results = []

    for start, end, pitch, conf in notes:
        candidates = possible_positions(pitch)
        if not candidates:
            # 超出吉他音域，仍保留音符但无法标出弦/品
            results.append((start, end, pitch, conf, None, None))
            continue

        # 代价：品位跳变 + 品位高度 + 不偏好空弦（空弦音色突兀，轻度惩罚）
        def cost(pos):
            string_num, fret = pos
            jump = abs(fret - current_fret)
            height = fret * 0.4
            open_penalty = 0 if fret != 0 else 0.5
            # 高音弦上的低音弹起来不舒服，轻度惩罚
            string_penalty = (string_num - 1) * 0.2
            return smoothing_weight * jump + height + open_penalty + string_penalty

        best_string, best_fret = min(candidates, key=cost)
        current_fret = best_fret
        results.append((start, end, pitch, conf, best_string, best_fret))

    return results


def quantize_time(seconds: float, bpm: float, grid: int = 16):
    """把时间（秒）按 BPM 量化到 grid 分音符（默认 16 分）。"""
    quarter_length = (seconds / 60.0) * bpm  # 1.0 = 四分音符
    grid_factor = grid / 4  # 16 分音符 -> 4
    quantized = round(quarter_length * grid_factor) / grid_factor
    return max(0.0, quantized)


def midi_to_xml_pitch(midi: int):
    """把 MIDI 音高转成 MusicXML 的 step/alter/octave。"""
    p = m21_pitch.Pitch(midi=midi)
    return p.step, p.alter if p.alter is not None else 0, p.octave


def duration_type(divs: int):
    """根据 divisions 数量返回 MusicXML note type。"""
    if divs == 0:
        return "16th"
    mapping = [
        (1920, "whole"),
        (960, "half"),
        (480, "quarter"),
        (240, "eighth"),
        (120, "16th"),
        (60, "32nd"),
        (30, "64th"),
    ]
    for threshold, name in mapping:
        if divs >= threshold:
            return name
    return "64th"


def build_musicxml(positioned_notes, bpm: float = 120.0):
    """直接生成带 <technical><string/><fret/></technical> 的 MusicXML。"""
    DIVISIONS = 480  # 一个四分音符 = 480
    BEATS_PER_MEASURE = 4

    # 量化
    quantized = []
    for start, end, pitch, conf, string_num, fret in positioned_notes:
        q_start = quantize_time(start, bpm)
        q_end = quantize_time(end, bpm)
        q_dur = max(q_end - q_start, 0.25)  # 最短 16 分音符
        quantized.append((q_start, q_dur, pitch, string_num, fret))

    # 按起始时间分组，同时间音符合并成和弦
    groups = {}
    for q_start, q_dur, pitch, string_num, fret in quantized:
        groups.setdefault(q_start, []).append((q_dur, pitch, string_num, fret))

    # 按 measure 组织
    measure_groups = {}
    for offset in sorted(groups.keys()):
        measure_idx = int(offset // BEATS_PER_MEASURE)
        local_offset = offset % BEATS_PER_MEASURE
        measure_groups.setdefault(measure_idx, {})[local_offset] = groups[offset]

    # 构建 XML
    import xml.etree.ElementTree as ET

    root = ET.Element("score-partwise", {"version": "3.1"})
    root.text = "\n  "

    ident = ET.SubElement(root, "identification")
    ET.SubElement(ident, "creator", {"type": "composer"}).text = "Guitar Transcription Demo"
    enc = ET.SubElement(ident, "encoding")
    ET.SubElement(enc, "software").text = "basic-pitch + music21"

    part_list = ET.SubElement(root, "part-list")
    part_list.text = "\n    "
    part_list.tail = "\n  "
    score_part = ET.SubElement(part_list, "score-part", {"id": "P1"})
    score_part.text = "\n      "
    score_part.tail = "\n  "
    ET.SubElement(score_part, "part-name").text = "Guitar"
    ET.SubElement(score_part, "part-abbreviation").text = "Gtr."

    part = ET.SubElement(root, "part", {"id": "P1"})
    part.text = "\n    "

    for measure_idx in sorted(measure_groups.keys()):
        measure = ET.SubElement(part, "measure", {"number": str(measure_idx + 1)})
        measure.text = "\n      "
        measure.tail = "\n    "

        # 第一小节写入谱号、拍号、调弦信息
        if measure_idx == 0:
            attrs = ET.SubElement(measure, "attributes")
            attrs.text = "\n        "
            attrs.tail = "\n      "
            ET.SubElement(attrs, "divisions").text = str(DIVISIONS)
            time = ET.SubElement(attrs, "time")
            time.text = "\n          "
            time.tail = "\n        "
            ET.SubElement(time, "beats").text = str(BEATS_PER_MEASURE)
            ET.SubElement(time, "beat-type").text = "4"
            clef = ET.SubElement(attrs, "clef")
            clef.text = "\n          "
            clef.tail = "\n        "
            ET.SubElement(clef, "sign").text = "TAB"
            ET.SubElement(clef, "line").text = "5"
            staff = ET.SubElement(attrs, "staff-details")
            staff.text = "\n          "
            staff.tail = "\n        "
            ET.SubElement(staff, "staff-lines").text = "6"
            for line, (string_num, info) in enumerate(GUITAR_STRINGS.items(), start=1):
                tuning = ET.SubElement(staff, "staff-tuning", {"line": str(line)})
                tuning.text = "\n            "
                tuning.tail = "\n          "
                ET.SubElement(tuning, "tuning-step").text = info["name"]
                ET.SubElement(tuning, "tuning-octave").text = str(
                    m21_pitch.Pitch(midi=info["midi"]).octave
                )
            attrs.tail = "\n      "

        local_offsets = sorted(measure_groups[measure_idx].keys())
        cursor = 0.0

        for local_offset in local_offsets:
            # 填充休止符
            gap = local_offset - cursor
            if gap > 1e-9:
                gap_divs = int(round(gap * DIVISIONS))
                if gap_divs > 0:
                    rest = ET.SubElement(measure, "note")
                    rest.text = "\n        "
                    rest.tail = "\n      "
                    ET.SubElement(rest, "rest")
                    ET.SubElement(rest, "duration").text = str(gap_divs)
                    ET.SubElement(rest, "voice").text = "1"
                    ET.SubElement(rest, "type").text = duration_type(gap_divs)
                    cursor = local_offset

            items = measure_groups[measure_idx][local_offset]
            # 同一和弦内不能有两音占用同一根弦
            used_strings = set()
            chord_items = []
            for q_dur, pitch, string_num, fret in items:
                if string_num is None or string_num in used_strings:
                    continue
                used_strings.add(string_num)
                chord_items.append((q_dur, pitch, string_num, fret))

            if not chord_items:
                continue

            first_dur = int(round(chord_items[0][0] * DIVISIONS))
            for idx, (q_dur, pitch, string_num, fret) in enumerate(chord_items):
                dur_divs = int(round(q_dur * DIVISIONS))
                n = ET.SubElement(measure, "note")
                n.text = "\n        "
                n.tail = "\n      "
                if idx > 0:
                    ET.SubElement(n, "chord")
                step, alter, octave = midi_to_xml_pitch(pitch)
                pitch_el = ET.SubElement(n, "pitch")
                pitch_el.text = "\n          "
                pitch_el.tail = "\n        "
                ET.SubElement(pitch_el, "step").text = step
                if alter != 0:
                    ET.SubElement(pitch_el, "alter").text = str(int(alter))
                ET.SubElement(pitch_el, "octave").text = str(octave)
                ET.SubElement(n, "duration").text = str(dur_divs)
                ET.SubElement(n, "voice").text = "1"
                ET.SubElement(n, "type").text = duration_type(dur_divs)
                ET.SubElement(n, "stem").text = "down"
                notations = ET.SubElement(n, "notations")
                notations.text = "\n          "
                notations.tail = "\n        "
                tech = ET.SubElement(notations, "technical")
                tech.text = "\n            "
                tech.tail = "\n          "
                ET.SubElement(tech, "string").text = str(string_num)
                ET.SubElement(tech, "fret").text = str(fret)

            cursor = local_offset + chord_items[0][0]

        # 小节末尾补休止符
        remaining = BEATS_PER_MEASURE - cursor
        if remaining > 1e-9:
            rem_divs = int(round(remaining * DIVISIONS))
            if rem_divs > 0:
                rest = ET.SubElement(measure, "note")
                rest.text = "\n        "
                rest.tail = "\n      "
                ET.SubElement(rest, "rest")
                ET.SubElement(rest, "duration").text = str(rem_divs)
                ET.SubElement(rest, "voice").text = "1"
                ET.SubElement(rest, "type").text = duration_type(rem_divs)

    # 美化 XML
    def indent(elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                indent(child, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    indent(root)
    return ET.tostring(root, encoding="utf-8", method="xml").decode("utf-8")


def main():
    parser = argparse.ArgumentParser(description="MP3 -> MusicXML 吉他六线谱 Demo")
    parser.add_argument("input", help="输入音频文件（mp3 / wav / flac 等）")
    parser.add_argument("--output", "-o", default="output.musicxml", help="输出 MusicXML 路径")
    parser.add_argument("--bpm", type=float, default=120.0, help="拍速，默认 120")
    parser.add_argument("--confidence", type=float, default=0.3,
                        help="basic-pitch 置信度阈值，低于此值的音符会被过滤")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误：找不到输入文件 {input_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[1/4] 从 {input_path} 提取音符事件...")
    note_events = _note_events_from_basic_pitch(str(input_path))
    print(f"      原始检测到 {len(note_events)} 个音符")

    note_events = [n for n in note_events if n[3] >= args.confidence]
    print(f"      置信度 ≥ {args.confidence} 后剩余 {len(note_events)} 个音符")

    if not note_events:
        print("未检测到足够音符，输出空谱。", file=sys.stderr)
        sys.exit(1)

    print("[2/4] 为音符分配吉他弦/品位...")
    positioned = choose_positions(note_events)
    in_range = [n for n in positioned if n[4] is not None]
    print(f"      在吉他音域内可弹奏的音符：{len(in_range)}/{len(positioned)}")

    print("[3/4] 生成 MusicXML...")
    xml = build_musicxml(positioned, bpm=args.bpm)

    output_path = Path(args.output)
    output_path.write_text(xml, encoding="utf-8")
    print(f"[4/4] 已保存：{output_path.resolve()}")
    print("\n提示：")
    print("  • 可用 MuseScore / Guitar Pro / Finale 打开生成的 .musicxml")
    print("  • 若节奏对不齐，可用 --bpm 指定更接近原曲的速度")
    print("  • 最终制谱建议人工校对，AI 扒谱在密集和弦上仍会错音或漏音")


if __name__ == "__main__":
    main()
