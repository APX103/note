# 自研迷你唤醒词引擎（WakeNet 复刻）

魔杖项目 `magic-wand/` 的语音唤醒模块：**不依赖乐鑫收费定制服务，自己造唤醒词模型**。
照 WakeNet 公开文档的配方（log-mel/MFCC 特征 + 小型量化 CNN + 多帧平滑触发）实现完整链路：
数据合成 → 训练 → int8 量化 → 纯 C 运行时，目标词暂定 **"Lumos"**。

## 实测指标（2026-09-19，Mac 本机）

| 指标 | 数值 | 说明 |
|---|---|---|
| 参数量 | 33,075（int8 权重 ~33KB） | 深度可分离卷积 ×3 + GAP + FC |
| 验证集 int8 准确率 | **96.2%** | 验证集 = 完全留出的 2 个语音（Daniel/Tessa），说话人无关 |
| 正样本召回（thr=0.5） | **30/30 = 100%** | held-out 语音说 "lumos" |
| unknown 误判 | 8/432 clips | 易混词（music/luminous/hocus pocus…） |
| 误报流测试 | 160s 负样本流，p>0.9 命中 3 窗 | 单窗尖峰，经 `wn_trigger` 平滑后基本消除 |
| C ↔ numpy 对拍 | 前向偏差 1.2e-07（逐位一致） | 整数累加 + 相同 requant 语义 |
| mel 前端对拍 | 最大偏差 3.4e-05 | FFT/滤波器组与训练侧对齐 |
| 端到端（PCM→概率） | 正样本 p(lumos)=0.984 | esp32/ 对拍程序实测 |

诚实声明：正样本全部来自 macOS `say` 合成（9 语音 × 5 语速 × 3 语气），**真实人声未验证**——
把你的录音放进 `data/raw/mylumos/*.wav` 重跑一遍即可混训。安静房间玩具场景够用。

## 目录

```
wakenet/
├── scripts/
│   ├── record.py       # ⓪ 按空格录音：真声正样本/负样本采集器（可选）
│   ├── synthesize.py   # ① macOS say 合成正/负样本（缓存，重跑只补新增）
│   ├── make_dataset.py # ② 整理成 1s 定长数据集 + 说话人无关验证集切分
│   ├── train.py        # ③ 训练：50ep 常规 + 20ep QAT（量化感知）+ 最优checkpoint
│   └── export_c.py     # ④ int8 逐通道量化 + 生成 C 头文件和对拍文件
├── esp32/              # 纯 C 运行时（无依赖，可直接进 ESP32 工程）
│   ├── wakenet.h/.c    # int8 前向 + 滑窗平滑触发器
│   ├── mel_fbank.h/.c  # PCM → log-mel（512点FFT + 40 mel）
│   ├── wakenet_model.h # 自动生成：权重/scale/滤波器组
│   └── test_main.c     # 本机对拍（ESP32 上不要编译此文件）
├── data/  models/      # 生成物（63MB 音频可随时删，重跑可再生）
└── .venv/              # torch + numpy（record.py 另需 sounddevice）
```

## 复现全流程

```bash
cd magic-wand/wakenet
.venv/bin/python scripts/synthesize.py    # ~2min，1719 条
.venv/bin/python scripts/make_dataset.py  # 秒级
.venv/bin/python scripts/train.py         # ~12min（M 系列 CPU）
.venv/bin/python scripts/export_c.py      # ~1min
cd esp32 && clang -O2 -o /tmp/wntest wakenet.c mel_fbank.c test_main.c -lm
/tmp/wntest net test_features.txt test_expected.txt
/tmp/wntest mel test_pcm.raw test_mel_expected.txt
```

## 换唤醒词 / 加自己的声音

- 换词：改 `synthesize.py` 的 `POS_TEXTS`（英文短词效果最好），删 `data/raw/` 重跑。
- 加真声：`.venv/bin/pip install sounddevice` 后用采集器（空格开始/停止，一条一文件，
  实时电平条 + 远/正常/近音量分桶统计，提醒你换距离换音量）：
  ```bash
  .venv/bin/python scripts/record.py --goal 50        # 正样本 → data/raw/mylumos/
  .venv/bin/python scripts/record.py --dir data/raw/unknown \
      --tag chat --chunk 2                            # 负样本：日常聊天，长录自动切 2s
  .venv/bin/python scripts/record.py --test           # 先自检 1 秒 + 回放
  ```
  数量参考：个人用 50~100 条真声正样本足够（多样性 > 数量：0.3~3m 距离、正常/大声/耳语、
  安静/有背景音都覆盖）；负样本随手录几十分钟日常中文聊天即可。
  然后 `make_dataset.py && train.py && export_c.py`。注意留 5~10 条不放进 `mylumos/` 做真机验收；
  录到 `unknown/` 的文件名首段会被当作"说话人"，别用 Daniel/Tessa 开头的 tag。
- 训练按"说话人"切验证集（留出 Daniel/Tessa 两个语音），指标不会因数据泄漏虚高。

## ESP32 端集成（三步）

```c
#include "wakenet.h"
#include "mel_fbank.h"

static float feats[WN_NFRAMES][40];
static wn_trigger_t tg;

void app_main(void) {
    wn_trigger_init(&tg, /*avg_n=*/4, /*thr=*/0.7f);   // 连续4窗均值>0.7才触发
    // 音频任务以 16kHz 喂环形缓冲；每 0.3s 取最近 1s 判一次：
    mel_frames(pcm_1s, 16000, feats);
    float probs[3];
    wn_forward(&feats[0][0], probs);                   // [lumos, unknown, noise]
    if (wn_trigger_update(&tg, probs[0])) { /* 点亮魔杖! */ }
}
```

资源占用：静态缓冲 ~13KB（两层激活 ping-pong）+ 权重 33KB（放 flash）。
单次推理在 ESP32-S3 @240MHz 估计 <50ms（本机 clang -O2 实测 <10ms）。

## 踩坑记录（对后人有用）

1. **类不均衡直接训会塌成"全判 unknown"**——必须按类加权采样 + 按验证召回挑 checkpoint。
2. **训练增广是随机流，run 间方差很大**——用"验证集 score 最优 checkpoint 回滚"消灭方差，
   score = 召回 − 2×unknown误报。
3. **float 模型直接量化精度从 99% 崩到 81%**——判定边距太薄，requant 取整噪声累积翻转临界
   样本。用 QAT（伪量化 + STE 直通梯度）微调后 int8 回到 96.2%。
4. **mel 对拍对不上（稳定 0.07）**——不是 FFT 精度问题，是期望值用 float 波形、C 端吃 int16
  PCM 的量化往返差。设备端输入本来就是 int16，期望值必须按 int16 往返算。
5. **唤醒词模型的对拍要共享同一套标定 scale**——训练 QAT 用的激活 scale 存进 stats.json，
   导出直接读同一份，两边永远一致。

## 下一步（可选）

- [ ] 用真机录音（`mylumos/`）混训，验证真声召回
- [ ] StickS3 上板：I2S/PDM 采音 + 本目录 esp32/ 三文件直编
- [ ] 加 VAD/能量门控：静音时不跑推理（魔杖唤醒后才激活，功耗无所谓，可跳过）
