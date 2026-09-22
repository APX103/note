# 第 18 章　堆外常规铁素体-马氏体钢

> **核心命题**　Gr.91（T91）与 Gr.92（NF616）最初为化石电厂的高温管道开发，凭借成熟的工业供应链与 ASME 规范合格化，顺利扩展到高温气冷堆、钠冷快堆的堆外构件。它们的工程化优势无可替代——但 600 ℃ × 10⁵ 小时蠕变断裂强度只有约 85–132 MPa，且 Type IV 蠕变与 Z 相脆化是长期可靠性的隐患。本章关键不是新合金，而是化石电厂经验向核电领域的迁移与验证。

---

## 18.1　引言：从化石电厂到核电的迁移

铁素体-马氏体钢的工程化优势无可替代：

- **成熟的工业供应链**：管材、锻件、板材均已大规模生产；
- **完整的规范合格化**：ASME Code、ECCC、METI 等规范全面覆盖；
- **40 年以上的化石电厂运行经验**：超过 100 万小时的蠕变断裂数据。

正是这些优势使 **Grade 91（T91/P91，9Cr-1Mo-VNb）** 与 **Grade 92（NF616/P92，9Cr-0.5Mo-1.8W-VNb）** 顺利扩展到第四代堆的堆外构件——高温气冷堆的蒸汽发生器与热气导管、钠冷快堆的蒸汽发生器与中间热交换器。

本章与第 17 章的奥氏体钢形成互补：奥氏体钢 316L(N) 适用于 >550 ℃ 的高温段，铁素体-马氏体钢 Gr.91/92 适用于 <620 ℃ 的中高温段——两者在 SFR 与 VHTR 的堆外构件中分工协作。

## 18.2　Grade 91（T91/P91）的系谱

### 18.2.1　从快堆到化石电厂

**Grade 91（T91/P91，9Cr-1Mo-VNb）最初由 ORNL Sikka 团队在 1970 年代为快堆蒸汽发生器/高温换热器开发**——这是它核工程渊源的有趣事实。后来扩展至化石电厂，成为主流 9-12Cr CSEF（creep strength enhanced ferritic）钢（ScienceDirect 综述）。今天 Grade 91 的工业基础主要来自化石电厂，再反哺核电。

### 18.2.2　蠕变性能

**Grade 91 在 600 ℃ 下的蠕变断裂强度约为 Grade 9（9Cr-1Mo）的两倍**（INIS）。蠕变失效在 >650 ℃ 时急剧加速，原因是 M23C6 粗化、Laves 相析出和 Z 相形成（MDPI Metals 12(12), 2022）。

长时蠕变数据的关键：**600 ℃ × 10⁵ 小时蠕变断裂强度约为 85–95 MPa**（详见第 6 章；近期 ECCC/ASME 修订后实际值约 88–94 MPa）。Panait 等人（*Int. J. Pres. Ves. Pip.* 87, 2010）是被引最多的 Grade 91 长时实验，系统观察了 10⁵ 小时蠕变后的组织演化。

### 18.2.3　蠕变数据库的延伸

Swindeman（ORNL/OSTI, 2007）验证 Grade 91 蠕变断裂数据库足以将 ASME Code 覆盖延伸至 **60 万小时（650 ℃ 以下）**——这为 40 年设计寿期提供了充分依据。

Klueh（2004，被引 788）系统综述了 9-12Cr 系铁素体/马氏体钢 10⁵ 小时蠕变断裂强度（含 T91）的代际发展。

## 18.3　Grade 92（NF616/P92）

### 18.3.1　成分与性能

**Grade 92（NF616/P92，9Cr-0.5Mo-1.8W-VNb）** 是第三代铁素体-马氏体钢。通过 W 合金化获得更高的蠕变强度：

- **600 ℃ × 10⁵ 小时蠕变断裂强度约 132 MPa**（Topbasi et al., *JNM*, 2015）；
- 600 ℃ 与 650 ℃ 下蠕变强度均优于 Grade 91；
- **但蠕变延性较低**（OECD/NEA SMINS Korea 会议论文集）。

