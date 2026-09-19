# 第 11 章　SMR 许可

> **核心命题**　SMR 许可的核心挑战在于"现行监管框架是为大型核电站设计的"。本章梳理美国 NRC 监管框架、行业规范与标准、国际许可战略，并讨论监管现代化趋势（如 10 CFR Part 53、风险指引型监管）。

---

## 11.1　引言

核设施许可证（licensing）是核电站从设计到运行、退役全寿期都必须遵守的法定程序。许可证分为：

- **设计认证（Design Certification, DC）**：针对反应堆设计本身；
- **厂址许可（Site Permit）**：针对具体厂址（早期厂址许可 ESP、建造运行联合许可证 COL）；
- **运行许可（Operating License, OL）**：针对实际运行；
- **退役许可（Decommissioning）**：针对退役；
- **出口 / 进口许可**：核燃料、设备、技术；
- **保障监督**（IAEA + 国家监管）。

SMR 许可面临的核心挑战：

1. **应急计划区（EPZ）**：传统 EPZ 半径 10 英里（16 km）+ 50 英里（80 km）食入路径；SMR 因源项小、CDF 低，目标是 EPZ = 厂址边界。
2. **安保人员配置**：传统要求按大型核电站配置；SMR 单堆功率小，安保等级是否可下调？
3. **运行人员配置**：传统 1 台堆 3+ 操纵员；SMR 多机共享，人员如何配置？
4. **多机组叠加**：12 个模块的法律关系（一台许可证 vs 12 台）？
5. **新技术（液态金属、气冷、熔盐）**：现有法规（10 CFR 50、ASME BPVC）不直接适用。

## 11.2　NRC 关于 SMR 的许可

### 11.2.1　10 CFR 监管框架

美国 NRC 主要监管文件：

- **10 CFR Part 50**：传统两步许可（建造许可 CP + 运行许可 OL）；
- **10 CFR Part 52**：一步许可（建造运行联合许可证 COL）+ 设计认证 DC + 早期厂址许可 ESP；
- **10 CFR Part 53**（开发中）：针对先进反应堆（非 LWR）的新规则；
- **10 CFR Part 100**：厂址准则；
- **10 CFR Part 20**：辐射防护；
- **10 CFR Part 73**：物理保护；
- **10 CFR Part 74 / 75**：核材料衡算与保障监督。

### 11.2.2　设计认证（DC）

DC 流程：

1. 厂商提交 **DCD**（Design Control Document）；
2. NRC 进行 **审评**（typically 36–60 个月）；
3. 公开听证、提交安全评价报告（SER）；
4. **最终设计认证规则**（10 CFR Part 52 Appendix）；
5. DC 有效期 15 年，可延期。

DC 一旦获得，任何业主可基于该 DC 申请 COL，**不再重复设计审评**，仅审厂址相关事项。

### 11.2.3　SMR DC 案例

- **NuScale**：2017 年提交 DCD，2020 年 9 月获 NRC 颁发 DC（**史上首个 SMR DC**）；
- **GE Hitachi BWRX-300**：2024 年向 NRC 提交申请，目标 2026–2027 获 DC；
- **Holtec SMR-300**：已开始与 NRC 的预申请对话；
- **Kairos Power Hermes**：测试堆，2024 年获建造许可。

### 11.2.4　应急计划区（EPZ）

传统大型 LWR：

- **疏散区（Plume Exposure EPZ）**：半径 10 英里（16 km）；
- **食入区（Ingestion EPZ）**：半径 50 英里（80 km）；
- **撤离时间要求**：疏散区在事故后 4 小时内撤离。

SMR 目标：

- **EPZ = 厂址边界**（即无需场外疏散）；
- 基于源项分析（CDF × 源项 × 大气扩散）证明厂址边界外剂量低于保护行动指南（PAG）。

NRC 在 2022 年通过了"基于性能的 EPZ"规则（RG 1.242），允许 SMR 基于具体源项分析确定 EPZ 大小。

### 11.2.5　运行人员与安保人员

- 传统要求：1 台堆 3 名持照操纵员 + 1 名高级操纵员；
- SMR 挑战：12 台堆共享 1 个控制室，人员配置需要新的"人员配备模型"；
- NRC 已接受基于**任务分析**的人员配置方法（NUREG-1791）；
- 安保人员：基于**设计基准威胁（DBT）** + 现场具体情况进行定制。

## 11.3　支持 SMR 许可的行业规范和标准

