# 第 14 章　核级石墨

> **核心命题**　核级石墨是高温气冷堆、熔盐堆与早期英国气冷堆的"骨骼"——它既是慢化剂又是反射层，在数百到上千摄氏度下承受高注量中子辐照。但石墨在辐照下会经历复杂的尺寸与性能变化（a 轴收缩、c 轴膨胀、辐照拐点），一旦越过拐点材料即快速失稳。IG-110、NBG-18、PCEA 等核级石墨的等级开发、辐照数据库与 ASME 规范合格化，是高温堆工程化的核心议题。

---

## 14.1　引言：核级石墨的独特地位

核级石墨（nuclear-grade graphite）在第四代堆中扮演双重角色：**慢化剂**（热化中子能谱）与**反射层/堆芯结构**（包裹燃料区、形成堆芯几何）。它在高温气冷堆（HTGR/VHTR）中是堆芯骨架，在熔盐堆（MSR）中是慢化剂兼结构（如 MSRE 的热解石墨），在英国 Magnox 与 AGR 反应堆中是慢化剂主体。

石墨之所以不可替代，是因为它同时具备：

- **低原子序数**：极佳的中子慢化能力；
- **高温稳定性**：在惰性气氛中可工作到 >2000 ℃；
- **低中子吸收截面**：中子经济性好；
- **足够的机械强度**：可作结构件；
- **低活化**：衰变热与残余放射性相对可控。

但石墨在快中子辐照下会经历复杂的微观组织演化，导致尺寸与性能变化——这是核级石墨工程化的核心挑战。

## 14.2　核级石墨的等级

不同等级的核级石墨在原料、工艺与性能上各有取舍。下表汇总了主流等级：

| 等级 | 制造商 | 原料/工艺 | 应用 |
|---|---|---|---|
| IG-110 | Toyo Tanso（日本东洋碳素） | 石油焦，等静压 | HTR-PM（中国） |
| NBG-18 | SGL Group（德国 SGL） | 沥青焦，挤压 | NGNP（美国）候选 |
| PCEA | GrafTech（美国） | 石油焦，挤压 | NGNP 候选 |
| G347A | Tokai Carbon（日本东海碳素） | — | 高温堆候选 |
| PPEA | GrafTech（美国） | 沥青焦，挤压 | NGNP 候选 |

**IG-110** 是中国 HTR-PM 选用的等级，**等静压**成型带来良好的各向同性（BAF 各向异性比 <1.1），辐照尺寸变化较小。**NBG-18** 是美国 NGNP 项目的候选，挤压成型带来较强的各向异性，需在部件设计中精确考虑。**G347A** 由日本 Tokai Carbon 制造（注意：不是法国厂商）。

## 14.3　制造工艺

核级石墨的制造流程高度专业化：

1. **原料准备**：石油焦或沥青焦煅烧（1200–1400 ℃），去除挥发分；
2. **粉碎与筛分**：把煅烧焦粉碎成不同粒径；
3. **配料与混捏**：与煤焦油沥青粘结剂混捏；
4. **成型**：挤压（各向异性）、模压或等静压（各向同性）；
5. **焙烧**：在 800–1200 ℃ 缓慢焙烧，沥青粘结剂碳化；
6. **浸渍—再焙烧**：用沥青浸渍再焙烧，循环多次提高密度；
7. **石墨化**：在 2800–3000 ℃ 高温处理，使无定形碳转化为石墨晶体结构；
8. **净化**：在含卤素气体中处理去除金属杂质。

最终产品的微观组织是**填充焦颗粒 + 粘结剂相 + 孔隙**的三相结构。

## 14.4　微观组织与各向同性

核级石墨的微观组织决定其辐照行为。关键参数：

- **晶粒尺寸（Lc）**：反映石墨化程度；
- **晶格常数 c/2（约 3.354 Å）**：理想石墨的层间距；
- **各向异性比（BAF，Bacon Anisotropy Factor）**：等静压石墨 BAF <1.1，挤压石墨 BAF 可达 1.3–1.5。

各向同性是核级石墨的关键设计目标——各向异性会导致辐照尺寸变化在不同方向差异显著，增加部件热应力与失效风险。IG-110 因等静压工艺而成为首选。

## 14.5　辐照行为

核级石墨在快中子辐照下的行为复杂，是其工程化的核心议题。

### 14.5.1　尺寸变化

石墨晶体呈层状结构（六方），中子辐照导致：

- **a 轴收缩**：基面内原子被打出形成间隙原子，a 轴方向收缩；
- **c 轴膨胀**：间隙原子在层间聚集形成新层面，c 轴方向膨胀。

宏观上，各向同性石墨的整体体积变化呈现两阶段：**初期收缩 → 拐点（turnaround）→ 反向膨胀**。拐点是设计寿期的关键阈值——越过拐点后，石墨体积膨胀加速，性能急剧恶化。

### 14.5.2　性能变化

辐照过程中其他性能变化：

- **热导率下降**：辐照缺陷散射声子；
- **弹性模量上升**：辐照致硬化；
- **辐照蠕变**：在应力与辐照耦合下持续变形；
- **热膨胀系数变化**：影响部件配合。

### 14.5.3　温度与剂量范围

核级石墨的辐照数据库覆盖：

- 温度范围：300–1200 ℃；
- 剂量范围：1–30 dpa（或以等效 DIDO 中子注量 × 10²¹ n/cm² EDN 表示）。

不同温度下的尺寸变化曲线是核级石墨等级合格化的核心数据。

## 14.6　事故工况：氧化与 Wigner 能量

### 14.6.1　氧化事故

高温气冷堆有两种典型氧化事故：

