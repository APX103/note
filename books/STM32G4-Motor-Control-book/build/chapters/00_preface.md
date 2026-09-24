# 前言 {.unnumbered}

> 本电子书按照《STM32G4入门与电机控制实战——基于X-CUBE-MCSDK的无刷直流电机与永磁同步电机控制实现》一书的目录框架，由 AI 综合 ST 官方文档（Datasheet、Reference Manual、User Manual、X-CUBE-MCSDK 文档）与公开技术资料整理编写，供学习参考之用。
>
> \textbf{[注意]} **免责声明**：本书为基于公开资料的学习整理稿，不是原书的复制或翻译；所有硬件参数以 ST 官方最新文档为准，涉及实际接线与上电操作时请务必核对官方手册。电机运行实验请使用套件附带的安全低电压（12 V）进行。

## 编者简介 {.unnumbered}

**李佳伦**　本书编者。内容基于公开的目录框架与 ST 官方技术文档，由 AI 整理编写：硬件事实（芯片规格、板卡资源、套件组成）逐条对照 ST 官网与手册核实；电机控制理论（BLDC 方波、PMSM 矢量控制、SVPWM）按通行教科书体系重新推导展开；实践章节基于 X-CUBE-MCSDK 5.x 的公开文档与固件架构撰写。

## 全书结构与阅读建议 {.unnumbered}

全书围绕 ST 官方 P-NUCLEO-IHM03 电机控制套件展开，分为四个部分，共 8 章正文 + 附录：

### 第一部分　平台与工具（第 1 \textasciitilde{} 3 章） {.unnumbered}

- 第 1 章　STM32G4 概述
- 第 2 章　STM32 电机控制套件 P-NUCLEO-IHM03
- 第 3 章　软件开发环境

### 第二部分　基础实验（第 4 章） {.unnumbered}

- 第 4 章　NUCLEO-G431RB 基础实验

### 第三部分　电机控制理论（第 5 \textasciitilde{} 6 章） {.unnumbered}

- 第 5 章　无刷直流电机控制技术
- 第 6 章　永磁同步电机控制技术

### 第四部分　实战案例（第 7 \textasciitilde{} 8 章） {.unnumbered}

- 第 7 章　基于 P-NUCLEO-IHM03 套件的电机入门控制实例
- 第 8 章　基于 P-NUCLEO-IHM03 套件的有感电机控制案例
- 附录与参考文献

### 三条阅读路径 {.unnumbered}

- **快速上手路径**（已有嵌入式基础）：第 2 章 $\rightarrow$ 第 3 章 $\rightarrow$ 第 7 章，半天内让电机转起来；缺理论再回读第 5、6 章。
- **理论补课路径**（会调 SDK 但想懂原理）：第 5 章 $\rightarrow$ 第 6 章，重点读坐标变换与 SVPWM 的几何解释，配合第 7 章把每个 SDK 概念对号入座。
- **完整学习路径**（嵌入式入门读者）：按章节顺序通读，第 4 章每个实验都在 CubeIDE 里亲手做一遍，第 7、8 章跟着 MC Workbench 步骤操作。

## 主要参考资料来源 {.unnumbered}

- ST 官方芯片文档：STM32G431 datasheet（DS12550）、STM32G4 Reference Manual（RM0440）
- ST 官方板卡文档：NUCLEO-G431RB User Manual（UM2079，MB1367）、X-NUCLEO-IHM16M1 User Manual（UM2383）、P-NUCLEO-IHM03 Data Brief
- ST 电机控制软件：X-CUBE-MCSDK（含 MC Workbench、Motor Profiler、ST MC Monitor 与固件库）官方文档与 Release Notes
- iPower/iFlight GBM2804H-100T 云台电机官方规格
- 电机控制通行理论：坐标变换、SVPWM、磁场定向控制的经典教材推导（详见各章末参考）

## 关于本书的图 {.unnumbered}

全书 23 幅示意图（芯片框图、驱动板信号链、六步换相波形、坐标变换矢量图、SVPWM 空间矢量、FOC 控制框图等）均为本书重新绘制，源文件（TikZ / Python）随书目录 `figures/` 提供，可自行修改后用 `figures/build_tikz.sh` 与 `figures/gen_py_figs.py` 重新生成。
