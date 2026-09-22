# 第 9 章　钙钛矿叠层太阳电池

> **核心命题**　单结电池受 Shockley-Queisser 极限约束（最优 33.7%，带隙 1.34 eV），叠层是突破 30% 效率的唯一路径。钙钛矿/硅叠层在 2024 年由隆基（LONGi）推到 34.6%，全钙钛矿叠层在 2025 年达 30.1%——均已超越单结硅（27.3%）与单结钙钛矿（26.7%）的极限。本章覆盖四端、两端钙钛矿/硅、全钙钛矿、钙钛矿/有机四类叠层架构的设计与挑战。

---

## 9.1　钙钛矿材料的带隙调控

叠层电池的核心原理是把太阳光谱分段利用：顶电池吸收高能短波光子（用宽带隙材料），底电池吸收低能长波光子（用窄带隙材料），减少热化损失。这要求顶/底电池的带隙精确匹配。

钙钛矿的卤素组成可调性使其天然适合叠层：

| 顶/底电池 | 材料 | 带隙（eV） | 作用 |
|---|---|---|---|
| 宽带隙顶电池 | 混合 Br/I 钙钛矿 | 约 1.68–1.75 | 吸收短波 |
| 窄带隙底电池 | Pb-Sn 混合钙钛矿 | 约 1.20–1.25 | 吸收长波 |
| 硅底电池 | c-Si | 约 1.12 | 吸收长波 |

宽带隙钙钛矿（混合 Br/I）的典型带隙 1.68 eV 和 1.75 eV（Bush/McGehee 工作，*ACS Energy Letters*, 2018，被引 571 次），与硅底电池（1.12 eV）或 Pb-Sn 窄带隙钙钛矿（1.2 eV）匹配。带隙调控的核心挑战是**光致相分离**——带隙 > 1.65 eV 的 I/Br 混合卤化物钙钛矿在光照下易发生卤素偏聚，导致带隙窄化与效率退化（Yu et al., 2024，被引 22 次）。

理论极限：两端（2T）双结叠层电池最高效率可达 **45%**（Sun et al., *Phys. Status Solidi A*, 2025），远超单结 33.7%。

## 9.2　四端钙钛矿叠层太阳电池

**四端（4T）叠层**是最简单的叠层架构：顶电池与底电池机械堆叠，各自独立引出电极（共四个端子）。优势是顶/底电池可独立优化、无电流匹配约束；缺点是需要两套电路、两个逆变器，系统成本高。

### 9.2.1　透明电极

4T 叠层要求顶电池的背电极**透明**（让长波光透过到底电池）。透明电极的挑战是同时实现高透光（> 90%）与低方阻（< 10 Ω/□），主流方案：

- IZO（铟锌氧化物）：高透光、低方阻、可低温沉积；
- 超薄金属（Au、Ag、Cu）：厚度 < 10 nm，兼顾透光与导电；
- TCO（透明导电氧化物）：FTO、ITO。

### 9.2.2　半透明钙钛矿太阳电池

半透明钙钛矿电池是 4T 叠层顶电池的关键组件。通过透明电极与宽带隙钙钛矿的组合，实现顶电池对短波光的吸收 + 长波光的透过。典型半透明钙钛矿电池效率 14–18%，4T 钙钛矿/硅叠层整体效率可达 25–28%。

## 9.3　两端钙钛矿/硅叠层太阳电池

**两端（2T）钙钛矿/硅叠层**是当前效率纪录最活跃的方向：顶/底电池单片集成在同一衬底上，共用两个端子。优势是系统简单（一个逆变器）、成本低；挑战是顶/底电池的电流必须匹配，且中间复合层的工艺复杂。

### 9.3.1　宽带隙钙钛矿太阳电池

顶电池必须用宽带隙钙钛矿（1.68–1.75 eV）以让长波光透过到底电池。关键挑战：

- **光致相分离**：Br/I 混合钙钛矿在光照下卤素偏聚，带隙窄化（见 9.1）；
- **V_oc 损失**：宽带隙钙钛矿的 V_oc 损失（相对带隙）通常大于窄带隙；
- **顶电池厚度**：需精确控制顶电池厚度以实现电流匹配。

代表性宽带隙钙钛矿：Cs₀.₂₂FA₀.₇₈Pb(I₀.₈₅Br₀.₁₅)₃（带隙约 1.68 eV）、MAPb(I₀.₆Br₀.₄)₃（带隙约 1.75 eV）。

### 9.3.2　绒面硅和平面硅太阳电池

