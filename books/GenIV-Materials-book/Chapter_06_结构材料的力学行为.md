# 第 6 章　结构材料的力学行为

> **核心命题**　在 500 ℃ 以上的高温环境中，金属材料的力学性能不再是"瞬时强度"的世界，而是"时间相关强度"的世界——蠕变、疲劳及其交互作用主导了部件寿期。T91 钢在 600 ℃ 下 10⁵ 小时的蠕变断裂应力约为 85–100 MPa，不到室温屈服强度的六分之一。设计这些部件需要的不是简单的强度校核，而是 ASME Section III Division 5 那样基于损伤累积的时变评估。

---

## 6.1　高温服役的力学范式

第四代堆结构材料工作在 500–1000 ℃ 区间，远超现役 LWR 的 300 ℃。在这个温度窗口，金属原子扩散变得显著，材料在恒定应力下会发生**蠕变**（creep）——随时间持续变形直至断裂。蠕变断裂强度随温度升高呈指数下降，温度每升高 50 ℃，10⁵ 小时蠕变断裂应力往往下降 30–50%。

这一现实使高温部件的设计不能再用 LWR 的"许用应力 + 安全系数"范式，而必须采用**时变损伤评估**：把蠕变损伤与疲劳损伤按某种累积规则叠加，确保设计寿期内总损伤不超过临界值。ASME 锅炉与压力容器规范（BPVC）专门为高温服役设立了**第 III 卷第 5 分卷**（Section III Division 5），就是这种范式的工程化体现。

本章从铁素体-马氏体钢、奥氏体不锈钢两类主力合金出发，讨论它们的力学行为、组织失稳机理与设计评估方法。

## 6.2　铁素体-马氏体钢的高温力学行为

### 6.2.1　T91（Grade 91，Mod 9Cr-1Mo-VNb）

T91 是第四代堆与高温化石电厂的主力 9-12Cr 钢。经正火 + 回火处理后，其典型显微组织为**回火板条马氏体** + 在板条界/原奥氏体界面上析出的 **M₂₃C₆ 碳化物** + 基体内弥散分布的细小 **MX 型 (V,Nb)(C,N) 碳氮化物**（Li et al., *JMEP*, 2020，被引 49）。

室温力学性能：屈服强度（YS）约 600 MPa，抗拉强度（UTS）约 730 MPa，均匀延伸率约 8%（Samuha et al., *Materials & Design*, 2023）。

高温蠕变是 T91 的关键限制。**600 ℃ 下 10⁵ 小时的蠕变断裂强度约为 85–100 MPa**（不同炉次与文献值在 85–130 MPa 之间；METU 论文给出 P91 在低应力区约 85 MPa；Masuyama 综述指出较新炉次可达 130 MPa）。这相当于室温屈服强度的六分之一，可见高温下材料的"时间相关强度"远低于瞬时强度。

T91 在 600 ℃ 下的蠕变断裂强度约为 Grade 9（9Cr-1Mo）的两倍（INIS）。蠕变失效在 >650 ℃ 时急剧加速，原因是 M23C6 粗化、Laves 相析出和 Z 相形成（*MDPI Metals* 12(12), 2022）。

### 6.2.2　HT9（12Cr-1Mo-WV）

HT9 由 Sandvik 设计，曾在美国 FFTF 中用作燃料包壳与导管，在 EBR-II 中用作金属燃料包壳。600 ℃ 下 UTS 约 600 MPa，屈服强度通常在 600 ℃ 下处于 400–500 MPa 范围（Ryu et al., *J. Nucl. Mater.*, 2011，被引 27）。屈服与抗拉强度在 600–800 ℃ 之间急剧下降。

TerraPower 现代炉次的 HT9 在 300–600 ℃ 范围内屈服强度较历史炉次有显著提升，用于行波堆（TWR）。ANL 报告（Gruber et al., 2019）证实 HT9 在长时间蠕变试验中表现出异常高的蠕变强度。

### 6.2.3　马氏体钢的长期组织失稳

