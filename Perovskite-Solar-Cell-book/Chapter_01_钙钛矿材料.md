# 第 1 章　钙钛矿材料：光伏之星

> **核心命题**　钙钛矿（ABX₃）材料以其强吸光、双极传输、带隙可调、缺陷容忍、低激子结合能、可溶液加工等一揽子优异特性，在十年内把光伏效率从 3.8% 推到 26.7%（NREL 认证）——这是光伏史上最快的技术跃迁。本章建立全书的"材料—结构—缺陷—器件"框架。

---

## 1.1　钙钛矿光伏的发展

2009 年，Kojima 等人在《JACS》首次报道了 CH₃NH₃PbI₃（甲胺铅碘）钙钛矿作为染料敏化电池的敏化剂，光谱响应延伸至 800 nm，器件效率仅 **3.8%**（Kojima et al., *JACS* 131, 6050, 2009）。这篇论文当时并未引起轰动——钙钛矿层在液态电解质中几小时就溶解，电池几乎没有实用价值。

真正的转折发生在 2012 年。Snaith 组（Oxford）用 Al₂O₃ 骨架替代介孔 TiO₂、以固态 spiro-OMeTAD 替代液态电解质，把钙钛矿电池效率推到 **10.9%**（Lee et al., *Science* 338, 643, 2012）；同年 Park 组（Kim et al., *Sci. Rep.* 2, 591, 2012）报道全固态介观 CH₃NH₃PbI₃ 电池效率 9.7%。固态器件的实现，使钙钛矿从" curiosities"一跃成为光伏明星。

此后效率纪录以每年 2–3 个百分点的速度攀升：2014 年突破 17%、2015 年突破 20%、2017 年 Seok 组通过"碘化管理"实现 FAPbI₃ 基电池认证 **22.1%**（Yang et al., *Science* 356, 1376, 2017）。截至 2025 年，NREL 认证的单结钙钛矿电池最高效率已达 **26.7%**（NREL Best Research-Cell Efficiency Chart；交叉印证见 Fluxim record tracker）。钙钛矿/硅叠层在 2024 年由隆基（LONGi）推到 **34.6%**，逼近单结 Shockley-Queisser 极限（33.7%）。

> ⚠️ **效率纪录时效性**：钙钛矿领域效率纪录更新极快，建议读者引用时直接查阅 NREL 官网（nrel.gov/pv/cell-efficiency.html）核验当月最新值。

## 1.2　钙钛矿材料的特性

钙钛矿材料之所以能实现这样的效率跃迁，源于它同时具备一揽子在传统光伏材料中互斥的优异特性。本节逐一拆解。

### 1.2.1　吸光能力强

MAPbI₃ 在可见光区的吸收系数高达约 **10⁴–10⁵ cm⁻¹**，吸收边陡峭（De Wolf et al., *J. Phys. Chem. Lett.*，被引 3419 次）。这意味着仅 300–500 nm 厚的钙钛矿薄膜就能吸收绝大部分入射光，远薄于晶硅（需要约 150 μm）。强吸光不仅是材料利用率的提升，更直接决定了薄膜化、柔性化的可能。

### 1.2.2　传输性能好

钙钛矿是罕见的**双极性传输材料**——电子与空穴的扩散长度相当。Stranks 等人（*Nat. Mater.* 12, 361, 2013）首次报道 MAPbI₃₋ₓClₓ 薄膜的电子/空穴扩散长度 > 1 μm；Dong 等人（*Science* 347, 967, 2015）进一步发现 MAPbI₃ **单晶**的电子-空穴扩散长度可达 **> 175 μm**，载流子迁移率约 100 cm²/V·s 量级，陷阱密度低至 10⁹–10¹⁰ cm⁻³。这一指标意味着光生载流子能在复合前被有效抽取。

### 1.2.3　带隙可调节

通过调整卤素组成（Cl/Br/I 比例）与 A 位阳离子，钙钛矿的带隙可在约 **1.48–2.3 eV** 之间连续调节：

