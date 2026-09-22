# 第 2 章　液态金属引起的腐蚀

> **核心命题**　液态金属冷却剂把第四代堆推到了一个全新的腐蚀范式：腐蚀不再是氧化还原驱动的电化学过程，而是由元素在液态金属中的溶解度、温度梯度驱动的质量迁移以及杂质参与的化学反应共同主导。钠的腐蚀几乎完全由氧含量决定，铅铋的腐蚀则取决于能否通过氧控形成保护性氧化膜——同样是液态金属，机理截然不同。

---

## 2.1　液态金属冷却剂的特性

钠冷快堆（SFR）与铅冷快堆（LFR）是六类第四代堆型中最接近工程化的两类，它们的共同特点是采用常压运行的液态金属冷却剂。下表汇总了主要候选液态金属的热物理性质。

| 冷却剂 | 熔点（℃） | 沸点（℃） | 密度（g/cm³，近熔点） | 液态热导率（W/m·K） |
|---|---|---|---|---|
| 钠 Na | 97.7 | 883 | 约 0.93 | 约 76 |
| 锂 Li | 180.5 | 1342 | 约 0.51 | 约 85 |
| 铅 Pb | 327.5 | 1749 | 约 10.7 | 约 15 |
| 铅铋共晶 LBE | 123.5 | 约 1670 | 约 10.5 | 约 10–13 |

数据来源：OECD/NEA《铅铋共晶与铅性质手册》（2007/2015 版）；Sobolev（2007）*J. Nucl. Mater.* 362:235。

钠的常压沸点高达 883 ℃、热导率约 76 W/m·K，使 SFR 可在低压下实现高功率密度。铅铋共晶 LBE 的熔点仅约 124 ℃，远低于纯铅的 327.5 ℃，运行温度窗口宽、对包壳的瞬时热冲击小，是 ADS（加速器驱动次临界堆）与小型 LFR 的首选。锂的热导率最高（约 85 W/m·K），但熔点较高且与结构材料反应剧烈，主要面向聚变堆自冷却包层而非裂变堆。

值得强调的是，液态金属并非"惰性传热流体"。它们与固态金属结构直接接触时，会发生溶解、化学反应与质量迁移，腐蚀驱动力与水化学完全不同。

## 2.2　液态金属腐蚀的三大机理

法国 CEA 的 Balbaud-Célérier 等人在系统综述中把液态金属腐蚀归纳为三类机理，这是理解第 2–3 节的基础：

1. **溶解（Dissolution）**：合金元素（特别是 Ni、Cr、Mn）选择性溶入液态金属。溶解度随温度升高而增大，随液态金属中已有该元素浓度增大而下降。
2. **质量迁移（Mass transfer）**：在带温度梯度的回路中，高温区元素溶解进入液态金属，被流动冷却剂带到低温区后因溶解度下降而沉积。这种持续的溶解—沉积循环，使得即使整体金属"看起来未消耗"，高温区仍不断流失材料。
3. **杂质驱动腐蚀（Impurity-driven）**：液态金属中溶解的氧、碳、氮、氢等杂质参与化学反应，形成氧化物、碳化物或加速溶解。杂质控制是抑制此类腐蚀的关键手段。

这三类机理在不同冷却剂中的相对权重不同。在液态钠中，杂质驱动（特别是氧）几乎主导一切；在液态铅铋中，氧含量的高低决定了是溶解机制占优还是氧化保护机制占优。

## 2.3　液态钠中的腐蚀

### 2.3.1　氧是钠腐蚀的主导变量

钠本身对铁基合金的腐蚀性弱，但钠中溶解氧会显著加剧腐蚀。IAEA/INIS 的综述指出，钠腐蚀方程在 10 ppm O₂ 浓度下被广泛引用，氧含量是减蚀最有效的调节变量。

典型 SFR 钠回路的氧控制目标约为 **≤1 ppm**（冷阱控制，阿贡国家实验室 ANL 的实测值约 1 ppm）。电化学氧传感器回路常以 <5 ppm 为监测基准。当 O₂ > 约 10–25 ppm 时，316 不锈钢会明显出现腐蚀区与加速质量迁移。

### 2.3.2　溶解氧控制的腐蚀方程

Dai 等人（2021，被引 90 次）的系统综述表明，钠中 316 系不锈钢的腐蚀速率强烈依赖三个变量：**温度、钠中氧含量、流速**。三者协同决定质量迁移速率。低氧（<1 ppm）时，316 不锈钢在 550 ℃ 钠中年腐蚀速率典型值约 0.004–4 μm/yr，几乎可忽略；高氧（>10 ppm）时则显著加速。

