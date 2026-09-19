# 内存一致性和缓存连贯性理论

> 本书基于 Hill, Lipasti 与 Wood 的 *A Primer on Memory Consistency and Cache Coherence* 一书的章节框架，由 AI 综合 Lamport、Adve、Gharachorloo、Sorin 等奠基研究者的论文，x86/ARM/RISC-V/IBM POWER 各 ISA 规范，以及 ISCA/MICRO/HPCA/ASPLOS 等体系结构顶会的公开资料独立整理编写，供学习研究参考之用。
>
> **【注意】**　本书为基于公开资料的学术性整理稿，不构成芯片设计、编译器实现与性能优化的工程决策依据。所有 ISA 形式化细节、协议状态机与原子指令语义以各厂商官方规范（Intel SDM、ARM ARM、RISC-V 规范、IBM POP）与最新同行评议论文为准。

## 编者简介

**李佳伦**　本书编者。本书内容基于 Hill、Lipasti、Wood 专著的章节框架，由 AI 综合 Leslie Lamport 的连续一致性奠基论文（1979）、Sarita Adve 与 Kourosh Gharachorloo 的内存模型综述、Daniel Sorin 等的连贯性协议研究，x86（Intel SDM）、ARM（ARM ARM）、RISC-V（RVWMO 规范）、IBM POWER 各 ISA 官方手册，以及 ISCA、MICRO、HPCA、ASPLOS 等计算机体系结构顶会的论文整理编写而成，仅供学习研究参考。

## 全书结构

全书分为 4 个部分，共 11 章：

### 第一部分　一致性与连贯性基础

- [第 1 章　一致性与连贯性简介](./Chapter_01_一致性与连贯性简介.md)
- [第 2 章　连贯性基础](./Chapter_02_连贯性基础.md)

### 第二部分　内存一致性模型

- [第 3 章　内存一致性的动机以及连续一致性](./Chapter_03_内存一致性的动机以及连续一致性.md)
- [第 4 章　全存储顺序以及 x86 内存模型](./Chapter_04_全存储顺序以及x86内存模型.md)
- [第 5 章　松弛内存一致性](./Chapter_05_松弛内存一致性.md)

### 第三部分　缓存连贯性协议

- [第 6 章　连贯性协议](./Chapter_06_连贯性协议.md)
- [第 7 章　监听协议](./Chapter_07_监听协议.md)
- [第 8 章　目录连贯性协议](./Chapter_08_目录连贯性协议.md)
- [第 9 章　连贯性高级话题](./Chapter_09_连贯性高级话题.md)

### 第四部分　异构系统与验证

- [第 10 章　异构系统的一致性和连贯性](./Chapter_10_异构系统的一致性和连贯性.md)
- [第 11 章　一致性模型与连贯性协议的定义与验证](./Chapter_11_一致性模型与连贯性协议的定义与验证.md)

## 主要参考资料来源

- **奠基专著**（仅作框架参考，不复制内容）：Hill M. D., Lipasti M. H., Wood D. A. *A Primer on Memory Consistency and Cache Coherence* (2nd ed.). Morgan & Claypool / Springer, 2020.
- **奠基论文**：Lamport (1979) 连续一致性；Adve & Gharachorloo (1996) 共享内存一致性模型综述；Gharachorloo et al. (1990) 释放一致性；Sorin et al. (2000/2011) 一致性教程。
- **ISA 规范**：Intel Software Developer's Manual（x86 TSO）、ARM Architecture Reference Manual（ARMv8）、RISC-V Unprivileged Spec（RVWMO）、IBM POWER ISA。
- **体系结构顶会**：ISCA、MICRO、HPCA、ASPLOS、POPL 上的内存模型与连贯性协议论文。
- **案例研究**：MIPS R10000、Sun Starfire E10000、IBM Power5、SGI Origin 2000、AMD HyperTransport、Intel QPI/UPI。

## 阅读建议

- **计算机体系结构研究生**：按章节顺序通读，重点关注第 3–5 章（一致性模型）与第 7–8 章（监听/目录协议），这是面试与论文的核心。
- **编译器/系统软件工程师**：可跳读第 6–9 章的协议细节，重点查阅第 3–5 章（FENCE 语义、DRF、原子指令）以理解 lock-free 编程的底层保证。
- **芯片设计工程师**：第 6–9 章是协议设计的核心，第 11 章的形式化验证是流片前必经环节。
- **GPU/异构计算研究者**：直接切入第 10 章，关注 GPU 的时间连贯性与异构系统的一致性模型。
