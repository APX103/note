# 第 5 章　松弛内存一致性

> **核心命题**　现代 RISC（RISC-V RVWMO、IBM POWER、ARMv8）普遍采用松弛一致性模型，允许编译器与硬件大幅重排内存操作以隐藏延迟。本章讨论 XC 示例模型、释放一致性（RC）、数据竞争自由（DRF）契约，以及商用松弛模型的差异。

---

## 5.1　动机

### 5.1.1　重排序内存操作的机会

SC 与 TSO 都限制了内存操作的重排。但现代处理器有大量机制可以受益于更激进的重排：

- **非阻塞缓存**（non-blocking cache）：miss 时不阻塞后续 hit；
- **乱序执行**（out-of-order execution）：load/store 可以乱序执行；
- **写合并**（write coalescing）：多个 store 合并为一次写；
- **预取**（prefetch）：提前取数据。

这些机制在 SC/TSO 下被部分限制，但**如果放松更多重排**，性能可以进一步提升。

### 5.1.2　利用重排序的机会

松弛模型的核心思想：**默认允许所有重排，仅在程序员显式要求同步时才施加顺序约束**。这通过 FENCE 指令或 acquire/release 语义实现。代价是程序员负担加重——必须正确插入 FENCE，否则会出现难以调试的并发 bug。

## 5.2　一个松弛一致性模型（XC）示例

Sorin/Hill/Wood 教材定义了一个名为 **XC**（Relaxed, Coherent）的示例模型，它具备松弛模型的所有关键特征但又不至于过于复杂。

### 5.2.1　XC 模型的基本概念

XC 允许以下重排（不同地址之间）：

- load→store
- load→load
- store→store
- store→load（与 TSO 相同）

但对**同一地址**的操作仍保持连贯性约束（load 读最近 store）。XC 只通过 FENCE 恢复顺序。

### 5.2.2　使用 XC 的 FENCE 的示例

考虑发布模式：

```
P1:                        P2:
data = 42;                 while (flag == 0);
FENCE;                     FENCE;
flag = 1;                  print(data);
```

FENCE 保证 P1 的 `data = 42` 在 `flag = 1` 之前对其他核可见，P2 的 load(flag) 在 load(data) 之前。没有 FENCE，XC 允许这些重排，发布模式会失效。

### 5.2.3　形式化 XC

XC 的形式化用"保持程序顺序"（preserved program order, PPO）关系刻画——只有被 FENCE 标记的顺序被保持，其余可重排。

### 5.2.4　展示 XC 正确运行的示例

XC 的正确性体现为：在正确使用 FENCE 的程序中，XC 的行为等价于 SC。这与下一节的 DRF 契约紧密相关。

## 5.3　实现 XC

XC 的实现比 TSO 更激进：

- store buffer 可以满负荷工作；
- 不同地址的 load/store 可以乱序；
- FENCE 通过 drain buffer + 等待 ack 实现。

### 5.3.1　在 XC 中使用原子指令

原子指令（如 LR/SC、compare-and-swap）在 XC 中自带 FENCE 语义——它们既是原子的，也施加 acquire/release 顺序。

### 5.3.2　在 XC 中的 FENCE

FENCE 在 XC 中是全屏障，drain 所有挂起的 load/store 并等待 ack。

### 5.3.3　一个警告

松弛模型的威力也是它的危险——**漏掉一个 FENCE 就会导致难以复现的并发 bug**。这正是 DRF 契约与高级语言内存模型（C++/Java）的价值所在——它们把 FENCE 的正确使用抽象到语言层。

## 5.4　无数据竞争程序的连续一致性

**数据竞争自由（DRF, Data-Race-Free）契约**是松弛模型的理论基石，由 Adve & Hill 在 1990 年 ISCA 论文《Weak Ordering – A New Definition》中提出：

> 如果一个程序是无数据竞争的（即所有冲突访问都被同步操作保护），那么它在松弛模型下的行为等价于 SC。