| 材料 | 带隙（eV） |
|---|---|
| FAPbI₃ | 约 1.48 |
| MAPbI₃ | 约 1.55 |
| CsPbI₃ | 约 1.73 |
| MAPbBr₃ | 约 2.3 |

带隙可调是钙钛矿相对其他光伏技术的根本优势之一——它既能逼近单结 SQ 极限的最优带隙（1.34 eV），又能用于叠层顶电池（宽带隙约 1.68–1.75 eV）与室内光伏（最优带隙约 1.9 eV）。这些数据来自 Whitcher 等（*Phys. Rev. X* 8, 021034, 2018）等多源综合。

### 1.2.4　缺陷态密度低

钙钛矿薄膜的缺陷态密度典型值为 **10¹⁵–10¹⁶ cm⁻³**（单晶可低至 10⁹–10¹⁰ cm⁻³，Dong 2015）。更关键的是，钙钛矿表现出独特的**缺陷容忍性**：多数本征点缺陷形成浅能级而非深陷阱（Kang 等，2017，第一性计算，被引 1512 次）。这与硅、GaAs 等传统半导体形成鲜明对比——后者对深能级缺陷极为敏感。

### 1.2.5　激子结合能低

光激发在半导体中产生的是束缚的电子-空穴对（激子）还是自由载流子，取决于激子结合能 E_b 与热能 kT 的相对大小。MAPbI₃ 的激子结合能仅约 **10 meV**（约 kT≈26 meV 的三分之一），意味着室温下大部分激子在产生瞬间即解离为自由载流子（Chen 等，2018）。这是钙钛矿无需 p-n 结内建电场强分离载流子、仍能高效工作的物理基础。

### 1.2.6　可溶解性

钙钛矿前驱体（PbI₂、MAI、FAI 等）可溶于常用极性溶剂（DMF、DMSO、GBL），使得钙钛矿薄膜可以通过旋涂、刮涂、狭缝涂布、喷墨打印等低成本溶液工艺制备（详见第 6 章）。这是钙钛矿产业化成本优势的根基——相比硅的 Czochralski 单晶生长或 GaAs 的 MOCVD 外延，溶液工艺的设备投资低一个数量级。

### 1.2.7　钙钛矿材料稳定性

稳定性是钙钛矿产业化的核心障碍。主要的退化因素包括：

- **水分**：钙钛矿在潮湿空气中水解退化；
- **氧气**：在光照下与氧气反应生成超氧化物；
- **紫外光**：即使无水无氧，UV 仍致 TiO₂ 等界面退化（Lee et al., *Sci. Rep.* 6, 38150, 2016，被引 512 次）；
- **热**：85 ℃ 高温下有机阳离子分解（IEC 61215 标准）。

测试标准包括 **IEC 61215**（含 85 ℃ 湿冻、湿热循环）与 **ISOS** 协议（López et al., *Chem. Soc. Rev.*, 2026）。稳定性问题的工程对策（封装、二维钙钛矿、界面钝化）贯穿全书。

## 1.3　钙钛矿材料的结构

### 1.3.1　晶体结构基本知识

钙钛矿的名字来源于矿物 CaTiO₃，由 Gustav Rose 于 1839 年发现并以俄罗斯矿物学家 Lev Perovski 命名。理想的钙钛矿晶体结构为立方晶系（空间群 Pm-3m），通式 **ABX₃**：B 位阳离子位于立方体体心，与六个 X 位阴离子配位形成 BX₆ 八面体；A 位阳离子位于立方体顶角，由八个 BX₆ 八面体共享角包围。

实际钙钛矿常因 A 位阳离子尺寸不匹配而发生晶格畸变，形成四方或正交结构。MAPbI₃ 随温度发生三相转变：正交 Pnma（< 约 160 K）→ 四方 I4/mcm（160–330 K）→ 立方 Pm-3m（> 约 330 K，即约 57 ℃）（Whitfield et al., *Sci. Rep.* 6, 35685, 2016）。

