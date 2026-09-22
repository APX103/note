# 第 11 章　一致性模型与连贯性协议的定义与验证

> **核心命题**　如何确保一个一致性模型或连贯性协议是"对"的？本章讨论操作化定义与公理化定义两类形式化方式、行为探索（litmus 测试）、以及形式化方法（模型检测、定理证明）与硬件测试两类验证手段。

---

## 11.1　定义

一致性模型与连贯性协议都需要严格的**定义**——否则"对错"无从谈起。有两类风格化定义。

### 11.1.1　操作化定义

**操作化定义**（operational definition）用一个**抽象机**（abstract machine）描述合法行为：

- SC 的"全局交换开关 / 任意时刻仅一核访存"；
- TSO 的"每核 FIFO 写缓冲 + 一把全局锁"；
- ARMv8 的 Flowing/operational 模型。

优点：直观、易于人工理解；缺点：难以穷举所有行为，难以直接用于自动化验证。

Owens/Sarkar/Sewell 的 x86-TSO（TPHOLs 2009）给出了操作化模型的经典示例。

### 11.1.2　公理化定义

**公理化定义**（axiomatic definition）用一组**公理**刻画合法执行：

- **happens-before**（happens-before 关系）；
- **preserved program order**（PPO，被保持的程序序）；
- **coherence**（同地址的操作顺序）；
- **acyclicity**（关系图无环）。

优点：适合形式化验证（可直接输入模型检测器/定理证明器）；缺点：抽象，人工理解门槛高。

代表工具链：**cat** 语言（DSL，描述公理）+ **herd** 模拟器（在 cat 模型上模拟 litmus 测试）。Alglave 等在《Herding Cats》（*ACM TOPLAS* 2014，被引超 536）中提出这一统一框架，对 x86、ARM、POWER 给出统一的 cat 模型，并建立 litmus 标准命名（mp/sb/lb/wrc/rwc 等）。

## 11.2　探索内存一致性模型的行为

### 11.2.1　基准测试

**Litmus 测试**（litmus test）是探索内存模型行为的标准工具——小段并发代码 + 预期结果，用于区分内存模型。经典 litmus：

- **Store Buffering（SB）**：两线程各写对方将读的位置后再读对方位置；`r1=0, r2=0` 的结果**在 SC 下被禁止，在 TSO 下被允许**（源于每核 store buffer）。这是区分 TSO 与 SC 的经典测试。
- **Message Passing（MP）**：在 SC 与 TSO 下都被禁止，但在 ARM/POWER 无 fence 的松弛模型下被允许——区分 TSO 与松弛模型的经典测试。

### 11.2.2　探索

**herdtools7**（Alglave & Maranget，Inria）是探索内存模型行为的标准工具链：

- **diy7**：自动生成 litmus 测试；
- **herd7**：在 .cat 模型上模拟结果；
- **litmus7**：在真实硬件上随机化运行数百万次，做 hardware probe。

近期 GPU 专用工具：Dartagnan（Ponce de Leon 等，形式化建模）与 GPUHarbor（Sorensen & Levine，基于 WebGPU 的浏览器化 GPU 内存测试平台）。

## 11.3　验证实现

定义清楚后，需要**验证实现**符合定义。两类手段。

### 11.3.1　形式化方法

**形式化方法**（formal methods）用数学手段证明实现的正确性：

- **模型检测**（model checking）：显式状态枚举（Murphi，David Dill, Stanford）或符号模型检测（SMV/BDD）。广泛用于 cache coherence 协议验证（CMU 课程实验即用 Murphi）。FLASH 协议的参数化验证（CHARME 2001）是经典案例。
- **定理证明**（theorem proving）：Coq、Isabelle/HOL。x86-TSO 即在 HOL 中机械化（Owens/Sarkar/Sewell）。
- **TLA+**：用于协议规约与验证，工业界（如 Intel、Amazon）广泛使用。

### 11.3.2　测试

**测试**（testing）在真实硬件上捕捉违规行为：

- litmus7 的随机化运行（数百万次迭代）；
- 硬件探针。

测试不能证明正确性，但能发现 bug——尤其对于商用 ISA 文档不全或实现偏离规范的情况。

## 11.4　历史与进一步阅读资料

### 11.4.1　Alpha 21164 的教训