F-M 钢的工程性能瓶颈不在短时强度，而在**长期组织失稳**导致的强度衰退：

- **Laves 相 (Fe,Cr)₂(W,Mo)**：初期提供沉淀硬化，但长期时效中迅速粗化，钉扎力下降 → 回复与软化。
- **Z 相 Cr(V,Nb)N**：缓慢形成，但会溶解有益的细小 MX (V,Nb)(N,C) 碳氮化物，生成大颗粒无强化作用的相 → **长期蠕变强度崩塌**（creep strength breakdown）。

Hald（*Int. J. Pres. Ves. Pip.*, 2008，被引 633）系统综述了 9-12%Cr 钢的微观组织与长期蠕变性能。Cambridge 相变研究中心观察到 P91 中 Laves 相在约 30000 小时已长大到很大尺寸。SuperVM12 因长期蠕变中不形成 Z 相而具有高抗力（*MDPI Metals* 12(7), 2022）。

## 6.3　奥氏体不锈钢的高温力学行为

### 6.3.1　316L(N) 与氮合金化

316L(N)（控氮 316，含 N 约 0.06–0.08%）是法国 Superphénix 的主选材，ASTRID 沿用。氮合金化显著提升长时蠕变强度：**氮含量倍增使 600 ℃ 下 10⁵ 小时许用应力提高超过 38%**（Kumar et al., *J. Nucl. Mater.*, 2013，被引 27）。

RCC-MRx（法国 AFCEN 规范）给出的 316L(N) 在 550 ℃ 的蠕变断裂强度**高于** ASME NH 等价值（MatISSE 2015 比较）。在 600 ℃ 下，316L(N) 的 RCC-MRx 许用应力也普遍高于 ASME Code Case NH 值——这是规范差异对设计裕量的实际影响。

### 6.3.2　15-15Ti 高燃耗包壳

15-15Ti（D9 改进型，AIM1/DIN 1.4970）是法国 CEA 为高燃耗 SFR 包壳开发的奥氏体钢。它通过 **Si（约 0.8%）+ Ti 微合金化**，结合 MC 析出与空洞形核位点控制，把抗辐照肿胀性能推至约 100–150 dpa。Séran 等人（ASTM STP 1125, 1990/1992，被引 87）是 15-15Ti 在 Phénix 反应堆中肿胀与辐照蠕变的奠基论文。

## 6.4　疲劳-蠕变交互作用

实际部件往往同时承受温度循环（疲劳）与恒定应力（蠕变），两者的损伤并非简单线性叠加，而存在显著**交互作用**：保载时间的引入会显著缩短疲劳寿命。

### 6.4.1　试验与建模

- 316L 在 600 ℃ 空气中的保载效应是经典研究主题（INIS-IAEA: "Creep fatigue interaction. Hold time effects on LCF of 316L at 600 ℃"）。
- Liu 等人（*MDPI Metals* 6(9), 2016，被引 20）提出统一蠕变-疲劳方程，是 Coffin-Manson 方程的扩展，引入温度/频率依赖性。

### 6.4.2　寿命预测模型

- **应变范围划分法（Strain Range Partitioning，SRP）**由 S.S. Manson 和 G.R. Halford 在 NASA 提出，把总非弹性应变范围划分为四个分量（PP、PC、CP、CC），每个对应 Coffin-Manson 型关系，最后组合求总寿命（Halford, NASA Technical Report, 1983）。
- **Ostergren 损伤函数**：基于拉伸滞回能的能量模型，结合频率分离法（区分拉伸/压缩保载）（Goswami, 1995）。

### 6.4.3　ASME Section III Division 5

ASME BPVC Section III Division 5 是专为高温堆（HTGR、氟盐冷堆、钠冷快堆）设立的规范，覆盖时变蠕变区。蠕变-疲劳与累积损伤评估程序在 Subsection HB Subpart B（Class A 部件）中，使用弹性/非弹性分析及损伤交互图（Sham, OSTI biblio, 2023；INL 全文）。历史脉络上，它源于 Code Case 1592-1596 系列 → Code Case N-47（曾用于 Clinch River Breeder Reactor）。NRC RG 1.87 Rev.3（DG-1436）认可 2017 版 Division 5 及 Code Case N-872、N-898。

