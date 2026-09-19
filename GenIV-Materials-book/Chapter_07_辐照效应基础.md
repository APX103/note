# 第 7 章　辐照效应基础

> **核心命题**　中子辐照通过级联碰撞在材料中产生过饱和点缺陷，这些缺陷聚集为位错环、空洞、析出相，进而引发硬化、脆化、肿胀、辐照蠕变与偏析。dpa（位移每原子）是衡量损伤剂量的标准单位，但 NRT-dpa 模型已被 2018 年提出的 ARC-dpa 修正——后者考虑了级联内缺陷复合，更接近真实损伤。本章建立辐照效应的统一图像，为后续各材料体系的辐照行为讨论奠定基础。

---

## 7.1　辐照损伤的产生过程

### 7.1.1　从 PKA 到级联碰撞

快中子（或裂变碎片、γ 射线）穿过材料时，会与晶格原子发生弹性碰撞，把部分原子撞出原来的位置——这个被撞出的原子称为**初级离位原子（Primary Knock-on Atom，PKA）**。PKA 仍具有足够能量，会继续撞击其他原子，形成级联碰撞（cascade），最终在晶格中留下空位—间隙原子对（Frenkel pair）。

每个原子平均被位移的次数，称为 **dpa（displacements per atom）**——这是衡量辐照剂量的标准单位。1 dpa 意味着材料中每个原子平均被撞离原位一次；100 dpa 意味着每个原子平均被撞离原位 100 次（虽然大部分会立即复合回去）。

### 7.1.2　NRT-dpa 与 ARC-dpa

传统的 **NRT-dpa 模型**（Norgett-Robinson-Torrens, 1975）是国际标准化 dpa 计算方法，把损伤能量除以 2.5 倍阈能位移能（Ed）。铁的标准 Ed 值为 **40 eV**（NRT 标准广泛采用值）。

但 NRT-dpa 系统性高估了实际缺陷数量，因为它忽略了级联内大量空位-间隙的瞬时复合。2018 年 Nordlund 等人提出了**ARC-dpa（athermal recombination-corrected dpa）**，引入复合修正因子，更接近真实损伤（Nordlund et al., *J. Nucl. Mater.* 512, 2018，被引 787；配套 Nature Communications 论文被引 483）。在低能级联区，NRT 高估约 2–3 倍。ARC-dpa 已被 IAEA CRP F44003 项目推荐为新标准。

值得注意的是，级联中只有约 6% 的缺陷能逃逸级联成为**自由迁移缺陷（freely-migrating defect，FMD）**——其余 94% 在级联内瞬时复合。真正引发后续微观组织演化的，是这部分长寿命 FMD（Griffiths, *MDPI Materials*, 2021）。

### 7.1.3　缺陷的归宿

逃逸级联的空位与间隙原子在晶格中迁移，最终去向包括：与相反类型缺陷复合、被位错、晶界、析出相界面等"沉阱"吸收、或聚集成稳定的缺陷团簇（位错环、空洞）。

## 7.2　关键辐照现象

### 7.2.1　辐照硬化与脆化（DBTT 上移）

辐照产生的位错环与析出相阻碍位错运动，使材料屈服强度上升、延伸率下降——这就是**辐照硬化**。对体心立方（BCC）金属如铁素体-马氏体钢，辐照会显著提高**韧脆转变温度（DBTT）**，使材料在原本韧性的温度区间变得脆性。

Klueh（2004，被引 788）的同等条件对比表明：在相同低剂量下，9Cr 系（T91）的 DBTT 上移通常低于 12Cr 系（HT9）；9Cr-2WVTa 钢的脆化更小。但这一规律不能直接外推到高剂量——以下两个极端案例说明 DBTT 上移对剂量/温度的强敏感性：

- **T91 钢在 325 ℃ / 70 dpa（高剂量）辐照后 DBTT 上移近 310 ℃**——目前最严重的 T91 脆化记录（Cabet et al., 2019，被引 313）；
- **HT9 在 EBR-II/FFTF 中约 26 dpa、375–390 ℃（低剂量）辐照后 DBTT 上移约 124 ℃**（Chen, 2013）。

两个数据点的剂量与温度均不同，不可直接比较——T91 的 310 ℃ 是 70 dpa 高剂量的极端值，HT9 的 124 ℃ 是 26 dpa 低剂量的典型值。

此外，**铁素体钢在极低剂量（<1 dpa）下即脆化**，而奥氏体不锈钢在 LWR 剂量约 80 dpa 后仍保持韧性（Griffiths, *MDPI Materials*, 2021）。

此外还存在**非硬化型脆化**：F82H 在 500 ℃ 辐照至 5 和 20 dpa 后出现脆化但强度无变化。

### 7.2.2　辐照肿胀（void swelling）

