# 第 3 章　内存一致性的动机以及连续一致性

> **核心命题**　内存一致性模型规定多个线程看到的内存操作全局顺序。Lamport 的连续一致性（SC）是最直观也最严格的模型——它要求所有线程看到的操作顺序等于某种全局交错。SC 是理解所有后续一致性模型（TSO、松弛）的基准。

---

## 3.1　共享内存行为的问题

考虑两个处理器 P1、P2 共享两个变量 flag 与 data（初值都为 0）：

```
P1:                        P2:
data = 42;                 while (flag == 0);
flag = 1;                  print(data);
```

程序员的直觉是：P2 退出循环后，data 一定是 42——因为 P1 先写 data 再写 flag。但在真实多处理器硬件上，**这个直觉可能被打破**：

- 如果硬件把 P1 的两个 store 重排（先写 flag 后写 data），P2 可能读到 flag = 1 但 data 还是 0；
- 如果硬件把 P2 的两个 load 重排（先读 data 后读 flag），同样会出问题。

这就是**共享内存行为的问题**：程序员需要一份"契约"来知道什么样的行为是合法的、什么样的重排是被允许的。这份契约就是**内存一致性模型**。

## 3.2　什么是内存一致性模型

**内存一致性模型**（memory consistency model）规定了多处理器共享内存行为的合法边界——它定义了"什么样的执行结果是合法的"。

一个一致性模型需要回答：

- 一个 load 可以读到哪些值？（最近的写？还是可能更早的写？）
- 不同地址的操作可以被重排吗？
- 同一地址的多个操作必须保持什么顺序？
- 原子指令（lock、compare-and-swap）的语义是什么？

不同的硬件平台选择不同的一致性模型：x86 选择 TSO，ARM/RISC-V/POWER 选择松弛模型。理解这些模型的差异是并行编程的基础。

## 3.3　一致性与连贯性的对比

第 2 章定义的**连贯性**（coherence）与本章的**一致性**（consistency）容易混淆，但二者是不同层次的概念：

| 概念 | 范围 | 关注点 |
|---|---|---|
| 连贯性 | 单个内存位置 | 写入是否对所有缓存可见（SWMR、数据值不变量） |
| 一致性 | 所有内存位置 | 多线程看到的操作全局顺序 |

关键关系：**连贯性是一致性的必要非充分条件**。没有连贯性，SC 一定不成立（因为陈旧值会破坏 SC 的"load 读最近写"语义）。但有连贯性，SC 仍可能不成立（因为不同地址的操作可以被重排）。

## 3.4　连续一致性（SC）的基本思想

**连续一致性**（Sequential Consistency, SC）由 Leslie Lamport 在 1979 年的奠基论文《How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs》（*IEEE TC* 28(9): 690–691）中提出。SC 的核心定义：

> 一次多处理器执行的执行结果等于把所有处理器的操作按某种单一全局顺序排列的结果，且每个处理器自身的操作在此顺序中保持其程序顺序。

用更通俗的话：**SC 等价于一个"全局交换开关"模型**——想象所有处理器的 load/store 操作串行经过一个共享内存开关，任一时刻只允许一个操作通过。每个处理器看到的内存操作顺序就是这个全局顺序。

SC 的两个关键约束：

1. **保持程序顺序**：每个处理器内，操作按程序文本顺序出现在全局顺序中；
2. **单一全局顺序**：所有处理器看到同一个全局顺序（没有"两个处理器看到不同顺序"的情况）。

## 3.5　一点关于 SC 形式化的内容

SC 的形式化可以用"存在一个全局线性序 <"来表述：

- 若操作 a 在某核的程序序中先于操作 b（a →_program b），则 a < b；
- 每个 load 读到的值是 < 中最近一次同地址 store 的值。

这个形式化简洁但极其严格——它禁止了所有重排（除了同一处理器内程序序本就保持的）。

## 3.6　朴素的 SC 实现

SC 的最朴素实现：把所有核的 load/store 串行经过一个**全局交换开关**（multiswitch）——任一时刻只允许一个内存操作通过。这完全符合 SC 的"单一全局顺序"直觉，但代价是**完全串行化**——性能极差。

这个朴素模型不可用于实际硬件，但它给出了 SC 的"参考实现"，便于理解。

