// AFE 集成实测：乐鑫闭源 AFE（NS+VAD，WebRTC 内核）串在自研 wakenet 前面，
// 在 StickS3 上跑通整条链路并实测各环节耗时与总占空比。
//
//   合成音频(16k) → afe.feed → [NS降噪 + VAD] → afe.fetch → 增强音频
//                → 自研 mel_fbank → 自研 wn_forward → p(lumos)
//
// 关键点：
//   - wakenet_init=false：不用乐鑫唤醒词模型 → 不需要 srmodels 分区，默认分区表可烧
//   - aec_init=false：魔杖无回放，不需要回声消除
//   - ns/vad 用 WebRTC 内核（ns_model_name/vad_model_name=NULL）→ 同样不依赖模型分区
//   - 合成音频按实时节奏喂入（静音↔类语音↔噪声循环），占空比数字才有意义
//
// 组装/烧录：./build.sh
#include <Arduino.h>
#include "esp_afe_sr_iface.h"
#include "esp_afe_sr_models.h"
#include "wakenet.h"
#include "mel_fbank.h"

static const esp_afe_sr_iface_t *afe = nullptr;
static esp_afe_sr_data_t *afe_data = nullptr;
static int feed_chunk = 0;   // samples per feed (mono)

// 合成音频时间线：静音 1.5s → 类语音 2s → 白噪声 1s → 循环
static void synth_chunk(int16_t *buf, int n, int64_t sampleClock) {
    const int SR = 16000;
    int phase = (sampleClock / SR) % 4;             // 0..3s 循环
    bool speech = (phase == 1 || phase == 2);
    bool noise = (phase == 3);
    for (int i = 0; i < n; i++, sampleClock++) {
        double t = (double)(sampleClock % SR) / SR;
        int v = 0;
        if (speech) {
            double env = 0.5 * (1.0 + sin(2.0 * M_PI * 4.0 * (sampleClock % 4000) / 4000.0)); // 4Hz 音节包络
            v = (int)(6000 * env * (0.6 * sin(2 * M_PI * 700 * t) + 0.4 * sin(2 * M_PI * 1300 * t)));
        } else if (noise) {
            v = (esp_random() % 2400) - 1200;
        }
        buf[i] = (int16_t)v;
    }
}

void setup() {
    Serial.begin(115200);
    delay(1500);
    Serial.println("\n[AFE + wakenet 集成实测] ESP32-S3 @240MHz");

    Serial.printf("heap before: internal=%u psram=%u\n",
                  heap_caps_get_free_size(MALLOC_CAP_INTERNAL),
                  heap_caps_get_free_size(MALLOC_CAP_SPIRAM));

    // ---- AFE：NS(WebRTC) + VAD(WebRTC)，无 AEC/SE/AGC/WakeNet/模型分区 ----
    afe_config_t *cfg = afe_config_init("M", NULL, AFE_TYPE_SR, AFE_MODE_LOW_COST);
    cfg->aec_init = false;
    cfg->se_init = false;
    cfg->ns_init = true;
    cfg->afe_ns_mode = AFE_NS_MODE_WEBRTC;
    cfg->ns_model_name = NULL;
    cfg->vad_init = true;
    cfg->vad_model_name = NULL;   // NULL = WebRTC VAD（不依赖模型分区）
    cfg->wakenet_init = false;
    cfg->agc_init = false;
    cfg->memory_alloc_mode = AFE_MEMORY_ALLOC_MORE_PSRAM;

    afe = esp_afe_handle_from_config(cfg);
    afe_data = afe->create_from_config(cfg);
    afe_config_free(cfg);
    if (!afe_data) { Serial.println("[FATAL] AFE create failed"); return; }
    feed_chunk = afe->get_feed_chunksize(afe_data);
    Serial.printf("AFE init OK, feed chunk=%d samples (%.0f ms)\n",
                  feed_chunk, feed_chunk * 1000.0 / 16000);
    afe->print_pipeline(afe_data);

    Serial.printf("heap after AFE: internal=%u psram=%u\n",
                  heap_caps_get_free_size(MALLOC_CAP_INTERNAL),
                  heap_caps_get_free_size(MALLOC_CAP_SPIRAM));
    Serial.println("pipeline: synth -> AFE[NS+VAD] -> mel -> wakenet (实时节奏)\n");
}

// 1 秒滑窗缓存
static int16_t window16000[16000];
static int win_fill = 0;

void loop() {
    static int16_t chunk[1024];
    static int64_t sampleClock = 0;
    static uint64_t work_us = 0, real_us = 0, last_report = 0;
    static uint32_t n_feed = 0;
    static double feed_ms = 0, fetch_ms = 0;

    uint32_t t0 = micros();
    synth_chunk(chunk, feed_chunk, sampleClock);
    sampleClock += feed_chunk;

    uint32_t t1 = micros();
    afe->feed(afe_data, chunk);
    uint32_t t2 = micros();
    afe_fetch_result_t *res = afe->fetch(afe_data);
    uint32_t t3 = micros();

    if (res && res->data) {
        int got = res->data_size / 2;
        if (got > feed_chunk) got = feed_chunk;
        for (int i = 0; i < got; i++) {
            window16000[win_fill % 16000] = res->data[i];
            win_fill++;
        }
        // 每积累 1 秒新音频：mel + wakenet 整窗推理
        if (win_fill - last_report >= 16000) {
            last_report = win_fill;
            static float feats[WN_NFRAMES][40], probs[WN_CLASSES];
            // 重排环形缓冲为线性 1s 窗口
            static int16_t lin[16000];
            for (int i = 0; i < 16000; i++) lin[i] = window16000[(win_fill + i) % 16000];
            uint32_t m0 = micros();
            mel_frames(lin, 16000, feats);
            uint32_t m1 = micros();
            wn_forward(&feats[0][0], probs);
            uint32_t m2 = micros();
            Serial.printf("[%5.1fs] vad=%s p(lumos)=%.3f | feed %.2fms fetch %.2fms mel %.1fms wn %.1fms | work=%llums duty=%.0f%%\n",
                          win_fill / 16000.0,
                          res->vad_state == VAD_SPEECH ? "SPEECH" : "silence",
                          probs[0],
                          feed_ms / n_feed, fetch_ms / n_feed,
                          (m1 - m0) / 1000.0, (m2 - m1) / 1000.0,
                          (unsigned long long)(work_us / 1000),
                          100.0 * work_us / (real_us ? real_us : 1));
        }
        n_feed++;
        feed_ms += (t2 - t1) / 1000.0;
        fetch_ms += (t3 - t2) / 1000.0;
    }
    work_us += (t3 - t0);
    real_us += feed_chunk * (1000000LL / 16000);   // 本 chunk 的实时时长

    // 按实时节奏喂入（占空比 = work/real 才有意义）
    int32_t budget = feed_chunk * 1000000L / 16000;
    int32_t spent = micros() - t0;
    if (budget > spent) delayMicroseconds(budget - spent);
}
