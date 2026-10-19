# MP3 → MusicXML 吉他六线谱 Demo

一个最小可用的自动扒谱示例：输入一段吉他音频（mp3/wav/flac），输出带弦/品位标注的 MusicXML，可用 MuseScore / Guitar Pro 打开查看六线谱。

## 安装

```bash
cd other/guitar-transcription-demo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> `basic-pitch` 会下载一个约 30–50 MB 的预训练模型，首次运行时需要联网。

## 使用

```bash
python transcribe.py input.mp3 -o out.musicxml --bpm 120
```

参数说明：

| 参数 | 默认值 | 说明 |
|---|---|---|
| `input` | - | 输入音频文件 |
| `-o, --output` | `output.musicxml` | 输出文件路径 |
| `--bpm` | `120` | 目标拍速，影响节奏量化 |
| `--confidence` | `0.3` | 音符置信度阈值，过滤低置信度检测 |
| `--max-fret` | `24` | 吉他最大品位数；古典吉他可设 `19` |

## 流程

1. **音频 → MIDI 音符事件**：使用 Spotify 开源的 `basic-pitch` 做多音高检测。
2. **音符 → 吉他位置**：根据标准调弦 E–A–D–G–B–E，为每个音高找出所有可行弦/品。
   - 同时发声的音符合并成和弦，用回溯搜索做弦/品分配。
   - 优化目标：相邻和弦手型跳变最小、同一和弦内品位跨度合理、避免过高把位。
3. **节奏量化**：按指定 BPM 把音符起止时间对齐到 16 分音符网格。
4. **生成 MusicXML**：直接写出带 `<technical><string/><fret/></technical>` 标签的六线谱 XML，`music21` 只用来把 MIDI 转成音名/八度。

## 直接渲染 PNG 六线谱

不依赖 MuseScore，用 `render_tab.py` 把 MusicXML 画成 PNG：

```bash
DYLD_LIBRARY_PATH=/opt/homebrew/lib python render_tab.py out.musicxml -o tab.png --max-measures 50
```

> macOS 需要 `DYLD_LIBRARY_PATH=/opt/homebrew/lib` 才能让 `cairosvg` 找到系统 cairo 库。

## 限制

- 这是** demo 级别**的实现，不是工业级扒谱软件。
- 复杂和弦、快速连音、背景噪音、多乐器混合都会显著降低准确率。
- 同一时刻若多个音落在同一根弦上，会在和弦分配阶段尽量避免；无法避免时丢弃冲突音符。
- 输出后建议用制谱软件人工校对、修正节奏与把位。

## 参考

- [basic-pitch](https://github.com/spotify/basic-pitch)
- [music21](https://web.mit.edu/music21/)
- Wiggins & Kim, [*Guitar Tablature Estimation with a Convolutional Neural Network*](https://archives.ismir.net/ismir2019/paper/000033.pdf), ISMIR 2019 — 用 CNN 直接从音频预测弦/品（TabCNN）。
- Simionato et al., [*Playability-Aware Audio-to-Tablature Guitar Transcription via Diffusion Models*](https://arxiv.org/abs/2608.30854), arXiv 2026 — 用扩散模型 + 可演奏性约束做 audio-to-tab。
