# 第 3 章　半导体材料的接触及能带结构

> **核心命题**　钙钛矿电池的高效运作建立在一系列能带对齐之上：钙钛矿与电子/空穴传输层的异质结、金属电极的肖特基势垒、 pn 结内建电场。本章从功函数出发，串起 pn 结与肖特基接触的能带图像，为第 5 章的电荷传输层界面分析奠基。

---

## 3.1　材料的功函数

理解任何半导体接触的能带行为，起点是**功函数**（work function）Φ：把一个电子从费米能级移到真空能级所需的能量。

| 概念 | 定义 |
|---|---|
| 功函数 Φ | E_Fermi → E_vacuum 的能量 |
| 电子亲和势 χ | E_conduction band → E_vacuum 的能量 |
| 电离能 IE | E_valence band → E_vacuum 的能量 |

对金属，Φ 直接等于费米能级到真空能级的距离。对半导体，还要区分电子亲和势 χ（导带底到真空）与电离能 IE（价带顶到真空）。

典型材料的功函数（参考值，具体取决于表面状态）：

| 材料 | 功函数（eV） |
|---|---|
| Au | 约 5.1 |
| Ag | 约 4.3 |
| ITO | 约 4.7–4.9 |
| TiO₂（ETL） | 约 4.0–4.2 |
| MAPbI₃ | 约 4.3（导带底约 −3.9 至 −4.1 eV） |
| spiro-OMeTAD（HTL） | 约 5.0 |

spiro-OMeTAD 氧化掺杂后 HOMO 能级进一步加深约 420 meV（≈ −5.4 eV，Rombach et al., *Energy Environ. Sci.* 14, 5161, 2021）。这些功函数差异决定了载流子在界面间的流动方向与势垒高度。

## 3.2　同质 pn 结能带结构及其特性

### 3.2.1　pn 结能带结构

把 P 型半导体与 N 型半导体接触，多数载流子因浓度梯度扩散（空穴从 P 侧向 N 侧，电子从 N 侧向 P 侧），在界面处留下固定的离子化施主（N 侧正）与受主（P 侧负），形成**空间电荷区**（也叫耗尽区，depletion region）。空间电荷产生**内建电场** E_bi，方向从 N 指向 P，最终与扩散流平衡，结两侧费米能级拉平。

能带图上表现为：N 侧能带上翘、P 侧能带下弯，形成"阶梯"状的能带弯曲。导带与价带在结区的总弯曲量等于内建电势 V_bi：

```
V_bi = (kT/q)·ln(N_A·N_D / n_i²)
```

### 3.2.2　pn 结内电场强度

内建电场是 pn 结整流特性的物理基础。在耗尽区内，电场在冶金结面处最强，向两侧线性衰减（突变结近似）。最大电场：

```
E_max = q·N_A·x_p / ε_s = q·N_D·x_n / ε_s
```

其中 x_p、x_n 是耗尽区在 P、N 侧的宽度，ε_s 是半导体介电常数。

对钙钛矿电池而言，传统 p-n 结的概念并不完全适用——钙钛矿吸收层本身不是 p-n 结，而是依赖与 ETL、HTL 形成的异质结能带对齐来抽取载流子（见 3.3.3 与第 5 章）。但内建电场与耗尽区的概念仍是理解钙钛矿/传输层界面的工具。

### 3.2.3　空间电荷区宽度和结电容

耗尽区总宽度 W（PV Education 标准公式）：

```
W = √[ (2ε_s/q)·(N_A + N_D)/(N_A·N_D)·(V_bi − V) ]
```

W 随正向偏压 V 减小、随反向偏压增大。结电容（耗尽层电容）：

```
C_j = ε_s / W
```

C_j 随偏压变化，这是变容二极管与一些电容-电压（C-V）表征技术的物理基础。

## 3.3　金属半导体接触肖特基势垒

### 3.3.1　肖特基势垒的形成

金属与半导体接触时，因功函数差而在界面处形成势垒。对 N 型半导体，理想肖特基势垒高度遵循 **Schottky-Mott 规则**：

```
Φ_Bn = Φ_M − χ_S
```

