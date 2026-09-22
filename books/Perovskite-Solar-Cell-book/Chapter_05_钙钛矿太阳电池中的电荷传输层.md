# 第 5 章　钙钛矿太阳电池中的电荷传输层

> **核心命题**　电荷传输层（HTL/ETL）及其与钙钛矿的界面，决定了载流子抽取效率与非辐射复合损失。spiro-OMeTAD 与 TiO₂/SnO₂ 是当前主流选择，但 spiro-OMeTAD 高达约 300 美元/克的成本与 TiO₂ 的 UV 不稳定性是产业化的两大障碍。本章从材料选型到界面缺陷抑制、界面保护层、无传输层器件，系统讨论界面工程。

---

## 5.1　概述

钙钛矿吸收层本身是优良的双极性传输材料，但仅靠钙钛矿无法高效地抽取载流子——需要 ETL（电子传输层）与 HTL（空穴传输层）提供选择性接触。理想传输层的三个要求：

1. **能带对齐**：ETL 导带低于钙钛矿导带（利于电子抽取），HTL 价带高于钙钛矿价带（利于空穴抽取）；
2. **高迁移率**：传输层内载流子迁移率应足够高，避免串联电阻损失；
3. **致密无针孔**：防止钙钛矿与电极直接接触造成短路。

传输层与钙钛矿的界面更是决定效率的关键——界面缺陷是非辐射复合的主要中心，界面能带对齐决定 V_oc 损失。

## 5.2　电荷传输层与界面

### 5.2.1　空穴传输层

**spiro-OMeTAD**（2,2',7,7'-四(N,N-二对甲氧基苯基氨基)-9,9'-螺二芴）是高效率 n-i-p 结构的标准 HTL，HOMO 约 −5.0 eV（Rombach et al., *Energy Environ. Sci.* 14, 5161, 2021，被引 793 次）。其优势是成膜性好、能级匹配，但有几个根本局限：

- **成本高昂**：商业级 spiro-OMeTAD 约 **300 美元/克**（具体价格因供应商而异，文献报道范围 90–460 美元/克）；
- **需化学掺杂**：本征 spiro-OMeTAD 导电性差，需用 Li-TFSI + tBP + Co(III) 络合物掺杂，但 Li-TFSI 易吸潮、tBP 易挥发，是稳定性退化的根源；
- **空穴迁移率低**：掺杂后仍仅 10⁻⁴–10⁻³ cm²/V·s。

**替代 HTL**：

| 材料 | 类型 | HOMO (eV) | 优势 | 局限 |
|---|---|---|---|---|
| PTAA（聚三芳基胺） | 聚合物 | 约 −5.1 | 迁移率较高、稳定性好 | 成本仍较高 |
| PEDOT:PSS | 导电聚合物 | 约 −5.0 | 低温、可溶液加工 | 酸性腐蚀 ITO |
| NiOₓ | 无机 | 约 −5.2 | 高稳定性、高迁移率 | 需磁控溅射 |
| CuSCN | 无机 | 约 −5.3 | 高迁移率、低成本 | 与钙钛矿反应风险 |

CuSCN 作为无机 HTL 已实现 > 20% 效率（Arora et al., *Science*, 2017），是替代 spiro-OMeTAD 的重要候选。

### 5.2.2　空穴传输层-钙钛矿界面

HTL/钙钛矿界面的关键问题：

- **未配位 Pb²⁺**：钙钛矿表面暴露的 Pb²⁺ 形成深能级缺陷，是非辐射复合中心；
- **能带对齐损失**：HTL 的 HOMO 与钙钛矿 VBM 之间的能量失配导致 V_oc 损失；
- **界面反应**：CuSCN 等与钙钛矿在界面可能发生离子交换。

界面钝化策略（详见 5.3）主要针对未配位 Pb²⁺。

### 5.2.3　电子传输层

**TiO₂** 是介观 n-i-p 结构的传统 ETL，需 **450–500 ℃ 烧结**才能获得锐钛矿相与电子迁移率。其优势是化学稳定、与钙钛矿导带匹配良好（CB 约 −4.0 至 −4.2 eV）；缺点是高温工艺不适合柔性衬底、UV 光催化特性导致钙钛矿降解（Lee et al., *Sci. Rep.* 6, 38150, 2016，被引 512 次）。

**SnO₂** 是低温 ETL 的主流选择，可在 **< 150 ℃** 通过溶胶-凝胶或原子层沉积制备。SnO₂ 带隙约 3.6 eV（无 UV 吸收问题）、导带位置与钙钛矿匹配良好、电子迁移率高（> 100 cm²/V·s）。SnO₂ 已成为高效率钙钛矿电池（含钙钛矿/硅叠层）的首选 ETL。

**有机 ETL**：C₆₀（富勒烯）与 PCBM（[6,6]-苯基-C61-丁酸甲酯）在 p-i-n 倒置结构中用作 ETL，优点是低温溶液加工、与钙钛矿界面缺陷钝化（富勒烯的 C=C 与未配位 Pb²⁺ 作用），缺点是迁移率较低、稳定性不如无机 ETL。

### 5.2.4　电子传输层-钙钛矿界面

ETL/钙钛矿界面的关键问题：

- **碘空位 V_I**：界面处 V_I 富集形成深能级缺陷；
- **界面能带对齐**：ETL 导带必须低于钙钛矿导带，否则电子抽取受阻；
- **能带偏移类型**：理想为 Type-I 对齐（详见第 3 章）。

TiO₂/SnO₂ 与 MAPbI₃ 的能带对齐通常为 Type-I，是高效电子抽取的基础。