这就是著名的 **SC for DRF** 契约。它的意义在于：程序员只需保证程序无数据竞争（用锁、原子操作正确同步），就能享受 SC 的直观语义，同时获得松弛模型的性能。

这个契约是 C++11、Java 内存模型的理论基础——高级语言通过 SC-DRF 向程序员承诺"正确同步的程序行为等价于 SC"。

## 5.5　一些松弛模型概念

### 5.5.1　释放一致性

**释放一致性**（Release Consistency, RC）由 Gharachorloo 等人在 1990 年 ISCA 论文《Memory Consistency and Event Ordering in Scalable Shared-Memory Multiprocessors》中提出。RC 区分两类同步操作：

- **acquire**（获取，如 lock）：acquire 之后的普通访问不能重排到 acquire 之前；
- **release**（释放，如 unlock）：release 之前的普通访问不能重排到 release 之后；
- acquire 与 release 之间的普通访问可以任意重排。

RC 比 XC 更精细——它把同步语义编码到 acquire/release 标注里，减少了对显式 FENCE 的依赖。RC 影响了 Stanford DASH 多处理器，被引超 1800 次。

### 5.5.2　因果性和写原子性

松弛模型需要维护两个关键不变量：

- **写原子性**（write atomicity / multicopy atomicity）：一个 store 被所有核同时观察到。否则不同观察者可能看到不一致顺序（IRIW 反例）。
- **因果性**（causality）：禁止"自因果"循环——一个写不能由它自身推断出来（Java 内存模型特别关注这点）。

## 5.6　松弛内存模型案例研究

### 5.6.1　RVWMO

**RISC-V Weak Memory Ordering（RVWMO）**是 RISC-V 的默认内存模型，载于 RISC-V Unprivileged ISA Manual。RVWMO 的核心是**保持程序顺序（PPO, Preserved Program Order）**——共 12 条规则，分四组：

- **重叠地址规则**（3 条）：同地址操作的顺序；
- **显式同步规则**（4 条）：FENCE、acquire（aq 位）、release（rl 位）、RCsc 配对；
- **句法依赖规则**（3 条）：地址/数据/控制依赖；
- **流水线依赖规则**（2 条）：经中间 store 的传递依赖。

RVWMO 的 aq/rl 位让 AMO/LR/SC 指令携带 acquire/release 语义，无需额外 FENCE。

### 5.6.2　IBM POWER

IBM POWER 是最松的商用模型之一（在 ARMv8 之前），允许 store→load、store→store、load→load、load→store 全部重排。三类屏障：

- `sync`（重权，全屏障）；
- `lwsync`（轻权，不排 store→load）；
- `isync`（指令同步，控制依赖）。

POWER 的形式化由 Sarkar 等人在 PLDI 2011 论文《Understanding POWER Multiprocessors》中给出（被引超 380 次）。

## 5.7　进一步阅读和商用松弛内存模型

### 5.7.1　学术文献

- Adve & Gharachorloo 1996 综述（经典）；
- Alglave et al. PLDI 2014《Herding Cats》（公理化统一框架，被引超 530）；
- Maranget/Sarkar/Sewell《A Tutorial Introduction to the ARM and POWER Relaxed Memory Models》。

### 5.7.2　商用模型

ARMv8 从 ARMv7 的非多副本原子模型修订为 multicopy-atomic（Pulte 等 POPL 2018，被引超 240）。RISC-V RVWMO 是 multicopy-atomic 的。IBM POWER 是非 multicopy-atomic 的（最松）。

## 5.8　比较内存模型

### 5.8.1　松弛内存模型彼此之间以及与 TSO 和 SC 的关系

严格程度排序（从严格到松）：SC > TSO > ARMv8/RVWMO > IBM POWER。

SC 禁止所有重排；TSO 仅允许 store→load；ARMv8/RVWMO 允许大部分重排但保留 acquire/release；POWER 几乎允许所有重排。

### 5.8.2　松弛模型有多好

松弛模型在性能上明显优于 SC/TSO——尤其在多核可扩展性与隐藏延迟方面。代价是程序员负担与验证复杂度。SC-DRF 契约在很大程度上缓解了程序员负担。