底电池的表面形貌对顶电池沉积影响巨大：

- **绒面硅（textured Si）**：商业化硅电池的标准形貌，金字塔结构减反效果好，但钙钛矿层在金字塔斜面上难以均匀沉积；
- **平面硅（flat Si）**：钙钛矿层易于均匀沉积，但硅底电池的减反效果差；
- **亚微米织构**：介于绒面与平面之间，兼顾减反与钙钛矿沉积可行性，效率可超 30%（De Bastiani et al., *J. Mater. Chem. A*, 2020，被引 149 次）。

### 9.3.3　中间电荷复合层

2T 叠层的中间复合层（recombination layer / tunnel junction）连接顶电池的电子与底电池的空穴，是单片集成的关键。主流方案：

- **IZO（铟锌氧化物）**：优异的电光性能，是主流选择（Harter et al., *ACS Energy Letters*, 2024，被引 50 次）；
- **SnO₂ / ITO**：双层结构；
- **C₆₀ / SnO₂**：有机-无机复合；
- **隧穿结**：高掺杂 p⁺⁺/n⁺⁺ 结，载流子通过量子隧穿复合。

### 9.3.4　减反层

顶电池表面的减反层（anti-reflection layer）提升光利用率：

- **MgF₂**：经典减反材料，折射率约 1.38；
- **LiF**：更优的减反效果，同时兼具 UV 滤光功能；
- **纳米结构减反**：亚波长纳米柱、蛾眼结构。

### 9.3.5　效率纪录

两端钙钛矿/硅叠层的效率进展：

- 2017 年 Bush/McGehee 报道 23.6%（*Nat. Energy*）；
- 2020 年 Al-Ashouri 突破 29%（*Science*）；
- 2023 年 11 月 **LONGi 宣布 33.9%**（隆基官方；Liu et al., *Nature*, 2024，被引 501 次，经认证稳定 PCE 33.89%）；
- 2024 年 6 月 LONGi 提升至 **34.6%**；
- 2024 年 Science 报道无铟透明电极（用 RPD-SnOₓ 替代 ITO）钙钛矿/硅叠层认证 **33.6%**（*Science*, 2024，DOI 10.1126/science.aef5355），证明了无铟工艺的产业化可行性。

叠层理论极限 45%，当前纪录 34.6% 仍有巨大提升空间。

## 9.4　两端全钙钛矿叠层太阳电池

**全钙钛矿叠层**（all-perovskite tandem）用 Pb-Sn 窄带隙钙钛矿底电池替代硅，实现"全薄膜、轻量化、柔性"叠层。

### 9.4.1　高效 Pb-Sn 窄带隙钙钛矿太阳电池

Pb-Sn 混合钙钛矿（如 FA₀.₇₅Cs₀.₂₅Pb₀.₅Sn₀.₅I₃）的带隙约 **1.2–1.25 eV**（Lim et al., *Energy Environ. Sci.*, 2024，被引 156 次），是全钙钛矿叠层底电池的关键。底电池单结效率已 > 22%。主要挑战是 Sn²⁺ 氧化（详见第 8 章），需要严格的惰性气氛工艺与抗氧化策略。

### 9.4.2　中间电荷复合层

全钙钛矿叠层的中间复合层需在两个钙钛矿层之间工作，挑战包括：

- 溶剂兼容性（顶电池沉积不能溶解底电池）；
- 界面缺陷控制；
- 离子迁移阻挡。

常用方案：SnO₂ / ITO / PEDOT:PSS 等多层结构。

### 9.4.3　效率纪录

全钙钛矿叠层的效率进展：

- 2022 年单结效率约 27.4%；
- 2024 年 SolaEon 报道 29.34%；
- 2025 年基于极性钝化降低缺陷，认证 **30.1%**（器件效率 30.6%，Lin & Tan 团队 *Nature*；*PV Magazine*, 2025）；
- 2025 年 SolaEon 进一步推到 31.38%（当前全钙钛矿叠层最高报道之一）。

当前 NREL 效率表已单列"全钙钛矿叠层"子类记录这些绝对效率纪录。

## 9.5　两端钙钛矿/有机叠层太阳电池

钙钛矿/有机叠层用有机太阳能电池（OPV）作为窄带隙底电池。代表性工作：宽带隙钙钛矿顶电池（1.79–1.86 eV）+ 有机底电池，最高效率 **26.4%**（认证 25.56%，*Nature News & Views*, 2024）。优势是全柔性、全溶液工艺；局限是有机底电池的稳定性与效率仍低于硅或 Pb-Sn 钙钛矿。