即金属功函数 Φ_M 与半导体电子亲和势 χ_S 之差。若 Φ_Bn 较大，接触表现为整流特性（肖特基二极管）；若 Φ_Bn 很小或为负，则表现为欧姆接触。

### 3.3.2　费米能级钉扎

实际金属-半导体接触常偏离 Schottky-Mott 规则的预测——势垒高度几乎不随金属功函数变化，称为**费米能级钉扎**（Fermi level pinning）。原因是界面态（金属诱导带隙态 MIGS、缺陷态等）把费米能级"钉"在带隙中的某个固定位置。这一现象在钙钛矿/金属电极界面同样存在，影响背电极的接触电阻与载流子抽取。

### 3.3.3　钙钛矿电池中的能带对齐

钙钛矿电池的高效运作依赖三类关键能带对齐（详见第 5 章）：

1. **钙钛矿/HTL 异质结**：HTL 的 HOMO/价带需高于（更接近真空能级）钙钛矿的价带顶，以利空穴抽取；spiro-OMeTAD（HOMO ≈ −5.0 eV）与 MAPbI₃（VBM ≈ −5.4 eV）的对齐提供空穴抽取驱动力。
2. **钙钛矿/ETL 异质结**：ETL 的导带需低于（更负）钙钛矿导带底，以利电子抽取；TiO₂（CB ≈ −4.0 至 −4.2 eV）与 SnO₂ 的导带位置与 MAPbI₃（CB ≈ −3.9 至 −4.1 eV）匹配良好（Kumar et al., *Nanomaterials*, 2021）。
3. **金属背电极接触**：Au（Φ ≈ 5.1 eV）与 spiro-OMeTAD 形成准欧姆接触；Ag 在 p-i-n 倒置结构中与 C₆₀/BCP 形成电子抽取接触。

异质结能带对齐的三种类型（ResearchGate 综述；ACS Langmuir, 2021）：

- **Type-I（straddling，跨骑）**：ETL 与 HTL 的带隙都大于钙钛矿，电子与空穴都被限制在钙钛矿内——这是钙钛矿电池的理想构型；
- **Type-II（staggered，交错）**：一种载流子的带边跨越钙钛矿，有利于电荷分离（如某些量子点异质结）；
- **Type-III（broken，断开）**：带边完全错开，可用于隧穿结（如叠层电池的中间复合层）。

## 3.4　小结

本章建立了半导体接触的能带图像：功函数决定金属与半导体的接触特性；同质 pn 结通过耗尽区内建电场实现整流；肖特基势垒由金属-半导体功函数差决定，但常因费米能级钉扎而偏离理想模型。钙钛矿电池虽不依赖传统 p-n 结，但其高效运作依赖钙钛矿与 HTL/ETL 的精确能带对齐——Type-I 异质结对齐是理想构型。这些能带对齐原则是第 5 章电荷传输层界面工程的物理基础。

## 参考文献

1. Sze S. M., Ng K. K. *Physics of Semiconductor Devices*. 3rd ed. Wiley, Ch.1.
2. Neamen D. A. *Semiconductor Physics and Devices*. 4th ed. McGraw-Hill.
3. PV Education. Solving for the depletion region width. https://www.pveducation.org/pvcdrom/pn-junctions/solving-for-depletion-region
4. Rombach F. M., Haque S. A., McGill S. A. Insights into charge recombination and loss mechanisms in perovskite solar cells. *Energy Environ. Sci.*, 2021, 14: 5161. https://pubs.rsc.org/ee/article/14/10/5161/726930
5. Kumar et al. Energy level alignment in perovskite/ETL. *Nanomaterials*, 2021. https://pmc.ncbi.nlm.nih.gov/articles/PMC7970561/
6. Wikipedia. Schottky barrier. https://en.wikipedia.org/wiki/Schottky_barrier
7. ACS Appl. Electron. Mater. Fermi level pinning at metal-semiconductor contacts. 2024. https://pubs.acs.org/doi/10.1021/acsaelm.3c01231
8. ACS Langmuir. Heterojunction band alignment types. 2021. https://pubs.acs.org/doi/10.1021/acs.langmuir.1c00209
9. Warwick University. *Metal-semiconductor contact lecture notes*.
