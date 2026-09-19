# 第 11 章　钙钛矿太阳电池研究中的常用尖端表征技术

> **核心命题**　时间分辨与空间分辨光谱是钙钛矿电池机理研究的眼睛——它们把载流子寿命、缺陷密度、界面复合、相分离这些不可见的微观过程变成可测量的数字。本章介绍瞬态吸收光谱（TAS）、瞬态荧光光谱（TRPL）、各类显微与电学表征技术，及其在钙钛矿电池研究中的具体应用。

---

## 11.1　时间分辨光谱技术

时间分辨光谱通过皮秒至微秒时间尺度的泵浦-探测，捕捉载流子的产生、传输、复合全过程，是钙钛矿机理研究的核心工具。

### 11.1.1　瞬态吸收光谱

**瞬态吸收光谱**（Transient Absorption Spectroscopy，TAS）是泵浦-探测（pump-probe）技术：先用一束强泵浦光激发样品，再用一束弱探测光在不同延迟时间测量样品的吸收变化 ΔA(λ, t)。TAS 可同时捕捉：

- **基态漂白**（ground-state bleach, GSB）：激发态布居导致基态吸收减少；
- **受激发射**（stimulated emission, SE）：激发态受激发射；
- **光诱导吸收**（photoinduced absorption, PA）：激发态或陷阱态的吸收。

**在钙钛矿研究中的应用**：

- Price 等（*Nat. Commun.*, 2015，被引 783 次）首次用 TAS 研究 MAPbI₃ 的热载流子分布，证明钙钛矿的热载流子冷却显著缓慢——这是热载流子电池研究的基础；
- 区分激子与自由载流子（通过 GS/SE 峰的位置与演化）；
- 测量电荷抽取效率（在有/无传输层时对比载流子寿命变化）；
- 追踪光致相分离（Br/I 偏聚）的动力学。

TAS 的优势是时间分辨率高（飞秒至纳秒），可覆盖从热载流子冷却到陷阱复合的全过程。

### 11.1.2　瞬态荧光光谱

**瞬态荧光光谱**（Time-Resolved Photoluminescence，TRPL）测量样品光致发光强度随时间的衰减，是评估钙钛矿载流子寿命与缺陷密度的标准方法。

**双指数拟合**（Staub et al., *Phys. Rev. Applied*, 2016，被引 338 次）：

TRPL 衰减曲线通常用双指数拟合：

```
I(t) = A₁·exp(-t/τ₁) + A₂·exp(-t/τ₂)
```

- **τ₁（快分量，数十 ns）**：界面或缺陷辅助的非辐射复合；
- **τ₂（慢分量，数百 ns 至 μs）**：体相辐射复合；
- **平均寿命** τ_ave = (A₁τ₁² + A₂τ₂²)/(A₁τ₁ + A₂τ₂)。

**在钙钛矿研究中的应用**：

- **评估载流子寿命**：高质量钙钛矿薄膜 τ_ave 可达数百 ns，单晶可达 μs 级；
- **缺陷密度评估**：τ₁ 越短、A₁ 占比越大，界面缺陷越严重；
- **界面复合损失**：对比钙钛矿单独、钙钛矿/ETL、钙钛矿/HTL 的 TRPL，可量化界面复合损失（载流子被传输层抽取导致 PL 寿命缩短）；
- **钝化效果评估**：钝化前后 TRPL 寿命的变化是钝化有效性的直接证据。

### 11.1.3　时间分辨率光谱技术在太阳电池研究中的应用

时间分辨光谱在钙钛矿电池研究中的具体应用场景：

1. **载流子动力学**：从光吸收到复合的全过程，包括热载流子冷却（fs–ps）、载流子-声子散射（ps–ns）、陷阱复合（ns–μs）；
2. **缺陷表征**：通过 TRPL 寿命与 SCLC（空间电荷限制电流）结合，估算缺陷密度（详见 11.2.4）；
3. **界面电荷抽取**：对比钙钛矿/传输层界面的 PL 猝灭程度，量化电荷抽取效率；
4. **相分离动力学**：用原位 TAS 追踪光照下 Br/I 偏聚的时间演化；
5. **稳定性退化机理**：原位监测老化过程中载流子寿命的变化，定位退化根源。

## 11.2　空间分辨显微技术