### 1.3.2　钙钛矿材料的结构

判断一种 A-B-X 组合能否形成稳定钙钛矿结构，常用 **Goldschmidt 容忍因子**：

```
t = (rA + rX) / [√2·(rB + rX)]
```

Bartel 等（*J. Mater. Sci.*, 2019，被引 2030 次）系统分析得出，形成稳定钙钛矿的窗口约为 **0.825 < t < 1.059**（分类准确率 74%）。对 Pb²⁺ 与 I⁻ 体系，典型 A 位阳离子的容忍因子为：Cs⁺ 约 0.81、MA⁺ 约 0.91、FA⁺ 约 0.99——这也解释了为何 FA⁺ 基钙钛矿的热力学稳定性最好。

FAPbI₃ 存在一个工程化难题：室温下稳定的黄色 δ 相（非钙钛矿，不吸光）需加热到 > 150 ℃ 才能转化为黑色 α 相（光活性钙钛矿）。研究者通过 Cs⁺、MA⁺ 混合或界面应变来稳定 α 相。

### 1.3.3　二维钙钛矿结构

把三维钙钛矿的"层"用大体积有机间隔阳离子隔开，就得到二维钙钛矿。主要有两类：

- **Ruddlesden-Popper（RP）相**：通式 **A'₂Aₙ₋₁BₙX₃ₙ₊₁**，采用双层单价有机间隔体（如 BA⁺，丁胺），层间存在范德华间隙；
- **Dion-Jacobson（DJ）相**：通式 **A'Aₙ₋₁BₙX₃ₙ₊₁**，采用单层二价有机间隔体，无范德华间隙，稳定性通常更优。

二维钙钛矿的疏水有机间隔层显著提升抗湿稳定性，是钙钛矿稳定性工程的重要方向（详见 Cresp et al., *Adv. Funct. Mater.*, 2024）。代价是带隙变大、载流子传输受层间势垒限制，效率低于三维钙钛矿。

### 1.3.4　B 位阳离子与 X 位阴离子

B 位阳离子决定了钙钛矿的核心光电性质。Pb²⁺ 是迄今效率最高的选择，但毒性是根本顾虑（详见第 8 章无铅替代）。Sn²⁺ 是最接近 Pb²⁺ 的替代，但易氧化为 Sn⁴⁺。Bi³⁺、Sb³⁺ 等低毒替代正被广泛研究。

X 位阴离子（I⁻、Br⁻、Cl⁻）决定带隙与稳定性。I⁻ 给出窄带隙（适合单结），Br⁻ 拓宽带隙（适合叠层顶电池），Cl⁻ 主要用于改善结晶质量（Cl⁻ 在最终结构中含量极低，但显著影响薄膜形貌）。

## 1.4　钙钛矿材料的缺陷

### 1.4.1　钙钛矿缺陷的产生及后果

钙钛矿薄膜的低温溶液制备过程不可避免地产生各类点缺陷。虽然钙钛矿的缺陷容忍性使多数缺陷形成浅能级，但深能级缺陷仍是非辐射复合中心，直接降低开路电压与填充因子。缺陷也是离子迁移的通道，是 I-V 迟滞与稳定性退化的根源之一。

### 1.4.2　钙钛矿缺陷的类型

主要本征点缺陷包括（Shen et al., *Joule*, 2023，被引 190 次）：

- **碘空位 V_I**：最普遍，可形成深陷阱；
- **铅间隙 Pb_i**：深能级，强复合中心；
- **碘间隙 I_i**：影响离子迁移；
- **反位 Pb_I**：Pb 占据 I 位，深能级；
- **MA_I、Pb_MA 等反位缺陷**。

### 1.4.3　钙钛矿缺陷钝化

缺陷钝化是提升效率与稳定性的关键工程手段（详见第 5 章界面工程）。主要策略：

