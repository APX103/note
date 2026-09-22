# 第 7 章　监听协议

> **核心命题**　监听协议通过共享总线广播所有请求，让各缓存监听总线上事务并据此更新状态。本章从基准 MSI 监听协议逐步扩展到 MESI/MOESI，并讨论非原子总线、分割事务总线与总线优化，最后用 Sun Starfire E10000 与 IBM Power5 作为案例。

---

## 7.1　监听简介

**监听协议**（snooping protocol）是最早的缓存连贯性协议，依赖一条所有缓存共享的**广播介质**（早期是物理总线 bus，后期是逻辑总线 logical bus）。每个事务广播到所有缓存的**监听器**（snooper），各自根据自身状态响应。

监听的优势是**简单低延迟**——所有缓存都"听到"每个事务，无需查找"谁有副本"。代价是**可扩展性差**——总线带宽随核数线性下降（n 个核分摊固定带宽，每核带宽 ∝ 1/n）。

监听协议是小型 SMP（对称多处理器，2–16 核）的主流方案。

## 7.2　基准监听协议

### 7.2.1　高级协议规范

基准监听 MSI 协议建立在"原子请求 + 原子事务"的系统模型上：请求发出后立即被所有缓存看到，数据响应也立即返回，不引入瞬态状态。

### 7.2.2　简单监听系统模型：原子请求，原子事务

最简单的监听模型假设总线是**原子的**——所有缓存同时看到每个事务。MSI 状态机在这个模型下非常简洁：

- 处理器 load miss（I 态）→ 发 GetS 广播，所有缓存看到，有 M 副本的写回并转 I，自己收到数据后转 S；
- 处理器 store（I/S 态）→ 发 GetM 广播，所有缓存使副本失效（转 I），自己收到数据后转 M。

### 7.2.3　基准监听系统模型：非原子请求、原子事务

真实系统中请求不是原子的——GetM 发出后需要等待数据响应，期间的块处于**瞬态状态**（transient states）：

- **IS**：I → S 过渡（已发 GetS，等数据）；
- **IM**：I → M 过渡（已发 GetM，等数据）；
- **SM**：S → M 过渡（已发 GetM，等 invalidate ack）。

瞬态状态的引入使状态机更复杂，但允许请求与响应分离。

### 7.2.4　运行示例

考虑 P1 写 X（初值 0，所有缓存为 I）：

1. P1 发 GetM，X 处于 IM；
2. 内存返回 X 的数据给 P1；
3. P1 转 M，写 X = 42。

P2 读 X：

1. P2 发 GetS，X 处于 IS；
2. P1（M 态）听到 GetS，写回 X = 42 给内存，转 S；
3. 内存返回 42 给 P2；
4. P2 转 S。

### 7.2.5　协议简化

某些瞬态状态可以被合并或简化，例如在原子请求模型下 IS/IM 可省略。

## 7.3　添加独占状态

### 7.3.1　动机

MSI 在写一个只有自己有副本的块时，仍需发 GetM（虽然无人需要 invalidate），浪费带宽。**E（Exclusive）状态**解决这个问题。

### 7.3.2　到达独占状态

当缓存独占读一个块（无人有副本）时，内存返回数据并授予 E 态——干净独占。后续写 E→M 无需任何总线事务（RFO 优化）。

### 7.3.3　协议的高级规范

MESI（M、E、S、I）的状态机比 MSI 多一个 E 态。E→M 转换无总线消息，是 MESI 相对 MSI 的核心优化。

### 7.3.4　详细规范

MESI 的详细状态机在 Intel 处理器上沿用，其 RFO（Request For Ownership）术语用于 S→M 转换（需广播 invalidate）。

### 7.3.5　运行实例

P1 独占读 X（所有缓存为 I）：内存返回 X，授予 E。P1 写 X：E→M，无总线事务。这比 MSI（需发 GetM）省了一次总线消息。

## 7.4　添加拥有状态

### 7.4.1　动机

MESI 的 M 态是脏独占——其他缓存要读时，M 态缓存必须先写回内存，再让请求者从内存读，延迟高。**O（Owned）状态**允许脏共享——O 态缓存可直接向请求者提供数据，无需写回内存。

### 7.4.2　高层级协议规范

MOESI（M、O、E、S、I）增加 O 态：脏共享。O 态缓存是 owner，可向 S 态请求者直接提供数据。

### 7.4.3　详细协议规范

MOESI 是 AMD64 架构的官方连贯性协议（AMD64 Architecture Programmer's Manual Vol.2 §7）。

### 7.4.4　运行实例

P1（M 态）听到 P2 的 GetS：P1 转 O（脏共享），直接把数据发给 P2，P2 转 S。无需写回内存，延迟低。

## 7.5　非原子总线

