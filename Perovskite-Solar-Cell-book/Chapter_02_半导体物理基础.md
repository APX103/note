# 第 2 章　半导体物理基础

> **核心命题**　钙钛矿太阳电池的本质是一个半导体异质结器件。理解它的效率极限，需要回到能带论、载流子统计、漂移扩散输运与非平衡复合这一套半导体物理基本图像。本章为后续器件分析提供理论坐标。

---

## 2.1　固体的能带论基础

半导体物理的起点是能带论。在孤立原子中，电子占据离散的能级；当大量原子结合成晶体时，原子轨道相互作用形成连续的**能带**。被电子完全填满的最高能带称为**价带**（valence band），其上方的未填满能带称为**导带**（conduction band），两者之间的能量禁区称为**带隙** E_g。半导体的带隙通常在 0.1–4 eV 之间。

根据布洛赫定理，周期性势场中的电子波函数具有 ψ(r) = u_k(r)·e^(ik·r) 的形式，其中 u_k(r) 具有晶格周期性。电子的能量-波矢关系 E(k) 决定了其动力学行为，其曲率通过**有效质量** m\* 表征：

```
1/m* = (1/hbar^2)(d^2E/dk^2)
```

有效质量是半导体物理的核心概念——它把晶体中复杂的周期势场简化为一个"准自由电子"模型。E-k 关系的曲率越大（能带越陡），有效质量越小，载流子越易运动。钙钛矿之所以有高载流子迁移率，正是因为其导带与价带在能带极值附近的曲率较大。

## 2.2　载流子的准经典运动

### 2.2.1　布洛赫电子的有效质量和运动速度

在外电场 E 中，布洛赫电子的群速度 v_g = (1/ℏ)(dE/dk)，加速度 dv_g/dt = qE/m\*。有效质量可以是正值（导带底，电子）或负值（价带顶）。价带顶的负有效质量在数学上等价于一个带正电的正质量粒子——这就是**空穴**（hole）的物理图像。

### 2.2.2　能带填充与材料导电特性

根据能带填充情况，固体分为：

- **导体**：价带未满或与导带重叠，外加电场即可产生电流；
- **绝缘体**：带隙很大（> 4 eV），价带电子无法被激发到导带；
- **半导体**：带隙适中（约 0.1–4 eV），少量电子可被热激发到导带，产生本征载流子。

钙钛矿 MAPbI₃ 的带隙约 1.55 eV，是典型的半导体；FAPbI₃ 的 1.48 eV 更接近 Shockley-Queisser 极限的最优带隙（1.34 eV）。

## 2.3　平衡载流子统计分布

### 2.3.1　载流子浓度计算

半导体中电子与空穴的平衡分布服从**费米-狄拉克统计**。在非简并近似（费米能级距带边 > 3kT）下，可简化为玻尔兹曼近似。导带电子浓度 n 与价带空穴浓度 p 为：

```
n = N_c · exp(-(E_c - E_F)/kT)
p = N_v · exp(-(E_F - E_v)/kT)
```

其中 N_c、N_v 分别为导带与价带的有效态密度：

```
N_c = 2·(2π·m_e\*·kT/h²)^(3/2)
N_v = 2·(2π·m_h\*·kT/h²)^(3/2)
```

以硅在 300 K 为例：N_c ≈ 2.8×10¹⁹ cm⁻³，N_v ≈ 1.04×10¹⁹ cm⁻³，E_g = 1.12 eV（Neamen, *Semiconductor Physics and Devices* 4th ed.）。

### 2.3.2　本征半导体

本征半导体（未掺杂）的费米能级 E_i 位于带隙中央附近，本征载流子浓度为：

```
n_i = √(N_c·N_v)·exp(-E_g/2kT)
```

硅在 300 K 时 n_i ≈ 1.0–1.5×10¹⁰ cm⁻³。n_i 随温度指数增长——这就是半导体器件高温性能退化的根源。钙钛矿的本征载流子浓度因带隙与有效质量不同而异，但其离子-电子混合导电特性使"本征载流子"的概念更为复杂（见 2.5 节）。

