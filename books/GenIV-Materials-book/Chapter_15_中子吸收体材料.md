# 第 15 章　中子吸收体材料

> **核心命题**　中子吸收体通过 (n,α)、(n,γ) 反应把中子"吃掉"，是反应堆控制棒、停堆屏蔽与可燃毒物的核心功能材料。B4C（碳化硼）以 ¹⁰B 的 3837 barns 热中子俘获截面成为快堆控制棒的主流，但 (n,α) 反应释放的氦会导致肿胀与开裂——这是 B4C 控制棒寿期的根本限制。EuB6、Eu2O3 等稀土吸收体试图通过减少 He 释放延长寿期。

---

## 15.1　引言：中子吸收体的功能定位

中子吸收体（neutron absorber）是一类与结构材料功能截然不同的核材料——它不承载机械载荷（至少不是主要功能），而是通过**高中子俘获截面**把中子"吃掉"，实现对反应性的控制。它的三类核心应用：

1. **控制棒（control rod）**：可移动的吸收体组件，通过插入/抽出堆芯调节反应性；
2. **停堆屏蔽（shutdown shielding）**：永久或半永久的高吸收截面部件，提供后备停堆能力；
3. **可燃毒物（burnable poison）**：在燃料周期初提供负反应性补偿，随运行逐渐"燃耗"消失。

第四代堆（特别是快中子堆）的控制棒工况远比现役轻水堆严苛：高温（500–600 ℃）、高剂量（>100 dpa，>10²¹ n/cm²）、寿期约 800 EFPD（等效满功率天）。这把中子吸收体的选材与寿期评估推到了新的高度。

## 15.2　主要吸收材料

第四代堆与快堆的主要中子吸收材料可分为四大类：

### 15.2.1　B4C（碳化硼，快堆主流）

B4C 是快堆控制棒的主流材料，其优势在于：

- **¹⁰B 的极高俘获截面**：¹⁰B 热中子（0.025 eV）俘获截面 = **3837 barns**（JAEA JENDL 核数据；Carter et al., *Phys. Rev.* 92, 1953）；
- **¹⁰B(n,α)⁷Li 反应无共振峰**：截面随中子能量单调下降（1/v 行为），适合宽谱屏蔽；
- **高硬度**：约 36 GPa（Vickers），第三硬已知陶瓷；
- **理论密度**：2.52 g/cm³，菱方晶体结构；
- **熔点高**：约 2445 ℃（分解温度 2350 ℃）。

天然硼的俘获截面约 749 barns（¹⁰B 丰度约 19.9%），快堆控制棒通常使用 **¹⁰B 富集**的 B4C 以提升寿期。

### 15.2.2　Eu2O3、EuB6（稀土吸收体）

铕（Eu）的两个稳定同位素 ¹⁵¹Eu、¹⁵³Eu 都有极高的中子俘获截面，是 B4C 的有力替代：

- **Eu₂O₃（氧化铕）**：作为液态金属快堆（LMFBR）候选吸收体被评估（Pasto, 1976, OSTI）；但热导率低，辐照中易致芯块开裂（IAEA 综述称其为"反应堆用最重要的铕化合物"）；
- **EuB₆（六硼化铕）**：作为 B4C 替代品，**He 生成更少、肿胀更轻、寿期更长**；美国 FFTF 计划与法国 CEA 均评估过（Birney, 1984, INIS）。CEA 现代综述（Guo et al., 2018）把 EuB₆ 列为"减少肿胀、延长寿期"的 B4C 替代方案。

### 15.2.3　Ag-In-Cd（压水堆沿用）

**Ag-In-Cd** 是低熔点三元合金：Cd 吸收热中子、In 与 Ag 吸收超热中子——这是 **PWR 标准控制棒吸收体**（IAEA-TECDOC-1132, 1998）。在第四代堆中较少使用，主要因熔点低（约 780 ℃）不适合高温工况。

### 15.2.4　Hf（铪）与 Ta（钽）

**Hf（铪）** 是高熔点金属，天然 6 种稳定同位素**均有高俘获截面**——这是它独特的优势。早期美国海军反应堆与商用 PWR 采用；可与 **Ta（钽）固溶强化**形成 Hf-Ta 合金（IAEA-TECDOC-1132；NRC ML020810111）。Hf 的高成本与有限供应是其在大型快堆中推广的障碍。

IAEA-TECDOC-1132 把三大类吸收体并列：陶瓷 B4C、高熔点金属 Hf、低熔点合金 Ag-In-Cd。

## 15.3　B4C 在快堆中的辐照行为

B4C 是快堆控制棒的主流，但它的辐照行为复杂——这是其寿期的根本限制。

### 15.3.1　氦产生与肿胀

¹⁰B(n,α)⁷Li 反应产物是 **α 粒子与 ⁷Li**——α 粒子即氦核（⁴He）。He 在 B4C 晶界/晶内聚集成气泡导致肿胀与开裂。辐照后形成的"helium bubbles"是肿胀主因（You et al., *J. Nucl. Sci. Technol.*, 2018，样品辐照至约 80×10²⁰ captures/cm³）。

法国 Phénix LMFBR 辐照实验表明 B4C 在约 10²⁰ captures/cm³ 量级发生明显肿胀与微裂纹（Froment & Gosset 综述）。