## 6.5　小结

500 ℃ 以上的高温服役使结构材料进入"时间相关强度"主导的设计范式。铁素体-马氏体钢（T91、HT9）的高温蠕变受 Laves 相粗化与 Z 相析出制约，长期使用上限约 620 ℃；奥氏体不锈钢（316L(N)、15-15Ti）的氮合金化与 Ti/Si 微合金化显著提升长时蠕变与抗辐照肿胀性能。疲劳-蠕变交互作用是真实工况的常态，必须用 SRP 或 ASME Division 5 的损伤交互图评估。设计这些部件需要的是损伤累积评估，而不是简单的强度校核。

## 参考文献

1. Samuha S., et al. Mechanical performance and microstructure of Grade 91 steel. *Materials & Design*, 2023. https://modeling.matse.psu.edu/research_files/papers/2023_Samuha_Mat_Des.pdf
2. Li H., et al. Mechanical properties and phases evolution in T91 steel. *Journal of Materials Engineering and Performance*, 2020. http://www.eng.usf.edu/~volinsky/T91.pdf
3. Ryu W. S., et al. Thermal creep modeling of HT9 steel for fast reactor applications. *Journal of Nuclear Materials*, 2011. https://www.sciencedirect.com/science/article/abs/pii/S0022311510010676
4. Hald J. Microstructure and long-term creep properties of 9-12% Cr steels. *International Journal of Pressure Vessels and Piping*, 2008. https://www.sciencedirect.com/science/article/abs/pii/S0308016107000634
5. Kumar S., et al. Time dependent design curves for a high nitrogen grade of 316LN. *Journal of Nuclear Materials*, 2013. https://www.sciencedirect.com/science/article/abs/pii/S0029549313005438
6. Séran et al. Behavior under neutron irradiation of the 15-15Ti AIM1. *ASTM STP 1125*, 1990/1992. https://inis.iaea.org/records/t222b-e7619
7. Courcelle A. (CEA). 15-15Ti AIM1 in Phénix. *EPJ Web of Conferences (MINOS 2015)*, 2016. https://www.epj-conferences.org/articles/epjconf/pdf/2016/10/epjconf_MINOS2015_04003.pdf
8. CEA. *Sodium-cooled nuclear reactors monograph*. CEA, 2016. https://www.cea.fr/english/Documents/scientific-and-economic-publications/nuclear-energy-monographs/CEA_Monograph7_Sodium-cooled-nuclear-reactors_2016_GB.pdf
9. Halford G. R. *Strain range partitioning — Total strain range version*. NASA Technical Report, 1983. https://ntrs.nasa.gov/citations/19850029452
10. Liu Y. Unified creep-fatigue equations. *MDPI Metals*, 2016, 6(9): 219. https://www.mdpi.com/2075-4701/6/9/219
11. Sham T. L. *ASME Section III Division 5 — High Temperature Reactors*. OSTI, 2023. https://www.osti.gov/biblio/1967444
12. Gruber C., et al. *Long-term creep tests of HT9*. ANL, 2019. https://publications.anl.gov/anlpubs/2019/11/154297.pdf
13. Masuyama F. *Advanced 9-12Cr steel development*. 2007. https://www.phase-trans.msm.cam.ac.uk/2007/model_Masuyama_2007.pdf
14. API TR 938-B. *Grade 91 creep-Allowable stress basis*. https://eballotprodstorage.blob.core.windows.net/eballotscontainer/API%2520TR%2520938-B_2n%2520ed.%2520draft%2520_Rev.13.pdf
15. DTU. *Review of Z-phase precipitation in 9-12wt% Cr steels*. https://backend.orbit.dtu.dk/ws/files/114091830/Review_of_Z_phase_precipitation_in_9_12wt_Cr_steels_postprint.pdf