**DEC Alpha 21164** 因不保证数据依赖序（data-dependency ordering）而著名：一个读可能在挂起的连贯性失效/写提交完成前返回**本地缓存的陈旧值**，效果上"读到未提交/陈旧数据"。这破坏了 double-checked locking 等惰性初始化模式，迫使 Linux 内核历史上在 Alpha 上使用显式屏障（`smp_read_barrier_depends()`）。这是弱内存模型踩坑的教科书案例。

### 11.4.2　x86 "processor ordering" 的澄清

Intel 在 2007–2008 年的澄清（Intel SDM rev.27 / AMD 文档 3.17，2008 年 11 月）把早期模糊的"processor ordering"收敛为 TSO 形式化。白皮书《Intel 64 Architecture Memory Ordering White Paper》（文档号 318147，2007）是这一澄清的关键文件。Sarkar/Sewell 等的 Cambridge 团队推动了这一形式化。

### 11.4.3　ARMv8 multicopy-atomic 修订

ARMv8 于 2017 年修订为 multicopy-atomic 模型（旧模型允许"写先对部分线程可见再对所有线程可见"，但因未被产品实现利用而去除）。Pulte 等在 POPL 2018《Simplifying ARM Concurrency》（被引超 240）给出 axiomatic 与 operational 两套等价模型。

## 11.5　小结

一致性模型与连贯性协议的定义有两类风格：操作化（抽象机，直观）与公理化（happens-before + acyclicity，适合验证）。Litmus 测试（SB 区分 SC/TSO，MP 区分 TSO/松弛）是探索模型行为的标准工具。herdtools7（diy7/herd7/litmus7）是 litmus 工具链。验证手段分形式化方法（Murphi 模型检测、Coq/Isabelle 定理证明、TLA+）与硬件测试。历史教训：Alpha 21164 的数据依赖漏洞、x86 processor ordering 的 TSO 澄清（2007–2008）、ARMv8 的 multicopy-atomic 修订（2017）。

## 参考文献

1. Owens S., Sarkar S., Sewell P. A better x86 memory model: x86-TSO. TPHOLs 2009. https://www.cl.cam.ac.uk/~pes20/weakmemory/x86tso-paper.tphols.pdf
2. Alglave J., Maranget L., Tautschnig M. Herding cats. *ACM TOPLAS*, 2014. http://www0.cs.ucl.ac.uk/staff/j.alglave/papers/toplas14.pdf
3. herdtools7. https://github.com/herd/herdtools7
4. Pulte C., Flur S., Deacon W., et al. Simplifying ARM concurrency: Multicopy-atomic axiomatic and operational models for ARMv8. POPL 2018. https://doi.org/10.1145/3158107
5. Intel. *Intel 64 Architecture Memory Ordering White Paper*. 318147, 2007. https://www.cs.cmu.edu/~410-f10/doc/Intel_Reordering_318147.pdf
6. RISC-V. *RVWMO Explanatory Material*. https://docs.riscv.org/reference/isa/v20260120/unpriv/mm-eplan.html
7. Russ Cox. *Hardware memory models*. https://research.swtch.com/hwmm
8. Bornholt J. *Memory models tutorial*. https://jamesbornholt.com/blog/memory-models/
9. Lustig D., et al. Automated synthesis of comprehensive memory model litmus test suites. ASPLOS 2017. https://research.nvidia.com/sites/default/files/pubs/2017-04_Automated-Synthesis-of/ASPLOS_2017_Memory_Model_Verification.pdf
10. CMU. *Murphi coherence lab*. https://users.ece.cmu.edu/~bgold/teaching/coherence.html
11. Flash parameterized verification. CHARME 2001. http://mcmil.net/pubs/CHARME01.pdf
12. UMD. *Alpha reordering*. https://www.cs.umd.edu/~pugh/java/memoryModel/AlphaReordering.html
13. McKenney P. *Memory ordering in modern microprocessors*. http://www.rdrop.com/users/paulmck/scalability/paper/ordering.2007.09.19a.pdf
14. Cambridge weak memory project. https://www.cl.cam.ac.uk/~pes20/weakmemory/
15. SIGARCH blog. *GPU memory consistency testing*. https://www.sigarch.org/gpu-memory-consistency-specifications-testing-and-opportunities-for-performance-toolting/
16. Sorin D. J., Hill M. D., Wood D. A. *A Primer on Memory Consistency and Cache Coherence* (2nd ed.). 2020, Chapter 11. https://pages.cs.wisc.edu/~markhill/papers/primer2020_2nd_edition.pdf