过饱和空位在合适的形核位点聚集成**空洞**（void），导致材料宏观体积膨胀，称为**辐照肿胀**。肿胀与温度、剂量、材料成分强相关。

- 奥氏体不锈钢的**肿胀峰温度约 400–560 ℃**（快堆谱）；肿胀起始剂量通常在约 **50 dpa 以上**（固溶退火态 304/316），冷加工态可延迟起始（Yamamoto et al., 2022；Griffiths, 2021）。
- 肿胀峰的 **Ni 含量依赖性**：在 30–50 at% Ni 处存在肿胀极小值（Griffiths, 2021）。
- 铁素体-马氏体钢的肿胀阈值超过 150–200 dpa——比奥氏体钢高约一个数量级。

### 7.2.3　辐照蠕变（irradiation creep）

辐照蠕变是应力与辐照耦合的变形：在中子辐照下，材料即使在低于热蠕变阈值的温度也会在应力作用下持续变形。**肿胀-蠕变耦合系数 D ≈ 6×10⁻³ MPa⁻¹**（Garner/Mansur 公式）。辐照蠕变在低应力下与应力呈线性关系，高应力下应力指数接近 2（Grossbeck & Wolfer, 1988；Griffiths et al., 2023）。

### 7.2.4　辐照诱发偏析（RIS）

辐照产生的过饱和点缺陷在流向沉阱的过程中会"拖曳"溶质原子，导致晶界附近成分变化——称为**辐照诱发偏析（Radiation-Induced Segregation，RIS）**。典型表现是 **Cr 贫化 + Ni/Si 富集**（inverse Kirkendall 效应 + 溶质-间隙复合体拖曳）。Cr 贫化促进 **IASCC**（辐照协助应力腐蚀开裂）（Dai et al., *Phys. Rev. Materials*, 2022，APT 直接证据）。

### 7.2.5　辐照诱发析出（RIP）

RIS 驱动的局部成分富集会触发新相析出——称为**辐照诱发析出（Radiation-Induced Precipitation，RIP）**。在奥氏体不锈钢（316、304）中主要的 RIP 相是 **γ'（Ni₃Si）** 和 **G 相（M₆Ni₁₆Si₇）**，与空洞肿胀和脆化相关（Brager, 1978，被引 142；Tencé et al., *Acta Materialia*, 2025）。

### 7.2.6　氦脆与氢脆

**¹⁰B 热中子 (n,α) 反应截面约 3837 靶恩（barns）**（天然硼加权约 749 b，因为 ¹⁰B 丰度约 19.9%）——这是所有稳定核素中最高的热中子吸收截面之一（JAEA JENDL 核数据；Carter et al., *Phys. Rev.* 92, 1953）。¹⁰B(n,α)⁷Li 反应产生氦（α 粒子 → ⁴He），氦泡在晶界形核导致沿晶脆化。Ni 即使无 B 也有较高 (n,α) 截面，B-10 显著放大氦生成。IAEA TECDOC-1039 给出 400 ℃ 辐照、特定氦水平下 Charpy DBTT 上移量级约 350 ℃。

## 7.3　缺陷表征手段

辐照损伤的微观表征需要多种互补技术。Odette 等人（2009）的经典论文联合使用 SANS+APT+PAS 研究 F-M 钢纳米特征，确立了多技术互补矩阵：

| 技术 | 探测对象 | 优势 |
|---|---|---|
| **PAS（正电子湮灭）** | 开体积缺陷（空位、空洞、位错环） | 亚纳米级自由体积灵敏度 |
| **APT（原子探针层析）** | 三维原子尺度成分图 | 溶质团簇、偏析 |
| **SANS（小角中子散射）** | 纳米析出/空洞（尺寸、密度、体积分数） | 体量统计定量 |
| **TEM（透射电镜）** | 位错环、空洞、析出相实空间成像 | 直接可视化 |

## 7.4　中尺度建模方法

辐照损伤涉及从原子（皮秒、纳米）到工程部件（年、米）跨越十几个数量级的多尺度过程，单一方法无法覆盖。当前主流是**多尺度建模链**：第一性原理 → 分子动力学（MD）→ 动力学蒙特卡洛（KMC）→ 团簇动力学/速率理论（rate theory）→ 相场（phase field）→ 晶体塑性有限元（CPFEM）。

- **速率理论**：Mansur（1979）的经典工作奠定了肿胀速率理论的基础。Griffiths（2021）用它对 316 SS 在 EBR-II 中的肿胀建模。
- **相场法**：Li 等人（*Nature npj Comput. Mater.*, 2017，被引 170）把肿胀速率理论与微观演化耦合。
- **OECD/NEA 多尺度建模权威报告**：State-of-the-Art Report on Multi-scale Modelling of Nuclear Fuels（NSC-R2015-5, 2020）。

