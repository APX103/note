# Hi3322（谛听 HiDiTing V100）开发板调研索引

> 调研日期：2026-09-08 · 适用硬件：华为海思 Hi3322 穿戴开发板（速智达 HY601M / 润开鸿 HH-HSP500 等）
> 结论一句话：这是海思"谛听"轻智能穿戴方案的开发平台，跑穿戴级 OpenHarmony，带 50 GOPS NPU；官方工具链 Windows 优先、Linux 次之、macOS 为零，但 Mac 可以覆盖约 90% 的开发环节（编译走 Docker，烧录借 Windows）。

> **⚠️ 2026-09-18 更新：上文"macOS 为零 / 编译走 Docker / 烧录借 Windows"的结论已过时。**
> 官方自工具链 **V26.08.1**（2026-09 初）起提供毕昇编译器 darwin-arm64 包、hs-flash darwin-universal2 烧录器，SDK 构建脚本补齐 darwin 分支并内置 mac 通用签名/压缩工具——Apple Silicon Mac 可**原生编译 + 原生烧录**，无需 Docker/Windows。同时官方 `fbb` CLI 明确面向 AI Agent 设计（JSON 契约 + gdb agent 模式）。
> 详见同目录 [fbb-cli-mac-research.html](fbb-cli-mac-research.html)。本页其余芯片/板卡/资料信息仍有效。

---

## 目录

