# 第 1 章　一致性与连贯性简介

> **核心命题**　一致性与连贯性是多处理器正确性的两大支柱：一致性规定所有处理器看到的内存操作全局顺序，连贯性规定单个内存位置的写入不会让陈旧数据被读取。两者既独立又协作——连贯性是一致性的必要非充分条件。本章建立全书的概念地图，澄清二者的边界与协作。

---

## 1.1　一致性（亦称内存一致性、内存一致性模型或内存模型）

**内存一致性**（memory consistency / memory consistency model / memory model）是一份关于"多处理器共享内存行为的契约"：它规定了多个线程对共享变量的读/写操作，在所有处理器看来应当呈现的合法全局顺序。

理解一致性的关键在于：单处理器下的"程序顺序"是清晰的——指令按程序文本顺序执行。但多处理器下，每个处理器有自己的程序顺序，而内存操作又作用在共享变量上——不同处理器看到的操作顺序可能不同。**一致性模型就是规定这些"可能不同"的合法边界**。

最严格的一致性模型是 Lamport 在 1979 年提出的**连续一致性**（Sequential Consistency, SC）：要求所有处理器看到的操作顺序等于某种全局交错，且每个处理器内的程序顺序被保持。SC 最直观但也最慢，因为它禁止了所有重排。现代商用处理器（x86、ARM、RISC-V、IBM POWER）都不同程度地放松了 SC 以换取性能——它们各自的一致性模型是第 3–5 章的主题。

## 1.2　连贯性（亦称缓存连贯性）

**缓存连贯性**（cache coherence / cache coherence）保证：当某个处理器写入一个内存位置后，其他处理器的缓存中该位置的副本会被失效或更新，**保证不会读到陈旧值**。

连贯性的形式化由两条不变量刻画（Sorin/Hill/Wood 教材）：

- **单写多读不变量**（Single-Writer/Multiple-Reader, SWMR）：对任意内存位置，在任意时刻要么有一个处理器可以写（也可以读），要么有若干处理器可以读（但不能写），二者不可同时存在；
- **数据值不变量**（Data-Value Invariant）：某次读取返回的值，等于此前最后一次对该位置的写入值。

连贯性的粒度通常是**缓存行**（cache block / cache line，典型 64 字节）。这意味着同缓存行内两个不相关变量的写会互相失效——这就是**伪共享**（false sharing）的根源。

## 1.3　异构系统中的一致性与连贯性

当 CPU 与 GPU、加速器协同工作时，一致性模型与连贯性协议都需要重新设计：

- **一致性模型异构**：CPU（x86 TSO）+ GPU（松弛 RC）+ 加速器（更松），三者如何统一？现代方案是用 acquire/release 语义 + 作用域（scope）显式标注同步可见范围。
- **连贯性协议异构**：GPU 数万并发线程使传统每核目录/监听协议不可扩展，催生了**时间连贯性**（temporal coherence）与**释放一致性导向的连贯性**（release-consistency-directed coherence）等新范式。
- **统一内存架构**：CXL（2019）、Apple Silicon UMA、AMD Infinity Fabric 等技术正在让 CPU-GPU 间的硬件连贯性成为主流。

异构系统的一致性与连贯性是第 10 章的主题，也是当前体系结构研究的前沿。

## 1.4　定义并验证内存一致性与缓存连贯性

如何确保一个一致性模型或连贯性协议是"对"的？这涉及两类手段：

- **形式化方法**：用操作化定义（抽象机）或公理化定义（happens-before、acyclicity）刻画合法行为，然后用模型检测（Murphi、TLA+）或定理证明（Coq、Isabelle/HOL）验证实现。
- **测试**：用 litmus 测试（小段并发代码 + 预期结果）在真实硬件上做随机化运行，捕捉违规行为。

第 11 章系统讨论定义与验证的方法学。

## 1.5　一致性与连贯性小测验

在深入后续章节前，读者可以用以下问题自测：

1. 如果一个系统没有缓存连贯性，SC 还能成立吗？（答：不能，连贯性是 SC 的必要条件。）
2. 两个处理器分别写同一缓存行的两个不同变量，会发生什么？（答：伪共享，互相失效。）
3. 为什么 x86 允许 store→load 重排而 ARM 几乎允许所有重排？（答：x86 是 TSO，仅放松 store→load；ARM 是弱序模型。）

## 1.6　本书未涵盖的内容

本书聚焦于共享内存多处理器的一致性与连贯性。以下主题不在本书范围：

- 分布式系统的一致性（Paxos、Raft、CAP 定理）——这是分布式系统的范畴，与共享内存模型不同；
- 数据库事务隔离级别——虽然概念相关，但属于数据库领域；
- 持久内存（PMEM/NVM）的崩溃一致性——这是新兴方向，需要额外讨论。

## 1.7　小结

一致性与连贯性是多处理器正确性的两大支柱：一致性规定全局行为，连贯性保证单地址的写入可见性。连贯性是一致性的必要非充分条件。本书用 4 篇 11 章展开这两个主题：第 1–2 章建立基础，第 3–5 章讨论内存一致性模型（SC、TSO、松弛），第 6–9 章讨论缓存连贯性协议（监听、目录、高级话题），第 10–11 章讨论异构系统与验证方法学。

## 参考文献

1. Lamport L. How to make a multiprocessor computer that correctly executes multiprocess programs. *IEEE Transactions on Computers*, 1979, C-28(9): 690–691. https://doi.org/10.1109/TC.1979.1675439
2. Adve S. V., Gharachorloo K. Shared memory consistency models: A tutorial. *IEEE Computer*, 1996, 29(12): 66–76. https://doi.org/10.1109/2.546611
3. Sorin D. J., Hill M. D., Wood D. A. *A Primer on Memory Consistency and Cache Coherence* (2nd ed.). Morgan & Claypool / Springer, 2020. https://pages.cs.wisc.edu/~markhill/papers/primer2020_2nd_edition.pdf
4. Hennessy J. L., Patterson D. A. *Computer Architecture: A Quantitative Approach* (6th ed.). Morgan Kaufmann, 2019.
5. CMU 15-418. *Parallel Computer Architecture and Programming*. https://www.cs.cmu.edu/afs/cs/academic/class/15418-s12/www/lectures/10_coherence.pdf
