// 自研迷你唤醒词引擎 int8 前向（与 scripts/export_c.py 的 numpy int8 路径逐位对齐：
// 整数累加 + float requant 取整，ReLU 层量化下限 0）。
// 结构: stem(40→C0) → [dw(d2)+pw(C0→C1)] → [dw(d4)+pw(C1→C2)] → [dw(d8)+pw(C2→C3)] → GAP → FC
#include "wakenet.h"
#include "wakenet_model.h"
#include <math.h>
#include <string.h>

static int8_t requant(int32_t acc, float rq) {
    long r = lrintf((float)acc * rq);
    if (r < 0) r = 0;            // 所有卷积层后接 ReLU
    if (r > 127) r = 127;
    return (int8_t)r;
}

// 普通卷积 stride=1；x/y 布局 [C][T]；rq 为逐输出通道 requant 系数
static void conv(const int8_t *x, int ci, int T, const int8_t *w, const int32_t *b,
                 int co, int K, int pad, int dil, const float *rq, int8_t *y) {
    for (int o = 0; o < co; o++)
        for (int t = 0; t < T; t++) {
            int32_t acc = b[o];
            for (int i = 0; i < ci; i++) {
                const int8_t *xr = x + i * T;
                const int8_t *wr = w + (o * ci + i) * K;
                for (int k = 0; k < K; k++) {
                    int ti = t - pad + k * dil;
                    if (ti >= 0 && ti < T) acc += (int32_t)xr[ti] * (int32_t)wr[k];
                }
            }
            y[o * T + t] = requant(acc, rq[o]);
        }
}

// 深度可分离卷积的 depthwise 半边（通道=输出，逐通道 requant）
static void conv_dw(const int8_t *x, int C, int T, const int8_t *w, const int32_t *b,
                    int K, int pad, int dil, const float *rq, int8_t *y) {
    for (int c = 0; c < C; c++)
        for (int t = 0; t < T; t++) {
            int32_t acc = b[c];
            const int8_t *xr = x + c * T;
            const int8_t *wr = w + c * K;
            for (int k = 0; k < K; k++) {
                int ti = t - pad + k * dil;
                if (ti >= 0 && ti < T) acc += (int32_t)xr[ti] * (int32_t)wr[k];
            }
            y[c * T + t] = requant(acc, rq[c]);
        }
}

void wn_forward_q(const int8_t *q, float probs[WN_CLASSES]) {
    static int8_t a[WN_C3 * WN_T], b[WN_C3 * WN_T];
    conv(q, WN_MEL, WN_T, wn_stem_w, wn_stem_b, WN_C0, 5, 2, 1, wn_stem_requant, a);
    conv_dw(a, WN_C0, WN_T, wn_b1_dw_w, wn_b1_dw_b, 5, 4, 2, wn_b1_dw_requant, b);
    conv(b, WN_C0, WN_T, wn_b1_pw_w, wn_b1_pw_b, WN_C1, 1, 0, 1, wn_b1_pw_requant, a);
    conv_dw(a, WN_C1, WN_T, wn_b2_dw_w, wn_b2_dw_b, 5, 8, 4, wn_b2_dw_requant, b);
    conv(b, WN_C1, WN_T, wn_b2_pw_w, wn_b2_pw_b, WN_C2, 1, 0, 1, wn_b2_pw_requant, a);
    conv_dw(a, WN_C2, WN_T, wn_b3_dw_w, wn_b3_dw_b, 5, 16, 8, wn_b3_dw_requant, b);
    conv(b, WN_C2, WN_T, wn_b3_pw_w, wn_b3_pw_b, WN_C3, 1, 0, 1, wn_b3_pw_requant, a);
    // 时间 GAP（scale 不变，取整回 int8）+ FC
    int8_t gap[WN_C3];
    for (int c = 0; c < WN_C3; c++) {
        float m = 0.0f;
        for (int t = 0; t < WN_T; t++) m += a[c * WN_T + t];
        long r = lrintf(m / WN_T);
        if (r < 0) r = 0;
        if (r > 127) r = 127;
        gap[c] = (int8_t)r;
    }
    float logits[WN_CLASSES];
    for (int o = 0; o < WN_CLASSES; o++) {
        int32_t acc = wn_fc_b[o];
        for (int c = 0; c < WN_C3; c++) acc += (int32_t)gap[c] * (int32_t)wn_fc_w[o * WN_C3 + c];
        logits[o] = (float)acc * wn_fc_logit_scale[o];
    }
    float mx = logits[0];
    for (int i = 1; i < WN_CLASSES; i++) if (logits[i] > mx) mx = logits[i];
    float s = 0;
    for (int i = 0; i < WN_CLASSES; i++) { probs[i] = expf(logits[i] - mx); s += probs[i]; }
    for (int i = 0; i < WN_CLASSES; i++) probs[i] /= s;
}

void wn_forward(const float *feats, float probs[WN_CLASSES]) {
    static int8_t q[WN_MEL * WN_T];
    for (int m = 0; m < WN_MEL; m++)
        for (int t = 0; t < WN_T; t++) {
            float v = feats[t * WN_MEL + m] * (127.0f / WN_FEAT_CLAMP);
            long r = lrintf(v);
            if (r < -127) r = -127;
            if (r > 127) r = 127;
            q[m * WN_T + t] = (int8_t)r;
        }
    wn_forward_q(q, probs);
}

void wn_trigger_init(wn_trigger_t *tg, int avg_n, float thr) {
    memset(tg, 0, sizeof(*tg));
    tg->avg_n = avg_n > 16 ? 16 : avg_n;
    tg->thr = thr;
}

int wn_trigger_update(wn_trigger_t *tg, float p) {
    tg->buf[tg->idx] = p;
    tg->idx = (tg->idx + 1) % 16;
    if (tg->n < 16) tg->n++;
    if (tg->n < tg->avg_n) return 0;
    float s = 0;
    for (int i = 0; i < tg->avg_n; i++) s += tg->buf[(tg->idx + 15 - i) % 16];
    s /= tg->avg_n;
    if (!tg->fired && s > tg->thr) { tg->fired = 1; return 1; }
    if (s < tg->thr * 0.6f) tg->fired = 0;   // 滞回，防抖
    return 0;
}
