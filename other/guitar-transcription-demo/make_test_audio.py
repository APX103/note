#!/usr/bin/env python3
"""生成一段简单的合成吉他测试音频。"""

import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = 44100
TOTAL_SECONDS = 8.0

def note(freq, duration, harmonics=(1, 0.5, 0.25, 0.125)):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    samples = np.zeros_like(t)
    for i, weight in enumerate(harmonics):
        samples += weight * np.sin(2 * np.pi * freq * (i + 1) * t)
    # 简单包络
    attack = int(0.02 * SAMPLE_RATE)
    release = int(0.1 * SAMPLE_RATE)
    env = np.ones_like(t)
    env[:attack] = np.linspace(0, 1, attack)
    env[-release:] = np.linspace(1, 0, release)
    return samples * env

# 一段简单的 E 小调琶音 + 和弦
freqs = {
    'E2': 82.41, 'G2': 98.00, 'B2': 123.47,
    'E3': 164.81, 'G3': 196.00, 'B3': 246.94, 'E4': 329.63
}

audio = np.zeros(int(SAMPLE_RATE * TOTAL_SECONDS))

def add_at(start, samples):
    s = int(start * SAMPLE_RATE)
    e = min(s + len(samples), len(audio))
    audio[s:e] += samples[:e - s]

# 琶音
for i, name in enumerate(['E2', 'G2', 'B2', 'E3', 'G3', 'B3', 'E4', 'B3', 'G3', 'E3']):
    add_at(0.2 + i * 0.5, note(freqs[name], 0.5))

# 和弦（放在 6 秒处）
chord_samples = np.zeros(int(SAMPLE_RATE * 1.5))
for name in ['E2', 'B2', 'E3', 'G3', 'B3', 'E4']:
    n = note(freqs[name], 1.5)
    chord_samples[:len(n)] += n[:len(chord_samples)]
add_at(6.0, chord_samples)

# 归一化
peak = np.max(np.abs(audio))
if peak > 0:
    audio = audio / peak * 0.9
audio = (audio * 32767).astype(np.int16)

wavfile.write('test_guitar.wav', SAMPLE_RATE, audio)
print("已生成 test_guitar.wav")
