// M5StickS3 上板性能基准：实测 wn_forward（整窗）与 mel_frames（逐帧）耗时。
// 目的：把"双引擎算力够不够"从估算变成实测。板上跑 ~10s 出结果，看串口。
// 组装/烧录：运行本目录 build.sh（复制 C 源到本目录 + arduino-cli 编译烧录）。
#include <Arduino.h>
#include "wakenet.h"
#include "mel_fbank.h"

static float feats[WN_FRAMES][WN_MEL];
static float probs[WN_CLASSES];

void setup() {
    Serial.begin(115200);
    delay(1500);
    Serial.println("\n[wakenet on-device bench] ESP32-S3 @240MHz, Arduino -Os");

    // 随机特征填充（计时与数据无关，只测算力）
    for (int t = 0; t < WN_FRAMES; t++)
        for (int m = 0; m < WN_MEL; m++)
            feats[t][m] = (float)(esp_random() % 800) / 100.0f - 4.0f;

    // --- 1) wn_forward 整窗推理 ---
    wn_forward(&feats[0][0], probs);            // warmup
    const int N1 = 200;
    uint32_t t0 = micros();
    for (int i = 0; i < N1; i++) wn_forward(&feats[0][0], probs);
    uint32_t fwd_us = (micros() - t0) / N1;

    // --- 2) mel 单帧（160 样本 = 10ms hop）---
    static int16_t pcm[WN_WIN];
    static float mel1[40];
    for (int i = 0; i < WN_WIN; i++) pcm[i] = (int16_t)(esp_random() % 2000 - 1000);
    // mel_frames 是整段接口：用 1s PCM 折算逐帧成本
    static int16_t pcm1s[16000];
    static float melAll[WN_NFRAMES][40];
    for (int i = 0; i < 16000; i++) pcm1s[i] = (int16_t)(esp_random() % 2000 - 1000);
    mel_frames(pcm1s, 16000, melAll);           // warmup
    const int N2 = 50;
    t0 = micros();
    for (int i = 0; i < N2; i++) mel_frames(pcm1s, 16000, melAll);
    uint32_t mel_us = (micros() - t0) / N2;
    (void)pcm; (void)mel1;

    Serial.printf("wn_forward full window : %lu us/call\n", (unsigned long)fwd_us);
    Serial.printf("  -> 每 100ms 滑一窗占空比: %.1f%%\n", fwd_us * 10.0 / 1e4);
    Serial.printf("  -> 每 300ms 滑一窗占空比: %.1f%%\n", fwd_us * 3.33 / 1e4);
    Serial.printf("mel_frames 1s (97帧)    : %lu us/call\n", (unsigned long)mel_us);
    Serial.printf("  -> 逐帧成本: %.1f us / 10ms 帧 = 占空比 %.1f%%\n",
                  mel_us / 97.0, mel_us / 97.0 / 1e4 * 100.0);
    Serial.println("[done] 双引擎同时跑(唤醒@100ms滑窗 + 手势武装期10Hz)合计见上行推算");
}

void loop() { delay(1000); }