空间分辨显微技术把测量聚焦到纳米至微米尺度，揭示钙钛矿薄膜的横向不均匀性、晶界行为、缺陷分布。

### 11.2.1　共聚焦荧光显微镜与 PL mapping

共聚焦荧光显微镜与 PL（光致发光）mapping 通过扫描样品表面，绘制 PL 强度与寿命的二维分布。应用：

- 揭示薄膜横向不均匀性（亮区 vs 暗区）；
- 定位非辐射复合中心（PL 暗点对应缺陷富集）；
- 评估晶界与晶内的复合差异。

### 11.2.2　电子显微镜（SEM/TEM/EBSD）

- **扫描电子显微镜（SEM）**：表面形貌与晶粒尺寸，是钙钛矿薄膜的基础表征；
- **透射电子显微镜（TEM）**：原子级结构与界面分析；
- **电子背散射衍射（EBSD）**：晶体学取向图。

EBSD 在钙钛矿研究中揭示了一个重要发现：SEM 图像中常见的"畴"常被误认为晶粒（Muscarella et al., *J. Phys. Chem. Lett.*, 2019，被引 153 次）；MAPbI₃ 的晶体学取向本身不直接决定光学与局部电子性质。Jariwala 等（*Joule*, 2019，被引 308 次）用超高灵敏 EBSD 把 PL 与取向图叠加，发现局部晶体取向偏差与非辐射复合相关。Sun 等（*Adv. Energy Mater.*, 2020，被引 46 次）综述了 EBSD 在卤化物钙钛矿中的应用，指出电子束损伤是该技术历史应用不足的原因。

### 11.2.3　原子力显微镜（AFM）与衍生技术

- **AFM（原子力显微镜）**：表面形貌与粗糙度；
- **导电 AFM（c-AFM）**：纳米级电流分布，揭示横向导电不均匀性；
- **开尔文探针力显微镜（KPFM）**：纳米级表面电势与功函数分布（Lanzoni et al., 2021，被引 70 次）；
- **扫描隧道显微镜（STM）**：原子级表面结构与态密度。

KPFM 在钙钛矿研究中特别有价值——它可直接测量表面功函数的横向分布，揭示相分离、离子迁移、界面偶极的局部变化。

### 11.2.4　其他常用表征技术

| 技术 | 测量对象 | 应用 |
|---|---|---|
| XRD（X 射线衍射） | 晶体结构、相纯度 | 钙钛矿相 vs δ 相、晶格参数 |
| XPS（X 射线光电子能谱） | 化学态、元素组成 | Pb²⁺ vs Pb⁰、Sn²⁺ vs Sn⁴⁺（Lin et al., 2021，被引 121 次） |
| UPS（紫外光电子能谱） | 功函数、VBM、能级 | 能带对齐图绘制 |
| UV-Vis（紫外可见吸收） | 光学带隙、吸收系数 | 带隙测量、Tauc plot |
| EQE（外量子效率） | 光子-电子转换效率 | 光谱响应、电流损失分析 |
| IQE（内量子效率） | 吸收光子的转换效率 | 区分反射损失与复合损失 |
| 暗 I-V | 二极管特性、复合 | 理想因子 n、V_oc 损失 |
| TPV/TPC（瞬态光电压/电流） | 复合动力学 | 载流子寿命、复合速率 |
| 阻抗谱（EIS） | 复合电阻、离子过程 | R_rec、离子迁移追踪（Hauff et al., 2022，被引 327 次） |
| SCLC（空间电荷限制电流） | 缺陷密度、迁移率 | 陷阱密度 t_SCLC（Le Corre et al., 2021，被引 714 次） |

### 11.2.5　SCLC 与缺陷密度

**空间电荷限制电流（SCLC）** 是钙钛矿缺陷密度评估的标准方法：通过单载流子器件（如 ITO/PEDOT/钙钛矿/PCBM/Ag 仅传输空穴）的暗 I-V 曲线，提取陷阱密度。典型曲线在低偏压为欧姆区（I ∝ V）、中偏压为陷阱填充区（I ∝ V^n, n > 3）、高偏压为 Child's law 区（I ∝ V²）。陷阱密度：

```
N_t = (2ε·V_TFL) / (q·L²)
```