## 9.6　总结与展望

钙钛矿叠层电池的效率纪录汇总：

| 架构 | 效率 | 理论极限 |
|---|---|---|
| 4T 钙钛矿/硅 | 约 25–28% | — |
| 2T 钙钛矿/硅 | 34.6%（LONGi） | 45% |
| 2T 全钙钛矿 | 31.38%（SolaEon，2025） | 45% |
| 2T 钙钛矿/有机 | 26.4% | — |

产业化的核心玩家：

- **Oxford PV**（英国）：2024 年 9 月完成钙钛矿/硅叠层组件首批商业销售，组件效率 24.5%；
- **LONGi（隆基）**：钙钛矿/硅叠层 34.6% 纪录的产业化产线；
- **Hanwha Q-Cells**：商业化 M10 钙钛矿/硅叠层电池效率 **28.6%**（2024 年 12 月），1000 小时 MPPT 后保持 95% 效率。

叠层电池是钙钛矿光伏突破单结极限、挑战晶硅主流地位的终极路径。未来 3–5 年，钙钛矿/硅叠层的产业化组件效率有望突破 28–30%，全钙钛矿叠层有望突破 32%。

## 参考文献

1. Shockley W., Queisser H. J. Detailed balance limit of efficiency of p-n junction solar cells. *J. Appl. Phys.*, 1961, 32: 510.
2. Sun J., et al. Tabulated values of the Shockley-Queisser limit for tandem solar cells. *Phys. Status Solidi A*, 2025. https://onlinelibrary.wiley.com/doi/10.1002/pssa.202400524
3. Bush K. A., et al. Compositional engineering for efficient wide band gap perovskites. *ACS Energy Lett.*, 2018. https://www.colorado.edu/lab/mcgehee/sites/default/files/attached-files/compositional_engineering_for_efficient_wide_band_gap_perovskites_with_improved_stability_to_photoinduced_phase_segregation.pdf
4. Yu et al. Phase segregation in wide-bandgap perovskites. 2024. https://www.sciopen.com/article/10.26599/EMD.2024.9370037
5. LONGi. 33.9% perovskite/silicon tandem record. 2023. https://www.longi.com/en/news/new-world-record-for-the-efficiency-of-crystalline-silicon-perovskite-tandem-solar-cells/
6. Liu J., et al. Perovskite/silicon tandem with 33.89% certified efficiency. *Nature*, 2024. https://pubmed.ncbi.nlm.nih.gov/39236747/
7. Harter A., et al. IZO recombination layer for tandem cells. *ACS Energy Lett.*, 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC11565564/
8. De Bastiani M., et al. Textured Si bottom cell for perovskite/silicon tandem. *J. Mater. Chem. A*, 2020. https://pubs.rsc.org/mh/article/7/11/2791/690275/
9. Lim J. W., et al. All-perovskite tandem solar cells: from fundamentals to technological translation. *Energy Environ. Sci.*, 2024. https://pubs.rsc.org/ee/article/17/13/4390/807715/
10. PV Magazine. All-perovskite tandem with dipolar passivation achieves 30.1% efficiency. 2025. https://www.pv-magazine.com/2025/12/01/all-perovskite-tandem-solar-cell-with-dipolar-passivation-achieves-30-1-efficiency/
11. Nature News & Views. Perovskite/organic tandem solar cells. 2024. https://www.nature.com/articles/d41586-024-03789-1
12. Bush K. A., et al. 23.6%-efficient monolithic perovskite/silicon tandem solar cells. *Nat. Energy*, 2017.
13. Al-Ashouri A., et al. Monolithic perovskite/silicon tandem with 29% efficiency. *Science*, 2020.
14. Oxford PV. First commercial perovskite-silicon tandem modules. 2024-09. https://www.oxfordpv.com/press-releases
15. Hanwha Q-Cells. 28.6% commercial M10 perovskite-silicon tandem. 2024. https://www.hanwha.com/newsroom/news/press-releases/hanwha-qcells-achieves-world-record-efficiency-for-commercially-scalable-perovskite-silicon-tandem-solar-cell.do
16. Green M. A., et al. Solar cell efficiency tables. *Prog. Photovolt.*, 2024. https://onlinelibrary.wiley.com/doi/full/10.1002/pip.3831
17. NREL. Best Research-Cell Efficiency Chart. https://www.nrel.gov/pv/cell-efficiency.html