- **离子掺杂**：碱金属离子（K⁺、Rb⁺、Cs⁺）占据间隙或钝化界面；
- **额外卤素阴离子**：Cl⁻、 pseudohalide（BF₄⁻、PF₆⁻）钝化碘空位；
- **Lewis 碱钝化**：含 N、S、O 孤对电子的分子（如吡啶、硫脲）钝化未配位 Pb²⁺；
- **表面终止层**：二维钙钛矿界面层（如 PEAI）、SnO₂–RbCl 等界面钝化层。

## 1.5　钙钛矿太阳电池

### 1.5.1　钙钛矿电池器件结构

钙钛矿电池主要有三类结构（Rombach et al., *Energy Environ. Sci.* 14, 5161, 2021，被引 793 次）：

- **介观 n-i-p**：FTO / 致密 TiO₂ / 介孔 TiO₂ / 钙钛矿 / spiro-OMeTAD / Au。
- **平面 n-i-p**：FTO / 致密 TiO₂ 或 SnO₂ / 钙钛矿 / spiro-OMeTAD / Au。
- **平面 p-i-n（倒置）**：ITO / NiOₓ 或 PTAA / 钙钛矿 / C₆₀ 或 PCBM / BCP / Ag。

p-i-n 结构因低温工艺（< 150 ℃）、迟滞小、适合叠层顶电池，已成为高效率与柔性器件的主流。

### 1.5.2　器件结构组成材料

| 层 | 典型材料 | 作用 |
|---|---|---|
| 透明电极 | FTO、ITO、Ag 纳米线 | 透光导电 |
| 电子传输层（ETL） | TiO₂、SnO₂、C₆₀、PCBM | 抽取电子、阻挡空穴 |
| 钙钛矿吸收层 | MAPbI₃、FAPbI₃、混合阳离子 | 吸光产生载流子 |
| 空穴传输层（HTL） | spiro-OMeTAD、PTAA、NiOₓ、CuSCN | 抽取空穴、阻挡电子 |
| 背电极 | Au、Ag、Cu、碳 | 收集载流子 |

### 1.5.3　钙钛矿电池工作原理

钙钛矿电池的工作流程：

1. 钙钛矿吸收层吸收光子，产生电子-空穴对（因 E_b ≈ 10 meV，室温下基本为自由载流子）；
2. 自由载流子在钙钛矿内扩散（扩散长度 > 1 μm，足以到达界面）；
3. 电子被 ETL 选择性抽取，空穴被 HTL 选择性抽取（能带对齐提供选择性）；
4. 载流子在外电路做功。

与传统 p-n 结电池不同，钙钛矿电池的载流子分离主要靠传输层的能带对齐，而非钙钛矿本身的内建电场。

### 1.5.4　钙钛矿电池性能指标

衡量电池性能的四大指标：

- **短路电流 J_sc**（mA/cm²）：单位面积光生电流；
- **开路电压 V_oc**（V）：无电流时的电压，由准费米能级分裂决定；
- **填充因子 FF**：实际最大功率与 J_sc·V_oc 之比，反映串联/并联电阻损失；
- **光电转换效率 PCE = J_sc·V_oc·FF / P_in**，P_in = 100 mW/cm²（AM1.5G）。

当前单结钙钛矿纪录（约 26.7%）的典型参数：J_sc ≈ 26 mA/cm²、V_oc ≈ 1.18 V、FF ≈ 0.86。

### 1.5.5　钙钛矿电池发展展望

钙钛矿电池的未来发展方向（贯穿后续章节）：

- **稳定性**：通过封装、二维钙钛矿、界面工程突破 IEC 61215 认证（第 4、5 章）；
- **大面积制备**：从旋涂到狭缝涂布、卷对卷印刷（第 6 章）；
- **干法工艺**：真空蒸镀与硅工艺兼容（第 7 章）；
- **无铅化**：双钙钛矿、Sn 基钙钛矿（第 8 章）；
- **叠层**：突破单结 SQ 极限（第 9 章）；
- **新应用**：室内光伏、柔性可穿戴（第 4、10 章）。

## 参考文献