其中 V_TFL 是陷阱填充极限电压，L 是器件厚度。钙钛矿薄膜的 N_t 典型值 10¹⁵–10¹⁶ cm⁻³。

需要注意的是，Le Corre 等在后续批判性论文（2024，被引 49 次）中指出 SCLC 在卤化物钙钛矿中因离子迁移、滞后等问题存在争议，使用需谨慎——这与他们 2021 年（被引 714 次）的推广性综述形成对照。

### 11.2.6　UPS 与能级对齐

UPS（紫外光电子能谱）用 He I（21.2 eV）光源测量样品的功函数、电离能（VBM 位置），是绘制能带对齐图的核心工具。结合 UV-Vis 测量的带隙，可确定导带位置。UPS 在钙钛矿界面工程（第 5 章）中用于验证 ETL/HTL 与钙钛矿的能带对齐是否如设计预期。

## 11.3　小结

时间分辨与空间分辨表征技术是钙钛矿电池机理研究的眼睛。TAS 揭示热载流子与相分离动力学，TRPL 量化载流子寿命与缺陷，EBSD/KPFM 揭示横向不均匀性，XPS/UPS 确定化学态与能级，SCLC/EIS 测量缺陷密度与复合电阻。这些表征的合理组合——而非单一技术——是理解钙钛矿电池效率损失与稳定性退化的关键。研究者在使用时需注意各技术的局限（如 SCLC 的离子迁移干扰、XPS 的束损伤、EBSD 的电子束损伤），批判性地解读数据。

## 参考文献

1. Price M. B., et al. Hot-carrier cooling and photoinduced refractive index changes in organic-inorganic lead halide perovskites. *Nat. Commun.*, 2015. https://www.nature.com/articles/ncomms9420
2. Staub F., et al. Beyond bulk lifetimes: Insights into lead halide perovskite films from time-resolved photoluminescence. *Phys. Rev. Applied*, 2016, 6: 044017. https://link.aps.org/doi/10.1103/PhysRevApplied.6.044017
3. Muscarella L. A., et al. Crystallographic orientation and the open-circuit voltage in perovskite solar cells. *J. Phys. Chem. Lett.*, 2019. https://pubs.acs.org/doi/10.1021/acs.jpclett.9b02757
4. Jariwala S., et al. Crystallographic and electronic mismatches in perovskite solar cells. *Joule*, 2019. https://www.sciencedirect.com/science/article/pii/S2542435119304295
5. Sun S., et al. EBSD review for halide perovskites. *Adv. Energy Mater.*, 2020. https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/aenm.2022000364
6. Lanzoni et al. KPFM modes for perovskite characterization. 2021. https://www.sciencedirect.com/science/article/pii/S2211285521005255
7. Lin H., et al. In situ XPS of perovskite degradation. *npj Materials Degradation*, 2021. https://www.nature.com/articles/s41529-021-00162-9
8. Le Corre V. M., et al. Charge extraction via SCLC for perovskite. *ACS Energy Lett.*, 2021. https://pmc.ncbi.nlm.nih.gov/articles/PMC8043077/
9. Le Corre V. M., et al. SCLC: A problematic technique for metal halide perovskites. 2024. https://portal.findresearcher.sdu.dk/en/publications/space-charge-limited-current-measurements-a-problematic-technique/
10. Hauff E. A., et al. Impedance spectroscopy of perovskite solar cells. *J. Mater. Chem. C*, 2022. https://pubs.rsc.org/tc/article/10/2/742/753839/
11. Roose B., et al. EIS of all-perovskite tandem. *ACS Energy Lett.*, 2024. https://pubs.acs.org/doi/10.1021/acsenergylett.3c02018
12. deQuilettes D. W., et al. Photoinduced halide redistribution in mixed-halide perovskites. *Nat. Commun.*, 2016.
13. Stranks S. D., et al. Recombination kinetics in organic-inorganic perovskites. *J. Phys. Chem. Lett.*, 2014.
14. Kratos Analytical. XPS and UPS of PbBr perovskite. https://www.kratos.com/wp-content/uploads/2024/02/MO456A-XPS-and-UPS-of-a-PbBr-Perovskite-with-Work-Function-Measurement.pdf
15. Journal of Applied Physics. IMPS/IMVS for perovskite IQE. 2020. https://pubs.aip.org/aip/jap/article/128/13/133103/1027191/
