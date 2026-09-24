# 基于 P-NUCLEO-IHM03 套件的电机入门控制实例

> **核心命题**　本章把前三章的积累兑现：用 MC Workbench 五分钟生成一个无感 FOC 工程让电机转起来，然后逐一玩透六个实例——无感 FOC、无感方波、速度闭环、旋钮调速、故障处理、API 调用。所有实例的配置差异都来自第 5、6 章讲过的原理选项：控制策略、观测器、启动参数、环路上的 PI。

---

**实验前置检查清单**（每个实例开工前过一遍）：

1. 堆叠好的套件、电机三线接好、12 V 电源在手边（2.4 节操作纪律）；
2. CubeIDE + X-CUBE-MCSDK 已安装（第 3 章）；
3. 电机参数已用 Motor Profiler 测得（3.6.3 节；后文以 GBM2804H-100T 典型值演示：极对数 7、相电阻约 11 Ω、相电感数十 mH 量级——以你实测为准）。

## 无感 FOC 快速控制实例

**目标**：从零开始，让电机以无感 FOC 稳速旋转，并在 MC Monitor 里看到转速曲线。

**步骤一：MC Workbench 新建工程**

1. 打开 MC Workbench $\rightarrow$ New Project；
2. 电机选型页：Catalog 里没有 GBM2804H-100T 时选 "Custom"，手动填入极对数 7、最大电流（0.3 A 起步）、相电阻、相电感、反电动势常数（Profiler 实测值）；
3. 板卡选型页：选 P-NUCLEO-IHM03（IHM16M1 + NUCLEO-G431RB 组合）——电流检测拓扑（Three-shunt）、引脚映射、采样增益自动配置，**不要手改**；
4. 控制策略：Drive = FOC；Feedback = Sensorless（Observer = STO，CSTO + PLL 结构，见 6.2.3 节原理）；Control mode = Speed；
5. 生成工程：Project Generation 选 STM32CubeIDE $\rightarrow$ Generate。

**步骤二：编译烧录**：CubeIDE 打开生成的工程 $\rightarrow$ Build $\rightarrow$ Run（ST-LINK 一键下载运行）。

**步骤三：上电与验证**

1. 接 12 V 电源——固件默认待机，电机不通电；
2. 打开 ST MC Monitor，连接板卡，在启动页给一个低速指令（如 1000 rpm）点 Start：电机经历"定位 $\rightarrow$ 开环拖动 $\rightarrow$ 切入闭环"三段（5.3.2 节讲过为什么），随后稳速旋转；
3. Monitor 的速度曲线上能看到三段过程与稳态直线；相电流波形接近正弦——这是 FOC 工作的签名。

**固件分层**：生成的工程在用户代码与硬件之间隔着完整中间件（图 7.1），应用层只调 `mc_api.h`：

![MC SDK 5.x 固件分层：应用层（mc_api 调用）→ 电机控制中间件（FOC 内核、观测器、保护）→ MC 驱动层（PWM/ADC 硬件抽象）→ HAL/LL；换板卡只动下层，升级 SDK 不动用户代码](images/fig_07_mcsdk_layers.pdf)

**排错速查**（首转失败 top 3）：电机抖动不转 = 相序接反（任意对调两根电机线重试）；启动即过流 = 最大电流设太小/启动参数激进；转起来但速度发散 = 观测器增益不合适（用 Monitor 的 observer 调试页微调）。所有故障先读 7.5 节的故障码再动手。

## 无感方波控制实例

**目标**：同一套硬件跑 Six-Step（BEMF 无感），与 FOC 对比体验。

**MC Workbench 差异配置**：Drive 选 Six-Step；Feedback 保持 Sensorless（BEMF 检测——对应 IHM16M1 板上的 BEMF 感知电路，5.3.2 节的过零 + 30° 延时逻辑已内置）；重新生成工程。

**实验现象对比**（建议同转速下对比，用手感 + 听觉 + 电流波形记录）：

| 观察项 | 六步方波 | 无感 FOC |
| --- | --- | --- |
| 低速手感 | 有顿挫、齿槽感明显 | 平滑 |
| 噪声 | 换相"嗒嗒"声 | 接近无声 |
| 相电流波形 | 方波（梯形段） | 正弦波 |
| 启动 | 三段式，需调启动参数 | 三段式，参数更宽容 |

这个对比实验的价值在于把第 5 章的"转矩纹波"从公式变成手感。方波驱动的电流利用率与低速平稳性全面落后，但算法简单、对电流采样质量不敏感——风机水泵类负载至今仍大量使用。

## 无感速度模式控制实例

**目标**：验证速度闭环的斜坡、稳态精度与负载响应——第 6.4.3 节理论的实感。

**操作**（在 7.1 的 FOC 工程上）：MC Monitor 速度页给阶跃指令（如 500 $\rightarrow$ 3000 rpm），观察曲线：

- **斜坡段**：SDK 默认对速度指令加斜率限制（防电流冲击），斜率可在 Workbench 的高级参数里改——对应 API `MC_ProgramSpeedRampMotor1`（7.6 节）；
- **稳态段**：速度波动主要来自观测器噪声，可微调速度环滤波；
- **加载测试**：用手指轻捏电机轴施加负载，速度短暂跌落后回到设定值（速度环积分的作用），同时 Monitor 里 $i_q$ 上升——转矩通道的完整闭环亲眼可见。

**速度环整定实践**：在 Monitor 里在线改速度环 PI（无需重烧），按 6.4.3 的带宽分离原则：响应太软 $\rightarrow$ 增大增益；速度振荡/电流啸叫 $\rightarrow$ 减小并检查内环带宽。改好后回填 MC Workbench 参数页固化。

## 旋钮控制电机运行速度实例

