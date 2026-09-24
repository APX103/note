# 软件定义无线电工程师读本

> 本书是 *Software-Defined Radio for Engineers*（Travis F. Collins, Robin Getz, Di Pu, Alexander M. Wyglinski 著，Artech House 2018，ISBN-13: 978-1-63081-457-1）的中文学习译本。原书由 Analog Devices（ADI）以永久电子书许可在其官网免费分发，配套硬件为 ADALM-Pluto SDR。
>
> ⚠️ **版权与用途说明**：原书为 Artech House 版权作品，本译本仅为个人学习研究用途的笔记整理，不替代原书；请勿用于商业用途或公开再分发。翻译以"通顺可读"为先，技术术语尽量遵循国内通行译法，并保留必要的英文原词。

## 原书信息与获取

- 原书页面：<https://www.analog.com/en/resources/technical-books/software-defined-radio-for-engineers.html>
- 原书 PDF（英文原版）已批量下载至本书目录下的 `pdf/`（已 gitignore，不入库）：整本书 `SDR4Engineers.pdf`（375 页）+ 11 章分章 PDF + 4 个附录 PDF。
- 重新下载方法见 `tools/download_pdfs.sh`。

## 全书结构（按原书目录）

- [第 1 章　软件定义无线电导论](./Chapter_01_软件定义无线电导论.md) ✅ 已译
- 第 2 章　信号与系统（Signals and Systems）⏳ 待译
- 第 3 章　通信中的概率（Probability in Communications）⏳ 待译
- 第 4 章　数字通信基础（Digital Communications Fundamentals）⏳ 待译
- 第 5 章　理解 SDR 硬件（Understanding SDR Hardware）⏳ 待译
- 第 6 章　定时同步（Timing Synchronization）⏳ 待译
- 第 7 章　载波同步（Carrier Synchronization）⏳ 待译
- 第 8 章　帧同步与信道编码（Frame Synchronization and Channel Coding）⏳ 待译
- 第 9 章　信道估计与均衡（Channel Estimation and Equalization）⏳ 待译
- 第 10 章　正交频分复用（Orthogonal Frequency Division Multiplexing）⏳ 待译
- 第 11 章　SDR 的应用（Applications for Software-Defined Radio）⏳ 待译
- 附录 A　更长的通信史 / 附录 B　MATLAB 与 Simulink 入门 / 附录 C　均衡器推导 / 附录 D　三角恒等式 ⏳ 待译

## 译本工作流（每章通用）

1. `python3 tools/extract_figures.py pdf/SDR4Engineers_CH01.pdf 1 images/` —— 从原书 PDF 提取插图与英文题注（`images/captions_01.tsv`）；
2. 横躺（原书旋转 90° 排版）的插图用 `sips -r 90 images/fig_XXXX.png` 转正；
3. 按 PyMuPDF 提取的章节文本（`doc[p].get_text('text', sort=True)`）翻译成 `Chapter_XX_*.md`，插图以 `![](images/fig_XXYY.png)` 原位嵌入；
4. `python3 build.py` —— Pandoc + Tectonic 编译成 PDF 成书。

## 编者

**李佳伦**　译。基于 ADI 官网免费分发的英文原版 PDF 翻译整理，插图取自原书。
