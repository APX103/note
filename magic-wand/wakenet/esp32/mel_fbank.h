#pragma once
// PCM → 归一化 log-mel 特征（与训练侧 scripts/train.py::logmel 对齐）。
// 16kHz 单声道 int16；480 点窗(30ms) / 160 点步进(10ms) / 40 mel / 512 点 FFT。
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define WN_SR 16000
#define WN_WIN 480
#define WN_HOP 160
#define WN_FFT 512
#define WN_NFRAMES 97

// pcm: 至少 16000 个样本（1s 窗口）；out: [帧][mel] 的归一化 clamp 后特征
void mel_frames(const int16_t *pcm, int n_samples, float out[WN_NFRAMES][40]);

#ifdef __cplusplus
}
#endif