### 18.3.2　应用扩展

OECD/NEA SMINS-2 报告（2012）系统讨论了 Grade 92 在创新核系统中的应用。NRC 文件 ML25261A140 评估了 Grade 92、Grade 92 + TMT、HT-UPS、NF-709 等高温堆候选材料的筛选。

## 18.4　应用场景

铁素体-马氏体钢在第四代堆堆外构件中的应用：

- **高温气冷堆（VHTR/HTR）**：蒸汽发生器、热气导管、中间热交换器外壳；
- **钠冷快堆（SFR）**：蒸汽发生器（水—钠界面）、过热器、再热器；
- **超临界水冷堆（SCWR）**：候选包壳与堆内构件（见第 4 章）；
- **熔盐堆（MSR）**：部分堆外低温段构件。

Grade 91 工程长期使用上限约 **620 ℃**（ASME II 表至 650 ℃，但 >620 ℃ 时许用应力急剧下降至 <50 MPa）。Grade 92 因 W 合金化可上探至约 650 ℃（OECD/NEA SMINS 综述）。

## 18.5　挑战与限制

### 18.5.1　Type IV 蠕变（焊缝热影响区）

**Type IV 开裂**发生在**临界/细晶热影响区（ICHAZ/FGHAZ）**——Grade 91 焊缝主导失效模式，最关键在约 600 ℃（Abson, TWI 综述, 2013，被引 256）。这是 Gr.91/92 在核电应用中的关键可靠性隐患。

对策：

- **焊缝强度降低因子（WSRF）**：ECCC 提供参考数据；焊缝几何与 WSRF 影响 Type IV 损伤；
- **PWHT 优化**：把焊后热处理温度从 600 ℃ 提至 840 ℃ 可使断裂位置偏离 Type IV 区。

### 18.5.2　Z 相脆化

**Z 相 Cr(V,Nb)N** 通过**消耗细小 MX（V/Nb 碳氮化物）强化相**形成，导致 9-12%Cr 钢**长时蠕变强度突然下降**。Cr 越高、Z 相形成越快（ResearchGate 综述，被引最多）。

Abe（2008，被引 784）综述指出 Z 相、M₆X、Fe₂(W,Mo) Laves 相协同析出导致长时蠕变强度损失。12%Cr 钢的"反向设计"思路甚至主动利用 Z 相作为强化相（Rashidi et al., 2017）。

### 18.5.3　循环软化

**Grade 91 是循环软化材料**，影响 EPP（弹性-全塑性）设计——ASME Section III Division 5 的 Code Case 正在扩展应变限值（ANL 2020）。这是 F-M 钢设计评估中需特殊处理的因素。

## 18.6　规范合格化

### 18.6.1　ASME Code

Grade 91 已在 ASME Code 中获批用于高温设计。HT-9 的 Code Case 开发策略——T91 与 HT-9 蠕变抗力相近（Serrano De Caro, 2012, OSTI）。

ASME Section III Division 5（2017 版为里程碑）涵盖 316H、Alloy 800H、2.25Cr-1Mo、Grade 91（NRC NUREG 技术评审）。

### 18.6.2　其他规范

- **日本 METI**：Gr.91/92 的高温规范；
- **欧盟 ECCC**：欧洲蠕变合作委员会的蠕变数据库；
- **RCC-MRx**：法国 AFCEN 规范，对 Gr.91/92 的覆盖较有限（主要用于 SFR 堆外奥氏体钢）。

## 18.7　制造技术

Grade 91/92 的制造技术高度成熟：

- **管材**：无缝管（挤压 + 冷拔）、焊管；
- **锻件**：大型锻件（用于压力容器、阀门）；
- **板材**：热轧板、冷轧板；
- **焊接**：TIG、SAW、EBW，需配合严格的 PWHT；
- **弯管**：热弯 + PWHT，需控制 Type IV 区的薄弱环节。

