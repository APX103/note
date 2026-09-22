# 第 3 章　气体环境引起的腐蚀

> **核心命题**　气体冷却介质看似"温和"，实则把腐蚀问题推到了一个精微的化学平衡：在高温氦气中，ppm 量级的杂质比例决定合金是被氧化、渗碳还是脱碳；在超临界 CO₂ 中，铬的选择性氧化与碳迁移并行发生。Inconel 617 合金的 Code Case 于 2019 年获批、2021 版 ASME BPVC 第 III 卷第 5 分卷正式纳入，许用温度高达 950 ℃——是第四代堆高温合金合格化的里程碑。

---

## 3.1　引言：气体冷却的"温和"假象

氦冷与超临界 CO₂（sCO₂）冷却有两类不同的应用背景。VHTR/HTR 使用高温氦气作为一回路冷却剂，VHTR 出口温度目标高达 900–1000 ℃；已经商运的中国 HTR-PM（球床高温气冷堆）一回路氦气出口温度为 750 ℃，腐蚀裕度比 VHTR 目标值更宽。sCO₂ 布雷顿循环则是一种先进的能量转换系统，可作为多种高温堆与先进裂变堆、聚变堆甚至太阳能热发电的二次侧动力转换。

气体冷却的腐蚀机理与液态金属或水化学完全不同。它本质上是高温气体—合金界面化学，温度与气相杂质比例共同决定氧化膜的性质——是保护性的还是破坏性的。这一章讨论两类气体环境中的合金腐蚀行为。

## 3.2　VHTR 高温氦气中的合金腐蚀

### 3.2.1　杂质的角色

VHTR 一回路氦气并非纯氦，不可避免含有 ppm 量级的杂质：**H₂、CO、CO₂、CH₄、N₂、H₂O**。这些杂质的**比例**（而非仅浓度）决定了主导腐蚀机制：

- **氧化性气氛**（O₂、H₂O 占优）：形成 Cr₂O₃、MnCr₂O₄ 等保护性氧化膜；
- **渗碳性气氛**（CH₄、CO 占优）：碳渗入合金晶界，形成碳化物，使合金脆化；
- **脱碳性气氛**（H₂ 占优、CO 低）：合金中的碳被氢还原迁出，导致脱碳软化。

Zheng 等人（*J. Nucl. Mater.*, 2023，被引 12 次）系统研究了杂质比例对 **Inconel 617 与 Incoloy 800H** 在模拟 VHTR 氦气中腐蚀行为的影响。研究发现在 950 ℃ 含微量 CH₄ 的氦气中，617 与 800H 出现渗碳及拉伸性能变化；两种合金腐蚀行为相似、机制可比。这意味着合金选型时不仅看名义成分，还要预测实际运行气氛的氧化/渗碳/脱碳平衡。

### 3.2.2　中间热交换器候选合金

VHTR 的中间热交换器（Intermediate Heat Exchanger，IHX）是温度与应力最严苛的部件之一，需要把一回路 900–1000 ℃ 的氦气热量传递给二次侧工艺流体（如 sCO₂ 或氮气）。候选合金主要是固溶强化型 Ni 基合金：**Inconel 617（UNS N06617，Ni-22Cr-12.5Co-9Mo）**、Hastelloy X 与 Incoloy 800H。

### 3.2.3　Alloy 617 的 ASME 合格化

Alloy 617 的工程化是第四代堆高温合金合格化的里程碑事件。**ASME Code Case N-898（编号 2752）于 2019 年批准 Alloy 617 用于核建造，最高许用温度 950 ℃（1750 ℉，约 954 ℃）**，并于 2021 版 ASME BPVC 第 III 卷第 5 分卷正式纳入。这是 ASME 规范迄今批准的最高许用温度——比此前获批材料（如 Alloy 800H 的 760 ℃、316 系的约 800 ℃）高出约 200 ℃。

合格化的依据是 INL（Wright、Ren 等）多年积累的 800–1000 ℃ 长时蠕变断裂数据。Wright（2018，被引 49 次）确认 617 是 >750 ℃ VHTR IHX 的首选材料。值得注意的是，早期草案曾拟覆盖至 982 ℃（1800 ℉），最终批准版定为 950 ℃（1750 ℉）。在 621–787 ℃（1150–1450 ℉）中温区，617 的许用应力在同类材料中最高（Haynes International 数据手册）。

## 3.3　超临界 CO₂ 中的腐蚀

超临界 CO₂（sCO₂）布雷顿循环因其在高温下可达约 50% 热效率而成为先进反应堆动力转换的有力候选。Sandia/Wright 等人（2011，被引 62 次）的评估表明，再压缩 sCO₂ 循环在涡轮进口约 700 ℃ 下可达约 50% 热效率；简单回热循环仅约 34.5%。DOE 目标为 715 ℃ 涡轮进口下 50% 效率。压力方面，压缩机进口近临界点（约 7.4–8 MPa），高压侧常 20–30 MPa。

### 3.3.1　腐蚀机理

sCO₂ 中的合金腐蚀机制由 Xu 等人（2023，被引 24 次）系统综述：

- **铬氧化**：形成 Cr₂O₃ 表面膜；
- **碳迁移与内渗碳**：CO₂ 分解析出的碳向合金内部迁移；
- **breakaway 氧化**：保护性氧化膜破裂后腐蚀加速；
- **Cr 贫化**：表面 Cr 因氧化消耗而贫化，丧失再钝化能力。