### 2.3.3　非本征半导体

通过掺杂引入施主（donor，贡献电子）或受主（acceptor，贡献空穴），可获得 N 型或 P 型半导体：

- **N 型**：掺入施主（如磷掺入硅），费米能级靠近导带，n ≈ N_D；
- **P 型**：掺入受主（如硼掺入硅），费米能级靠近价带，p ≈ N_A。

无论掺杂如何，平衡时满足**质量作用定律**：n·p = n_i²。钙钛矿的"掺杂"更为复杂——碘空位 V_I 使薄膜呈弱 N 型，而 Sn²⁺ 氧化为 Sn⁴⁺ 产生 Sn 空位使 Sn 基钙钛矿呈 P 型。

## 2.4　半导体中载流子的输运

### 2.4.1　载流子的漂移运动

在电场 E 中，载流子受力产生定向漂移，漂移速度 v_drift = μ·E，其中 μ 为迁移率。漂移电流密度：

```
J_drift = q·n·μ_n·E + q·p·μ_p·E
```

迁移率 μ 反映载流子在晶格散射下的运动能力。钙钛矿单晶的载流子迁移率可达约 100 cm²/V·s（Dong et al., 2015），与硅相当；薄膜的迁移率较低（10–50 cm²/V·s）但已足够支撑高效电池。

### 2.4.2　载流子的扩散运动

载流子浓度不均匀时，会从高浓度区向低浓度区扩散。扩散电流密度：

```
J_diff = q·D_n·(dn/dx) - q·D_p·(dp/dx)
```

其中 D 为扩散系数，与迁移率满足**爱因斯坦关系**：

```
D = μ·kT/q
```

300 K 时热电压 kT/q ≈ 25.9 mV（约 26 mV）。扩散长度 L = √(Dτ) 是载流子在复合前能扩散的距离——钙钛矿薄膜的扩散长度 > 1 μm，是其高效率的物理基础。

## 2.5　非平衡过剩载流子

### 2.5.1　非平衡载流子的产生与复合

光照或注入会打破平衡，产生非平衡过剩载流子 Δn、Δp。当激发源撤去后，过剩载流子通过**复合**消失。复合率 R 与过剩载流子浓度成正比：

```
R = Δn / τ
```

其中 τ 为**少数载流子寿命**。钙钛矿的载流子寿命从薄膜的数十 ns 到单晶的微秒级不等，长的寿命直接贡献高效率。

复合机制主要有：

- **辐射复合**（radiative）：电子-空穴直接复合发光，理想情况下主导；
- **Shockley-Read-Hall（SRH）复合**：通过深能级缺陷辅助复合，是实际损失的主因；
- **俄歇复合**（Auger）：高载流子浓度下三粒子复合。

钙钛矿的缺陷容忍性使其 SRH 复合速率低于传统半导体，这是它接近辐射复合极限的关键。

### 2.5.2　准费米能级

非平衡状态下，电子与空穴不再共享同一费米能级，而是各自有**准费米能级** E_Fn、E_Fp：

```
n = n_i·exp((E_Fn - E_i)/kT)
p = n_i·exp((E_i - E_Fp)/kT)
```

准费米能级的分裂量 ΔE_F = E_Fn - E_Fp 直接决定了太阳电池的开路电压：

```
q·V_oc ≤ E_Fn - E_Fp = kT·ln(np/n_i²)
```

钙钛矿电池的开路电压可达 1.18 V 以上，意味着准费米能级分裂接近带隙宽度（1.55 eV），与辐射复合极限的差距已缩小到约 0.3–0.4 V。

## 2.6　连续性方程

载流子的守恒关系由**连续性方程**描述：

```
∂n/∂t = G - R + (1/q)·(dJ_n/dx)
```

