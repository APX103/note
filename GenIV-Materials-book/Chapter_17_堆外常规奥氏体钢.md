# 第 17 章　堆外常规奥氏体钢

> **核心命题**　堆外构件（管道、热交换器、容器）的工作介质虽然仍是液态钠，但温度应力与辐照剂量都远低于堆芯——这把材料选型从"极限性能"拉回到"成熟可靠"。316L(N) 凭借 Superphénix 的工程经验与 RCC-MRx 规范的完整覆盖，成为钠冷快堆堆外构件的事实标准。本章的关键不是新材料探索，而是长时性能数据库的精细化与规范衔接的工程化。

---

## 17.1　引言：堆外构件的选材逻辑

堆芯构件（燃料包壳、绕丝、组件导管）追求极限性能，是材料学的前沿。堆外构件（主回路管道、中间热交换器、蒸汽发生器、主容器）则不同——它们不直接接触燃料区的高注量快中子，温度应力也相对温和。它们的选材逻辑是：

- **可靠性优先**：堆外构件一旦失效，泄漏后果严重；
- **可焊性与制造工艺成熟**：大型管道与容器需要成熟的焊接工艺；
- **长时性能数据库完整**：寿期 40–60 年需要完整的蠕变、疲劳、腐蚀数据；
- **规范合格化**：必须纳入 ASME、RCC-MRx 等正式规范。

基于这些逻辑，**304 与 316 系列奥氏体不锈钢**因其成熟的高温力学性能、良好的可焊性、与液态钠相容性以及完整的工业供应链，成为钠冷快堆堆外构件的事实标准。本章的关键不是新材料探索，而是长时性能数据库的精细化与规范衔接的工程化。

## 17.2　法国 SFR 选材传承

法国是全球钠冷快堆工程经验最丰富的国家之一。从 Rapsodie、Phénix 到 Superphénix，法国积累了 50 余年的 SFR 选材与运行经验。

### 17.2.1　316L(N) 的选用

**316L(N) 为 Superphénix 主选材**，ASTRID 沿用；含 N 约 0.06–0.08%，专为高温（约 650 ℃）蠕变强化开发。氮合金化是关键——氮含量从约 0.07% 增至约 0.14%（倍增）可使 600 ℃ 下 10⁵ 小时许用应力提高超过 38%（Kumar et al., *JNM*, 2013）。

### 17.2.2　国际对比

不同国家的 SFR 选材有相近但不完全相同的奥氏体钢等级，主要在 N、C、Ti、B 等微量元素上有细微调整：

| 等级 | 来源 | 关键微量元素特点 |
|---|---|---|
| 316L(N) | 欧洲/法国（Superphénix/ASTRID） | 控氮 N 约 0.06–0.08%，低 C |
| 316FR | 日本（JOYO/JSFR） | 控氮 + 优化 B 含量 |
| 316LN | EFR/DFBR 提案 | 高 N（约 0.07–0.14%），P 优化 |
| 15-15Ti AIM1 | 法国（Phénix 包壳，见第 8 章） | Ti（约 0.2%）+ Si（约 0.8%）+ N |

它们都基于 316 体系，但针对本国 SFR 工程的特定需求做了微调，规范衔接（RCC-MRx、JSME、ASME）也各有差异。

### 17.2.3　IAEA 权威文献

IAEA 核能丛书 NF-T-4.2《Structural Materials for Liquid Metal Cooled Fast Reactor Fuel Assemblies — Operational Behaviour》系统论述了 316 系奥氏体钢在快堆中的行为，是该方向的权威参考。

## 17.3　长时力学行为

### 17.3.1　蠕变与疲劳

堆外构件的寿期评估依赖 40–60 年（约 3.5–5.3×10⁵ 小时）的长时蠕变与疲劳数据。这超出了实验室直接测试的范围，需要靠**时间—温度参数外推**（Larson-Miller、Manson-Haferd 等）从短时数据外推。

