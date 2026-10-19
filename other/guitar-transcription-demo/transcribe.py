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
DEFAULT_MAX_FRET = 24


def possible_positions(pitch: int, max_fret: int = DEFAULT_MAX_FRET):
    """返回某个音高在吉他上所有可行的（弦号，品）组合。"""
    candidates = []
    for string_num, info in GUITAR_STRINGS.items():
        fret = pitch - info["midi"]
        if 0 <= fret <= max_fret:
            candidates.append((string_num, fret))
    # 按弦号排序：高音弦在前，低音弦在后
    candidates.sort(key=lambda x: x[0])
    return candidates


def _event_cost(assignment, prev_avg_fret: float, max_fret: int):
    """为一个和弦/事件内的弦/品分配打分。"""
    frets = [fret for _, fret in assignment if fret > 0]
    strings = [s for s, _ in assignment]
    avg_fret = sum(frets) / len(frets) if frets else prev_avg_fret

    # 1. 与上一个手型位置的跳变
    jump = abs(avg_fret - prev_avg_fret)

    # 2. 内部手型跨度（同一和弦内最大-最小品位）
    span = max(frets) - min(frets) if len(frets) > 1 else 0
    span_penalty = 0 if span <= 4 else (span - 4) ** 2

    # 3. 品位高度（避免高把位）
    height_penalty = sum(f ** 1.5 for f in frets) / max(len(frets), 1) * 0.3

    # 4. 空弦惩罚（空弦音色与按弦不同，和弦里适度避免）
    open_count = sum(1 for f in frets if f == 0)
    open_penalty = open_count * 0.8

    # 5. 弦号惩罚：低音优先用低音弦，高音优先用高音弦
    string_penalty = sum((s - 1) * 0.15 for s in strings)

    # 6. 超出 max_fret 的硬惩罚（理论上不会出现，因为 possible_positions 已过滤）
    range_penalty = sum(max(0, f - max_fret) * 100 for f in frets)

    return 2.0 * jump + span_penalty + height_penalty + open_penalty + string_penalty + range_penalty


def _assign_event(notes_in_event, prev_avg_fret: float, max_fret: int):
    """
    为一个和弦（同时发声的音符列表）找到最佳弦/品分配。
    返回 (assignment_list, avg_fret)。
    assignment_list 元素为 (start, end, pitch, conf, string_num, fret)。
    """
    # 每个音符的所有可行位置
    note_candidates = []
    for start, end, pitch, conf in notes_in_event:
        candidates = possible_positions(pitch, max_fret)
        if not candidates:
            # 该音超出吉他音域，保留音符但标记无弦/品
            note_candidates.append([(start, end, pitch, conf, None, None, [])])
        else:
            note_candidates.append([
                (start, end, pitch, conf, s, f, [(s, f)])
                for s, f in candidates
            ])

    # 为每个音符选一个位置，且所有位置弦号不重复
    # 用回溯搜索；吉他和弦音符数通常 <= 6，状态空间有限
    best_assignment = None
    best_cost = float("inf")

    def backtrack(idx, used_strings, current, current_positions):
        nonlocal best_assignment, best_cost
        if idx == len(note_candidates):
            cost = _event_cost(current_positions, prev_avg_fret, max_fret)
            if cost < best_cost:
                best_cost = cost
                best_assignment = current[:]
            return

        for choice in note_candidates[idx]:
            _, _, _, _, string_num, fret, positions = choice
            if string_num is None:
                # 超出音域的音符，不参与弦冲突
                current.append(choice[:6])
                backtrack(idx + 1, used_strings, current, current_positions)
                current.pop()
            elif string_num not in used_strings:
                current.append(choice[:6])
                backtrack(idx + 1, used_strings | {string_num}, current, current_positions + positions)
                current.pop()

    backtrack(0, set(), [], [])

    if best_assignment is None:
        #  fallback：按原顺序贪心分配，避免同弦冲突
        used = set()
        best_assignment = []
        for choices in note_candidates:
            chosen = None
            for start, end, pitch, conf, s, f, _ in choices:
                if s is None or s not in used:
                    chosen = (start, end, pitch, conf, s, f)
                    if s is not None:
                        used.add(s)
                    break
            if chosen is None:
                # 所有弦都被占用，该音无法在当前和弦内分配
                start, end, pitch, conf = choices[0][0], choices[0][1], choices[0][2], choices[0][3]
                chosen = (start, end, pitch, conf, None, None)
            best_assignment.append(chosen)

    # 计算本次事件平均品位（按弦音符）
    pressed = [fret for _, _, _, _, _, fret in best_assignment if fret is not None and fret > 0]
    avg_fret = sum(pressed) / len(pressed) if pressed else prev_avg_fret
    return best_assignment, avg_fret


def choose_positions(notes, max_fret: int = DEFAULT_MAX_FRET):
    """
    为每个 MIDI 音符选择（弦号，品）。
    改进策略：
    - 同时发声的音符合并成和弦，整体优化弦/品分配。
    - 最小化相邻和弦之间的手型跳变。
    - 惩罚同一和弦内过大的品位跨度。
    """
    notes = sorted(notes, key=lambda x: x[0])

    # 按起始时间分组（容差 1ms）
    events = []
    current_event = []
    current_start = None
    tol = 1e-3
    for n in notes:
        start = n[0]
        if current_start is None or abs(start - current_start) <= tol:
            current_event.append(n)
            current_start = start
        else:
            events.append(current_event)
            current_event = [n]
            current_start = start
    if current_event:
        events.append(current_event)

    results = []
    prev_avg_fret = 5.0
    for event in events:
        assignment, prev_avg_fret = _assign_event(event, prev_avg_fret, max_fret)
        results.extend(assignment)

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
    parser.add_argument("--max-fret", type=int, default=DEFAULT_MAX_FRET,
                        help="吉他最大品位数，默认 24；古典吉他可设 19")
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
    positioned = choose_positions(note_events, max_fret=args.max_fret)
    in_range = [n for n in positioned if n[4] is not None]
    out_of_range = len(positioned) - len(in_range)
    print(f"      在吉他音域内可弹奏的音符：{len(in_range)}/{len(positioned)}")
    if out_of_range > 0:
        print(f"      超出 {args.max_fret} 品的音符：{out_of_range} 个（已过滤）")

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
