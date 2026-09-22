# 第 12 章　SiCf/SiC 复合材料

> **核心命题**　SiCf/SiC 复合材料把脆性的陶瓷 SiC 转化为"伪塑性"的工程材料：连续 SiC 纤维承受载荷，BN/PyC 界面相允许纤维-基体脱粘，从而避免了灾难性脆性断裂。它兼具 >1000 ℃ 的高温强度、低活化与不发生辐照脆化的特性，是唯一可能突破金属体系温度上限的候选。但 SiC 辐照致热导率下降、基体开裂、规范合格化滞后，是它工程化的三大门槛。

---

## 12.1　引言：从脆性陶瓷到工程复合材料

碳化硅（SiC）陶瓷本身具有优异的高温强度（>1000 ℃）、低活化特性与化学稳定性，是第四代堆与聚变堆高温结构材料的天然候选。但烧结 SiC 是脆性材料——一旦出现裂纹即灾难性断裂，没有金属那样的"屈服—强化"裕量，无法直接用于承受机械载荷的结构件。

连续 SiC 纤维增强 SiC 基复合材料（SiCf/SiC）的根本创新在于：通过引入**纤维-基体间的弱界面相**（BN 或热解碳 PyC），允许纤维在基体开裂时脱粘并桥联裂纹，把脆性断裂转化为"伪塑性"的渐进失效。这一突破使 SiC 陶瓷成为可工程化的结构材料，把它推到了第四代堆高温结构材料候选的前沿。

## 12.2　SiCf/SiC 的应用定位

SiCf/SiC 在第四代堆与聚变堆中有多类应用场景：

- **VHTR 控制棒连杆**：在 900–1000 ℃ 氦气中承受拉伸与冲击载荷；
- **GFR 包壳**：气冷快堆的高温包壳候选；
- **聚变堆第一壁**：承受高热流与等离子体粒子辐照；
- **FHR/MSR 部件**：与 FLiBe 等氟盐相容性好（详见第 5 章）。

SiC/SiC 在氟盐中的腐蚀行为已在第 5 章讨论。本章聚焦 SiC/SiC 作为结构件的组分设计、辐照行为与规范进展。

## 12.3　复合材料的三相组分

SiCf/SiC 由三相组成，每相都至关重要：

### 12.3.1　SiC 纤维

第二代与第三代 SiC 纤维的代表：

- **Hi-Nicalon Type S**（日本 Nippon Carbon）：氧含量低（<0.5 wt%），近化学计量比，结晶度高；
- **Tyranno SA3**（日本 Ube Industries）：含少量 Al，高温稳定性极佳。

这些第三代纤维的关键改进是**低氧含量与近化学计量比**，使纤维在高温与辐照下保持稳定，避免了第一代纤维（如 Nicalon NL202，含氧约 10%）因 CO 气体释放导致的性能退化。

### 12.3.2　界面相（Interphase）

**BN 或热解碳（PyC）界面相**是 SiCf/SiC 实现伪塑性的关键。它是一层厚度约 0.3–1 μm 的弱结合层，作用是：

- 在基体裂纹扩展到纤维时，允许纤维-基体界面脱粘（debonding）；
- 纤维桥联裂纹，承担额外载荷；
- 通过纤维拔出（fiber pull-out）吸收能量，避免灾难性断裂。

但 PyC 界面相在氧化气氛中不稳定（>500 ℃ 即氧化），新一代研究转向 BN 界面相或自愈合多层界面相。

### 12.3.3　SiC 基体

SiC 基体通过 **化学气相渗透（CVI）** 或液相烧结（LSI、MI）工艺填充到纤维预制件中。CVI 是最成熟工艺，能保持纤维性能，但孔隙率高（约 10–15%）且周期长（数周至数月）。

## 12.4　关键性能特点

SiCf/SiC 相对金属体系的性能优势：

- **高温强度**：在 >1000 ℃ 仍保持高强度，远超金属体系；
- **低活化**：SiC 的衰变热与残余放射性远低于铁基合金；
- **不发生辐照脆化**：与金属不同，SiC 在辐照下不出现 DBTT 上移；
- **抗蠕变**：高温蠕变速率极低；
- **化学稳定性**：与液态金属、熔盐相容性好。

## 12.5　辐照行为

### 12.5.1　SiC 的辐照肿胀

中子辐照会在 SiC 晶格中产生过饱和点缺陷，导致**各向同性肿胀**。肿胀量级：<1000 ℃ 范围内饱和肿胀约 2%，温度升高肿胀下降。这是 SiC/SiC 复合材料在高温下需要考虑的尺寸变化。

### 12.5.2　辐照致热导率下降

更关键的限制是**辐照致热导率下降**：辐照产生的缺陷散射声子，使 SiC 的热导率显著降低（可降至未辐照值的 30–50%）。这对包壳等需要散热的应用是关键瓶颈——热导率下降会导致燃料中心温度升高。