完整的工业化供应链是 Gr.91/92 相对于 ODS 钢、SiC/SiC 等先进材料的根本优势。

## 18.8　小结

Grade 91（T91）与 Grade 92（NF616）最初为化石电厂开发，凭借成熟的工业供应链、完整的规范合格化与 40 年以上的运行经验，顺利扩展到高温气冷堆与钠冷快堆的堆外构件。Grade 91 在 600 ℃ × 10⁵ 小时蠕变断裂强度约 85–100 MPa，工程长期使用上限约 620 ℃；Grade 92 因 W 合金化达约 132 MPa，可上探至约 650 ℃。Type IV 蠕变（焊缝热影响区开裂）、Z 相脆化与循环软化是长期可靠性的三大隐患。化石电厂经验向核电领域的迁移与验证是本章的核心议题——核电应用需要比化石电厂更严格的焊缝控制、PWHT 优化与寿期评估。

## 参考文献

1. ScienceDirect. *Grade 91 steel overview*. https://www.sciencedirect.com/topics/engineering/grade-91-steel
2. Klueh R. L. Elevated-temperature ferritic and martensitic steels. ORNL, 2004. https://digital.library.unt.edu/ark:/67531/metadc891870/m2/1/high_res/d/885938.pdf
3. Panait C. G., et al. Long-term creep of Grade 91. *International Journal of Pressure Vessels and Piping*, 2010, 87. https://www.researchgate.net/publication/222544175
4. Swindeman R. W. (ORNL). *Grade 91 creep database extension to 600,000 hours*. OSTI, 2007. https://www.osti.gov/biblio/974278
5. Topbasi C., et al. Creep rupture of Grade 92. *Journal of Nuclear Materials*, 2015. https://www.nuce.psu.edu/motta/Publications/127_Topbasi_JNM_2015.pdf
6. OECD/NEA. *Structural Materials for Innovative Nuclear Systems (SMINS-2)*. OECD, 2012. https://www.oecd.org/content/dam/oecd/en/publications/reports/2012/12/structural-materials-for-innovative-nuclear-systems-smins-2_g1g3750c/9789264992092-en.pdf
7. Abson D. J. *Review of Type IV cracking of weldments in 9-12Cr CSEF steels*. TWI, 2013. https://www.twi-global.com/technical-knowledge/published-papers/review-of-type-iv-cracking-of-weldments-in-9-12cr-creep-strength-enhanced-ferritic-steels/
8. Abe F. Creep strength degradation of 9-12Cr steels. PMC/NIH, 2008. https://pmc.ncbi.nlm.nih.gov/articles/PMC5099789/
9. Rashidi A. M., et al. Reverse design of 12%Cr steels using Z-phase. *Materials Science and Engineering A*, 2017. https://www.sciencedirect.com/science/article/abs/pii/S0921509317304367
10. MDPI Metals. *P92 creep failure mechanisms*. 2022, 12(12): 2054. https://www.mdpi.com/2075-4701/12/12/2054
11. ANL. *Cyclic softening of Grade 91 and ASME Div. 5 EPP design*. ANL, 2020. https://publications.anl.gov/anlpubs/2020/02/158585.pdf
12. Serrano De Caro P. *HT-9 Code Case development strategy*. OSTI, 2012. https://www.osti.gov/biblio/1053132
13. NRC. *High-temperature reactor candidate materials (Grade 92, HT-UPS, NF-709)*. ML25261A140. https://www.scribd.com/document/967069162/ML25261A140
14. Cambridge Phase-Trans. *Long-term creep and microstructural stability of 9-12Cr steels*. https://www.phase-trans.msm.cam.ac.uk/2005/LINK/146.pdf
15. NRC NUREG. *Technical review of ASME Section III Division 5*. https://downloads.regulations.gov/NRC-2021-0117-0013/content.pdf
16. Swei et al. *Creep crack growth of P91 welds at 600 ℃*. *Thermal Science*. https://thermalscience.rs/pdfs/papers-2017/TSCI170729240S.pdf