**RCC-MRx 蠕变断裂强度**：316L(N) 在 550 ℃ 的 RCC-MRx 给定值**高于** ASME NH 等价值（MatISSE 2015 比较）。这意味着同一部件按 RCC-MRx 设计可获得更大裕量或更小壁厚。在 600 ℃ 下，316L(N) 的 RCC-MRx 许用应力也普遍高于 ASME Code Case NH 值。

**可忽略蠕变（negligible creep）曲线**：316L(N) 以 Rp0.2(moy) 为参考应力，与 RCC-MRx 吻合（KNS 2022）。这条曲线界定了一个温度—应力区间，在该区间内蠕变可忽略不计，设计可按弹性规范进行。

### 17.3.2　疲劳-蠕变交互作用

实际堆外构件同时承受温度循环（启停）与恒定应力（运行压力）。两者的损伤并非简单线性叠加——保载时间的引入会显著缩短疲劳寿命。详见第 6 章对疲劳-蠕变交互作用、SRP 寿命预测模型与 ASME Section III Division 5 的讨论。

## 17.4　钠侧腐蚀

堆外构件与液态钠长期接触，腐蚀行为已在第 2 章系统讨论。本章要点：

- **机制**：Ni、Cr、Mn、Si 选择性溶入液钠 → 高温段失重；
- **腐蚀速率强烈依赖溶解氧**：低 O₂（<5–10 ppm）时速率剧降；典型范围 **0.004–4 μm/yr**（Dai, *J. Nucl. Mater.* 综述 2021，被引 90）；
- **Alloy 709 对比数据**：ANL（2023）测量了 Alloy 709 与 316 系在 0.004–4 μm/yr 跨三温度范围的对比；
- **流动钠中 316LN**：钠暴露后**屈服强度 +15%、延伸率 -20%**（Bharasi, *JNM*, 2008）——这是钠致碳迁移导致的渗碳/脱碳效应。

## 17.5　低剂量辐照行为

堆外构件远离燃料区，但并非完全免辐照。在 SFR 设计中，堆外构件的累积剂量通常 **<1 dpa**。这一剂量不足以引发显著的空洞肿胀（奥氏体钢肿胀阈值约 50 dpa），但会带来轻微的辐照硬化与轻微的 DBTT 变化。

低剂量辐照评估主要关注：

- **辐照协助应力腐蚀开裂（IASCC）**：即使在 <1 dpa，RIS 也会使晶界 Cr 贫化，在敏感介质（含氧水）中促进 IASCC；
- **焊缝热影响区（HAZ）的辐照脆化**：HAZ 在辐照下更敏感；
- **与腐蚀协同**：辐照硬化 + 钠侧腐蚀的协同效应。

## 17.6　规范与标准

### 17.6.1　RCC-MRx（法国 AFCEN）

**RCC-MRx（AFCEN）**是法国规范，覆盖研究堆与钠冷快堆（ENEA/IRIS RT-2015-28 综述）。它是 SFR 堆外构件的主要设计依据，覆盖 316L(N) 在 425–650 ℃ 范围的许用应力、疲劳曲线与蠕变-疲劳损伤交互图。

### 17.6.2　ASME Section III Division 5

**ASME Section III Division 5** 是专为高温堆（HTGR/VHTR/GFR）金属构件设立的规范。HBB 子节涵盖 316H、Alloy 800H、2.25Cr-1Mo（高温阈值 >370 ℃ 对碳/低合金/马氏体钢）。ANL 对 Division 5 的局限性有系统分析。

### 17.6.3　规范差异的实际影响

RCC-MRx 与 ASME 在 316L(N) 上的差异不只是"哪个更保守"——它们基于不同的数据库、不同的外推方法、不同的损伤评估准则。设计同一部件按不同规范可能得出不同的壁厚与寿期，这是国际 SFR 项目中需要协调的工程议题。

## 17.7　新合金开发

尽管 316L(N) 是 SFR 堆外构件的主力，针对更高温度、更长寿期、更高可靠性的需求，新一代奥氏体钢仍在开发中：