### 11.3.1　ASME BPVC

- **Section III Division 1**：传统 LWR（Class 1/2/3）；
- **Section III Division 5**：高温反应堆（HTGR、SFR、MSR），2017 年发布；
- 涵盖材料、设计、制造、检验、运行。

### 11.3.2　ANS 标准

美国核学会（ANS）发布的标准系列：

- ANSI/ANS 20.x：SMR 系列；
- ANSI/ANS 30.x：先进反应堆风险指引；
- ANSI/ANS-54.1: SMR 总体设计准则；
- ANSI/ANS-30.3: 先进非 LWR 风险指引性能要求。

### 11.3.3　IEEE 标准

- IEEE 603：安全级 I&C 系统；
- IEEE 7-4.3.2：数字 I&C；
- IEEE 384：电缆隔离；
- IEEE 323：设备鉴定（Qualification）。

### 11.3.4　IEC 标准

- IEC 61513：核设施 I&C 总体；
- IEC 61226：I&C 分级；
- IEC 60987：HMI；
- IEC 62645：网络安全。

### 11.3.5　中国标准

- HAF（核安全法规）系列：HAF102（核动力厂设计安全规定）等；
- GB/T 16769：核电厂抗震设计；
- EJ（核行业标准）系列。

## 11.4　SMR 许可国际战略和框架

### 11.4.1　加拿大 CNSC

- **Pre-Licensing Review of Vendor Design**：厂商在正式申请前与 CNSC 进行预审评；
- **CMD**（Commission Member Document）公开；
- BWRX-300 在 Darlington 已通过此过程。

### 11.4.2　英国 ONR

- **Generic Design Assessment (GDA)**：通用设计评估；
- **Site Licence**：具体厂址；
- Rolls-Royce SMR 正在 GDA 流程中。

### 11.4.3　法国 ASN

- 受 EUR（European Utility Requirements）影响；
- **Code ASN**：基于 RCC 系列规范；
- 法国目前没有本土 SMR，但 NuScale、Rolls-Royce 在向 ASN 提交资料。

### 11.4.4　中国 NNSA

- HAF 系列法规；
- **核安全许可证**：选址、建造、首次装料、运行、退役；
- 玲龙一号（ACP100）已通过 NNSA 安全分析；
- HTR-PM 已获运行许可。

### 11.4.5　俄罗斯 Rostekhnadzor

- NP-001-15 等核安全导则；
- 浮动核电站（Akademik Lomonosov）已运行。

### 11.4.6　国际协调

- **MDEP（Multinational Design Evaluation Programme）**：OECD/NEA 主导，多国监管机构联合审评相同设计；
- **CNRA、CSNI**：监管方法、研究合作；
- **IAEA SSG** 系列：通用安全指南；
- **WENRA**（西欧核监管协会）：欧洲监管协调。

### 11.4.7　许可证协同（License-by-Reference）

一些国家采用"参考许可"模式：

- 一国完成完整审评（如美国 NuScale DC）；
- 其他国家参考该审评，仅审国别特定事项；
- 大幅缩短审评周期。

但实际操作中，由于各国监管要求差异，"参考"通常需要重新审评 30%–70% 内容。

## 11.5　结论

SMR 许可的核心矛盾是"旧框架 vs 新技术"。监管现代化的方向是：

1. **风险指引、性能导向（Risk-Informed, Performance-Based）**：从规定式走向性能式；
2. **技术中立（Technology-Neutral）**：监管框架兼容 LWR、HTGR、SFR、MSR；
3. **统一设计认证 + 国别附加**：减少重复审评；
4. **数字化工具**：监管软件、虚拟审查；
5. **应急计划区缩小**：基于源项的科学化定义；
6. **国际协调**：MDEP、IAEA 框架下的多边合作。

美国 10 CFR Part 53 的最终发布（预计 2025–2026）将是 SMR 监管现代化的里程碑。中国、加拿大、英国也在制定类似的先进反应堆监管框架。

## 11.6　延伸阅读

- NUREG/CR-7008, *Framework for Development of a Risk-Informed and Performance-Based Alternative to 10 CFR 50*.
- IAEA SSG-59, *Deterministic Safety Analysis for Nuclear Power Plants*.
- OECD/NEA CNRA. *Regulatory Challenges in the Licensing of New Nuclear Reactors*.
- MDEP 公开报告：https://www.oecd-nea.org/jcms/pl_32860/mdep