### 12.5.3　复合材料的辐照稳定性

SiCf/SiC 复合材料在辐照下：纤维与基体的辐照肿胀匹配良好，界面相（特别是 BN）保持稳定，整体不发生显著的力学性能退化（与金属不同）。这是 SiC/SiC 的根本优势之一。ORNL 的 Katoh Yutai 团队系统研究了 SiC/SiC 在 >30 dpa、800–1200 ℃ 范围内的辐照行为。

## 12.6　失效模式

SiCf/SiC 的失效模式与金属完全不同：

- **基体开裂（matrix cracking）**：在低应力下基体即出现多重微裂纹，但纤维继续承担载荷；
- **界面脱粘与纤维拔出**：是"伪塑性"的来源；
- **纤维断裂（fiber fracture）**：最终的极限失效模式；
- **氧化失效**：PyC 界面相氧化后失去伪塑性，需用 BN 替代。

设计 SiCf/SiC 部件时，必须用"基体开裂应力"作为设计极限，而非"极限拉伸强度"——这把设计裕量与失效模式的概念重新定义。

## 12.7　规范进展

SiCf/SiC 的工程化面临规范合格化的滞后：

- **ASME Section III Division 5** 对 SiC/SiC 的合格化正在推进中（Code Case N-880/N-881 系列，建议向 ASME 直接核实最新编号）；
- **ASTM C1779**：SiC/SiC 力学测试标准；
- **JCMA（日本碳素协会）** 与法国 CEA 也建立了 SiC/SiC 部件的设计准则。

SiCf/SiC 的规范合格化比金属体系更复杂，因为它涉及多尺度失效模式（基体、界面、纤维三个层次）与各向异性。当前的规范进展仍落后于金属（如 Alloy 617 已合格化至 950 ℃）。

## 12.8　代表项目与研究机构

- **日本**：Nippon Carbon（Hi-Nicalon 纤维）、Ube Industries（Tyranno 纤维）、京都大学（Katoh Yutai 系统工作）；
- **法国 CEA**：SiC/SiC 在 GFR 包壳中的应用评估；
- **美国 ORNL**：Katoh Yutai 后续在 ORNL 主导 SiC/SiC 辐照研究；
- **欧盟**：聚变堆 SiC/SiC 部件研究（EUROfusion 框架）。

## 12.9　小结

SiCf/SiC 复合材料通过连续 SiC 纤维 + BN/PyC 界面相 + CVI 基体的三相设计，把脆性 SiC 陶瓷转化为"伪塑性"工程材料，兼具 >1000 ℃ 高温强度、低活化与不发生辐照脆化的特性。它是唯一可能突破金属体系温度上限的候选。但 SiC 辐照致热导率下降（对散热部件关键）、基体开裂模式（重新定义设计裕量）与规范合格化滞后，是它工程化的三大门槛。日本、法国、美国、欧盟都在积极推进 SiC/SiC 的研发与合格化。

## 参考文献

1. Katoh Y., et al. *SiC/SiC composite for advanced nuclear systems*. ORNL/TM-2015. https://www.osti.gov/biblio/1235234
2. Katoh Y., et al. Radiation effects in SiC/SiC composites for fusion reactor blanket. *Journal of Nuclear Materials*. https://www.sciencedirect.com/science/article/abs/pii/S0022311507000931
3. ORNL. *SiC/SiC cladding accident-tolerant fuel*. ORNL publications. https://info.ornl.gov/sites/publications/
4. Koyanagi T., et al. *Irradiation resistance of silicon carbide*. *Current Opinion in Solid State & Materials Science*. https://www.sciencedirect.com/science/article/abs/pii/S1359028619300722
5. Koyanagi T., et al. *Single crystal SiC corrosion in Be-containing fluoride salt*. *Corrosion Science*, 2023. https://www.sciencedirect.com/science/article/abs/pii/S0010938X23003438
6. Lee J. J., et al. *Materials compatibility of SiC and FHR fluoride salts*. OSTI, 2019. https://www.osti.gov/servlets/purl/1531263
7. Nippon Carbon. *Hi-Nicalon Type S product information*. https://www.carbon.co.jp/english/products/
8. Ube Industries. *Tyranno Fiber product information*. https://www.ube.com/
9. ASTM C1779. *Standard test method for SiC/SiC composite flexural properties*.
10. ASME BPVC Section III Division 5. *High-temperature reactor construction code*.
11. Aitkaliyeva A., et al. *Irradiation effects in Generation IV nuclear reactor materials*. INL, 2017. https://inldigitallibrary.inl.gov/sites/sti/sti/Sort_7379.pdf
12. Zinkle S. J., Busby J. T. Structural materials for fission & fusion energy. *Materials Today*, 2009, 12(11): 12–19. https://www.sciencedirect.com/science/article/pii/S1369702109702949
