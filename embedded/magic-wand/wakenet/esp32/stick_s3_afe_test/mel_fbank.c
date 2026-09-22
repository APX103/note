// PCM → log-mel，浮点实现（ESP32-S3 带 FPU，玩具 Demo 无需定点化）。
// 滤波器组/窗函数/归一化参数来自自动生成的 wakenet_model.h。
#include "mel_fbank.h"
#include "wakenet.h"
#include "wakenet_model.h"
#include <math.h>
#include <string.h>

static void fft512(float *re, float *im) {
    for (int i = 1, j = 0; i < WN_FFT; i++) {
        int bit = WN_FFT >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) {
            float t = re[i]; re[i] = re[j]; re[j] = t;
            t = im[i]; im[i] = im[j]; im[j] = t;
        }
    }
    for (int len = 2; len <= WN_FFT; len <<= 1) {
        for (int i = 0; i < WN_FFT; i += len) {
            for (int k = 0; k < len / 2; k++) {
                // 直接按角度算旋转因子（避免增量旋转的精度漂移）
                float ang = -2.0f * 3.14159265358979f * (float)k / (float)len;
                float wr = cosf(ang), wi = sinf(ang);
                float ur = re[i + k], ui = im[i + k];
                float xr = re[i + k + len / 2], xi = im[i + k + len / 2];
                float vr = xr * wr - xi * wi;
                float vi = xr * wi + xi * wr;
                re[i + k] = ur + vr; im[i + k] = ui + vi;
                re[i + k + len / 2] = ur - vr; im[i + k + len / 2] = ui - vi;
            }
        }
    }
}

void mel_frames(const int16_t *pcm, int n_samples, float out[WN_NFRAMES][40]) {
    static float re[WN_FFT], im[WN_FFT];
    float mean = wn_feat_mean[0], std = wn_feat_std[0];
    int n_frames = (n_samples - WN_WIN) / WN_HOP + 1;
    if (n_frames > WN_NFRAMES) n_frames = WN_NFRAMES;
    for (int f = 0; f < n_frames; f++) {
        const int16_t *seg = pcm + f * WN_HOP;
        for (int i = 0; i < WN_WIN; i++) {
            re[i] = ((float)seg[i] / 32768.0f) * wn_window[i];
            im[i] = 0.0f;
        }
        memset(re + WN_WIN, 0, (WN_FFT - WN_WIN) * sizeof(float));
        memset(im + WN_WIN, 0, (WN_FFT - WN_WIN) * sizeof(float));
        fft512(re, im);
        for (int m = 0; m < 40; m++) {
            double acc = 0.0;                    // 双精度累加，压低与 numpy 的数值差
            for (int k = 0; k <= WN_FFT / 2; k++) {
                float p = re[k] * re[k] + im[k] * im[k];
                acc += (double)p * wn_mel_fb[k * 40 + m];
            }
            float v = ((float)log10(acc + 1e-8) - mean) / std;   // double log，对齐训练侧
            out[f][m] = v < -WN_FEAT_CLAMP ? -WN_FEAT_CLAMP : (v > WN_FEAT_CLAMP ? WN_FEAT_CLAMP : v);
        }
    }
    for (int f = n_frames; f < WN_NFRAMES; f++)   // 不足 1s 时补 0 特征
        memset(out[f], 0, sizeof(out[f]));
}
