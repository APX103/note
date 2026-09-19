// 本机对拍测试（macOS/Linux 编译运行，ESP32 上不需要此文件）：
//   ./wntest net test_features.txt test_expected.txt   — int8 前向 vs numpy 期望
//   ./wntest mel test_pcm.raw test_mel_expected.txt    — mel 前端 vs numpy 期望
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "wakenet.h"
#include "mel_fbank.h"

static int test_net(const char *feat_path, const char *exp_path) {
    FILE *f = fopen(feat_path, "r");
    if (!f) { perror(feat_path); return 1; }
    int T, M;
    if (fscanf(f, "%d %d", &T, &M) != 2 || T != WN_FRAMES || M != 40) {
        printf("特征维度不符: %d %d\n", T, M); return 1;
    }
    static int8_t q[40 * WN_T];
    for (int t = 0; t < T; t++)
        for (int m = 0; m < M; m++) {
            int v; fscanf(f, "%d", &v);
            q[m * WN_T + t] = (int8_t)v;
        }
    fclose(f);
    float probs[WN_CLASSES];
    wn_forward_q(q, probs);
    float exp[WN_CLASSES];
    f = fopen(exp_path, "r");
    for (int i = 0; i < WN_CLASSES; i++) fscanf(f, "%f", &exp[i]);
    fclose(f);
    float maxdiff = 0;
    for (int i = 0; i < WN_CLASSES; i++) {
        float d = probs[i] - exp[i];
        if (d < 0) d = -d;
        if (d > maxdiff) maxdiff = d;
    }
    printf("C    : %.6f %.6f %.6f\n", probs[0], probs[1], probs[2]);
    printf("numpy: %.6f %.6f %.6f\n", exp[0], exp[1], exp[2]);
    printf("net 对拍最大偏差 %g → %s\n", maxdiff, maxdiff < 5e-3 ? "PASS" : "FAIL");
    return maxdiff >= 5e-3;
}

static int test_mel(const char *pcm_path, const char *exp_path) {
    FILE *f = fopen(pcm_path, "rb");
    if (!f) { perror(pcm_path); return 1; }
    static int16_t pcm[16000];
    int n = (int)fread(pcm, sizeof(int16_t), 16000, f);
    fclose(f);
    static float feats[WN_NFRAMES][40], exp[WN_NFRAMES][40];
    mel_frames(pcm, n, feats);
    f = fopen(exp_path, "r");
    for (int t = 0; t < WN_NFRAMES; t++)
        for (int m = 0; m < 40; m++) fscanf(f, "%f", &exp[t][m]);
    fclose(f);
    float maxdiff = 0;
    for (int t = 0; t < WN_NFRAMES; t++)
        for (int m = 0; m < 40; m++) {
            float d = feats[t][m] - exp[t][m];
            if (d < 0) d = -d;
            if (d > maxdiff) maxdiff = d;
        }
    printf("mel 对拍 %d 样本 → 最大偏差 %g → %s\n", n, maxdiff, maxdiff < 0.05 ? "PASS" : "FAIL");
    // 顺跑一遍端到端
    float probs[WN_CLASSES];
    wn_forward(&feats[0][0], probs);
    printf("端到端(该 PCM) probs = %.4f %.4f %.4f\n", probs[0], probs[1], probs[2]);
    return maxdiff >= 0.05;
}

int main(int argc, char **argv) {
    if (argc == 4 && !strcmp(argv[1], "net")) return test_net(argv[2], argv[3]);
    if (argc == 4 && !strcmp(argv[1], "mel")) return test_mel(argv[2], argv[3]);
    printf("用法: %s net|mel <输入> <期望文件>\n", argv[0]);
    return 2;
}