1. [芯片与方案定位](#1-芯片与方案定位)
2. [开发板形态](#2-开发板形态)
3. [官方资料入口（总索引）](#3-官方资料入口总索引)
4. [三条开发路线](#4-三条开发路线)
5. [完整工具链条：写码 → Lint → 编译 → 上片 → 调试](#5-完整工具链条)
6. [Mac（ARM64）适配结论](#6-macarm64-适配结论)
7. [已知坑与 FAQ](#7-已知坑与-faq)
8. [推荐上手顺序](#8-推荐上手顺序)
9. [能做出什么东西](#9-能做出什么东西)

---

## 1. 芯片与方案定位

**Hi3322 = 上海海思"谛听"（DiTing / HiDiTing V100）轻智能穿戴一体化 SoC**，固件名 `diting-community`，方案代号 W620（2025 年迭代；前代 W610 对应 Hi3321）。

| 项目 | 规格 |
|---|---|
| CPU | 双 RISC-V 核：BCPU ≤64MHz + MCPU ≤266MHz |
| AI | Nano NPU，50 GOPS，端侧本地推理 |
| 连接 | LTE Cat.1（FDD B1/B3/B5/B8、TDD B34/B38/B39/B40/B41）、单频 GNSS、星闪 SLE 2.0（16Mbps 双向）、蓝牙 2.1+EDR ~ 5.4 |
| 显示 | MIPI / QSPI，最大 600×600，仿 3D GPU，60fps，H.264 硬解 |
| 摄像头 | 预留 VICAP 接口 |
| 音频 | AMIC 输入、预留 DMIC、HeadSet 差分接模拟 PA |
| 存储 | 2.3MB SRAM + 16MB PSRAM；外挂 WSON/WLCSP Nor Flash、Nand Flash |
| 电源 | 电池 + Charger 接口，待机 <180µA |
| 封装 | LGA 144（约 23.0 × 18.3 × 2.0 mm），模组形态 Hi2131E |
| OS | LiteOS（默认）/ OpenHarmony 双系统，JS/Native 双引擎 |

完整方案 = Hi3322 主控 + 4G Cat.1 + GNSS 套片，定位"一站式鸿蒙蜂窝表芯"；落地案例含两轮车仪表。

参考：
- 官方文档库 [HiDiTing 开发者中心](https://docs.hisilicon.com/projects/hs-fbb/master/)
- [海思智能表芯方案页](https://www.hisilicon.com/cn/scenario/e-consumer/smart-wearable/smart-watch)
- [芯查查 Hi3322 方案页（萤火工场）](https://www.xcc.com/lesson/programme/55364)
- [IT之家：谛听 W620 方案报道](https://www.ithome.com/0/899/295.htm)
- [腾讯新闻：谛听方案两轮车案例](https://news.qq.com/rain/a/20260622A0D6MC00)

## 2. 开发板形态

社区生态公开的开发板（[ohos_diting README](https://gitee.com/HiSpark/ohos_diting) 有淘宝购买链接）：

| 开发板 | 厂商 | 备注 |
|---|---|---|
| SZD_DEV_KIT_HY601M_V1.0 | 速智达 | ohos_diting 主文档基于此板；配 USB 串口调试线 + Type-C 线 |
| HH-HSP500 | 润开鸿 | 另一块官方推荐板 |

- 板卡硬件细节（接口、拨码、屏幕、烧录接线）见文档库"硬件指南 → 社区开发板使用指南"
- 海思社区论坛"谛听穿戴"专区另有 "Nano 开发板介绍及教程资料" 帖：https://developers.hisilicon.com/forum/0102108098553062001
- 拿到板子第一件事：核对丝印确认型号

## 3. 官方资料入口（总索引）

| 资源 | 链接 | 说明 |
|---|---|---|
| **总文档库** | https://docs.hisilicon.com/projects/hs-fbb/master/ | HiDiTing 开发者中心：快速入门、22 篇外设驱动案例、OS/AT/表盘/JS 应用指南、API 参考（30+ 模块）、硬件指南、工具中心、FAQ |
| **SDK 源码仓** | https://gitcode.com/HiSpark/hs-fbb | C 为主，基于 OpenHarmony 5.1；License 非标准开源协议，商用前确认 |
| **Docker 环境仓** | https://gitcode.com/HiSpark/hispark-docker | 官方编译镜像 `ubuntu22.04_dt_env.tar`；需 gitcode 账号 + git-lfs |
| **fbb CLI 引导** | `curl -fsSL https://dl.hispark.hisilicon.com/bootstrap.sh \| sh`（Linux）/ `irm https://dl.hispark.hisilicon.com/bootstrap.ps1 \| iex`（Win） | 一站式 CLI：装 SDK、编译、烧录、monitor |
| **BurnTool 文档/源码** | https://docs.hisilicon.com/repos/fbb_burntool/zh-CN/master/ · https://gitcode.com/HiSpark/fbb_burntool | 可视化烧录工具，Qt 编写，Apache-2.0 开源 |
| **ToolChain 文档** | https://docs.hisilicon.com/repos/fbb_toolchain/zh-CN/master/ | ARM GCC 使用指南（注：谛听实际用毕昇编译器，见 Docker 路线） |
| **HiSpark AI 文档** | https://docs.hisilicon.com/repos/hispark_ai/zh-CN/master/ | NPU/AI 全流程：AMCT 量化、ATC 转换、HiSpark Studio AI 插件 |
| **JS 应用/表盘仓** | https://gitee.com/HiSpark/ohos_diting | 预编译镜像 + JS 示例 + 表盘脚本（表盘协议 1.0） |
| **HiSpark 组织（Gitee）** | https://gitee.com/HiSpark | fbb_ws63、ohos_ws63、ModelZoo 等 28 仓；fbb 系陆续迁往 gitcode.com/HiSpark |
| **海思社区** | https://developers.hisilicon.com/ | 开发中心（SDK 发布包下载）、论坛谛听穿戴专区 |
| **芯课堂** | https://www.hisilicon.com/cn/chip-academy/materiallist | 硬件/SDK/工具资料下载 |
| **穿戴应用市场** | https://www.openwearplay.com/ | 北向应用市场，表盘/应用上架渠道 |
| **DevEco Studio** | https://cn.devecostudio.huawei.com/ | JS 应用开发 IDE，有 macOS ARM64 原生版 |
| **HiSpark Studio** | https://developers.hisilicon.com/cn/developertool | 官方一站式 IDE（VS Code 扩展形态），**仅 Windows 10/11 64 位**；开源于 https://gitcode.com/HiSpark/vscode-hispark-studio-extension |

## 4. 三条开发路线

| 路线 | 内容 | 写码工具 | 产物 | 上片方式 |
|---|---|---|---|---|
| **A. 固件/C** | 外设驱动、Native 组件、系统定制 | VS Code + clangd | `diting-community.fwpkg` | BurnTool / USB DFU 整包烧录（低频） |
| **B. JS 应用/表盘** | 手表应用、3D 表盘（日常迭代主力） | DevEco Studio（Mac ARM64 可用） | `xxx.bin` | DebugKits 推文件 + AT 命令安装（不重烧固件，热迭代） |
| **C. AI 模型** | 唤醒词/命令词/降噪/手势/健康监测 | VS Code + HiSpark Studio AI 插件 | 量化后的 exeom 离线模型 | 随应用打包走 B 路线 |

关键认知：**固件只需烧一次，日常开发 90% 是 B 路线的"推文件 + AT 安装"**。

## 5. 完整工具链条

### 5.1 写码

- **C**：clone `hs-fbb`，照文档库"参考案例 → 外设驱动"（adc/audio/can/display/dma/flash/gpio/i2c/key/pwm/qspi 屏适配/rtc/sdio/uart/usb/watchdog…22 篇）和 API 参考写。示例工程用 `fbb create-project-from-example` / `fbb list-examples`。
- **JS 应用**：《OpenHarmony JS 应用开发指南》（工程结构/生命周期/组件/系统接口/发布）+ HelloWorld 入门指南 + UIKit 表盘开发指南，均在总文档库。JS 示例另见 ohos_diting 仓 `src/application/wearable/jsapp/acts_validator`。
- **AI**：HiSpark AI 快速入门，LeNet5/MNIST 全流程样例。

### 5.2 Lint / 格式化（官方无专用工具，标准做法）

- C：`.clang-format` + clangd（CMake 系可生成 `compile_commands.json`）、clang-tidy / cppcheck
- JS：eslint + prettier
- 全部跨平台，Mac 原生可用

### 5.3 编译

**方式一：fbb CLI（官方主推，Windows/Linux）**

```bash
# 安装（自动装 uv + fbb-cli + fbb setup）
curl -fsSL https://dl.hispark.hisilicon.com/bootstrap.sh | sh    # Linux
fbb doctor                        # 验证环境
fbb sdk install hs-fbb@master     # 拉 SDK（--dir 指定路径）
fbb build pack_diting_community   # 编译社区固件（--clean 全量重编）
fbb build pack_diting_community_bike  # 行车形态固件
```

其他常用：`fbb menuconfig <target>`（Kconfig 图形配置）、`fbb config get/set`（CI 用）、`fbb list-targets / set-target`、`fbb create-project / create-component`。

**方式二：Docker 容器（Mac 的编译入口）**

```bash
git clone https://gitcode.com/HiSpark/hispark-docker.git   # 需 gitcode 账号 + git-lfs
docker load -i ubuntu22.04_dt_env.tar    # 镜像: swr.cn-north-4.myhuaweicloud.com/hispark_docker/ubuntu22.04_dt:env
# 容器内：
git clone https://gitcode.com/HiSpark/hs-fbb.git && cd hs-fbb
python3 src/tools/bin/fbb_tool/install_bisheng.py --root src \
  --config src/build/config/target_config/3322/3322.json --platform linux   # 毕昇编译器
cd src && ./build.py pack_diting_community
# 产物：output/3322/fwpkg/diting-community.fwpkg
```

- 构建体系：Python（统筹/签名合并）+ CMake + Kconfig；编译器为华为毕昇
- `install_bisheng.py` 会按**当前 Linux 架构**从 `tools.json` 选包 → 若有 aarch64 包，Apple Silicon 可原生编译（待验证，拿到 SDK 后第一件事翻 tools.json）
- `config.py` 里把 target 的 `fs_image` 设 True 可额外产出 `file.bin` 资源镜像（仅 Docker 环境支持）
- 官方 WSL_Docker 指南见文档库"快速入门 → WSL_DOCKER 环境使用指南"

**方式三：HiSpark Studio**（Windows 专用，一键编译烧录调试）

**JS 应用编译**：DevEco Studio 内构建，产出 `entry-default-unsigned.bin`；需配置 `image_converter_tool` 环境变量（工具位于 ohos_diting `src/tools/bin/graphic_tools/`）。

### 5.4 上片（烧录）

| 场景 | 工具 | 参数 |
|---|---|---|
| 整包固件（GUI） | BurnTool 26.03.3（Windows） | 芯片选 Hi3322，烧写串口，波特率 750000，自动烧写 |
| 整包固件（USB 加速） | USB DFU | 先发 `AT+USBDFUTRIGGER`，VID=0x3361 / PID=0x3322 |
| 整包固件（CLI） | `fbb flash -f xxx.fwpkg --chip 3322 -d`（USB，推荐）；`-p COM3 --manual-reset --timeout 600`（串口，需断电重上电） | Linux 仅串口方式 |
| 应用/表盘推送 | DebugKits（HiSpark Studio 内打开，Windows） | T3 口，921600 波特率；推到 `/user/helloworld.bin`、表盘 `/user/dial/`（路径固定） |
| 应用安装 | 串口 AT 命令 | `AT+OHOS=OHOSFWK_BM_INSTALL,/user/helloworld.bin`；双击电源键进 APP 列表 |
| 应用卸载/查询 | AT 命令 | `AT+OHOSFWK_BM_GET_APPLIST` 查包名 → `AT+OHOSFWK_BM_UNINSTALL,<包名>`；可选关签名校验 `AT+OHOSFWK_BM_SET=disable` |

注意：不同文档版本的 AT 前缀写法有差异（`AT^...` vs `AT+OHOS=...`），以最新 HiDiTing 文档库《AT 指令使用指南》为准。

### 5.5 调试

| 层级 | 工具 | 说明 |
|---|---|---|
| 串口日志 | `fbb monitor --port <口> --baud <率> --until <正则> --log` | CLI 自带；或 SSCOM 连 T2 口 750000 |
| 文件/寄存器级 | DebugKits | T3 口 921600：日志 + 寄存器读写 + 文件推送，排查外设主力 |
| GDB | HiSpark Studio GDB Launch/Attach（**仅 Windows**） | 配 JLink 类调试器 |
| 专项 | 音频/图形驱动调试指南、DFX 工具、产测工具 | 见文档库"工具中心" |

## 6. Mac（ARM64）适配结论

官方支持：HiSpark Studio 仅 Windows 10/11 64 位（烧录/调试功能标注"仅 Windows"）；fbb CLI 跨 Windows/Linux；无任何 macOS 支持。社区 hispark-rs（Rust 工具链、烧录器、QEMU）只覆盖 WS63/BS2X，不支持 Hi3322。

| 环节 | Mac 可行性 | 方案 |
|---|---|---|
| 写码（C/JS/AI） | ✅ 原生 | VS Code + clangd；DevEco Studio 有 macOS ARM64 原生版 |
| Lint | ✅ 原生 | clang-format/clang-tidy/eslint/prettier |
| 固件编译 | ✅ Docker | 官方 ubuntu22.04_dt 镜像，amd64 走 Rosetta 2；若毕昇有 aarch64 包则原生速度（待验证 tools.json） |
| AI 工具链 | ✅ Docker | HiSpark AI 的 CANN 镜像/WSL 包，同样容器化跑 |
| 固件烧录 | ⚠️ 无官方 Mac 工具 | 首选：UTM 装 Win11 ARM64 跑 BurnTool/HiSpark Studio（Prism 转译 x64，USB 串口可直通）；野路子：fbb-cli 本体是 Python 包（uv 安装，烧录走串口/USB DFU）可尝试 Mac 直跑；BurnTool 开源（Qt/Apache-2.0）可自行编译 |
| 应用/表盘推送 | ⚠️ 同上 | DebugKits 是 Windows GUI；或逆向其串口推送协议（921600） |
| 串口 AT/日志 | ✅ 可行 | screen/minicom/picocom 发 AT；`fbb monitor` 若能装也可用 |

**推荐组合：Mac 干写码/lint/编译/日志（约 90%）+ 一台 Windows（实体或 UTM 虚拟机）干烧录和 DebugKits 推送（约 10%）。**

本机环境（2026-09 核查）：Apple Silicon · macOS 26.5 · Docker 29.4.3 ✅ · Python 3.9 · VS Code ✅ · 未装 DevEco Studio。

## 7. 已知坑与 FAQ

- 调试报 "The board does not respond!"（DebugKits/工具连不上板）→ 板子进了低功耗模式，串口发 `AT^PM=0` 关闭后重试
- SDK / 工程路径**不能含空格和中文**；工程名不能含中文和特殊符号
- Windows 杀毒软件可能拦截工具链（报 access denied）→ 加白名单
- Linux 串口烧录需 `sudo usermod -aG dialout $USER`
- 端侧推理时间异常 → 检查单板日志等级设置
- 整包固件串口烧录较慢（老文档约 30 分钟），优先 USB DFU
- 烧录/调试波特率以最新文档为准：BurnTool/SSCOM（T2 口）750000，DebugKits（T3 口）921600；旧 ohos_diting README 写的 500000 是老版本数值
- 表盘 SDK 目前仅支持协议 1.0；协议 2.0 见 cooperation-team-L0UI/watch_face
- fbb 系仓库正从 Gitee 迁往 gitcode.com/HiSpark，两边都找找

## 8. 推荐上手顺序

官方文档建议路径：

1. 确认硬件（核对板卡型号、接线、拨码）
2. 搭环境（CLI 优先：`bootstrap` → `fbb doctor`）
3. 烧写 26.08.1 发行版固件验证板子
4. 跑通 HelloWorld 应用（`fbb list-examples` → 创建 → 编译 → DebugKits 推送 → AT 安装 → 双击电源键查看）
5. 按业务选示例（外设 22 篇 / JS 应用 / AI 语音 Demo）
6. 查 API 参考（驱动 30+ 模块、OSAL、POSIX、蓝牙/星闪、图形 60+ UI 组件、媒体 TTS/ASR）
7. 用工具中心（DebugKits/DFX）定位问题

Mac 用户的增量步骤：

- 先 clone `hispark-docker` + `hs-fbb`，翻 `tools.json` 确认毕昇编译器有无 aarch64-linux 包 → 决定 Docker 原生/模拟
- 准备一台 Windows（或 UTM Win11 ARM VM）专管 BurnTool 烧录 + DebugKits 推送
- 表盘脚本（ohos_diting `dial_converter_tool`）确认是否纯 Python → 是则 Mac 直接跑

## 9. 能做出什么东西

按投入由浅入深：

1. **表盘 + JS 轻应用**：天气/时钟/运动表盘、快捷卡片；成品可上架 [openwearplay.com](https://www.openwearplay.com/)（开源鸿蒙穿戴应用市场，首批 40+ 应用）
2. **端侧 AI**（50 GOPS NPU）：语音唤醒/自定义命令词、通话降噪、手势识别、心率异常检测；AMCT 量化（PTQ/QAT）→ NPU 部署，数据不出设备
3. **星闪应用**：星闪音频（Hi-Res/Audio Vivid 无损）、数字车钥匙（案例精度 0.6m）、与鸿蒙设备分布式互联
4. **多媒体设备**：MIPI/QSPI 屏 UI、H.264 硬解视频播放、VICAP 摄像头
5. **独立蜂窝穿戴**：4G Cat.1 + GNSS → 独立通话手表、儿童/老人定位表、两轮车仪表（谛听商业主线）

---

*本索引由调研整理（信息截至 2026-09-08），以官方文档库 <https://docs.hisilicon.com/projects/hs-fbb/master/> 为最终权威。*