- **水入堆芯（Water ingress）**：蒸汽发生器泄漏导致水蒸气进入一回路，与石墨反应 C + H₂O → CO + H₂，消耗石墨；
- **空气入堆芯（Air ingress）**：一回路压力边界破裂导致空气进入，石墨在 >400 ℃ 即氧化 C + O₂ → CO/CO₂。

这些事故的后果评估是 HTGR 安全分析的核心议题。

### 14.6.2　Wigner 能量释放

石墨在低温辐照下会储存 Wigner 能量（缺陷储存的应变能）。如果不定期退火释放，能量可能在事故工况下突然释放，导致石墨温度急剧升高。1957 年英国 **Windscale（现 Sellafield）** 事故即由此引发。现代高温堆运行温度高（>300 ℃），Wigner 能量在运行中即原位释放，不再是重大隐患。

## 14.7　辐照石墨废物处理

辐照石墨废物是退役核设施的主要低中放废物之一。处理方案：

- **直接浅层掩埋**：适用于活化程度较低的部件；
- **焚烧**：石墨燃烧释放 ¹⁴C（来自 ¹⁴N(n,p)¹⁴C 与 ¹³C(n,γ)¹⁴C），需过滤 ¹⁴CO₂；
- **等离子体处理**：高温熔融固定放射性核素；
- **WAGR（Windscale Advanced Gas-cooled Reactor）** 项目：英国退役项目的石墨废物处理示范（注意：早期文献中"WAMSR"是误称，应为 WAGR）；
- **IAEA GRS-Part 1**：IAEA 制定的辐照石墨废物管理指南。

## 14.8　熔盐堆石墨专题

熔盐堆（MSR）使用石墨作为慢化剂，但面临一个特殊挑战：**熔盐渗透**。MSRE 使用 CGB 等级石墨，但熔盐通过孔隙渗入石墨内部，导致：

- 局部反应（与裂变产物如 Te 反应）；
- 石墨尺寸与性能变化加剧；
- 退役时熔盐难以回收。

为缓解渗透，新一代熔盐堆石墨研究采用：

- **细孔结构石墨**：把孔隙尺寸降至熔盐表面张力无法渗透的尺度（<1 μm）；
- **热解碳涂层**：在石墨表面形成致密涂层；
- **核级 IG-110 等工业等级**：评估其在 FLiBe 中的适用性。

## 14.9　规范与标准化

核级石墨的规范合格化是 ASME Section III Division 5 的核心内容之一：

- **ASME Section III Division 5 Subsection HH**：石墨部件的设计、制造与检验规范；
- **ASTM D7219**：核级石墨的标准规范；
- **ASTM D7542**：石墨氧化速率测试方法。

日本、中国也建立了核级石墨等级的合格化数据库（如 IG-110 在 HTR-PM 中的合格化）。

## 14.10　关键数据

IG-110 核级石墨的典型性能（参考 Toyo Tanso 数据表）：

- 密度：1.76–1.78 g/cm³；
- 平均晶粒尺寸：约 20 μm；
- 各向异性比（BAF）：<1.10；
- 室温热导率：约 80–120 W/m·K；
- 抗拉强度：约 25 MPa；
- 抗压强度：约 80 MPa；
- 热膨胀系数：约 4.5 × 10⁻⁶ /℃。

## 14.11　小结

核级石墨是高温气冷堆、熔盐堆与早期气冷堆的"骨骼"，兼具慢化剂与结构功能。IG-110（HTR-PM 选用）、NBG-18（NGNP 候选）等代表了不同等级的工艺取向。核级石墨的辐照行为复杂——a 轴收缩、c 轴膨胀、拐点反向膨胀——其辐照数据库是等级合格化的核心。事故氧化（水入、空气入）、Wigner 能量释放、辐照石墨废物处理是工程化的关键议题。熔盐堆石墨面临熔盐渗透的额外挑战。ASME Section III Division 5 Subsection HH 与 ASTM D7219 是核级石墨的规范基础。

## 参考文献

1. IAEA. *Nuclear Graphite for High-Temperature Gas-Cooled Reactors*. IAEA TECDOC. https://www-pub.iaea.org/MTCD/Publications/
2. IAEA. *Management of Waste Containing Tritium and Carbon-14*. IAEA Technical Reports Series No. 421. https://www-pub.iaea.org/MTCD/Publications/
3. Toyo Tanso. *IG-110 nuclear graphite data sheet*. https://www.toyotanso.com/
4. SGL Group. *NBG-18 nuclear graphite data*. https://www.sglcarbon.com/
5. Burchell T. D. *A Microstructurally Based Fracture Model for Nuclear Graphite*. ORNL. https://info.ornl.gov/
6. Marshall S., et al. *Irradiation creep of nuclear graphite*. *Journal of Nuclear Materials*. https://www.sciencedirect.com/journal/journal-of-nuclear-materials
7. BCHW / NBG-18 irradiation database. *NGNP Graphite R&D*. ORNL/INL. https://www.osti.gov/
8. ASME BPVC Section III Division 5 Subsection HH. *Graphite core components*.
9. ASTM D7219. *Standard specification for nuclear-grade graphite*.
10. ASTM D7542. *Standard test method for oxidation of graphite*.
11. Wikipedia. *Windscale fire*. https://en.wikipedia.org/wiki/Windscale_fire
12. ORNL. *Graphite waste treatment technologies*. ORNL publications. https://info.ornl.gov/
13. McCoy H. E. *MSRE graphite experience*. ORNL-TM-2196. https://moltensalt.org/references/static/downloads/pdf/ORNL-TM-2196.pdf
14. Wikipedia. *HTR-PM*. https://en.wikipedia.org/wiki/HTR-PM
15. Wikipedia. *Molten-Salt Reactor Experiment*. https://en.wikipedia.org/wiki/Molten-Salt_Reactor_Experiment