### 7.5.1　动机

真实总线是**分割事务**（split-transaction）的——请求者发出请求后释放总线，数据响应在之后某时刻到达。这提升总线利用率，但增加瞬态状态冲突与死锁风险。

### 7.5.2　顺序响应与乱序响应

分割事务总线的响应可能**乱序**到达（后发的请求先得到响应），需要事务 ID 关联请求与响应。

### 7.5.3　非原子系统模型

非原子模型需要处理瞬态状态的并发——同一块的多个 miss 可能交错。

### 7.5.4　使用分割事务总线的一个 MSI 协议

分割事务 MSI 协议需要为每个未完成的请求维护瞬态状态，并通过事务 ID 关联。

### 7.5.5　一个优化的、非阻塞的使用分割事务总线 MSI 协议

进一步优化：非阻塞的分割事务总线监听协议允许缓存继续服务其他 miss，而非阻塞在单个 miss 上——通过为每个未完成 miss 维护独立瞬态状态，实现并行处理。

## 7.6　总线互连网络的优化

### 7.6.1　用于数据响应的独立非总线网络

把数据响应走独立网络（不经过总线），释放总线给请求。

### 7.6.2　用于连贯性请求的逻辑总线

物理上已不是单条总线（而是交叉开关或片上网络），但通过**强制全局排序**让所有缓存看到事务的同一顺序，从而保留监听语义——这是**逻辑总线**（logical bus）。

## 7.7　案例研究

### 7.7.1　Sun Starfire E10000

Sun Starfire（Ultra Enterprise E10000，1997）是 64 处理器 SMP 服务器，由 Erik Hagersten 等设计。它采用基于 Gigaplane-XB 交叉开关的广播式监听，通过 centerplane 上的全局地址路由器（global address router）把 snoop 地址经四条地址总线（ABUS0–ABUS3）广播到全部 16 块系统板，数据经 16×16 crossbar 返回。它是把广播监听扩展到数十处理器规模的代表案例。

### 7.7.2　IBM Power5

IBM Power5（2004）使用分布式 + 监听混合（hybrid snoop/directory）协议——既保留监听的低延迟，又用目录结构节省带宽。

## 7.8　监听协议的未来

监听协议在小型 SMP（2–16 核）仍是主流，但其可扩展性瓶颈（总线带宽 ∝ 1/n）限制了它在更大规模的应用。数十核以上的系统普遍转向目录协议（第 8 章）或混合方案。

## 7.9　小结

监听协议通过共享总线广播所有请求，让各缓存监听并响应。基准 MSI 监听协议在原子模型下最简单；非原子请求引入 IS/IM/SM 瞬态状态。MESI 增加 E（干净独占，RFO 优化，Intel），MOESI 增加 O（脏共享，AMD64）。分割事务总线提升利用率但增加复杂度。Sun Starfire E10000（64 核广播监听）与 IBM Power5（混合 snoop/directory）是代表性案例。监听协议的可扩展性瓶颈是总线带宽，限制了它在大型系统中的应用。

## 参考文献

1. Sorin D. J., Hill M. D., Wood D. A. *A Primer on Memory Consistency and Cache Coherence* (2nd ed.). 2020, Chapter 7. https://pages.cs.wisc.edu/~markhill/papers/primer2020_2nd_edition.pdf
2. Papamarcos M. S., Patel J. H. A low-overhead coherence solution for multiprocessors with private cache memories. ISCA 1984. (MESI / Illinois 协议)
3. AMD. *AMD64 Architecture Programmer's Manual, Vol. 2, §7*. https://www.cse.wustl.edu/~roger/569M/24593.pdf
4. Hagersten E., et al. Sun Starfire E10000 interconnect. https://dl.acm.org/doi/pdf/10.1145/509593.509630
5. UW-Madison ECE757. *Coherence lecture*. https://ece757.ece.wisc.edu/lect06-coherence.pdf
6. CMU 15-418. *Snoop implementation*. https://www.cs.cmu.edu/afs/cs/academic/class/15418-s19/www/lectures/12_snoopimpl.pdf
7. MIT 6.823. *Split-transaction bus*. https://csg.csail.mit.edu/6.823S20/Lectures/L14.pdf
8. ETH. *MOESI state machine*. https://spcl.inf.ethz.ch/Teaching/2014-dphpc/lecture/lecture2-cache-coherence.pdf
9. Rice COMP522. *MESI on split-transaction bus*. https://www.cs.rice.edu/~johnmc/comp522/lecture-notes/COMP522-2019-Lecture5-Cache-Coherence-I.pdf
10. Kalla R., Sinharoy B., Tendler J. M. IBM Power5 chip: A dual-core multithreaded processor. *IEEE Micro*, 2004, 24(2): 40–47.