## 5.3　界面缺陷抑制

界面缺陷钝化是提升 V_oc 与 FF 的核心手段（Shen et al., *Joule*, 2023，被引 190 次）。主要策略：

### 5.3.1　Lewis 碱钝化

含 N、S、O 孤对电子的分子（如吡啶、硫脲、胺基聚合物）与未配位 Pb²⁺ 配位，消除深能级缺陷。代表性工作：硫脲钝化、聚甲基丙烯酸甲酯 PMMA 界面层、芘衍生物钝化。

### 5.3.2　离子钝化

碱金属离子（K⁺、Rb⁺、Cs⁺）在界面处钝化碘空位或形成低维钙钛矿界面相。代表性工作：RbCl 掺杂 SnO₂ 界面、KI 处理钙钛矿表面。

### 5.3.3　二维钙钛矿界面层

在三维钙钛矿表面生长一层二维钙钛矿（如 PEAI 处理形成 BA₂PbI₄ 类界面相），既钝化表面缺陷又提供疏水保护层，是稳定性与效率兼顾的有效策略。

### 5.3.4　额外卤素阴离子

Cl⁻ 与 pseudohalide（BF₄⁻、PF₆⁻）在界面处钝化碘空位，同时改善结晶质量。

## 5.4　界面保护层

界面保护层用于阻断界面反应、提升稳定性：

- **LiF**（氟化锂）：极薄（< 1 nm）的 LiF 层在金属/有机界面形成偶极，降低电子抽取势垒；
- **Al₂O₃**：ALD 沉积的致密 Al₂O₃ 作为离子扩散阻挡层，防止金属电极与钙钛矿反应；
- **BCP**（浴铜灵）：在 C₆₀ 与金属电极之间作为修饰层；
- **PEAI 等二维钙钛矿界面层**：兼具钝化与保护功能。

## 5.5　无电荷传输层器件

无传输层器件（HTL-free 或 ETL-free）是降低成本与简化工艺的极端方向：

- **无 HTL 器件**：钙钛矿直接与碳电极接触，利用钙钛矿本身的双极性传输。碳电极无 HTL 器件效率已达 **20.08%**（文献报道），且稳定性优于 spiro-OMeTAD 器件；
- **无 ETL 器件**：研究较少，效率较低（< 15%）。

无传输层器件牺牲了部分效率，但显著降低了材料成本（无 spiro-OMeTAD、无 Au 电极）与工艺复杂度，是低成本产业化（特别是室内光伏）的有力候选。

## 5.6　展望

电荷传输层的未来发展方向：

1. **无机化**：NiOₓ、CuSCN、SnO₂ 等无机传输层替代有机材料，提升稳定性；
2. **低成本化**：替代 spiro-OMeTAD（约 300 美元/克）的聚合物或无机 HTL；
3. **界面工程精细化**：结合 ALD、二维钙钛矿界面层、Lewis 碱钝化的多层策略；
4. **叠层兼容**：宽带隙钙钛矿顶电池的传输层需在宽带隙下保持高效率（详见第 9 章）；
5. **无传输层化**：碳电极器件在低成本场景的应用拓展。

电荷传输层工程是钙钛矿电池从实验室效率纪录走向产业化可靠性的关键桥梁。

## 参考文献

1. Rombach F. M., Haque S. A., McGill S. A. Insights into charge recombination and loss mechanisms in perovskite solar cells. *Energy Environ. Sci.*, 2021, 14: 5161. https://pubs.rsc.org/ee/article/14/10/5161/726930
2. Lee J.-W., et al. UV degradation of perovskite solar cells. *Sci. Rep.*, 2016, 6: 38150. https://www.nature.com/articles/srep38150
3. Arora N., et al. Copper thiocyanate as low-cost inorganic hole-transporting material for high-efficiency perovskite solar cells. *Science*, 2017.
4. Shen X., et al. Defects in metal halide perovskites. *Joule*, 2023. https://www.cell.com/joule/pdf/S2542-4351(23)00039-9.pdf
5. Jiang Q., et al. Surface passivation of perovskite film for high-efficiency solar cells. *Nat. Photonics*, 2019.
6. Wang F., et al. 2D perovskite interface layers for stability. *Adv. Mater.*, 2024.
7. Rajagopal A., et al. SnO₂ ETL review. *Adv. Mater.*, 2018.
8. Habisreutinger S. N., et al. Carbon nanotube-polymer composites as hole transporters. *Nano Lett.*, 2014.
9. Ku Z., et al. Full carbon electrode perovskite solar cells. *Adv. Energy Mater.*, 2017.
10. Mei A., et al. A hole-conductor-free, fully mesoscopic perovskite solar cell. *Science*, 2014, 345: 295–298.
11. Calado P., et al. Evidence for ion migration in hybrid perovskite solar cells. *Nat. Commun.*, 2016. https://pmc.ncbi.nlm.nih.gov/articles/PMC5192183/
12. Chen B., et al. Efficient semitransparent perovskite solar cells for tandem applications. *Joule*, 2019.
13. Bush K. A., et al. 23.6%-efficient monolithic perovskite/silicon tandem solar cells. *Nat. Energy*, 2017.
14. Al-Ashouri A., et al. Monolithic perovskite/silicon tandem with 29% efficiency. *Science*, 2020.
15. Zheng J., et al. 33.9% perovskite/Si tandem. LONGi, 2023. https://www.longi.com/en/news/new-world-record-for-the-efficiency-of-crystalline-silicon-perovskite-tandem-solar-cells/
16. Wang Y., et al. LiF interface modifier for perovskite solar cells. *Adv. Energy Mater.*, 2023.
