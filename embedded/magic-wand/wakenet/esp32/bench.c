// 本机性能基准（勿进 ESP32 固件工程，与 test_main.c 同类）：
// 实测 wn_forward 整窗推理与 mel_frames 前端的单次耗时，用于推算 ESP32-S3 占空比。
// 用法: clang -O2 -o /tmp/wnbench bench.c wakenet.c mel_fbank.c -lm && /tmp/wnbench
#include "wakenet.h"
#include "mel_fbank.h"
#include "wakenet_model.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static double now_us(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1e6 + ts.tv_nsec / 1e3;
}

int main(void) {
    srand(42);

    // --- 1) wn_forward（float 特征 → 概率，内部量化 + 整窗推理）---
    static float feats[WN_FRAMES][WN_MEL];
    for (int t = 0; t < WN_FRAMES; t++)
        for (int m = 0; m < WN_MEL; m++)
            feats[t][m] = (float)(rand() % 800) / 100.0f - 4.0f;
    float probs[WN_CLASSES];
    wn_forward(&feats[0][0], probs); // warmup
    const int N1 = 300;
    double t0 = now_us();
    for (int i = 0; i < N1; i++) wn_forward(&feats[0][0], probs);
    double fwd_us = (now_us() - t0) / N1;

    // --- 2) mel_frames（1s PCM = 16000 样本 → 97×40 log-mel）---
    static int16_t pcm[16000];
    for (int i = 0; i < 16000; i++) pcm[i] = (int16_t)(rand() % 2000 - 1000);
    static float mel[WN_NFRAMES][40];
    mel_frames(pcm, 16000, mel); // warmup
    const int N2 = 100;
    t0 = now_us();
    for (int i = 0; i < N2; i++) mel_frames(pcm, 16000, mel);
    double mel_us = (now_us() - t0) / N2;

    // --- 3) 逐帧成本（流式实现只需为新帧算边际激活）---
    double mel_frame_us = mel_us / WN_NFRAMES;

    printf("wn_forward (full 97-frame window): %8.0f us/call\n", fwd_us);
    printf("mel_frames (1s PCM, 97 frames):    %8.0f us/call\n", mel_us);
    printf("mel per-frame (160-sample hop):    %8.1f us/frame\n", mel_frame_us);
    printf("probs: %.3f %.3f %.3f (sanity, random input)\n", probs[0], probs[1], probs[2]);
    return 0;
}