### 2.3.3　自耗效应与钠水反应

蒸汽发生器传热管一旦出现裂纹或小孔，水/汽泄漏入钠侧会引发剧烈的**钠水反应**（Sodium-Water Reaction，SWR）。反应局部放热并生成氢氧化钠与氢气，反过来扩大传热管破口，称为**自耗效应**（self-wastage）。这是 SFR 蒸汽发生器设计中的关键安全考量，需通过双壁管、泄漏检测系统与快速排钠措施防范。Jeong 等人在韩国核学会会议上系统综述了不同条件下的 wastage 速率建模。

## 2.4　液态铅铋中的腐蚀

铅铋共晶（LBE）腐蚀是 LFR 与 ADS 研究的核心难题。它的复杂性在于：LBE 对结构材料的腐蚀模式随氧含量发生根本性切换。

### 2.4.1　氧控窗口

LBE 腐蚀存在一个**氧含量控制窗口**，典型为 **10⁻⁷ 至 10⁻⁶ wt% O**（即约 1–10 ppb mass，通过含氧气体调控，以电化学氧传感器监测）。KIT 与多个实验室的研究表明：

- **氧含量高于约 10⁻⁶ wt%（即约 10 ppb mass）时**：溶解氧与 Fe、Cr 反应，在合金表面形成保护性氧化膜（Fe/Cr 复合氧化物），腐蚀以**氧化机制**为主导；
- **氧含量低于约 10⁻⁷ wt%（即约 1 ppb mass）时**：无法形成保护性氧化膜，腐蚀以**元素溶解机制**为主导，Ni、Cr 被选择性浸出。

通过电化学氧传感器实时监测，将氧含量稳定维持在窗口内是 LBE 回路设计的核心。

### 2.4.2　低氧 LBE 中的溶解腐蚀

Konys 等人（*J. Nucl. Mater.* 454, 2014）系统测量了奥氏体钢（1.4970、316L、1.4571）在 **550 ℃、10⁻⁷ mass% O、约 2 m/s 流速 LBE** 中的腐蚀行为。316L 在最长 8766 小时暴露后以溶解腐蚀为主——Ni、Cr 选择性浸出，呈现典型的多孔富铁表面层。在该低氧条件下，316L 运行数千小时即出现数十至数百微米的溶解深度，需要在部件设计中预留充分的腐蚀裕量。

Lambrinou 等人（*J. Nucl. Mater.* 490, 2017，被引 245 次）研究了 316L 在 500 ℃ 静态 LBE 中的溶解腐蚀，发现速率由 Ni、Cr 同时溶解的界面反应控制，最长 3000 小时试验显示明显溶解。SCK CEN 在 1000 h、450 ℃、流动 LBE、10⁻⁶ mass% O 条件下也观测到 316L 的溶解腐蚀。

### 2.4.3　含氧 LBE 中的保护性氧化

当氧含量足够时，T91（Mod 9Cr-1Mo）等铁素体-马氏体钢表面会形成分层结构的 Fe/Cr 复合氧化物——外层磁铁矿、中间 (Fe,Cr)₃O₄ 尖晶石、内层 Cr 富集氧化物——起到扩散阻挡作用。Ye 等人（2016，被引 76 次）系统研究了 T91 在液态 LBE 中的氧化机制。

俄罗斯 IPPE 与多家实验室给出了 T91、HT9、316L 在 600 ℃、静态 LBE、1000–2000 小时的对比腐蚀数据。降低氧浓度（如 1.26×10⁻⁶ wt%）可改善 T91 腐蚀，但溶解腐蚀仍存在。湍流 LBE 会进一步加速 316L 的溶解（Wan，2018，*Metals*，被引 39 次）。

### 2.4.4　缓蚀涂层

为突破氧控窗口的局限，研究者开发了多种**缓蚀涂层**。最具代表性的是 **FeCrAlY 涂层**——在 T91 包壳管表面形成稳定的 Al₂O₃ 层作为扩散阻挡层，抑制液态金属渗透。研究显示，无涂层与有涂层 T91 包壳管在 LBE 回路中 2000 小时后表现出明显差异。添加微量 Si 可进一步提升 FeCrAl 涂层的 LBE 耐蚀性。Cr、Al 含量的优化是涂层设计的关键。

## 2.5　腐蚀对力学性能的影响

液态金属腐蚀不仅是壁厚减薄问题。**液态金属致脆**（Liquid Metal Embrittlement，LME）是另一类值得关注的现象：某些液态金属（如 LBE 对铁基合金）会降低材料的断裂韧性与延伸率，特别是在有辐照硬化的敏化态下。