**目标**：脱离 PC，用一个电位器旋钮本地控制电机转速——"嵌入式产品化"的第一个原型。

**硬件**：10 kΩ 电位器两端接 3.3 V 与 GND，中心抽头接 NUCLEO 的一个空闲 ADC 通道（在 CubeMX 里给工程补一路 ADC 常规采样即可，避开 MC SDK 已占用的电流采样通道）。

**代码**（应用层，主循环 10 ms 周期执行）：

```c
/* 读取旋钮电压 → 映射为速度指令 → 下发给速度环 */
#include "mc_api.h"

#define SPEED_MIN   300     /* rpm，低于此速无感观测不稳 */
#define SPEED_MAX   3000    /* rpm */

void UserPoti_Task(void)    /* 10 ms 周期调用 */
{
    uint16_t adc = ReadPoti_ADC();               /* 0..4095 */
    int16_t rpm = SPEED_MIN + (int32_t)(SPEED_MAX - SPEED_MIN) * adc / 4095;

    if (MotorIsStarted()) {
        MC_ProgramSpeedRampMotor1(rpm * SPEED_UNIT, 200); /* 200 ms 平滑 */
    }
}
```

**要点**：速度指令经 `MC_ProgramSpeedRampMotor1` 平滑下发（斜坡由 SDK 执行）；启动/停止仍可用板上 B1 按键触发（4.3 节的 EXTI 回调里调 `MC_StartMotor1()`/`MC_StopMotor1()`）。此实验把"传感 $\rightarrow$ 指令 $\rightarrow$ 速度环 $\rightarrow$ 电机"的产品级数据流完整走了一遍。

## 故障处理及恢复实例

**目标**：理解 SDK 的故障管理机制，做一个"故障可查询、可恢复"的应用。

**故障检测**是 SDK 中间件内置的（过流、过压、欠压、速度反馈异常、启动失败等，枚举定义在固件 `mc_type.h` 一带，以随 SDK 的头文件为准）。应用层要做的是**消费故障**：

```c
if (MC_GetOccurredFaultsMotor1() != MC_NO_FAULTS) {
    uint16_t faults = MC_GetOccurredFaultsMotor1();
    LogFaultViaUART(faults);            /* 串口上报故障码（4.4 节通道） */
    HAL_Delay(3000);                    /* 等待现场排除（举例） */
    MC_AcknowledgeFaultsMotor1();       /* 确认清障 */
    MC_StartMotor1();                   /* 重新启动 */
}
```

**人为制造故障做实验**（安全范围内）：运转中轻捏电机轴到堵转 $\rightarrow$ 观察过流/启动失败故障码；串口日志看到码值后再松手让程序自动恢复。注意两点纪律：故障必须先 `MC_AcknowledgeFaultsMotor1` 清除才能再启动；真实产品里"自动重启"要加次数与冷却限制，避免打火花式循环重启。

## API 函数应用实例

`mc_api.h` 是应用层与电机控制栈之间唯一的边界。常用函数速览（以 Motor1 宏为例，5.x 头文件定义）：

| API | 作用 | 典型场景 |
| --- | --- | --- |
| MC_StartMotor1() | 启动电机（走启动序列） | 按键开机 |
| MC_StopMotor1() | 停止并封 PWM | 按键停机、故障停机 |
| MC_ProgramSpeedRampMotor1(target, ms) | 编程速度斜坡（0.1 Hz 单位） | 7.3 / 7.4 节调速 |
| MC_ProgramTorqueRampMotor1(target, ms) | 编程转矩斜坡（q 轴电流指令） | 力矩模式应用 |
| MC_GetSpeedMotor1() | 读当前机械转速（0.1 Hz 单位） | 状态显示 |
| MC_GetCurrentsMotor1() | 读 dq 轴电流（标幺） | 负载监测 |
| MC_GetStateMotor1() | 读状态机状态（IDLE/RUN/FAULT…） | 流程控制 |
| MC_GetOccurredFaultsMotor1() | 读故障位域 | 7.5 节故障处理 |
| MC_AcknowledgeFaultsMotor1() | 清除故障锁存 | 恢复运行 |

**一个综合小例子**——状态机 + 调速 + 上报（主循环 100 ms 片段）：

```c
switch (MC_GetStateMotor1()) {
case RUN:
    MC_ProgramSpeedRampMotor1(CmdRpm * 6, 500);   /* rpm → 0.1Hz 单位 ×6 */
    printf("rpm=%d iq=%f\r\n", MC_GetSpeedMotor1() / 6,
           (double)MC_GetIqMotor1_A());           /* 换算回工程单位显示 */
    break;
case FAULT_NOW:
    HandleFault();                                /* 7.5 节逻辑 */
    break;
default:
    break;
}
```

（单位换算细节以所用 SDK 版本的头文件注释为准——0.1 Hz 与 rpm 之间差一个 6 倍因子，是初学者最常踩的单位坑。）

## 本章小结

- 无感 FOC 五分钟上手：选官方套件型号 + 填电机参数 + 选 STO + 生成，硬件配置全部自动；
- 方波与 FOC 的手感/波形对比，把第 5、6 章理论变成感官经验；
- 速度闭环看斜坡、稳态、加载三段；旋钮实验打通产品化数据流；
- 故障处理三步：读码 $\rightarrow$ 排障 $\rightarrow$ 确认清除后重启；
- `mc_api.h` 是唯一的应用层边界，单位换算（0.1 Hz）是最大暗坑。

## 本章参考

- X-CUBE-MCSDK 5.x 用户文档：MC Workbench 向导、API 参考、故障枚举
- UM2383 / P-NUCLEO-IHM03 入门资料（官方 Getting Started 视频/文档）
- ST 社区 P-NUCLEO-IHM03 板块的启动排错问答
