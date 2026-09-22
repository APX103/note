# 第 10 章　异构系统的一致性和连贯性

> **核心命题**　GPU 与 CPU 协同时，一致性模型与连贯性协议都需要重新设计。GPU 数万并发线程使传统每核目录/监听协议不可扩展，催生了时间连贯性与释放一致性导向的连贯性。CXL（2019）、Apple Silicon UMA、AMD Infinity Fabric 让 CPU-GPU 间硬件连贯性成为主流。

---

## 10.1　GPU 的一致性和连贯性

### 10.1.1　早期的 GPU：架构和编程模型

GPU（Graphics Processing Unit）最初专为图形渲染设计，采用 **SIMT**（Single-Instruction Multiple-Thread）执行模型。SIMT 由 NVIDIA 在 2008 年的 Tesla 架构（Lindholm 等，*IEEE Micro* 28(2): 39–55）正式定义：一个 **warp**（NVIDIA，32 线程）或 **wavefront**（AMD，历史 64 线程）在 lockstep 执行同一条指令。

早期 GPU 的设计哲学是**无缓存连贯性**（coherence-free）——GPU 内部的 L1 缓存不维护连贯性，程序员通过显式同步（barrier、kernel 边界）保证数据可见。这与 CPU 的"硬件连贯性"形成鲜明对比。

权威 GPU 教材：Kirk & Hwu《Programming Massively Parallel Processors》（2010 第 1 版，2022 第 4 版）。

### 10.1.2　宏观视角：GPGPU 的一致性和连贯性

GPGPU（General-Purpose computing on GPU）的出现——CUDA（NVIDIA，2007）、OpenCL（Khronos，2009）、SYCL——让 GPU 承担通用计算，对共享内存与原子操作的需求浮现。但 GPU 的规模（NVIDIA H100 每 SM 2048 个线程，全芯片数万线程）使传统每核目录/监听协议代价高昂——这是 GPU 连贯性挑战的核心。

### 10.1.3　时间连贯性

**时间连贯性**（Temporal Coherence, TC）是 GPU 连贯性的奠基工作（Singh 等，HPCA 2013，被引超 217）。核心思想：

- 基于全局同步计数器（globally synchronized counters），在有效时间窗内 cache line 被授予临时独占权；
- 无需持续目录/监听消息——文献称其为"coherence-free"；
- 显式利用 GPU 的释放一致性导向（RC-directed）内存模型。

TC 是 GPU 主流的"同步点刷出挂起写"模型的形式化体现。后续工作如 Turn-based Spatiotemporal Coherence 进一步优化了这一框架。

### 10.1.4　释放一致性导向的连贯性

**释放一致性导向的连贯性**（release-consistency-directed coherence）：仅在 acquire/release（同步点）触发连贯性动作，普通访问不触发。Sinclair & Adve（MICRO 2015）描述的机制是"acquire 时刷整个 cache、release 前缓冲写"。

**NVIDIA Volta（2017）的 per-thread 内存模型**是 GPU 一致性的关键里程碑：随 CUDA 9 / PTX ISA 6.0 引入 Independent Thread Scheduling 与首个精细的 per-thread scoped 内存一致性模型，提供 acquire/release 语义。PTX 提供 `ld.acquire` / `st.release` / `fence` 带作用域（如 `gpu.cta` 块作用域、`gpu.sys` 系统作用域）。

NVIDIA PTX 内存模型的形式化分析由 Lustig 等在 ASPLOS 2019《A Formal Analysis of the NVIDIA PTX Memory Consistency Model》完成。作用域的性能差距显著——公开资料显示 block-scoped fence 可比 device-scoped 快约 21×。

## 10.2　不仅仅是 GPU：探索更多的异构性

### 10.2.1　异构系统的一致性模型

异构系统（CPU TSO + GPU 松弛 RC + 加速器更松）的一致性模型统一依赖：

- **作用域（scope）显式标注**同步可见范围（PTX 的 `gpu.cta`/`gpu.sys`，Vulkan/HIP 类似机制）；
- **acquire/release fence** 在异构边界上承担"传播写"的职责。

**OpenCL 2.0**（Khronos，2013）引入 SVM（Shared Virtual Memory）三档与 C11/C++11 风格内存模型。**HSA Foundation**（2012，AMD/ARM/Qualcomm 等）定义 HSAIL 中间语言与 HSA 内存模型（兼容 C++11/Java/OpenCL/.NET）。

