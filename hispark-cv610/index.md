# HiSpark CV610（海思 Hi3516CV610 · Sunniwell 生态板）开发调研索引

> 调研日期：2026-09-09 · 适用硬件：Sunniwell CV610 DevBoard（HiSpark 生态板，gitcode 仓 [hi_aiot_solution_cv610_ev_board](https://gitcode.com/HiSpark/hi_aiot_solution_cv610_ev_board)）
> 结论一句话：SoC 是**海思 Hi3516CV610**（双核 A7@950MHz + 1T NPU + 128MB DDR3，Linux 5.10 / OpenHarmony 6.1 双系统）；板子**出厂自带可跑系统**，Demo 开箱即验；编译走 `repo` 多仓 + `build.sh`（CMake+Kconfig）；**官方对 macOS 零支持**（工具链仅 x86_64 Linux 二进制，官方 Docker 镜像仅 amd64），Mac 的可行解 = Docker Desktop(Rosetta 2) 跑官方 wukun 镜像编译 + Mac 原生串口/TFTP；「AI 小智」集成高度可行——仓库自带的 `agent_audio_sample` 已完成约 70% 底座（唤醒/VQE/Opus/播放/云 provider 抽象），补一个小智协议 provider 即可，差异化方向是 **4MP 摄像头 + NPU 做"带视觉的小智"**。

---

## 目录

1. [芯片与板卡定位](#1-芯片与板卡定位)
2. [官方资料入口](#2-官方资料入口)
3. [构建体系与工具链](#3-构建体系与工具链)
4. [烧录与调试](#4-烧录与调试)
5. [Demo 跑通路径](#5-demo-跑通路径)
6. [Mac（ARM64）适配结论](#6-macarm64-适配结论)
7. [AI 小智集成方案](#7-ai-小智集成方案)
8. [已知坑与 FAQ](#8-已知坑与-faq)
9. [推荐上手顺序](#9-推荐上手顺序)

---

## 1. 芯片与板卡定位

**「CV610」= 华为海思 Hi3516CV610**（板上打标 Hi3516CRNCV610-20S），面向消费类市场的融合视觉计算芯片；Sunniwell（盛思瑞）只是生态板卡厂。芯片体系里 CV610 是海思 edge-AI 序列最小档（1 TOPS），同线还有 3403/3591 等。

| 项目 | 规格 | 出处口径 |
|---|---|---|
| CPU | ARM Cortex-A7 MP2 @ 950MHz（⚠️ 官方接口表一处写"单核"，两处矛盾，以 MP2 为准；不影响工具链选型） | 硬件指南 L39/L166 |
| NPU | 1 TOPS（海思官网口径，第二手；SDK 内为 AIComponent/IVE 子 SDK，有目标检测/人脸识别示例） | 海思官网 |
| 内存 | 内置 128MB DDR3 | 硬件指南 |
| 编码 | H.265/H.264（二手口径 4K@20fps / 6M@30fps；精确参数表属 NDA） | CSDN/迅为 |
| OS | Linux 5.10（主线）/ OpenHarmony 6.1（另条构建线） | README |
| 存储 | SPI NAND 256MB（默认）/ SPI NOR 32MB / eMMC 8GB（SD 卡槽接入） | 硬件指南 |

**生态板组成**（主板 + 扩展板按需组合）：

- **主板**：2×MiPi 2Lane 摄像头 FPC（可电阻改 4Lane）、RJ45 100M（烧录/调试用）、Type-C USB2.0、Type-C Debug UART（CH343P，**115200**）、Type-C 供电 5V/2A、**板载左右声道模拟硅麦 ×2 + 内置 acodec**、模拟音频输出、**喇叭接口 J47（8Ω/2W）**、音频回采口 J21、TF 卡槽、40PIN GPIO（3.3V）、JTAG 引出（配 RealView-ICE，日常不需要）
- **WiFi 板 WSx3**（二选一）：WS53 低功耗 / WS73 常电（Hi3873 模组，WiFi6 + BLE + **SLE 星闪**），板载 ES7210L ADC + 2 模拟硅麦 + 回采
- **4G Cat1 板**（Hi2131，国内全网通，与 WiFi 二选一）
- **屏接口板**：仅 SPI 屏，已适配 1.28" 双圆屏 / 2.1" 单圆屏 / 2.8" 单方屏（+CST3530 触摸）
- **Sensor 镜头板**：OS04D10 4MP 2Lane ×1 或 ×2（双目）
- **MCU 板**：Hi3016（交付清单）/ Hi3061（马达控制场景，可选）

音频要点：**只用主板（不插任何扩展板）就有麦 + 喇叭口**——`agent_audio_sample` 的 `inner` 变体即走内置 acodec，无需 ES7210。

三个推荐场景由 **SW1301 拨码**切换：①双屏+单摄 ②单屏+双摄 ③内置 ADC+双摄+SD 卡。

## 2. 官方资料入口

| 资源 | 链接 | 说明 |
|---|---|---|
| **应用仓（本板）** | https://gitcode.com/HiSpark/hi_aiot_solution_cv610_ev_board | samples/references 案例 + bsp(dts/patch) + 硬件文档；**不含 SDK 本体** |
| **父工程/文档站** | https://gitcode.com/HiSpark/hi_aiot_solution | build.sh、tools/burn、docs（mkdocs，zh-CN 全套：环境搭建/快速开始/烧录/工具/FAQ） |
| **repo manifest** | https://gitcode.com/HiSpark/hi_aiot_solution_manifest | 多仓清单；**源码必须 repo 全量拉，不能只克隆单仓** |
| **SDK 主仓** | https://gitcode.com/HiSpark/Hi3516CV610 | Hi3516CV610 BSP/MPP（tag_V2.0.0_Beta），内嵌 linux(5.10.y)/u-boot(2022.07)/busybox(1.34.1) 子模块 + 预编译工具链 tgz |
| 姊妹板应用仓 | https://gitcode.com/HiSpark/hi_aiot_solution_cv610_pico_board | cv610 启诺开发板 |
| 组件仓 | HiSpark/hi_aiot_solution_adapter · media · hiai · hichannel · network | 父工程按 Kconfig 收编的公共组件 |
| 硬件设计指南 | 应用仓 `hardware/hardware-design-guide/sunniwell-cv610-dev-board.md` | 你给的链接本体；V02 2026-08-06 |
| 原理图/PCB/Datasheet | 应用仓 `hardware/dev-kit/`、`hardware/other-hardware-docs/` | 公开交付 |
| 烧录指南 | 父仓 `docs/Instruction/burning-guide.md` | burn.sh + ToolPlatform 两法 |
| Vibe-Coding 指南 | 父仓 `docs/zh-CN/get-started/quick-start/vibe-coding-guide.md` + 仓库根 `AGENTS.md` + `.agents/skills` | **官方明确定位支持 AI 编码智能体开发**（对 ZCode 用户是利好） |

前置条件：**gitcode 账号 + 个人访问令牌（PAT）+ git-lfs**（repo sync 走 https + credential，SDK/工具链大文件）。

## 3. 构建体系与工具链

- **构建系统**：`bash scripts/build.sh build --target cv610_ev_board <references|samples|solutions> <app> [-DKEY=VAL]`；CMake（单阶段）+ Kconfig（每应用 `app.defconfig`）+ 第三方库走 CMake ExternalProject（openssl/curl/mbedtls/mqtt/lvgl/zeroclaw/micropython/libdatachannel/mediakit 等）
- **首次构建自动装 SDK**（`sdk/prepare.cmake` 解包 `sdk/Hi3516CV610`），首次全量（含内核）编译**数十分钟**，增量自动跳过
- **交叉工具链**：`arm-v01c02-linux-musleabi-`（GCC 10.3.0，musl，armv7 softfp/neon）——发行包名 `gcc-10.3-arm-musl-x86-linux-26.06.1-codesize.tgz`，**只有 Linux x86_64 宿主二进制**（AGENTS.md 另写 `arm-openeuler-linux-musleabi`，口径不一致，同族）
- 另有 Rust 工具链（host 侧工具用）+ Python3.10 + CMake 3.22
- **OpenHarmony 线**：`scripts/build_ohos.sh`，product `ipcamera_hispark_hi3516cv610_linux`（与 Linux SDK 是两套产物，走 OH 6.1 LTS 源码树）
- 产物：`_build/install/image/<app>/`：`uImage`、`rootfs_hi3516cv610_2k_128k_48M.ubifs`、`boot_image.bin`、`nand_burn_table.xml`、`nand_env.bin`（NAND）/ nor_* / emmc_* 三套按介质

**案例清单**（与"AI 对话/小智"相关的加粗）：

| 类别 | 案例 | 说明 |
|---|---|---|
| references | **cloud_agent** | 端云协同 AI 对话：音视频 MPP 编码上云（火山 VolcEngine RTC / 阿里百炼 Qwen MMI 双 provider），云端回音频流本地解码播放；GPIO 按键唤醒；可选本地 KWS |
| references | **agent_audio_sample**（samples） | **纯语音双向 AI 对话**：内置 ADC(`inner`，免扩展)/ES7210(`es7210`) 两变体；KWS 唤醒+命令词；三种模式（纯端侧/纯上云/端侧唤醒+上云）；**云端 OPUS 下行解码 + 喇叭播放已实现** |
| references | factory_demo（ws73_lcd 等） | **开箱即用整机**：视频采集+H.265 RTSP 推流+SPI 屏 LVGL 九页 UI+BLE 配网+ZeroClaw AI Agent（NPU 人/人脸/车辆检测 + JPEG 抓拍 + QQ/飞书/钉钉/WebUI 渠道） |
| references | ai_table_lamp / offline_voice_ac_control / zeroclaw_base | AI 台灯 / 离线语音+星闪空调 / ZeroClaw+舵机 |
| samples | ai_component、capture_picture、panel、ble_wifi、gui、h264_decoder、fastboot、autorate、local_voice_process（本地识别+阿里/讯飞/火山 ASR）、at_tool、push_stream、sensor(single/dual)、dialog_fullscreen_ui、framework_media | 单功能示例 |

## 4. 烧录与调试

- **出厂即用**：板的镜像已烧写小系统，ko/lib/sample 已拷到板内，**不烧录即可直接跑业务**（硬件指南"单板软件配置"）
- **常规烧录 `tools/burn/burn.sh`**：要求 U-Boot 正常；原理 = 串口打断 U-Boot 自启 → 配网 → U-Boot 内置 TFTP 客户端从宿主机拉镜像逐分区写 Flash；运行位置须为 Docker 容器或 WSL Ubuntu（`--device /dev/ttyUSB0 -p 69:69/udp -v` 镜像目录），宿主机与板同网段；先 `check_config.sh` 预检
- **救砖 `ToolPlatform`（BurnTool）**：全擦/无 U-Boot/新片场景，Windows GUI（父仓 `docs/zh-CN/tools/BurnTool.md`）
- 进入 U-Boot：复位后 1~2s 内串口按回车；或 SW2 按住上电进更新模式；BOOTROM 串口烧写模式由电阻 R924 选择
- 串口：CH343P，`picocom -b 115200 /dev/ttyUSB0`；启动介质由 BOOT_SEL 电阻选择（NAND 默认）
- 上板验证：`uname -a` 后按各案例 README 跑

## 5. Demo 跑通路径

1. **核对套件**：主板必带；确认有无 WiFi 板（WS73 常电推荐）、屏、Sensor 板、喇叭（8Ω/2W）——`factory_demo ws73_lcd` 需要全家桶；纯主板可跑 `agent_audio_sample/inner`（但需云 key）与 sensor/push_stream 类
2. **零编译先验板**：Type-C 连 Debug 口 → `picocom -b 115200` → 按出厂 README 直接跑板内 sample
3. **搭编译环境**（Mac 见下节）：Docker wukun 镜像或 Ubuntu 22.04
4. **拉源码**：`repo init -u https://gitcode.com/HiSpark/hi_aiot_solution_manifest.git -b main && repo sync && repo start master --all`
5. **第一个编译目标**：`samples base`（最小镜像，验通工具链）→ `samples push_stream`（摄像头 RTSP，Mac 上 `ffplay rtsp://板IP/...` 直接看效果）→ `references factory_demo` → `samples agent_audio_sample/inner -DCLOUD_AGENT_PROVIDER=volcengine|qwen`（需火山/百炼 key）
6. **烧录**：`burn.sh`（或救砖 ToolPlatform）→ 串口 `uname -a` 验证

## 6. Mac（ARM64）适配结论

**官方支持：零。** 环境搭建文档只写"Windows 和 Linux"，全仓 grep `macos|darwin` 无一命中编译链路。官方三选一：Ubuntu 22.04 原生 / Windows+WSL2(Ubuntu 22.04) / **官方 Docker 镜像** `swr.cn-north-4.myhuaweicloud.com/hi_spark/wukun:docker-v1.2.0-rc2`（Ubuntu 22.04.4，预装工具链+repo+picocom+tftpd-hpa+Rust+Python3.10+CMake3.22）。

两个硬事实（本次已核实）：

- 工具链 `arm-v01c02-linux-musleabi` 只发 **x86-linux** 二进制 → Mac 原生编译不可能
- **wukun 镜像为 `linux/amd64` 单架构**（registry manifest 实查）→ Apple Silicon 需 Docker Desktop 开 **Rosetta 2** 转译跑（性能打折，内核首编会更慢；无 Rosetta 则落 QEMU 更慢）

| 环节 | Mac 可行性 | 方案 |
|---|---|---|
| 写码/lint | ✅ 原生 | 本仓自带 `AGENTS.md` + `.agents/skills`，官方鼓励 AI 智能体开发 |
| 编译 | ✅ Docker(Rosetta) | Docker Desktop 拉 wukun（amd64）；VS Code Dev Containers/Remote-SSH 进容器（容器 SSH 口 2200） |
| TFTP 烧录服务 | ✅ Docker | `-p 69:69/udp` 映射，Mac 与板同网段（Mac 接板网线口同交换机/路由器） |
| 串口（打断 U-Boot / 日志） | ✅ 原生 | CH343 驱动 → `/dev/cu.usbserial-*`，`picocom/screen/minicom` 115200（brew 装 picocom） |
| 一键 burn.sh | ⚠️ 需拆解 | burn.sh 要串口+TFTP 同在容器。Mac 上两法：① **手动烧录**——Mac 串口终端打断 U-Boot，手敲 burning-guide 里的 `setenv serverip/ipaddr` + `tftp 0x44000000 <分区镜像>` + 烧写命令（分区表 nand_burn_table.xml 里有序）② socat 把 Mac 串口桥成 TCP（`host.docker.internal`）供容器内 burn.sh 用（待验证） |
| 救砖 ToolPlatform | ⚠️ | Windows GUI；UTM Win11 ARM 虚机或借 Windows 机器（低频场景） |
| 板上文件迭代 | ⚠️ 待验证 | 出厂 rootfs 是否带 dropbear/tftp 客户端未确认；若有 ssh/tftp，可只编译应用二进制 scp/tftp 上板，免整镜烧录 |

**推荐组合**：Mac 全程为主——Docker(Rosetta) 编译 + Mac 原生串口 + 容器 TFTP；救砖才需要 Windows。**若追求编译速度**：任意 x86_64 Linux（家里小主机/云 VM）+ VS Code Remote-SSH，是最顺路径；UTM Ubuntu ARM 虚机不推荐（工具链 x86，双层转译）。

对照 Hi3322 的结论：这次没有 fbb CLI/BurnTool 开源那种可挖的口子，但**烧录协议本身简单**（U-Boot 串口 + TFTP），Mac 上手动可完全替代。

## 7. AI 小智集成方案

### 7.1 小智生态盘点（调研结论）

- 本体：[78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32)（虾哥），ESP32 系固件 + 云端（官方 xiaozhi.me 或自建）；**协议开放**：WebSocket 主（`docs/websocket.md`，hello/listen/stt/tts/llm/mcp JSON + Opus 16kHz/60ms 二进制帧），MQTT+UDP 备选；协议"权威但不冻结"，自建服务器是生态常态
- 自建服务器：[xinnan-tech/xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server)（Python，~10.5k★，MIT，Docker 部署，2C2G 起）：ASR(FunASR/火山/腾讯…)→LLM(OpenAI 兼容/智谱/DeepSeek…)→TTS(EdgeTTS/CosyVoice…)全管线可配，含 VLM 视觉模型项、MCP、声纹、记忆
- **Linux SoC 移植先例**（证明可行）：[100askTeam/xiaozhi-linux](https://github.com/100askTeam/xiaozhi-linux)（C，RK3568/全志 T113/K230/i.MX6ULL，websocketpp+ALSA+LVGL）、`Yinyifeng18/xiaozhi-linux-rk3568`、`haoyn231/xiaozhi_linux_rs`(Rust)、[huangjunsen0406/py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi)（Python，3.4k★，**自带摄像头+VLM 多模态**，官方生态采纳）
- 视觉扩展：官方固件有 camera vision（拍照→阿里云 VLM）；服务器侧有 `XuSenfeng/xiaozhi-server-vision`

### 7.2 本仓库的底座（比从零移植好得多）

`agent_audio_sample` 已具备：音频采集（内置 ADC 免扩展）→ VQE 前处理（SDK TALKV2 或云知声 SSP）→ **KWS 唤醒词/命令词**（离线）→ 云端 provider 抽象（`-DCLOUD_AGENT_PROVIDER=volcengine|qwen`）→ **OPUS 下行解码 + AO 喇叭播放** → 运行期 config.json 切模式。`cloud_agent` 再加视频上云与外设控制（UART→SLE）。**缺的只是"小智协议"这个 provider**（上行 Opus 编码 + WebSocket/MQTT 客户端 + JSON 会话状态机）。

### 7.3 推荐架构（做成代码仓库）

```
fork hi_aiot_solution_cv610_ev_board
└── 新增 references/xiaozhi_agent/     # 仿 cloud_agent 目录规范
    ├── app.defconfig                  # 继承 agent_audio defconfig + CONFIG_OS_MQTT=y
    ├── patch/ ...                     # 复用 agent_audio 公共补丁
    ├── source/
    │   ├── provider/xiaozhi/          # 小智协议客户端：hello 握手、listen 状态、
    │   │                              #   stt/tts/llm JSON 处理、Opus 上行编码、
    │   │                              #   mcp 工具（GPIO/PWM/抓拍）上报
    │   └── (复用 common: 采集/VQE/KWS/AO 播放)
    └── rootfs/...                     # config: server 地址/token、WiFi
服务器：Mac/NAS 上 Docker 跑 xiaozhi-esp32-server（配智谱/DeepSeek LLM + EdgeTTS/FunASR）
```

实现取舍：

- **传输**：仓库 open_source 有 `mqtt`（+板端 UDP 天然可用）→ 可直接走小智 **MQTT+UDP** 变体避开引 WebSocket 库；或引入一个小型 ws 库（参考 100ask 的 websocketpp+boost，或 libdatachannel 已在仓但走 WebRTC 不同路）
- **上行 Opus**：下行解码已现成；上行编码用 libopus（musl 交叉编译一份即可，py-xiaozhi 帧参数 16k/mono/60ms）
- **唤醒**：复用现成 KWS（`-DCLOUD_AGENT_KWS=ON`），不必移植 Sherpa
- **视觉差异化（推荐主打）**：OS04D10 4MP 抓拍（`capture_picture` 现成）→ 小智服务器 VLM（智谱 GLM-V 等）→ "你看到了什么"；再叠 `ai_component` NPU 端侧检测（人/车/人脸）做事件抓拍主动上报——这是 ESP32 小智没有的硬件优势
- **生态位**：ZeroClaw（仓内自带 agent 框架+skills）与小智可并存：小智做语音/视觉 UX，ZeroClaw 做渠道与技能编排

工作量预估：协议 provider（C，~1.5–3k 行，参照 100ask 实现）+ 服务器部署（Docker 半天）+ 联调，属于"周末级起步、两周可 demo"的规模；不确定项：板端上行 Opus 编码链路是否已有现成封装（见到下行解码，上行未见样例代码，需翻 SDK MPP AudioEncode）。

## 8. 已知坑与 FAQ

- **repo 全量拉码**，不能只克隆应用仓；需 gitcode 账号 + PAT + git-lfs（凭据 `git credential approve` 注册）
- WiFi 只支持 **2.4GHz**；WS73/WS53 内核驱动与内核版本**严格绑定**（改内核配置需从 hisupport 拿 `WS73.rar` 重编）
- `agent_audio_sample` 的 inner/es7210 两变体内核不同，**切换必须先 `build.sh distclean`**（BSP 只在 `pub/` 无 uImage 时才重编）
- SW1301 拨码三场景：屏的数量、双摄、SD 卡与 SDIO WiFi 复用关系，接硬件前先核对
- 官方文档自身口径矛盾：CPU 一处 MP2 双核一接口表"单核"；AGENTS.md 工具链名与安装文档不一致（v01c02 vs openeuler）
- 首次编译数十分钟；增量自动跳过；`distclean` 慎用（会删 SDK 源码树需重下，见 factory_demo README）
- NPU 1 TOPS 为海思官网口径，完整 datasheet/编码参数表属 NDA，仓库未公开
- 40PIN GPIO 电平 3.3V（部分 1.8V 复用脚），热插拔禁止
- OH 6.1 与 Linux 5.10 是两条独立构建线（`build_ohos.sh`），产物/生态不同；主线建议先 Linux

## 9. 推荐上手顺序

1. 核对套件清单与拨码（SW1301 场景一/二/三），喇叭接 J47
2. 出厂系统 + 串口（Mac `picocom -b 115200 /dev/cu.usbserial-*`）跑板内 sample 验板
3. Docker Desktop（开 Rosetta 2）拉 `wukun:docker-v1.2.0-rc2`，容器内 repo sync
4. 编 `samples base` 烧录验通全链路（Mac 手动 TFTP 烧录法）
5. 编 `push_stream`，Mac `ffplay` 看摄像头流（成就感最快）
6. `agent_audio_sample/inner` + 火山或百炼 key，跑通官方版"语音 Agent"（小智的前身体验）
7. 起 `xiaozhi-esp32-server`（Mac Docker），开写 `references/xiaozhi_agent` provider
8. 叠视觉：抓拍 → 服务器 VLM；NPU 检测事件 → 主动播报

---

*本索引由调研整理（2026-09-09）。已核实：仓库/文档原文（本地 clone 应用仓 242MB + 父仓 docs/scripts）、wukun 镜像架构（amd64）。待拿到板子后验证：出厂 rootfs 是否带 dropbear/tftp、烧录实操、上行 Opus 封装、socat 串口桥。以官方文档站（父仓 `docs/`，mkdocs 渲染）为最终权威。*