在工程实践中，腐蚀与力学退化常常协同作用：溶解腐蚀使有效壁厚减薄，应力腐蚀开裂在减薄区加速，最终导致部件提前失效。因此 LFR 与 ADS 设计中，包壳与构件的腐蚀裕量、力学应力极限与寿期需要联合评估。

## 2.6　腐蚀的缓解与对策

综合文献，液态金属腐蚀的缓解可归纳为四类策略：

1. **冷却剂化学控制**：钠回路用冷阱控制氧含量至 ≤1 ppm；LBE 回路通过含氧气体把氧含量稳定在 10⁻⁷–10⁻⁶ wt% 窗口。
2. **合金成分优化**：T91、HT9 在含氧 LBE 中可形成保护性氧化物；高 Cr 奥氏体钢在低氧 LBE 中溶解较慢；新一代合金如 15-15Ti、Alloy 800H 也在评估中。
3. **缓蚀涂层**：FeCrAlY、FeCrAl + Si 涂层作为扩散阻挡层，已在多国实验室验证有效。
4. **系统设计**：减少温度梯度与流速骤变，降低质量迁移驱动力；为蒸汽发生器设计泄漏检测与快速排钠系统以应对 SWR。

## 2.7　小结

液态金属腐蚀不能简单套用水化学的经验。钠的腐蚀几乎完全由氧含量决定，把钠中氧控制在 ≤1 ppm 即可让腐蚀速率降至可忽略水平。铅铋腐蚀则取决于能否把氧含量维持在 10⁻⁷–10⁻⁶ wt% 窗口——窗口之上形成保护性氧化膜，窗口之下 Ni/Cr 选择性溶解。FeCrAlY 涂层为突破氧控窗口提供了额外手段。无论哪种冷却剂，质量迁移都是回路温度梯度的必然产物，必须从系统设计与化学控制双管齐下。

## 参考文献

1. OECD/NEA. *Handbook on Lead-bismuth Eutectic Alloy and Lead Properties, Materials Compatibility, Thermalhydraulics and Technologies*. OECD/NEA, 2007/2015. https://www.oecd-nea.org/science/reports/2007/pdf/chapter2.pdf
2. Sobolev V. Thermophysical properties of lead and LBE. *Journal of Nuclear Materials*, 2007, 362: 235. https://ui.adsabs.harvard.edu/abs/2007JNuM..362..235S/abstract
3. Balbaud-Célérier F., et al. Corrosion of structural materials by liquid metals (fusion, fission, ADS). HAL, 2020. https://hal.science/hal-02417812v1/document
4. IAEA/INIS. *A Review of Corrosion and Mass Transport in Liquid Sodium*. https://inis.iaea.org/records/jq9b4-k9f29/files/53069743.pdf
5. Argonne National Laboratory. *Corrosion Performance of Advanced Structural Materials in Sodium*. ANL, 2012. https://publications.anl.gov/anlpubs/2012/05/73045.pdf
6. Dai Y., et al. Review on corrosion and mass transport in liquid sodium. *Progress in Nuclear Energy*, 2021. https://www.sciencedirect.com/science/article/pii/S1738573321002874
7. Konys J., et al. Corrosion behavior of austenitic steels (1.4970, 316L, 1.4571) in flowing LBE at 450 and 550 ℃ with 10⁻⁷ mass% O. *Journal of Nuclear Materials*, 2014, 454. https://www.researchgate.net/publication/282281557
8. Lambrinou K., et al. Dissolution corrosion of 316L stainless steel in static liquid bismuth at 500 ℃. *Journal of Nuclear Materials*, 2017, 490. https://www.sciencedirect.com/science/article/pii/S0022311517302459
9. Ye X., et al. Oxidation mechanism of T91 steel in liquid lead-bismuth eutectic. *Scientific Reports*, 2016. https://pmc.ncbi.nlm.nih.gov/articles/PMC5062345/
10. Wan Y. Flow-accelerated corrosion of 316L stainless steel by turbulent lead-bismuth eutectic. *Metals*, 2018. https://www.researchgate.net/publication/327661949
11. Jeong et al. Wastage of steam generator tubes by sodium-water reaction. KNS Conference. https://www.kns.org/files/pre_paper/7/35-Jeong.pdf
12. KIT. *Corrosion of Steel T91 by flowing LBE at 400 ℃*. https://publikationen.bibliothek.kit.edu/1000056141/3951159
