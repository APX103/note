# 第 9 章　抗辐照铁素体-马氏体钢

> **核心命题**　铁素体-马氏体（F-M）钢以其 BCC 结构把空洞肿胀阈值从奥氏体钢的 50 dpa 推高到 150–200 dpa，是高注量快堆与聚变堆堆芯结构材料的首选。但 BCC 结构带来的辐照脆化（DBTT 大幅上移）和 >550 ℃ 的热蠕变崩塌，是 F-M 钢的两项根本瓶颈。HT9、T91、Eurofer97、F82H、CLAM 等代表钢种代表了不同堆型与应用场景下的设计取舍。

---

## 9.1　引言：F-M 钢在第四代堆中的角色

铁素体-马氏体钢（含 9–12%Cr，回火板条马氏体组织）凭借 BCC 结构，把空洞肿胀阈值推到了奥氏体钢的 3–4 倍以上——这是它在高注量快堆与聚变堆中获得首选地位的根本原因。HT9 在 FFTF 中运行至 200 dpa 仍处于肿胀孕育期，是任何奥氏体钢都难以企及的成就。

但 BCC 结构同时带来两项根本弱点：

1. **辐照脆化**：低温辐照下 DBTT 大幅上移，严重时使材料在常温即变脆；
2. **高温蠕变崩塌**：在 >550–600 ℃，热蠕变强度急剧下降，长期使用温度上限约 550 ℃。

这两项弱点界定了 F-M 钢的应用窗口与下一代合金的发展方向。

## 9.2　代表钢种

### 9.2.1　HT9（12Cr-1MoWV）

HT9 由 Sandvik 设计，曾在美国 FFTF 中用作燃料包壳与导管，在 EBR-II 中用作金属燃料包壳（ONR-RRR-088；Pahl et al., 1992）。

- **空洞肿胀行为**：HT9 测量的肿胀率约 **0.012–0.015 %/dpa**，远低于标准 F-M 钢的约 0.2 %/dpa 稳态速率和奥氏体钢的约 1 %/dpa（Y. Chen et al., 2013，被引 146）。
- **高剂量表现**：HT9 在高达 **200 dpa 的剂量下仍保持在孕育期/瞬态范围内**（Kim et al., 2022, LANL）。HT9 在 FFTF 中表现出极长的孕育期，远超 100 dpa（Porter et al., *JNM* 2019，被引 15）。
- **力学性能**：600 ℃ 下 UTS 约 600 MPa，屈服强度通常在 600 ℃ 下处于 400–500 MPa 范围（见第 6 章）。

### 9.2.2　T91（Mod 9Cr-1MoVNb，ASME Grade 91）

T91 是化石电厂与第四代堆的主力 9Cr 钢。它的 600 ℃ 蠕变断裂强度约为 Grade 9（9Cr-1Mo）的两倍（INIS），是 9-12Cr CSEF（creep strength enhanced ferritic）钢的标杆。蠕变失效在 >650 ℃ 时急剧加速（详见第 6 章与第 18 章）。

### 9.2.3　Eurofer97（9Cr-1WVTa，EU RAFM）

**EUROFER97 是欧盟 ITER TBM 与 EU-DEMO 第一壁/包层的参考 RAFM（Reduced Activation Ferritic-Martensitic）钢**，拥有最大的 RAFM 钢性能数据库（>3500 个溯源数据点），正在纳入 RCC-MRx 规范（Gorley et al., UKAEA-CCFE-PR(21)06）。

- 在 250–340 ℃ 辐照窗口下的 DBTT 上移显著；优化的热力学处理可使未辐照的 DBTT 降低约 100 ℃；>400–450 ℃ 时的上移较小。
- 在 >550 ℃ 时蠕变强度急剧下降。EUROfusion 改进的 EUROFER 变体（Tan et al., 2016；Pilloni et al., 2018）提高了该温度以上的持久强度。

### 9.2.4　F82H（Fe-8Cr-2W-V-Ta，日本 RAFM）

