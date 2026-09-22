#pragma once
// 自研迷你唤醒词引擎（WakeNet 复刻）：int8 量化前向。
// 配方: log-mel(40维,30ms/10ms) → 量化 → Conv/DSConv ×5 → 时间GAP → FC(3类) → softmax
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define WN_MEL 40
#define WN_FRAMES 97
#define WN_CLASSES 3          // 0=lumos 1=unknown 2=noise
#define WN_T 97               // 时间帧数（与训练一致）

// 输入已量化的特征 (40,97) 列主序: q[mel*WN_T + t]，输出 3 类概率
void wn_forward_q(const int8_t *q, float probs[WN_CLASSES]);

// 输入归一化后的 float 特征 (97,40) 行主序: f[t][mel]，内部量化后前向
void wn_forward(const float *feats /*[WN_FRAMES][WN_MEL]*/, float probs[WN_CLASSES]);

// 简单触发器：滑窗概率平滑。连续 avg_n 个窗的 lumos 概率均值 > thr 才置位。
typedef struct {
    float buf[16];
    int   n, idx, avg_n;
    float thr;
    int   fired;
} wn_trigger_t;

void wn_trigger_init(wn_trigger_t *tg, int avg_n, float thr);
int  wn_trigger_update(wn_trigger_t *tg, float p_lumos);   // 返回 1=触发

#ifdef __cplusplus
}
#endif
