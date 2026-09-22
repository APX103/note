#!/usr/bin/env python3
"""把原始 wav 整理成定长数据集 data/dataset.npz。

- 每条样本 = 1.0s @16kHz int16（16000 点）
- 正样本：能量裁边后随机放置在 1s 画布内（位置随机化，避免模型只认固定位置）
- 负样本：随机裁 1s（句子比 1s 长就随机窗口）
- 噪声类：程序化生成（白噪/粉噪/嗡嗡声/静音底噪）
- 切分：验证集 = 留出语音(Daniel/Tessa) 的全部样本 + 20% 噪声 —— 说话人无关评估
"""
import json, wave, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "dataset.npz"
META = ROOT / "data" / "dataset_meta.json"
SR, CLIP = 16000, 16000
VAL_VOICES = ("Daniel", "Tessa")
LABELS = {"lumos": 0, "unknown": 1, "noise": 2}


def load_wav(p: pathlib.Path):
    with wave.open(str(p)) as w:
        sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    x = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    if sr != SR:  # 线性重采样（自己录音可能是 44.1k）
        t = np.arange(len(x), dtype=np.float32) / sr
        x = np.interp(np.arange(0, len(x) / sr, 1 / SR), t, x).astype(np.float32)
    return x


def trim_silence(x, thr_ratio=0.02, margin_ms=50):
    e = np.abs(x)
    thr = e.max() * thr_ratio
    idx = np.where(e > thr)[0]
    if len(idx) < 10:
        return x
    m = int(margin_ms * SR / 1000)
    return x[max(0, idx[0] - m): idx[-1] + m]


def place_random(x):
    out = np.zeros(CLIP, dtype=np.float32)
    if len(x) >= CLIP:
        s = np.random.randint(0, len(x) - CLIP + 1)
        return x[s:s + CLIP]
    s = np.random.randint(0, CLIP - len(x) + 1)
    out[s:s + len(x)] = x
    return out


def gen_noise(n_clip, rng):
    out = []
    for i in range(n_clip):
        kind = i % 4
        t = np.arange(CLIP, dtype=np.float32)
        if kind == 0:      # 白噪
            x = rng.standard_normal(CLIP).astype(np.float32) * 0.05
        elif kind == 1:    # 粉噪（一阶近似）
            w = rng.standard_normal(CLIP).astype(np.float32)
            x = np.cumsum(w) * 0.002
            x -= x.mean()
        elif kind == 2:    # 工频嗡嗡 + 轻微白噪
            x = (0.03 * np.sin(2 * np.pi * 100 * t / SR)
                 + 0.01 * rng.standard_normal(CLIP).astype(np.float32))
        else:              # "静音"：极低底噪
            x = rng.standard_normal(CLIP).astype(np.float32) * 0.0015
        out.append(x.astype(np.float32))
    return out


def main():
    rng = np.random.default_rng(7)
    xs, ys, voices, splits = [], [], [], []

    def add(x, label, voice, is_val):
        xs.append(np.clip(x, -1, 1))
        ys.append(LABELS[label])
        voices.append(voice)
        splits.append(1 if is_val else 0)

    n_own = 0
    for p in sorted((RAW / "mylumos").glob("*.wav")):  # 用户真实录音优先吸收
        add(place_random(trim_silence(load_wav(p))), "lumos", "myvoice", False)
        n_own += 1

    for p in sorted((RAW / "lumos").glob("*.wav")):
        v = p.stem.split("_")[0]
        add(place_random(trim_silence(load_wav(p))), "lumos", v, v in VAL_VOICES)

    for p in sorted((RAW / "unknown").glob("*.wav")):
        v = p.stem.split("_")[0]
        add(place_random(load_wav(p)), "unknown", v, v in VAL_VOICES)

    for x in gen_noise(320, rng):
        is_val = rng.random() < 0.2
        add(x, "noise", "proc", is_val)

    X = np.stack(xs)
    y = np.array(ys)
    val = np.array(splits)
    voice = np.array(voices)
    np.savez_compressed(OUT, X=X.astype(np.float32), y=y, val=val, voice=voice)

    meta = {
        "labels": {v: k for k, v in LABELS.items()},
        "n": len(y),
        "train": int((val == 0).sum()),
        "val": int((val == 1).sum()),
        "by_class_train": {k: int(((y == LABELS[k]) & (val == 0)).sum()) for k in LABELS},
        "by_class_val": {k: int(((y == LABELS[k]) & (val == 1)).sum()) for k in LABELS},
        "own_recordings": n_own,
    }
    META.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