F82H 名义成分为 **Fe–8Cr–2W–0.2V–0.04Ta–0.1C**，由 JAERI + NKK 开发作为日本参考 RAFM 钢（Tanigawa et al., 2017，被引 202）。F82H-BA07 首次热处理（5 吨 VIM + ESR 重熔，2007）作为日本更广泛方法（BA）DEMO 活动的一部分。

优化的成分杠杆：限制 [Ti] < 0.01 wt% 以保持韧性；将 [Ta] 提高至 0.10 wt%；提高 [N] 至 0.01 wt% 以增强蠕变；ESR 重熔以去除富 Ta 夹杂（Gorley et al., 2021）。

### 9.2.5　CLAM（中国低活化马氏体钢）

**CLAM 是中国的参考 RAFM 钢**，自 2001 年起开发，用于 ITER TBM + 中国聚变 DEMO（CFETR）（Q. Huang, IAEA FEC；J. Yu et al., 2007）。

## 9.3　F-M 钢的优势：低肿胀

F-M 钢的核心优势是低肿胀：

- **肿胀阈值超过 150–200 dpa**——比奥氏体钢高约一个数量级；
- **EM10 导管在 155 dpa 下进行了辐照后检查**（Tissot et al., 2021）；
- 肿胀率量级：标准 F-M 钢约 0.2 %/dpa（稳态），奥氏体钢约 1 %/dpa，HT9 约 0.012–0.015 %/dpa（Chen 2013）。

## 9.4　F-M 钢的限制一：辐照脆化

BCC 结构的金属在低温辐照下 DBTT 显著上移，这是 F-M 钢的根本弱点。DBTT 上移对剂量与温度极为敏感：

- **典型快堆剂量（<30 dpa）下 DBTT 上移 50–150 ℃**（取决于温度与具体钢种）（Bhattacharya et al., 2022，被引 115；Petersen IAEA FEC 2006）；
- **高剂量（>50 dpa）极端值可达约 310 ℃**：T91 在 325 ℃ / 70 dpa 辐照后 DBTT 上移近 310 ℃（Cabet et al., 2019）；
- HT9 在 EBR-II/FFTF 中约 26 dpa、375–390 ℃（低剂量）辐照后 DBTT 上移约 124 ℃（Chen, 2013）；
- **铁素体钢在极低剂量（<1 dpa）下即脆化**。

低活化 RAFM 钢（Eurofer97、F82H、CLAM）通过 W、Ta 替换 Mo、Nb 实现低活化（满足近地表掩埋的活化限值），同时把 DBTT 上移控制在可接受范围。

## 9.5　F-M 钢的限制二：高温蠕变崩塌

F-M 钢在 >550 ℃ 时热蠕变强度急剧下降。**8–9Cr RAFM 钢的最大运行温度上限约 550 ℃**（热蠕变限制），设计运行窗口通常为 300–550 ℃。

Laves 相 (Fe,Cr)₂(W,Mo) 在 EUROFER97/F82H/CLAM 的热时效过程中析出，导致长期高温脆化（L. Yang et al., 2019；Terentyev, 2025）。这是 RAFM 钢在 DEMO 工况下必须克服的关键问题。

## 9.6　低活化要求（聚变堆专用）

聚变堆第一壁面临远高于裂变堆的辐照与衰变热要求。RAFM 钢的设计初衷是**用 W 替代 Mo，用 Ta 替代 Nb**，以满足浅层掩埋的活化限值。

需要更正一项常见误称：美国关于近地表放射性废物分类的经典引用是 **10 CFR Part 61.55**（NRC 10 类低放废物分类），不存在"10 CFR Part 811"。国际基准是欧盟的 **SEAFP/SEAFP-2** 项目（Safety and Environmental Assessment of Fusion Power），它定义了聚变堆材料的低活化目标（DOE 低活化材料委员会，Conn 1983）。

## 9.7　先进 F-M 钢的发展方向

为突破 550 ℃ 蠕变上限，下一代 F-M 钢的发展方向包括：