- **含 B 钢**：通过 B 的 (n,α) 反应增加肿胀阻力，但需平衡氦脆风险；
- **Si 增强的 316 改进型**：Si 含量约 0.8–1.5% 提升钠侧腐蚀抗力与蠕变强度；
- **15-15Ti 的堆外应用**：本用于快堆包壳（见第 8 章），其堆外构件版本在评估中；
- **Alloy 709**：ANL（2023）等机构评估其作为高温改进型奥氏体钢。

## 17.8　小结

304 与 316 系列奥氏体不锈钢凭借成熟的高温力学性能、良好的可焊性、与液态钠相容性以及完整的工业供应链，成为钠冷快堆堆外构件的事实标准。316L(N) 通过法国 Superphénix/ASTRID 的工程经验与 RCC-MRx 规范的完整覆盖，确立了 SFR 堆外选材的标杆。RCC-MRx 给出的 316L(N) 蠕变断裂强度普遍高于 ASME NH——规范差异对设计裕量的实际影响是国际 SFR 项目中的关键议题。钠侧腐蚀速率典型值 0.004–4 μm/yr，强依赖溶解氧。低剂量辐照（<1 dpa）主要带来 IASCC 与 HAZ 脆化风险。新一代含 B、Si 增强的 316 改进型与 Alloy 709 仍在评估中。

## 参考文献

1. IAEA. *Structural Materials for Liquid Metal Cooled Fast Reactor Fuel Assemblies — Operational Behaviour*. IAEA Nuclear Energy Series NF-T-4.2. https://www-pub.iaea.org/MTCD/Publications/PDF/Pub1548_web.pdf
2. Kumar S., et al. Time dependent design curves for a high nitrogen grade of 316LN. *Journal of Nuclear Materials*, 2013. https://www.sciencedirect.com/science/article/abs/pii/S0029549313005438
3. EERA-MatISSE. *Comparison of RCC-MRx and ASME — Hyeong Yeon Lee*. 2015. https://www.eera-jpnm.com/matisse/wp-content/uploads/2015/08/MatISSE-2015-Comparison-of-RCC-MRx-and-ASME-Hyeong-Yeon-Lee.pdf
4. Dai Y., et al. Review on corrosion and mass transport in liquid sodium. *Progress in Nuclear Energy*, 2021. https://www.sciencedirect.com/science/article/pii/S1738573321002874
5. ANL. *Alloy 709 sodium-side corrosion comparison*. ANL, 2023. https://publications.anl.gov/anlpubs/2023/09/184732.pdf
6. Bharasi N., et al. Tensile properties of 316LN after sodium exposure. *Journal of Nuclear Materials*, 2008. https://www.sciencedirect.com/science/article/abs/pii/S0022311508001955
7. AFCEN. *RCC-MRx code overview*. ENEA/IRIS RT-2015-28. https://iris.enea.it/retrieve/dd11e37c-d796-5d97-e053-d805fe0a6f04/RT-2015-28-ENEA.pdf
8. NRC. *ASME Section III Division 5 technical review*. NUREG. https://downloads.regulations.gov/NRC-2021-0117-0013/content.pdf
9. ANL. *Limitations analysis of ASME Section III Division 5*. ANL, 2021. https://publications.anl.gov/anlpubs/2021/06/169188.pdf
10. KNS 2022. *Negligible creep curves for 316LN*. https://www.kns.org/files/pre_paper/48/22A-490.pdf
11. UKAEA. *Comparison of RCC-MRx and R5 for 316L at 550 ℃*. UKAEA-CCFE-PR25276. https://scientific-publications.ukaea.uk/wp-content/uploads/UKAEA-CCFE-PR25276.PDF
12. CEA. *Sodium-cooled nuclear reactors monograph*. CEA, 2016. https://www.cea.fr/english/Documents/scientific-and-economic-publications/nuclear-energy-monographs/CEA_Monograph7_Sodium-cooled-nuclear-reactors_2016_GB.pdf
13. ResearchGate. *Chemical composition of 316LN / 316FR grades*. https://www.researchgate.net/figure/Chemical-composition-specified-for-316LN-316FR-and-316LN-used-proposed-in-EFR-DFBR_tbl4_266866552