## 3.7　具有缓存连贯性的基本 SC 实现

真实的 SC 实现借助缓存连贯性来并行化：

- 每个核独占执行，load 直接从自己缓存读（命中时无开销）；
- store 时，先通过连贯性协议**使其他缓存中该地址的副本失效**（invalidate），获得独占权后再写。

关键约束：**在 SC 下，store 必须等其他核的 invalidate ack 全部返回后才能提交**。否则，本核后续的 load 可能在其他核还持有旧副本时读到自己刚写的值，破坏全局顺序。

## 3.8　具有缓存连贯性的优化 SC 实现

第 3.7 节的基本实现有一个性能瓶颈：store 必须等 invalidate ack。能否用 store buffer 优化？

答案是有条件地可以：**store buffer 不得让本核后续的 load 绕过未完成的自己 store**。如果允许绕过（即 store forwarding 但 load 从内存读），就破坏了 SC——这正是 TSO 放松的点（见第 4 章）。

所以在严格 SC 实现中，store buffer 的使用受限——要么 store 不进 buffer，要么 load 必须先检查 buffer。

## 3.9　SC 的原子操作

SC 下的原子操作（read-modify-write，如 test-and-set、compare-and-swap）必须在全局顺序中**占单个不可分割的位置**——即读和写在全局顺序中是连续的，中间不能插入其他操作。

这要求连贯性协议提供"独占 + 原子"的保证——通常通过 lock 前缀（x86）、LR/SC（RISC-V/ARM）或专门的原子指令实现。

## 3.10　将它们放在一起：MIPS R10000

MIPS R10000（1996）是 SC 在乱序执行处理器上的经典实现。Yeager 在《The MIPS R10000 Superscalar Microprocessor》（*IEEE Micro* 16(2): 28–40, 1996）中描述：**虽然 R10000 内部乱序执行，但它在体系结构层面仍提供 SC 与精确异常**。

机制：通过 address resolution buffer（ARB）与 graduation（按程序序提交）阶段，使乱序执行的核在体系结构层面仍呈现 SC——所有 load/store 按程序序"毕业"对外可见。

R10000 证明了 SC 在乱序核上是可行的，但代价是性能损失——这也是为什么后来的 MIPS 与大多数 RISC 转向松弛模型。

## 3.11　关于 SC 的进一步阅读资料

- Lamport 1979 原始论文（仅两页，简洁有力）；
- Adve & Gharachorloo 1996 综述《Shared Memory Consistency Models: A Tutorial》；
- Adve et al. 1990《Implementing Sequential Consistency in Cache-Based Systems》——给出 SC 的可实现性充分条件。

## 3.12　小结

SC 是最直观也最严格的一致性模型：要求所有处理器看到的操作顺序等于某种全局交错。SC 的朴素实现是全局交换开关，真实实现借助缓存连贯性但要求 store 等 invalidate ack。MIPS R10000 证明 SC 在乱序核上可行但代价高昂——这为 TSO 与松弛模型的出现铺平了道路。SC 是理解后续所有一致性模型的基准。

## 参考文献

1. Lamport L. How to make a multiprocessor computer that correctly executes multiprocess programs. *IEEE Transactions on Computers*, 1979, C-28(9): 690–691. https://doi.org/10.1109/TC.1979.1675439
2. Adve S. V., Gharachorloo K. Shared memory consistency models: A tutorial. *IEEE Computer*, 1996, 29(12): 66–76. https://doi.org/10.1109/2.546611
3. Yeager K. C. The MIPS R10000 superscalar microprocessor. *IEEE Micro*, 1996, 16(2): 28–40. https://doi.org/10.1109/40.491460
4. Adve S. V., Hill M. D., et al. Implementing sequential consistency in cache-based systems. ICCP 1990. http://rsim.cs.uiuc.edu/Pubs/ps2pdf/iccp90.pdf
5. Sorin D. J., Hill M. D., Wood D. A. *A Primer on Memory Consistency and Cache Coherence* (2nd ed.). 2020, Chapter 3. https://pages.cs.wisc.edu/~markhill/papers/primer2020_2nd_edition.pdf
6. UCSD CSE 240A. *MIPS R10000 lecture*. https://cseweb.ucsd.edu/classes/wi13/cse240a/pdf/04/MIPS_R10K.pdf
