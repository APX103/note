# 第 4 章　超临界水引起的腐蚀

> **核心命题**　超临界水是一种行为怪异的介质：在临界点附近它的介电常数从 80 骤降到 5，使它从极性溶剂变成类似非极性烃类——腐蚀机理也随之从离子化学转变为自由基化学。SCWR 候选合金必须在 500–625 ℃、25 MPa 的超临界水中同时应对一般腐蚀、应力腐蚀开裂与氧化膜失稳三重挑战。

---

## 4.1　超临界水的独特性质

水的热力学临界点为 **374.1 ℃、22.064 MPa**。在此点之上，水既非液态也非气态，而呈现超临界流体特性——这是 GIF 官方 SCWR 页面给出的定义。SCWR 把水的工作参数推到临界点以上，在约 25 MPa 下运行，出口温度 500–625 ℃，热效率目标 43–48%（远高于现役 LWR 的约 33%）。

### 4.1.1　各国 SCWR 概念参数

GIF 官方门户汇总了各国 SCWR 概念的设计参数：

| 国家/概念 | 压力（MPa） | 入口（℃） | 出口（℃） | 目标热效率 |
|---|---|---|---|---|
| 加拿大 Canadian SCWR | 25 | 350 | 625 | 48% |
| 中国 CSR1000 | 25 | 280 | 500 | 43% |
| 欧盟 HPLWR（Phase 1 / Phase 2） | 25 | 280 | 500 / 510 | 44% |
| 日本 Super LWR | 25 | 290 | 560 | 46% |
| 俄罗斯 VVER-SKD | 24.5 | 290 | 540 | 45% |

加拿大 SCWR 源自 CANDU 压力管技术，热效率目标最高（48%）、出口温度最高（625 ℃），最具代表性。

### 4.1.2　介电常数与离子积的突变

超临界水之所以"行为怪异"，根源在临界点附近的物性突变：

- **密度突变**：常温水密度约 1.0 g/cm³，临界密度仅 0.323 g/cm³。SCWR 工况下水密度可从液相密度（约 0.7 g/cm³，入口 290 ℃）连续降至气相密度（约 0.1–0.3 g/cm³，高温段）。
- **介电常数骤降**：常温水 ε 约 78–80；临界点降至 ε 约 5–6；500 ℃、密度 0.30 g/cm³ 时 ε 约 4.1。水从强极性溶剂变为类似"非极性烃类"，可溶解有机物和气体，但对离子态物质溶解能力下降（Zheng，2020；Weingärtner, 2005）。
- **离子积变化**：临界点附近离子积比常温水高 10–100 倍（常温水 Kw = 10⁻¹⁴；近临界可达 ~10⁻¹²），但在更高温下又会下降。

介电常数骤降使超临界水既可表现出"离子化学"（近临界），又可表现出"自由基化学"（高温低密度）的双重行为。这是 SCW 中腐蚀机理随温度变化复杂的根本原因——从低温段的水化学（类似 LWR）连续过渡到高温段的气相氧化。

## 4.2　候选合金体系

SCWR 燃料包壳与结构件的候选材料公认分为四类（INL、ORNL 综述）：

1. **奥氏体不锈钢**：316L、304、347H（347H 用于更高温）；
2. **铁素体-马氏体（F-M）钢**：T91（Mod 9Cr-1Mo）、HT9（12Cr-1MoWV）、HCM12A（12Cr）、NF616/Grade 92（9Cr-2W）；
3. **Ni 基合金**：Inconel 625、690、Alloy 800H；
4. **ODS 钢**：9Cr、12Cr、14Cr 系列（含 Y₂O₃ 约 0.25–0.3 wt%），主要为包壳管候选。

## 4.3　一般腐蚀行为

### 4.3.1　奥氏体不锈钢的腐蚀增重

316L 在 500–550 ℃ SCW 中的腐蚀增重典型值约为 **10 mg/dm² 量级**（约 1000 小时暴露），具体值随溶解氧（DO）与表面状态而异。J. *Supercritical Fluids*（2017）发表了 316L 在 500 ℃ SCW 中暴露至 20000 小时的长期增重演化研究，是该方向的经典长时数据。

氧化膜典型结构为：**外层磁铁矿 Fe₃O₄ + 内层 Fe-Cr 尖晶石**。短时间还有 (Fe,Cr)₂O₃，随时间逐渐被磁铁矿/尖晶石取代（Payet 等，*Corrosion Science*, 2019）。

### 4.3.2　溶解氧的影响

DO 加剧腐蚀：促进赤铁矿（α-Fe₂O₃）形成、加重点蚀；316L 表面主要为松散磁铁矿 + 赤铁矿，导致点蚀、微裂纹和氧化膜剥落。Ruiz 等人（PMC, 2016）发表了 316L 与 347H 在 2000 ppb DO SCW 中的系统数据集。

### 4.3.3　F-M 钢的腐蚀

Ampornrat 与 Was（*J. Nucl. Mater.* 371, 2007，被引 238 次）系统测量了 T91、HCM12A、HT9 在 400/500/600 ℃ SCW 中的氧化增重，遵循抛物线动力学；600 ℃ 时氧化最严重。氧化膜为双层结构：外层磁铁矿/赤铁矿 + 内层 (Fe,Cr) 尖晶石。

总体趋势：Cr 含量越高（HT9 与 HCM12A 均为 12Cr）耐蚀略优于 T91（9Cr），但 F-M 钢总体耐 SCW 腐蚀逊于奥氏体不锈钢和 Ni 基合金。

### 4.3.4　Ni 基合金的相对优势

