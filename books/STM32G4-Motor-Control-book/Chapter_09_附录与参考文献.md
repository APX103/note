# 附录与参考文献 {.unnumbered}

## 参考文献 {.unnumbered}

1. STMicroelectronics, *STM32G431x6/x8/xB Datasheet（DS12550）* —— 芯片电气规格与外设清单
2. STMicroelectronics, *STM32G4 Series Reference Manual（RM0440）* —— 外设寄存器级文档
3. STMicroelectronics, *STM32G4 Nucleo-64 boards User Manual（UM2079，MB1367）* —— NUCLEO-G431RB 板卡资源
4. STMicroelectronics, *X-NUCLEO-IHM16M1 User Manual（UM2383）* 与产品页 —— 三相驱动扩展板
5. STMicroelectronics, *P-NUCLEO-IHM03 Data Brief* —— 套件组成与电源规格
6. STMicroelectronics, *X-CUBE-MCSDK 产品页、Release Notes 与用户文档* —— MC Workbench / Motor Profiler / 固件库
7. STMicroelectronics, STSPIN830 Datasheet 与产品页 —— 单片三相驱动器规格
8. iPower / iFlight, GBM2804H-100T 云台电机官方规格页
9. ST Community（community.st.com）电机控制板块 —— 启动排错与参数辨识实操问答
10. 电机控制通行教材中关于坐标变换、SVPWM、磁场定向控制的经典推导（本章理论框架的行业共识表述）

## 附录 A　mc_api 常用函数速查 {.unnumbered}

以 Motor1 宏为例（X-CUBE-MCSDK 5.x，`mc_api.h`；具体签名以随 SDK 头文件注释为准）：

| API | 功能 | 注意 |
| --- | --- | --- |
| MC_StartMotor1() | 启动（有感直接闭环，无感走三段启动） | 故障未清时调用无效 |
| MC_StopMotor1() | 停止并封锁输出 | — |
| MC_ProgramSpeedRampMotor1(target, ms) | 速度斜坡，target 单位 0.1 Hz（rpm × 6） | ms 为斜坡时长 |
| MC_ProgramTorqueRampMotor1(target, ms) | 转矩（iq）斜坡，标幺单位 | 转矩模式专用 |
| MC_GetSpeedMotor1() | 读机械转速（0.1 Hz） | 显示需除 6 得 rpm |
| MC_GetCurrentsMotor1() | 读 dq 电流 | 结构体返回 |
| MC_GetStateMotor1() | 状态机状态 | IDLE / RUN / FAULT 等 |
| MC_GetOccurredFaultsMotor1() | 故障位域 | 见附录 B |
| MC_AcknowledgeFaultsMotor1() | 清除故障锁存 | 重启前必须调用 |
| MC_SetCurrentReferenceMotor1() | 直接写 id/iq 指令 | 高级用法 |

## 附录 B　常见故障类型速查 {.unnumbered}

FOC 模式下 SDK 报告的典型故障（枚举名以所用版本 `mc_type.h` 为准，下表为含义速记）：

| 故障 | 含义 | 常见原因 |
| --- | --- | --- |
| 过流（Overcurrent） | 相电流超限或硬件比较器触发 | 参数错、堵转、相线短路 |
| 过压（Overvoltage） | 母线电压超限 | 减速过快回馈能量、电源问题 |
| 欠压（Undervoltage） | 母线电压不足 | 电源掉电、线径过细 |
| 速度反馈错误（Speed feedback） | 观测器/传感信号异常 | 无感启动失败、霍尔断线 |
| 启动失败 | 启动序列超时 | 启动电流/斜率参数不当、负载过重 |

处理三步：读码（GetOccurredFaults）→ 排除物理原因 → 确认清障（AcknowledgeFaults）后重启。

## 附录 C　套件关键参数速查 {.unnumbered}

| 项目 | 数值 |
| --- | --- |
| MCU | STM32G431RBT6：Cortex-M4F @170 MHz，128 KB Flash，32 KB SRAM |
| 驱动器 | STSPIN830：7 ~ 45 V，1.5 A RMS，1/3 电阻检测，3/6 PWM |
| 电机 | GBM2804H-100T：7 对极，相电阻约 11 Ω（标称 10 Ω ±5%），约 41.5 g |
| 电源 | 12 V / 2 A 直流适配器 |
| 用户资源 | LD2 = PA5；B1 = PC13；USART2 = PA2/PA3（ST-LINK 虚拟串口） |
| 文档 | DS12550 / RM0440 / UM2079 / UM2383 / P-NUCLEO-IHM03 Data Brief |

## 附录 D　随书图源说明 {.unnumbered}

全书 23 幅示意图均为本书绘制：TikZ 源码（`figures/*.tex`，`bash figures/build_tikz.sh` 重新编译）与 Python 脚本（`figures/gen_py_figs.py`，`python3 figures/gen_py_figs.py` 重新生成）。修改配色或标注后重建即可定制自己的教学版本。