### 10.2.2　异构系统的连贯性协议

异构系统的连贯性协议：

- **CXL（Compute Express Link，2019）**：建立在 PCIe 物理层之上，用硬件管理的 MESI 协议在 CPU 与设备间建立单一连贯性域。三种子协议：CXL.io（I/O）、CXL.cache（设备 coherent cache）、CXL.memory（内存扩展）。设备分 Type 1/2/3。
- **AMD Infinity Fabric**：在 CDNA 架构（MI200/MI300）上提供 CPU-GPU 间 coherent fabric 与零拷贝内存访问。
- **Apple Silicon UMA**：Apple M1（2020）采用统一内存架构，CPU 与 GPU 共享同一物理内存，无需数据拷贝；M1 Ultra（2022）将 UMA 扩展至 128 GB。
- **NVLink-C2C**：NVIDIA 的 CPU-GPU coherent 链路（Grace Hopper）。

CCIX 与 Gen-Z 曾是 CXL 的竞争方案，但 Gen-Z 于 2021–2022 并入 CXL Consortium，CCIX 失去势头，CXL 成为异构连贯性的事实标准。

## 10.3　进一步阅读资料

- Singh 等 HPCA 2013（GPU 时间连贯性）；
- Sinclair & Adve MICRO 2015（GPU 同步无 scope）；
- Lustig 等 ASPLOS 2019（PTX 内存模型形式化）；
- CXL Consortium 官方规范。

## 10.4　小结

GPU 的 SIMT 架构与数万并发线程使传统连贯性协议不可扩展，催生了时间连贯性（Singh 2013）与释放一致性导向的连贯性（Sinclair 2015）。NVIDIA Volta（2017）引入 per-thread scoped 内存模型。异构系统的一致性统一依赖作用域与 acquire/release fence。CXL（2019）成为 CPU-加速器硬件连贯性的事实标准，AMD Infinity Fabric 与 Apple Silicon UMA 是另两条路线。Gen-Z 并入 CXL 后，CXL 主导了异构连贯性的未来。

## 参考文献

1. Lindholm E., Nickolls J., Oberman S., Montrym J. NVIDIA Tesla: A unified graphics and computing architecture. *IEEE Micro*, 2008, 28(2): 39–55.
2. Kirk D. B., Hwu W. W. *Programming Massively Parallel Processors: A Hands-on Approach*. Elsevier, 4th ed. 2022.
3. Singh I., et al. Cache coherence for GPU architectures. HPCA 2013. https://www.cs.sfu.ca/~ashriram/papers/2013_HPCA_GPUCoherence.pdf
4. Sinclair M. D., Adve S. V. Efficient GPU synchronization without scopes. MICRO 2015. http://rsim.cs.illinois.edu/Pubs/15-MICRO-scopes.pdf
5. Lustig D., Sahasrabuddhe S., Giroux O. A formal analysis of the NVIDIA PTX memory consistency model. ASPLOS 2019. https://research.nvidia.com/publication/2019-04_formal-analysis-nvidia-ptx-memory-consistency-model
6. NVIDIA. *H100 Architecture Whitepaper*. https://www.techpowerup.com/gpu-specs/docs/nvidia-gh100-architecture.pdf
7. NVIDIA. *PTX ISA*. https://docs.nvidia.com/cuda/parallel-thread-execution/index.html
8. Khronos. *OpenCL 2.0 specification*. 2013. https://www.khronos.org/news/press/khronos-finalizes-opencl-2.0-specification-for-heterogeneous-computing
9. ACM. *CXL survey*. https://dl.acm.org/doi/full/10.1145/3669900
10. CXL Consortium. https://computeexpresslink.org/
11. Apple Newsroom. *Apple M1*. https://www.apple.com/newsroom/2020/11/apple-unleashes-m1/
12. AMD. *MI200 architecture*. Hot Chips 34, 2022. https://old.chipsandcheese.com/2022/09/18/hot-chips-34-amds-instinct-mi200-architecture/
13. HSA Foundation. https://en.wikipedia.org/wiki/Heterogeneous_System_Architecture
14. SIGARCH blog. *GPU memory consistency*. https://www.sigarch.org/gpu-memory-consistency-specifications-testing-and-opportunities-for-performance-toolting/
15. Lustig D., et al. Mixed-Proxy extensions for PTX. ISCA 2022. https://graymalk.in/papers/isca22.pdf
