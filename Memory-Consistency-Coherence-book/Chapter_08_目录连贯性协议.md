# 第 8 章　目录连贯性协议

> **核心命题**　当核数超出总线带宽时，目录协议把"哪个缓存有这份副本"的信息集中存放，请求只发给目录知道的 sharer，避免广播。本章讨论目录结构、状态表示、可扩展性优化，以及 SGI Origin 2000、AMD HyperTransport、Intel QPI 等案例。

---

## 8.1　目录协议介绍

监听协议的根本瓶颈是**广播**——每个请求发给所有缓存。当核数增加到几十、几百时，广播的带宽开销与延迟变得不可接受。

**目录协议**（directory protocol）的核心思想：为每个内存块维护一个**目录项**（directory entry），记录哪些缓存持有该块的副本（sharer set）与状态。请求只发给目录已知的相关 sharer，**避免广播**。

目录协议是大型 ccNUMA（Cache-Coherent Non-Uniform Memory Access）系统的主流方案。

## 8.2　基准目录系统

### 8.2.1　目录系统模型

基准目录系统：每个内存块对应一个目录项，记录 sharer 位图（每个核一位）与状态（如目录侧的 D（Dirty，某核持有 M 副本）、S（Shared，若干核持有 S 副本）、U（Uncached，无缓存））。

### 8.2.2　高层次协议规范

目录协议的状态机与监听类似（MSI/MESI/MOESI），但事务通过**点对点消息**而非总线广播：

- 缓存 miss → 发请求给 home node（该块所在节点）；
- home node 查目录项，转发请求给相关 sharer（或自己提供数据）；
- sharer 响应（invalidate ack、数据转移）。

### 8.2.3　避免死锁

目录协议的死锁风险来自循环等待（A 等 B 的响应，B 等 C，C 等 A）。标准对策（Sorin/Hill/Wood §8.2）：

- **请求/响应分离的网络**（物理或虚拟通道）；
- **多虚拟通道**（virtual channels）；
- **事务 ID** 关联请求与响应。

经典表述："A well-known solution for avoiding deadlock in coherence protocols is to use separate networks for each class of message."

### 8.2.4　详细协议规范

详细目录 MSI 协议在缓存侧与目录侧各有状态机，通过三类消息（请求、数据响应、invalidate ack）协同。

### 8.2.5　协议操作

目录协议的典型操作流程：

- load miss → GetS 给 home → home 查目录：若 D 态，转发给 dirty holder，dirty holder 写回并转 S，请求者转 S；若 S 态，home 直接提供数据，请求者转 S，sharer set 加请求者；
- store miss → GetM 给 home → home 使所有 sharer 失效（发 invalidate），收到所有 ack 后授予 M，请求者转 M。

### 8.2.6　协议简化

某些瞬态状态在目录侧可简化（如合并多个 invalidate ack）。

## 8.3　添加独占状态

目录协议同样可加 E 态（MESI）：当独占读且无人有副本时，授予 E。

## 8.4　添加拥有状态

目录协议也可加 O 态（MOESI），允许脏共享与 cache-to-cache 转移。

## 8.5　表示目录状态

目录状态表示是目录协议的核心开销，由 Agarwal & Simoni 在 ISCA 1988《An Evaluation of Directory Schemes for Cache Coherence》中系统分类：

### 8.5.1　粗略目录

**粗略目录**（coarse directory）：多位图，多位代表一组核。节省存储但增加无效化广播量（一个位覆盖多个核，invalidate 时广播给整组）。

### 8.5.2　有限指针目录

**有限指针目录**（limited pointer directory）：固定数量指针（如 i 个指针指向 i 个 sharer）。超限时降级为广播。LimitLESS（Chaiken/Kubiatowicz/Agarwal, MIT, ~1990）是硬件有限指针 + 软件 trap 维护全位图语义的混合方案。

## 8.6　目录组织

### 8.6.1　基于 DRAM 的目录缓存

目录存放在 DRAM 中（与内存一同分布），SRAM 目录缓存缓存热点目录项。

### 8.6.2　包容性目录缓存

**包容性目录缓存**（inclusive directory cache）：目录内容与缓存严格一致——目录命中即可知 sharer，但 LLC 替换某行时需向上层发 back-invalidation 维持包容不变量。

### 8.6.3　空目录缓存（无后备存储）

**空目录缓存**（null directory cache）：无 DRAM 后援。目录未命中时视为"sharer 全集"（退化为广播）或回查缓存。节省目录容量但增加广播。

## 8.7　性能和可扩展性优化

### 8.7.1　分布式目录

**分布式目录**（distributed directory）：目录与内存一同分布到各节点（home node），避免单点瓶颈。Stanford DASH（Lenoski 等，1992）与 SGI Origin 2000 的核心设计。

### 8.7.2　非阻塞目录协议

非阻塞目录协议允许目录同时处理多个未完成请求。

### 8.7.3　没有点对点排序的互连网络

某些互连网络不保证点对点消息的顺序，协议需用序列号或时间戳重新排序。