1. Kojima A., Teshima K., Shirai Y., Miyasaka T. Organometal halide perovskites as visible-light sensitizers for photovoltaic cells. *J. Am. Chem. Soc.*, 2009, 131: 6050–6051. https://pubs.acs.org/doi/10.1021/ja809598r
2. Lee M. M., Teuscher J., Miyasaka T., Murakami T. N., Snaith H. J. Efficient hybrid solar cells based on meso-superstructured organometal halide perovskites. *Science*, 2012, 338: 643. https://www.science.org/doi/10.1126/science.1228604
3. Kim H.-S., et al. Lead iodide perovskite sensitized all-solid-state submicron thin film mesoscopic solar cell with efficiency exceeding 9%. *Sci. Rep.*, 2012, 2: 591. https://www.nature.com/articles/srep00591
4. Yang W. S., et al. Iodide management in formamidinium-lead-halide-based perovskite layers for efficient solar cells. *Science*, 2017, 356: 1376–1379. https://www.science.org/doi/10.1126/science.aan2301
5. NREL. Best Research-Cell Efficiency Chart. https://www.nrel.gov/pv/cell-efficiency.html
6. Stranks S. D., et al. Electron-hole diffusion lengths exceeding 1 micrometer in an organometal trihalide perovskite absorber. *Nat. Mater.*, 2013, 12: 361–365. https://www.nature.com/articles/nmat3914
7. Dong Q., et al. Electron-hole diffusion lengths > 175 μm in solution-grown CH₃NH₃PbI₃ single crystals. *Science*, 2015, 347: 967–970. https://www.science.org/doi/10.1126/science.aaa5760
8. De Wolf S., et al. Organometallic halide perovskites: Sharp optical absorption edge. *J. Phys. Chem. Lett.* https://pubs.acs.org/doi/10.1021/jz500279b
9. Whitcher T. S., et al. Band gaps of halide perovskites. *Phys. Rev. X*, 2018, 8: 021034. https://link.aps.org/pdf/10.1103/PhysRevX.8.021034
10. Kang J., Wang L.-W. High defect tolerance in lead halide perovskite CsPbBr₃. *J. Phys. Chem. Lett.*, 2017. https://escholarship.org/content/qt38j557sc
11. Chen X., et al. Excitonic effects in methylammonium lead halide perovskites. 2018. https://www.osti.gov/servlets/purl/1437220
12. Whitfield P. S., et al. Structures and phase transitions in the trihalide perovskites CH₃NH₃PbI₃. *Sci. Rep.*, 2016, 6: 35685. https://www.nature.com/articles/srep35685
13. Bartel C. J., et al. New tolerance factor to predict the stability of perovskite oxides and halides. *J. Mater. Sci.*, 2019. https://pmc.ncbi.nlm.nih.gov/articles/PMC6368436/
14. Lee J.-W., et al. UV degradation of perovskite solar cells. *Sci. Rep.*, 2016, 6: 38150. https://www.nature.com/articles/srep38150
15. Rombach F. M., Haque S. A., McGill S. A. Insights into charge recombination and loss mechanisms in perovskite solar cells. *Energy Environ. Sci.*, 2021, 14: 5161. https://pubs.rsc.org/ee/article/14/10/5161/726930
16. Shen X., et al. Defects in metal halide perovskites. *Joule*, 2023. https://www.cell.com/joule/pdf/S2542-4351(23)00039-9.pdf
17. Cresp et al. RP vs DJ 2D perovskites. *Adv. Funct. Mater.*, 2024. https://hal.science/hal-05378026v1/file/Adv%20Funct%20Materials_24%20-RP%20vs%20DJ.pdf
18. López et al. Perovskite stability review. *Chem. Soc. Rev.*, 2026. https://pubs.rsc.org/cs/article/55/8/4648/1228286
19. Fluxim. Perovskite-silicon tandem PV record updates. https://www.fluxim.com/research-blogs/perovskite-silicon-tandem-pv-record-updates
