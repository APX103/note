# 第 13 章　碳/碳（C/C）复合材料

> **核心命题**　碳/碳复合材料把"碳"这种在惰性气氛中可工作到 2000 ℃ 以上的元素，转化为可承受高温机械载荷的工程材料。它在高温气冷堆中用作控制棒套管、热屏蔽、堆芯支撑，是不可替代的高温构件。但 C/C 在 >400 ℃ 含氧环境中即氧化，且辐照下尺寸与性能发生变化——这些限制把它定位为"高温惰性气氛专用"的特殊构件材料。

---

## 13.1　引言：C/C 在高温堆中的不可替代性

碳元素本身具有两个极端性质：在惰性气氛中可工作到 2000 ℃ 以上不发生相变或软化；但在含氧气氛中 >400 ℃ 即开始剧烈氧化。这一双重性质决定了碳/碳（C/C）复合材料的工程定位——**高温惰性气氛中的不可替代构件**。

在高温气冷堆（HTGR/VHTR）的设计中，控制棒套管、热屏蔽、堆芯支撑等部件需要在 900–1000 ℃ 氦气中长期承受机械载荷。金属体系（即使是 Alloy 617）也难以胜任这些部件的全寿期要求。C/C 凭借其在惰性气氛中的超高温度耐受性，成为这些部件的首选。

## 13.2　组分与制备工艺

### 13.2.1　碳纤维

C/C 复合材料使用的碳纤维主要分为两类：

- **PAN（聚丙烯腈）基碳纤维**：强度高、模量适中，是主流工业产品；
- **沥青（Pitch）基碳纤维**：模量高、热导率高（可达 2–4 倍于 PAN 基），用于需要高热导的部件。

纤维的弹性模量、热导率与强度由前驱体与石墨化温度决定。

### 13.2.2　碳基体

碳基体通过 **化学气相渗透（CVI/CVD）** 或 **液相浸渍—碳化（PIP）** 工艺填充到纤维预制件中：

- **CVI/CVD**：甲烷、丙烯等碳氢气体在 1000–1100 ℃ 热解，碳沉积在纤维表面。优点是基体纯度高、性能好；缺点是周期长（数周至数月）、孔隙率高。
- **PIP（Polymer Impregnation and Pyrolysis）**：用酚醛树脂或沥青浸渍纤维预制件，然后碳化（1000 ℃）→ 再浸渍 → 再碳化，循环多次直至致密。
- **石墨化处理**：在 2800–3000 ℃ 高温下处理，使碳基体转化为石墨结构，提升热导率与稳定性。

## 13.3　性能特点

C/C 复合材料的核心优势：

- **高温惰性气氛下的高强度**：在 >2000 ℃ 惰性气氛中仍保持高强度，远超任何金属；
- **低密度**：约 1.5–2.0 g/cm³，仅为钢的四分之一；
- **优异的抗热震性**：低热膨胀 + 高热导（沥青基）+ 低弹性模量，使 C/C 能承受剧烈温度变化；
- **低活化**：碳的衰变热与残余放射性极低；
- **断裂韧性**：与 SiC/SiC 类似，通过纤维-基体脱粘与拔出实现"伪塑性"。

## 13.4　限制与挑战

### 13.4.1　氧化

C/C 的根本限制是**氧化**：

- 在 >400 ℃ 含氧空气中，C/C 即开始剧烈氧化，转化为 CO/CO₂ 气体，材料迅速消失；
- 即使在 VHTR 氦气中，ppm 量级的 O₂、H₂O 杂质也会在长期服役中导致 C/C 氧化。

对策：

- **抗氧化涂层**：SiC 涂层（CVD SiC）是主流，形成 SiO₂ 保护层；但涂层缺陷（裂纹）会暴露 C 基体；
- **气氛控制**：把氦气中 O₂、H₂O 杂质控制在极低水平（详见第 3 章）；
- **设计裕量**：在预期氧化失活速率下预留壁厚裕量。

### 13.4.2　辐照行为

中子辐照会对 C/C 产生两类影响：

- **尺寸变化**：碳在辐照下 a 轴收缩、c 轴膨胀（详见第 14 章石墨辐照行为）；
- **性能变化**：热导率下降、弹性模量上升、辐照蠕变。

C/C 由于纤维与基体的各向异性，辐照尺寸变化比块体石墨更复杂，需在部件设计时精确预测。

### 13.4.3　各向异性

C/C 复合材料的力学性能强烈依赖纤维取向：