1. **添加 W、Ta**：提高蠕变强度（Gr.92、Eurofer97 改进型）；
2. **控制 δ-铁素体**：避免脆性相形成；
3. **亚稳态析出控制**：抑制 Laves 相粗化与 Z 相形成（见第 6 章）；
4. **梯度组织设计**：通过热机械处理获得细小均匀的板条马氏体。

## 9.8　小结

F-M 钢以其 BCC 结构把空洞肿胀阈值推至 150–200 dpa，是高注量快堆与聚变堆堆芯的首选。HT9 在 FFTF 中达到 200 dpa 仍处于肿胀孕育期。但 BCC 结构带来两项根本弱点：辐照脆化（DBTT 上移 50–150 ℃）和 >550 ℃ 的热蠕变崩塌。T91、HT9、Eurofer97、F82H、CLAM 分别代表了化石电厂、快堆、聚变堆等不同应用的设计取向。RAFM 钢通过 W/Ta 替换 Mo/Nb 满足聚变堆的低活化要求。下一代 F-M 钢的核心挑战是突破 550 ℃ 蠕变上限。

## 参考文献

1. Chen Y., et al. Void swelling of HT9 and austenitic steels in fast reactors. 2013. https://www.sciencedirect.com/science/article/pii/S1738573315300176
2. Porter D. L., et al. HT9 swelling in high burnup fast reactor fuel pin components. *Journal of Nuclear Materials*, 2019. https://www.sciencedirect.com/science/article/abs/pii/S0022311518312236
3. Kim et al. Void swelling of HT9 to 200 dpa. LANL, 2022. https://laro.lanl.gov/esploro/fulltext/journalArticle/Void-swelling-of-conventional-and-composition/9916361570903761
4. Klueh R. L. Elevated-temperature ferritic and martensitic steels. ORNL, 2004. https://digital.library.unt.edu/ark:/67531/metadc891870/m2/1/high_res_d/885938.pdf
5. Cabet C., et al. Irradiation damage in 9-12Cr steels. *Journal of Nuclear Materials*, 2019. https://hal.science/hal-03488269/file/S0022311519301990.pdf
6. Bhattacharya A., et al. Irradiation damage concurrent challenges with RAFM and ODS steels. OSTI, 2022. https://www.osti.gov/biblio/1876325
7. Tanigawa H., et al. Technical issues of reduced activation ferritic/martensitic steels for fusion. 2008. https://impact.ornl.gov/en/publications/technical-issues-of-reduced-activation-ferriticmartensitic-steels/
8. Gorley M., et al. DEMO structural materials qualification and development. UKAEA-CCFE-PR(21)06. https://scientific-publications.ukaea.uk/wp-content/uploads/UKAEA-CCFE-PR2106.PDF
9. Tissot et al. EM10 duct irradiation to 155 dpa. *Journal of Nuclear Materials*, 2021. https://www.sciencedirect.com/science/article/am/pii/S0022311520311831
10. Petersen K. (IAEA FEC). *Fusion materials — DBTT behavior*. 2006. https://www-pub.iaea.org/mtcd/meetings/fec2006/ft_1-4ra.pdf
11. Zinkle S. J., Ghoniem N. M. Operating temperature windows for fusion reactor structural materials. *Fusion Engineering and Design*, 2000, 51–52: 55–71. http://matrix.seas.ucla.edu/papers/2000/s-NG-operating.pdf
12. Tanigawa H., et al. Status and key issues of reduced activation ferritic/martensitic steels. *Fusion Science and Technology*, 2017. https://iopscience.iop.org/article/10.1088/1741-4326/57/9/092004
13. Yu J., et al. Development of CLAM steel for fusion. *Journal of Nuclear Materials*, 2007. https://www.sciencedirect.com/science/article/abs/pii/S0022311507003455
14. Yang L., et al. Laves phase precipitation in RAFM steels. PMC, 2019. https://pmc.ncbi.nlm.nih.gov/articles/PMC6982184/
