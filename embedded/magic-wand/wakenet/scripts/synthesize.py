#!/usr/bin/env python3
"""用 macOS 自带 `say` 合成唤醒词训练数据（正样本 lumos + 负样本干扰词/句子）。

产出: data/raw/lumos/*.wav  data/raw/unknown/*.wav  (16kHz 单声道 int16)
文件名编码了语音/语速信息，供数据集切分"说话人无关"验证集用。
自己的真实录音直接丢 data/raw/mylumos/*.wav 即可被后续步骤自动吸收。
"""
import subprocess, random, re, sys, wave, pathlib
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

VOICES = ["Daniel", "Karen", "Kathy", "Moira", "Rishi", "Samantha", "Tara", "Tessa", "Fred"]
VAL_VOICES = ["Daniel", "Tessa"]          # 完整留出：训练时一次都不出现
POS_TEXTS = ["lumos", "Lumos!", "lumos?"]
POS_RATES = [130, 150, 170, 190, 215]

# 负样本：发音易混词 + 日常口令句。误唤醒主要就发生在这些词上。
NEG_TEXTS = [
    "luminous", "music", "locus", "focus", "mucus", "menus", "mentors", "movers",
    "lasers", "mangoes", "windows", "campus", "famous", "bonus", "onwards",
    "purpose", "circus", "radius", "fibrosis", "neurosis", "hocus pocus",
    "lose", "loose", "muse", "news", "shoes", "juice", "moose", "chose",
    "close", "moves", "ruse", "fuse", "blues", "clues", "cruise", "truce",
    "lupus", "lukewarm", "lumber", "lump", "lunch", "locust", "lucas",
    "muses", "moss", "mouse", "mouth", "months", "monks", "much", "must",
    "most", "mast", "mask", "mesh", "mash", "marsh", "march", "circuits",
    "surplus", "obvious", "previous", "serious", "curious", "furious",
    "glorious", "various", "turn on the light", "turn off the light", "what time is it",
    "hey siri", "okay google", "alexa stop", "hello world", "good morning",
    "nice to meet you", "how are you today", "let us build something cool",
    "the weather is nice", "play some music", "stop the music",
    "set a timer for five minutes", "call me later", "i love this song",
    "open the door", "close the window", "what is for dinner",
]

rng = random.Random(42)


def say_to_wav(voice: str, rate: int, text: str, out: pathlib.Path) -> bool:
    aiff = out.with_suffix(".aiff")
    r = subprocess.run(["say", "-v", voice, "-r", str(rate), "-o", str(aiff), text],
                       capture_output=True)
    if r.returncode != 0 or not aiff.exists():
        aiff.unlink(missing_ok=True)
        return False
    wav = out.with_suffix(".wav")
    r = subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@16000", str(aiff), str(wav)],
                       capture_output=True)
    aiff.unlink(missing_ok=True)
    if r.returncode != 0:
        return False
    try:  # 校验确实可读、时长合理
        with wave.open(str(wav)) as w:
            ok = w.getframerate() == 16000 and 0.1 < w.getnframes() / 16000 < 15
        return ok
    except Exception:
        return False


def slug(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")[:24]


def main():
    jobs = []  # (voice, rate, text, outdir, prefix)
    for vi, v in enumerate(VOICES):
        for rate in POS_RATES:
            for ti, text in enumerate(POS_TEXTS):
                name = f"{v}_{rate}_{ti}.wav"
                jobs.append((v, rate, text, RAW / "lumos", name))
    for ti, text in enumerate(NEG_TEXTS):
        for vi, v in enumerate(VOICES):
            for rate in (150, 190) if (vi + ti) % 2 == 0 else (135, 170):
                name = f"{v}_{rate}_{ti:02d}_{slug(text)}.wav"
                jobs.append((v, rate, text, RAW / "unknown", name))

    print(f"待合成 {len(jobs)} 条（正样本 {sum(1 for j in jobs if j[3].name=='lumos')}，"
          f"负样本 {sum(1 for j in jobs if j[3].name=='unknown')}）")

    def work(job):
        v, rate, text, d, name = job
        d.mkdir(parents=True, exist_ok=True)
        out = d / name
        if out.exists():
            return True
        return say_to_wav(v, rate, text, out)

    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(work, jobs))
    ok = sum(results)
    print(f"完成 {ok}/{len(jobs)}，失败 {len(jobs)-ok}")
    for v in VAL_VOICES:
        n = len(list((RAW/'lumos').glob(f"{v}_*.wav")))
        print(f"  留出验证语音 {v}: {n} 条正样本")
    sys.exit(0 if ok == len(jobs) else 1)


if __name__ == "__main__":
    main()