Ni 基合金在 SCW 中表现优异。**Inconel 690** 在 25 MPa、500 小时暴露后腐蚀增重 < 0.12 mg/cm²（即 < 1.2 mg/dm²），明显优于奥氏体不锈钢。**Alloy 625** 在 600 ℃ 时腐蚀显著重于 400/500 ℃，在含 DO + Cl⁻ 时发生严重点蚀。

## 4.4　应力腐蚀开裂

慢应变速率试验（Slow Strain Rate Test，SSRT 或 CERT）是评估 SCW 中 SCC 倾向的标准方法。JRC（欧盟联合研究中心）发表了系统的 SSRT 结果（JRC Technical Report JRC62022）。

关键发现：

- SCC 倾向**随温度升高而增加**，在中高温段（约 550 ℃ 附近）敏感性最高；
- DO 显著影响 SCC——氧化速率与裂纹尖端应变速率的耦合是关键机制（ANL 综述，2013）；
- Novotny 等人（*J. Nucl. Mater.*, 2011，被引 70 次）系统研究了奥氏体不锈钢在 SCW 中的 SCC 倾向，是该方向的奠基性工作。

SCC 是 SCWR 候选材料合格化中最具挑战的失效模式，因为它在标准短时腐蚀试验中常常不显现，却会在长期服役中突然触发灾难性开裂。

## 4.5　SCWR 国际项目

- **欧洲 HPLWR（High Performance Light Water Reactor）**：压力容器式、热中子谱；25 MPa、入口 280 ℃、出口 500 ℃（Phase 2 目标 510 ℃），目标净电功率 1000 MWe（设计可至 1600 MW），热效率约 44%。项目分两阶段（HPLWR Phase 1 与 Phase 2，FP6 EU 项目），由 Schulenberg 主持。
- **日本 Super LWR（JSCWR 概念）**：由 Oka 于 1989 年在东京大学启动研究；1992 年 ANP92 会议首次发表；最终单通道堆芯设计为 25 MPa、入口 280 ℃、出口 500 ℃、热效率 43.8%、电功率 1530 MWe（单通道）。日本还发展 Super FR（快中子谱版本），采用 ZrH₂ 层增强共振吸收。
- **中国 CSR1000（CSCWR）**：热中子谱、UO₂ 燃料；25 MPa、入口 280 ℃、出口 >500 ℃、热效率 43%、电功率目标约 1000 MWe，基于 ABWR 与 PWR 技术演进。

## 4.6　小结

超临界水是一种化学行为随温度连续变化的介质——从近临界的离子化学过渡到高温低密度的自由基化学。SCWR 候选合金必须在 500–625 ℃、25 MPa 的 SCW 中同时抵抗一般腐蚀、应力腐蚀开裂与氧化膜失稳。Ni 基合金（Inconel 690、625）耐蚀性最佳，奥氏体不锈钢（316L）居中，F-M 钢（T91、HT9）耐蚀性最弱但抗辐照肿胀优势明显。DO 与温度是 SCC 的两个关键加速因子，必须通过水化学控制与设计裕量共同管理。

## 参考文献

1. Generation IV International Forum. SCWR Portal — Table of Concepts. https://www.gen-4.org/generation-iv-criteria-and-technologies/super-critical-water-reactors-scwr
2. GIF RSWG. *SCWR White Paper*. GIF, 2017. https://www.gen-4.org/sites/default/files/2024-07/2017%20GIF%20RSWG%20SCWR%20White%20Paper%20(2017).pdf
3. Ampornrat T., Was G. S. Oxidation of ferritic-martensitic alloys T91, HCM12A, and HT9 in supercritical water. *Journal of Nuclear Materials*, 2007, 371: 1–17. https://www.sciencedirect.com/science/article/abs/pii/S0022311507007362
4. Guzonas D., et al. *Corrosion of alloy 316L stainless steel after exposure to supercritical water at 500 ℃ for 20000 h*. *Journal of Supercritical Fluids*, 2017. https://www.researchgate.net/publication/315790457
5. Payet S., et al. Corrosion mechanism of 316L in hydrogenated supercritical water at 600 ℃. *Corrosion Science*, 2019. https://www.sciencedirect.com/science/article/am/pii/S0010938X18322376
6. Ruiz C., et al. *Corrosion data of 316L and 347H in SCW with dissolved oxygen*. PMC, 2016. https://pmc.ncbi.nlm.nih.gov/articles/PMC4845079/
7. Novotny R., et al. Stress corrosion cracking susceptibility of austenitic stainless steels in supercritical water. *Journal of Nuclear Materials*, 2011. https://www.sciencedirect.com/science/article/abs/pii/S0022311510004940
8. JRC. *Technical Report JRC62022 — SSRT results in SCW*. https://publications.jrc.ec.europa.eu/repository/handle/JRC62022
9. Argonne National Laboratory. *Technical Letter Report on SSRT in SCW*. ANL, 2013. https://publications.anl.gov/anlpubs/2013/10/77733.pdf
10. Zheng H. Thermophysical properties of supercritical water. *IOP Earth & Environmental Science*, 2020, 555: 012036. https://iopscience.iop.org/article/10.1088/1755-1315/555/1/012036/pdf
11. Weingärtner H. Supercritical water as a solvent. *Angewandte Chemie International Edition*, 2005. https://onlinelibrary.wiley.com/doi/10.1002/anie.200462468
12. Schulenberg T., et al. *HPLWR Phase 2 Project Summary*. IAEA INIS. https://inis.iaea.org/records/nrhte-xaj77
13. Oka Y. *Japanese SCWR research review*. *Frontiers in Nuclear Engineering*, 2023. https://www.frontiersin.org/journals/nuclear-engineering/articles/10.3389/fnuen.2023.1272766/full
14. Zhu X. *Chinese CSR1000 design*. *Frontiers in Energy Research*, 2021. https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2021.678741/full