## 5.9　高级语言模型

### 5.9.1　C++11 内存模型

C++11（ISO/IEC 14882:2011）引入了 `std::memory_order`，由 Boehm & Adve 在 PLDI 2008《Foundations of the C++ Concurrency Memory Model》奠基（被引超 650）。核心是 SC-DRF 契约。`memory_order` 枚举：

- `relaxed`：无序；
- `consume`：数据依赖（C++17 起建议不用）；
- `acquire`：后续读写不可重排到 acquire 之前；
- `release`：此前读写不可重排到 release 之后；
- `acq_rel`：acquire + release；
- `seq_cst`：额外保证单一全局总序（最强）。

### 5.9.2　Java 内存模型

Java 内存模型（JLS §17.4）由 Manson、Pugh、Adve 在 POPL 2005《The Java Memory Model》中提出。它用 happens-before + 因果性要求（causality requirements）刻画合法执行，纠正了原 JVM 模型的安全漏洞。

## 5.10　小结

松弛模型允许编译器与硬件大幅重排内存操作，仅在显式同步时施加顺序约束。XC 示例模型、释放一致性（RC）是代表性框架。DRF 契约（SC for DRF）是松弛模型的理论基石——无数据竞争的程序在松弛模型下行为等价于 SC。RISC-V RVWMO（13 条 PPO 规则 + aq/rl 位）与 IBM POWER（最松）是两端。C++11/Java 内存模型通过 SC-DRF 向程序员承诺直观语义。松弛模型在性能上明显优于 SC/TSO，但需要程序员正确使用 FENCE/acquire/release。

## 参考文献

1. Adve S. V., Hill M. D. Weak ordering – A new definition. ISCA 1990, pp. 2–14.
2. Adve S. V., Hill M. D. A unified formalization of four shared-memory models. *IEEE TPDS*, 1993, 4(6): 613–624. http://rsim.cs.uiuc.edu/Pubs/ps2pdf/tpds93.pdf
3. Gharachorloo K., Lenoski D., Laudon J., et al. Memory consistency and event ordering in scalable shared-memory multiprocessors. ISCA 1990, pp. 15–26. https://doi.org/10.1145/325096.325102
4. Boehm H.-J., Adve S. V. Foundations of the C++ concurrency memory model. PLDI 2008, pp. 68–78. https://doi.org/10.1145/1375581.1375591
5. Manson J., Pugh W., Adve S. V. The Java memory model. POPL 2005, pp. 378–391. https://rsim.cs.uiuc.edu/Pubs/popl05.pdf
6. Sarkar S., Sewell P., et al. Understanding POWER multiprocessors. PLDI 2011. https://www.cl.cam.ac.uk/~pes20/ppc-supplemental/pldi105-sarkar.pdf
7. Pulte C., Flur S., Deacon W., et al. Simplifying ARM concurrency: Multicopy-atomic axiomatic and operational models for ARMv8. POPL 2018. https://doi.org/10.1145/3158107
8. Alglave J., Maranget L., Tautschnig M. Herding cats. PLDI 2014. http://diy.inria.fr/herd/herding-cats-color.pdf
9. RISC-V. *Unprivileged ISA Manual, Chapter 17: RVWMO*. https://docs.riscv.org/reference/isa/v20260120/unpriv/rvwmo.html
10. Sorin D. J., Hill M. D., Wood D. A. *A Primer on Memory Consistency and Cache Coherence* (2nd ed.). 2020, Chapter 5. https://pages.cs.wisc.edu/~markhill/papers/primer2020_2nd_edition.pdf
11. Maranget L., Sarkar S., Sewell P. A tutorial introduction to the ARM and POWER relaxed memory models. https://www.cl.cam.ac.uk/~pes20/ppc-supplemental/test7.pdf
12. cppreference. *std::memory_order*. https://en.cppreference.com/cpp/atomic/memory_order
13. Pugh W. *The Java Memory Model FAQ*. https://www.cs.umd.edu/~pugh/java/memoryModel/jsr-133-faq.html