ORNL 的 Pint 团队（NACE 2024）发现，在 >约 550 ℃ 的 sCO₂ 中，常规 Fe 基合金会发生明显渗碳，因此高温段需用 Ni 基合金。

### 3.3.2　材料选择

Kang 等人（*Crystals*, 2023，被引 49 次）的综述指出，**Ni 基合金（Inconel 625、740H、Haynes 230）在 sCO₂ 中耐蚀性最佳**，优于奥氏体不锈钢与铁素体/马氏体钢。MIT 的 Gibbs（2010，被引 40 次）测试了 10 种工程合金在 610 ℃、25 MPa sCO₂ 中最长 3000 小时的腐蚀行为，为材料排序提供了系统数据。

NETL 在 DOE 资助下委托西门子设计了 100 MWe、730 ℃ 进口温度的 sCO₂ 涡轮样机，目前仍在材料与部件合格化推进中。商业示范方面，Echogen 公司的 EPS100（8 MWe）已在余热回收领域示范运行。

## 3.4　气体腐蚀的工程对策

气体腐蚀的对策不像液态金属那样靠"调节氧含量"那样直接，更多依赖于合金成分与系统设计的协同：

1. **合金成分优化**：高 Cr（>20%）、添加 Al/Si 促进保护性 Al₂O₃/SiO₂ 膜形成；Ni 基合金在高温段优于 Fe 基。
2. **气氛控制**：在 VHTR 氦气回路中通过净化系统控制 H₂O、O₂、CO、CH₄ 等杂质的相对比例，避免脱碳或强渗碳气氛。
3. **涂层**：Aluminide 涂层、MCrAlY 涂层在 sCO₂ 高温段可显著延长合金寿期。
4. **设计裕量**：为 IHX 等关键部件预留腐蚀裕量壁厚，并在设计阶段纳入氧化膜生长动力学预测。

## 3.5　小结

气体环境中的腐蚀看似"温和"，实则考验工程师对化学平衡的精确把握。VHTR 高温氦气的腐蚀由 ppm 级杂质比例决定；sCO₂ 循环的腐蚀由 Cr 选择性氧化与碳迁移并行主导。Alloy 617 在 2019 年获 ASME 批准至 950 ℃，是高温合金合格化的里程碑，但工程实践仍需配合气氛控制与设计裕量共同保证寿期。Ni 基合金是高温气体环境的优选，Fe 基合金在 >550 ℃ 的 sCO₂ 中因渗碳风险而不推荐用于高温段。

## 参考文献

1. Zheng X., et al. Effect of impurity ratios on high-temperature corrosion of Inconel 617 and Incoloy 800H in impure helium. *Journal of Nuclear Materials*, 2023. https://www.sciencedirect.com/science/article/abs/pii/S030645492300155X
2. Wright J. K. Creep and creep-rupture of Alloy 617. *Journal of Nuclear Materials*, 2018. https://www.sciencedirect.com/science/article/am/pii/S0029549317303461
3. Wright R. N. (ORNL). Summary of Studies of Aging and Environmental Effects on Alloy 617. ORNL, 2006. https://www.osti.gov/servlets/purl/911722-d67FAs/
4. Ren W. (ORNL). Assessment of Existing Alloy 617 Data. ORNL, 2005. https://info.ornl.gov/sites/publications/files/Pub188.pdf
5. DOE/ASME. DOE lists ASME adding Alloy 617 to the BPVC as one of 10 big wins for nuclear energy in 2020. https://www.asme.org/government-relations/capitol-update/doe-lists-asme-adding-alloy-617-to-the-boiler-and-pressure-vessel-code-as-one-of-10-big-wins-for-nuclear-energy-in-2020
6. World Nuclear News. Alloy qualified for use in high-temperature reactors. https://world-nuclear-news.org/Articles/Alloy-qualified-for-use-in-high-temperature-reacto
7. Haynes International. *Hastelloy X and Alloy 617 Datasheets*. https://haynesintl.com/wp-content/uploads/2023/09/220.pdf
8. Xu Y., et al. Review on corrosion of alloys in supercritical CO₂. 2023. https://www.sciencedirect.com/science/article/pii/S2405844023093775
9. Kang K., et al. Review on corrosion of Ni-based alloys in supercritical CO₂. *Crystals*, 2023, 13(5): 725. https://www.mdpi.com/2073-4352/13/5/725
10. Gibbs G. W. (MIT). *Corrosion of engineering alloys in supercritical CO₂*. MIT, 2010. https://dspace.mit.edu/entities/publication/f6ea6d9f-98a3-4b7f-b883-35e4ecd5805f
11. Pint B. (ORNL). *Supercritical CO₂ corrosion of alloys*. NACE 2024. OSTI. https://www.osti.gov/servlets/purl/2329597
12. NETL. *Pre-FEED Technology Gap Analysis for sCO₂ Power Cycle*. NETL, 2020. https://www.netl.doe.gov/sites/default/files/2020-03/89243319CFE000022-PreFEED-Technology-Gap-Analysis_200302.pdf
13. Sandia/Wright et al. *sCO₂ Brayton Cycle Analysis*. OSTI, 2011. https://www.osti.gov/servlets/purl/1119778