## 7.5　经典参考与奠基文献

- **Zinkle & Busby (2009)**, "Structural Materials for Fission & Fusion Energy," *Materials Today* 12(11): 12–19，**被引 1622 次**——综述了 5 类辐射损伤威胁。
- **Was G. S., *Fundamentals of Radiation Materials Science: Metals and Alloys***（Springer 教材，**被引 3630+**），辐射材料科学领域引文最高的标准教材。强调区分"radiation damage"（辐照后材料状态）与"radiation effects"（缺陷在固体内形成后的行为）。
- **Mansur L. H. (1979)**, "Advances in the Theory of Swelling in Irradiated Metals and Alloys," *J. Nucl. Mater.*，速率理论奠基。

## 7.6　小结

中子辐照通过级联碰撞在材料中产生过饱和点缺陷，引发硬化、脆化、肿胀、辐照蠕变、偏析与析出等一系列性能退化。dpa 是衡量剂量的标准单位，但 ARC-dpa 比 NRT-dpa 更接近真实损伤。奥氏体钢的肿胀阈值约 50 dpa，F-M 钢可超过 150 dpa；F-M 钢在 <1 dpa 即脆化，奥氏体钢在 80 dpa 后仍保持韧性。RIS 与 IASCC 是奥氏体钢在快堆中长期寿期的关键限制。多尺度建模链（MD → KMC → 速率理论 → 相场 → CPFEM）与多技术表征（TEM + APT + PAS + SANS）是当前辐照效应研究的方法学双支柱。

## 参考文献

1. Nordlund K., et al. Primary radiation damage: A review of current understanding and proposed new standard damage model. *Journal of Nuclear Materials*, 2018, 512: 450–479. https://helda.helsinki.fi/bitstreams/ecb33f51-b1a4-4b54-b744-dcf60b82c711/download
2. IAEA-NDS. *DPA Standard*. https://www-nds.iaea.org/dpa/
3. Griffiths M. Radiation damage in nuclear reactor materials. *MDPI Materials*, 2021, 14(10): 2622. https://www.mdpi.com/1996-1944/14/10/2622
4. Griffiths M. Review of void swelling in austenitic stainless steels. PMC, 2021. https://pmc.ncbi.nlm.nih.gov/articles/PMC8155959/
5. Zinkle S. J., Busby J. T. Structural materials for fission & fusion energy. *Materials Today*, 2009, 12(11): 12–19. https://www.sciencedirect.com/science/article/pii/S1369702109702949
6. Was G. S. *Fundamentals of Radiation Materials Science: Metals and Alloys*. Springer. https://link.springer.com/book/10.1007/978-3-540-49472-0
7. Cabet C., et al. Irradiation damage in 9-12Cr steels for fast reactors. *Journal of Nuclear Materials*, 2019. https://hal.science/hal-03488269/file/S0022311519301990.pdf
8. Klueh R. L. Elevated-temperature ferritic and martensitic steels. ORNL, 2004. https://digital.library.unt.edu/ark:/67531/metadc891870/m2/1/high_res_d/885938.pdf
9. Mansur L. H. Advances in the theory of swelling in irradiated metals and alloys. *Journal of Nuclear Materials*, 1979. https://www.sciencedirect.com/science/article/abs/pii/0022311579905415
10. Yamamoto et al. Data-driven model of void swelling in austenitic stainless steels. OSTI, 2022. https://www.osti.gov/servlets/purl/2417873
11. Odette G. R., et al. *SANS+APT+PAS combined study of nanofeatures in F-M steels*. 2009. https://academic.oup.com/mam/article-pdf/15/S2/244/48248766/mam0244.pdf
12. Li Y., et al. Phase-field modeling of radiation-induced microstructure evolution. *npj Computational Materials*, 2017. https://www.nature.com/articles/s41524-017-0018-y
13. Ke J., et al. Microstructure modeling of nuclear structural materials. *Current Opinion in Solid State & Materials Science*, 2023. https://www.sciencedirect.com/science/article/abs/pii/S0927025623004974
14. OECD/NEA. *State-of-the-Art Report on Multi-scale Modelling of Nuclear Fuels*. NSC-R2015-5, 2020. https://www.oecd-nea.org/upload/docs/application/pdf/2020-01/nsc-r2015-5.pdf
15. Dai C., et al. APT evidence of RIS at dislocation loops in irradiated stainless steel. *Physical Review Materials*, 2022, 6: 053606. https://link.aps.org/doi/10.1103/PhysRevMaterials.6.053606
16. Grossbeck M. L., Wolfer W. G. Irradiation creep of type 316 SS and PCA. *Journal of Nuclear Materials*, 1988. https://www.sciencedirect.com/science/article/abs/pii/0022311588904576