- 二维布铺层的 C/C 在面内强度高、层间强度低；
- 三维编织的 C/C 各向同性更好但成本高。

### 13.4.4　与冷却剂相容性

C/C 在液态金属（钠、铅铋）中相容性较好，但在熔盐中可能发生碳的溶解或剥落，需个案评估。

## 13.5　应用历史与现状

### 13.5.1　德国 AVR 与 THTR

德国的高温气冷堆 **AVR**（15 MWe，1967–1988）与 **THTR-300**（300 MWe，1985–1989）使用了 C/C 复合材料部件，特别是控制棒与热屏蔽。这些早期项目为 C/C 在高温堆中的应用积累了宝贵的工程经验。

### 13.5.2　中国 HTR-10 与 HTR-PM

中国的高温气冷堆 **HTR-10**（10 MWt，北京清华大学核研院）与 **HTR-PM**（200 MWe，山东石岛湾）也采用了 C/C 复合材料部件。HTR-PM 于 2021 年 12 月首次并网发电，2023 年 12 月实现商业运行，使 C/C 在高温堆中的工程化经验得到了进一步验证。

### 13.5.3　空间核动力

C/C 在空间核电源中也有应用——它在高温（>1500 ℃）下承受热离子转换器或热管的机械支撑。

## 13.6　规范与标准化

C/C 复合材料的规范合格化比金属体系滞后：

- **ASME Section III Division 5** 对 C/C 的规范覆盖仍有限；
- **JAEA** 与德国相关机构建立了 C/C 部件的设计准则；
- **ASTM** 制定了若干 C/C 力学测试标准。

C/C 部件的设计多采用"个案合格化（case-by-case qualification）"的方式，而非套用通用规范——这反映了 C/C 在核工程中的成熟度仍低于金属体系。

## 13.7　关键数据

C/C 复合材料的典型性能（量级，具体取决于纤维与工艺）：

- 密度：约 1.5–2.0 g/cm³；
- 拉伸强度（面内）：200–400 MPa；
- 热导率（沥青基）：100–300 W/m·K；
- 工作温度（惰性气氛）：可达 2000 ℃ 以上；
- 2000 ℃ 强度保留率：>80%（惰性气氛）；
- 氧化起始温度（空气中）：约 400 ℃。

## 13.8　小结

碳/碳复合材料凭借其在惰性气氛中 >2000 ℃ 的高温强度与低密度，是高温气冷堆控制棒、热屏蔽、堆芯支撑等部件的不可替代候选。德国 AVR/THTR、中国 HTR-10/HTR-PM 的工程经验验证了 C/C 在高温堆中的应用。但 >400 ℃ 含氧环境中的剧烈氧化、辐照尺寸变化、各向异性与规范滞后，把它定位为"高温惰性气氛专用"的特殊构件材料。SiC 涂层与气氛控制是抑制氧化的两大对策。C/C 部件的设计多采用个案合格化方式，反映其在核工程中的成熟度仍低于金属体系。

## 参考文献

1. IAEA. *High Temperature Gas Cooled Reactor Materials and Fuels*. IAEA TECDOC. https://www-pub.iaea.org/MTCD/Publications/
2. Buckthorpe D., et al. *Materials for VHTR components in the European RAPHAEL project*. https://www.sciencedirect.com/science/article/abs/pii/S0022311510004709
3. NASA. *Carbon-carbon composites review*. https://ntrs.nasa.gov/
4. Savage G. *Carbon-Carbon Composites*. Springer, 1993.
5. Goodman E. I. *The oxidation of carbon-carbon composites in HTGR helium*. ORNL. https://info.ornl.gov/
6. Sato T., et al. Oxidation behavior of C/C composites in HTGR helium. *Journal of Nuclear Materials*. https://www.sciencedirect.com/journal/journal-of-nuclear-materials
7. JAEA. *High Temperature Engineering Test Reactor (HTTR) experience*. https://www.jaea.go.jp/
8. Wikipedia. *HTR-PM*. https://en.wikipedia.org/wiki/HTR-PM
9. Wikipedia. *AVR reactor*. https://en.wikipedia.org/wiki/AVR_reactor
10. ASME BPVC Section III Division 5. *High-temperature reactor construction code*.
11. Generation IV International Forum. *VHTR Portal*. https://www.gen-4.org/generation-iv-criteria-and-technologies/very-high-temperature-reactor-vhtr
12. Zhang H., et al. *C/C composite control rod for HTR-PM*. Tsinghua University, Institute of Nuclear and New Energy Technology. https://www.tsinghua.edu.cn/ine/en/