### 8.7.4　静默与非静默逐出 S 状态的数据块

**静默逐出 S**（silent eviction）：S 态块被替换时不通知目录（dirty=0），节省一次上行消息。代价是下次有人请求 M 时目录可能误以为它还是 sharer，需额外处理。

## 8.8　案例研究

### 8.8.1　SGI Origin 2000

**SGI Origin 2000**（Laudon & Lenoski, ISCA 1997，被引超千次）是目录式 ccNUMA 的商业典范。每内存块附一个目录项；用 CrayLink fat-tree 互连，单系统可扩至 512 处理器 / 512 GB。其架构直接继承自 Stanford DASH。

### 8.8.2　相干超传输

**AMD HyperTransport（HT）相干 / HT Assist**：在 HyperTransport 3.0 上引入基于目录的连贯性。每个 home node 维护一个目录，记录"本节点内存的哪些行被远端缓存持有"，把广播 snoop 替换为目标化消息。奠基论文：Conway 等《Cache Hierarchy and Memory Subsystem of the AMD Opteron Processor》（*IEEE Micro* 30(2): 16–29, 2010）。

### 8.8.3　超传输助手

HT Assist 是 HyperTransport 相干的具体实现机制，用 probe filter（探测过滤器）减少 snoop 流量。

### 8.8.4　Intel QPI

**Intel QuickPath Interconnect（QPI）**（2008，随 Nehalem 微架构推出）取代前端总线（FSB），用于多 socket 系统的缓存连贯互连。QPI 采用 4–5 层架构（物理、链路、路由、传输、协议），协议层支持 cache-to-cache 转移和面向低延迟、高可扩展的 snoop 协议。后来由 UPI（Ultra Path Interconnect）接替。

## 8.9　讨论和目录协议的未来

目录协议是大型 ccNUMA 的主流方案。未来方向包括：

- **众核可扩展目录**：如 Cuckoo Directory（Ferdman 等 HPCA 2011）用 cuckoo hashing 解决目录冲突；
- **混合 snoop/directory**：在小范围内用 snoop（低延迟），大范围内用 directory（省带宽）；
- **异构一致性域**：CXL 等技术让 CPU 与加速器共享一致性域。

## 8.10　小结

目录协议通过集中存放 sharer 信息避免广播，是大型 ccNUMA 的主流方案。目录状态表示有全位图、粗略目录、有限指针（LimitLESS）等方案。目录组织有 DRAM 目录、包容性目录、空目录等。分布式目录是可扩展性的核心（SGI Origin 2000）。SGI Origin 2000（ccNUMA 典范）、AMD HT Assist（Opteron 目录）、Intel QPI（Nehalem 取代 FSB）是代表性案例。Cuckoo Directory 等新技术面向众核扩展。

## 参考文献

1. Sorin D. J., Hill M. D., Wood D. A. *A Primer on Memory Consistency and Cache Coherence* (2nd ed.). 2020, Chapter 8 (with Section 8.2 excerpt). https://pages.cs.wisc.edu/~markhill/papers/primer2020_2nd_edition.pdf
2. Agarwal A., Simoni R., et al. An evaluation of directory schemes for cache coherence. ISCA 1988. https://people.eecs.berkeley.edu/~kubitron/courses/cs252-F03/handouts/papers/p353-agarwal.pdf
3. Lenoski J., Gharachorloo K., Gupta A., Horowitz M., Hennessy J. The Stanford DASH multiprocessor. *IEEE Computer*, 1992, 25(3): 63–79. https://www.computer.org/csdl/magazine/co/1992/03/r3063/13rRUxjyXam
4. Laudon J., Lenoski D. The SGI Origin: A ccNUMA highly scalable server. ISCA 1997. https://www.cs.umd.edu/class/fall2019/cmsc714/readings/SGI-Origin-2000.pdf
5. Conway P., Kalyanasundharam N., Donley G., Lepak K., Hughes B. Cache hierarchy and memory subsystem of the AMD Opteron processor. *IEEE Micro*, 2010, 30(2): 16–29. https://ece757.ece.wisc.edu/uw-only/10_opteron.pdf
6. Intel. *QuickPath Interconnect introduction*. https://www.intel.com/content/www/us/en/io/quickpath-technology/quick-path-interconnect-introduction-paper.html
7. Chaiken D., Kubiatowicz J., Agarwal A. LimitLESS directories. MIT LCS TM-448, ~1990. https://dspace.mit.edu/bitstream/handle/1721.1/149175/MIT-LCS-TM-448.pdf
8. Ferdman M., et al. Cuckoo directory: A scalable directory for many-core systems. HPCA 2011. https://www.cs.cmu.edu/~18742/papers/Ferdman2011.pdf
9. Sorin D. J. *Coherence for multiprocessors*. Duke WDDD 2012. https://people.ee.duke.edu/~sorin/papers/wddd12_coherence.pdf
10. gem5. *Sorin et al. Excerpt 8.2*. https://www.gem5.org/_pages/static/external/Sorin_et-al_Excerpt_8.2.pdf