其中 G 为产生率（如光吸收），R 为复合率，(1/q)·(dJ_n/dx) 为电流散度的载流子贡献。空穴有对称形式。连续性方程是器件模拟的基础——与泊松方程耦合后，可数值求解电池内部的载流子分布与 I-V 曲线。

## 2.7　钙钛矿的特有物理

钙钛矿材料除上述标准半导体物理外，还有几项独特性质：

- **双极性传输**：电子与空穴的迁移率与扩散长度相当，使单一吸收层即可高效传输两类载流子；
- **离子-电子混合导电**：碘空位等可移动离子使钙钛矿呈现混合导电特性（Eames et al., *Nat. Commun.* 6, 7497, 2015，被引 3326 次）；
- **I-V 迟滞**：离子迁移导致正向/反向扫描的 I-V 曲线不重合（Calado et al., *Nat. Commun.*, 2016，被引 960 次）；
- **缺陷容忍性**：多数本征缺陷形成浅能级，使钙钛矿在缺陷态密度 10¹⁵–10¹⁶ cm⁻³ 下仍能保持高效率。

这些特性使钙钛矿不能完全用传统半导体模型描述——离子迁移的时间尺度（秒级）远慢于电子过程（纳秒级），使器件表现出独特的动态行为。

## 2.8　小结

本章建立了半导体物理的基本图像：能带决定带隙，费米能级决定载流子浓度，漂移与扩散决定输运，复合决定寿命与电压。Shockley-Queisser 单结极限（最优带隙 1.34 eV，理论效率 33.16%）是评估所有单结电池的标尺。钙钛矿的独特性在于双极性传输、离子-电子混合导电与缺陷容忍性——这些特性使其在偏离经典模型的同时仍能逼近辐射复合极限。后续各章的器件分析将以本章的物理图像为基础。

## 参考文献

1. Neamen D. A. *Semiconductor Physics and Devices*. 4th ed. McGraw-Hill, p. 113.
2. Sze S. M., Ng K. K. *Physics of Semiconductor Devices*. 3rd ed. Wiley.
3. Pierret R. F. *Semiconductor Device Fundamentals*. Addison-Wesley.
4. Shockley W., Queisser H. J. Detailed balance limit of efficiency of p-n junction solar cells. *J. Appl. Phys.*, 1961, 32: 510–520. https://en.wikipedia.org/wiki/Shockley%E2%80%93Queisser_limit
5. Stranks S. D., et al. Electron-hole diffusion lengths exceeding 1 micrometer in an organometal trihalide perovskite absorber. *Nat. Mater.*, 2013, 12: 361–365. https://www.nature.com/articles/nmat3914
6. Dong Q., et al. Electron-hole diffusion lengths > 175 μm in solution-grown CH₃NH₃PbI₃ single crystals. *Science*, 2015, 347: 967–970. https://www.science.org/doi/10.1126/science.aaa5760
7. Eames C., et al. Ionic transport in hybrid perovskite solar cells. *Nat. Commun.*, 2015, 6: 7497. https://www.nature.com/articles/ncomms8497
8. Calado P., et al. Evidence for ion migration in hybrid perovskite solar cells. *Nat. Commun.*, 2016. https://pmc.ncbi.nlm.nih.gov/articles/PMC5192183/
9. Lundstrom M. *Semiconductor Device Physics lecture notes*. Cornell University. https://hep.ph.liv.ac.uk/~gcasse/Phys389/PHYS389-lecture3.pdf
10. PV Education. *Carrier concentrations and pn junction*. https://www.pveducation.org/pvcdrom/pn-junctions/solving-for-depletion-region
11. Wikipedia. Effective mass (solid-state physics). https://en.wikipedia.org/wiki/Effective_mass_(solid-state_physics)
12. Ossila. Radiative efficiency limit (Shockley-Queisser). https://www.ossila.com/pages/radiative-efficiency-limit
13. UMich EECS517. *Einstein relation handout*. https://cpseg.eecs.umich.edu/classes/pub/eecs517/handouts/einsteins_relation.pdf