### 15.3.2　寿期限制机制

B4C 芯块的径向肿胀导致**包壳-吸收体间隙闭合**（gap closure → mechanical interaction）——这是控制棒寿期的主要限制因素（ANL Benchmark Exercise, 2022；Zhong, ANL, 2018）。一旦间隙闭合，包壳承受机械应力，最终导致控制棒失效。

FFTF 控制棒 B4C 吸收体**设计初值寿期约 600 满功率天（FPD）**（Mahagin, INIS/IAEA），实际运行验证可达约 1100 EFPD（Ethridge, *FFTF Core System*, 1990）。Gen IV 设计目标约 800 EFPD（见 15.1）。VVER-1000 B4C 辐照（Zakharov, 2000）显示 He 主要积聚于棒底部；辐照致肿胀/开裂使芯块碎裂至 2–5 mm。

经典 B4C He 释放关联式由 Basmajian（1977）建立，是控制棒寿期预测的基础工具。

## 15.4　EuB6 的优势与挑战

EuB6 作为 B4C 替代品的核心优势是：

- **He 生成显著减少**（Eu 主要通过 (n,γ) 反应，He 产额远低于 B4C 的 (n,α)）；
- **肿胀更轻**；
- **寿期更长**。

但 EuB6 也面临挑战：

- **成本较高**（Eu 是稀土，供应有限）；
- **制造工艺复杂**；
- **辐照数据库相对单薄**。

CEA 的 Guo 等人（2018）系统评估了 B4C 与 EuB6 的对比，把 EuB6 列为延长控制棒寿期的可行替代方案。

## 15.5　小结

中子吸收体通过 (n,α)、(n,γ) 反应实现反应性控制，是反应堆控制棒、屏蔽与可燃毒物的核心功能材料。B4C 以 ¹⁰B 的 3837 barns 热中子俘获截面成为快堆控制棒主流，但 (n,α) 反应释放的 He 导致肿胀与开裂——间隙闭合是寿期主要限制（FFTF 设计寿期约 600 FPD）。EuB6、Eu2O3 等稀土吸收体通过减少 He 生成延长寿期，但成本与制造工艺是推广障碍。Hf 因 6 种稳定同位素均有高俘获截面而独特，但高成本限制了其在大型快堆中的应用。Ag-In-Cd 因熔点低主要限于 PWR。

## 参考文献

1. IAEA. *Control assembly materials for water reactors*. IAEA-TECDOC-1132, 1998. https://www-pub.iaea.org/MTCD/Publications/PDF/te_1132_prn.pdf
2. IAEA INIS. *Europium compounds for reactor neutron absorbers*. https://inis.iaea.org/collection/NCLCollectionStore/_Public/53/072/53072408.pdf
3. JAEA Nuclear Data Center (JENDL). *B-10 neutron capture cross-section*. https://wwwndc.jaea.go.jp/cgi-bin/Tab80WWW.cgi?lib=J40&iso=B010
4. Carter R. S., et al. Measurement of the thermal neutron capture cross section of natural boron. *Physical Review*, 1953, 92: 716. https://link.aps.org/doi/10.1103/PhysRev.92.716
5. You S. J., et al. Helium bubble behavior in irradiated B4C. *Journal of Nuclear Science and Technology*, 2018. https://www.tandfonline.com/doi/full/10.1080/00223131.2017.1419889
6. Froment K., Gosset D. *Neutron irradiation effects in boron carbides*. Semantic Scholar. https://www.semanticscholar.org/paper/d09be86c1b12fedc4ebc22e80458889cc8d06b74
7. ANL. *Benchmark Exercise on fast reactor control rod lifetime*. ANL, 2022. https://publications.anl.gov/anlpubs/2022/07/176428.pdf
8. Zhong Y. (ANL). *VTR control rod lifetime study*. ANL, 2018. https://publications.anl.gov/anlpubs/2019/03/150841.pdf
9. Mahagin D. E. *Fast reactor neutron absorber materials*. INIS/IAEA. https://inis.iaea.org/records/jrpj5-n1b04/files/10494921.pdf
10. Basmajian J. A. *A correlation for boron carbide helium release in LMFBR control rods*. 1977. https://www.osti.gov/servlets/purl/5167658
11. Birney K. R. *Evaluation of EuB6 as control rod material*. INIS/IAEA, 1984. https://inis.iaea.org/records/hfnmy-gc211/files/16061286.pdf
12. Guo H., et al. (CEA). *B4C and EuB6 control rod materials review*. 2018. https://cea.hal.science/cea-02338548/document
13. Pasto A. E. *Eu2O3 as LMFBR absorber*. OSTI, 1976. https://www.osti.gov/servlets/purl/5346666
14. NRC. *Hf and Ta control rod alloys*. ML020810111. https://www.nrc.gov/docs/ML0208/ML020810111.pdf
15. Zakharov. *VVER-1000 B4C irradiation*. 2000. https://www.osti.gov/etdeweb/servlets/purl/20045881
16. IOP. *B4C properties review*. *IOP Conference Series*, 2019, 678: 012121. https://iopscience.iop.org/article/10.1088/1757-899X/678/1/012121/pdf
