# 第 8 章　新型绿色无铅钙钛矿材料在太阳电池领域的应用

> **核心命题**　铅基钙钛矿的毒性是产业化的根本顾虑——卤化铅钙钛矿 MAPbI₃ 材料本身含铅约 33 wt%，整块组件计约 12.6 wt%，均远超 RoHS 指令的 0.1 wt% 上限。本章讨论双钙钛矿（A₂BB'X₆，如 Cs₂AgBiBr₆）、Sn 基钙钛矿（FASnI₃）、Bi³⁺/Sb³⁺ 基 A₃B₂X₉，以及机器学习加速发现新型环境友好钙钛矿材料的研究前沿。

---

## 8.1　引言：铅毒性的产业化障碍

卤化铅钙钛矿（MAPbI₃、FAPbI₃）的高效率（> 26%）源于 Pb²⁺ 的独特电子结构：它的 6s² 孤对电子与卤素 p 轨道形成的 antibonding 态赋予钙钛矿优异的缺陷容忍性与高吸收系数。但铅的毒性是钙钛矿产业化的根本顾虑：

- **RoHS 限制**：欧盟 RoHS 指令限制非豁免产品中铅含量上限为 **0.1 wt%（1000 ppm）**，而 MAPbI₃ 材料本身含铅约 **33 wt%**（以整块组件计约 12.6 wt%），远超此限（Babayigit et al., *MRS Energy & Sustainability*, 2018）；
- **破损组件的铅浸出**：破损钙钛矿组件的铅浸出可能超过安全环境水平（Torrence et al., *Joule*, 2022，被引 87 次）；
- **公众接受度**：即使法规豁免，铅的公众形象仍是商业化的障碍。

因此，寻找"保持铅基钙钛矿光电优势但无铅毒性"的替代材料，是钙钛矿研究的核心前沿。Abate 等在《Joule》（2017，被引 514 次）提出"Perovskite Solar Cells Go Lead-Free"的批判性综述，系统讨论了这一方向。

## 8.2　双钙钛矿的研究

### 8.2.1　双钙钛矿的结构与原理

**双钙钛矿**（double perovskite）通式 **A₂BB'X₆**，通过在 B 位引入两种不同阳离子（B⁺ 与 B³⁺），把单一 Pb²⁺ 拆分为两个无毒或低毒离子，既维持电荷中性（2×1 + 1×3 + 6×(−1) = 0）又消除铅。

最具代表性的双钙钛矿是 **Cs₂AgBiBr₆**：

- **首次报道**：Slavney、Lindenberg 和 Karunadasa（Stanford）于 2016 年首次报道（*JACS*，被引约 2432 次），利用双钙钛矿结构把无毒的 Bi³⁺ 引入晶格；
- **载流子寿命**：Cs₂AgBiBr₆ 的室温光致发光寿命约 **660 ns**，达到与铅卤钙钛矿可比的载流子复合寿命——这是无铅钙钛矿的重大突破；
- **带隙**：约 **1.95–2.2 eV（间接带隙）**（*ACS Energy Letters*，被引 292 次），宽于 Shockley-Queisser 理想值（约 1.34 eV），是效率受限的根本原因；
- **器件效率**：经氢化处理的 Cs₂AgBiBr₆ 电池效率达 **6.37%**（Zhang et al., 2022，被引 474 次），而多数标准器件仅 2–3%。

### 8.2.2　双钙钛矿的优势与局限

| 优势 | 局限 |
|---|---|
| 无铅、环境友好 | 间接带隙（> 1.95 eV），效率低 |
| 稳定性优异（抗湿、抗热） | Ag/Bi 的成本与稀缺性 |
| 长载流子寿命（660 ns） | 光致相分离风险 |
| 缺陷容忍性较好 | 合成工艺窗口窄 |

其他研究中的双钙钛矿包括 Cs₂AgInCl₆（带隙约 3.2 eV，效率极低）、Cs₂NaBiCl₆ 等，但光电性能均不及 Cs₂AgBiBr₆。

## 8.3　Sn 基钙钛矿的研究

### 8.3.1　Sn²⁺ 作为 Pb²⁺ 的最接近替代

**锡（Sn²⁺）** 在化学性质与电子结构上最接近铅（Pb²⁺），是效率最高的无铅钙钛矿 B 位选择：

- **FASnI₃**：带隙约 **1.25–1.4 eV**（接近 SQ 极限最优值），认证效率 **14.0%**（*ACS Energy Letters*, 2022）；
- **Sn 基钙钛矿效率纪录**：无铅"全钙钛矿"锡卤化物电池效率达 **16.55%**（TaiyangNews 报道 16.65%，University of Queensland 创下）；
- **FASnI₃ 的优势**：带隙窄（适合单结与全钙钛矿叠层底电池）、载流子迁移率高。

### 8.3.2　Sn²⁺ 的氧化问题

Sn²⁺ 的根本缺陷是**易氧化为 Sn⁴⁺**：

```
Sn²⁺ → Sn⁴⁺ + 2e⁻
```

Sn⁴⁺ 的形成产生 Sn 空位（V_Sn），导致晶格自掺杂为 P 型并大幅增加复合中心，使 Sn 基钙钛矿的效率与稳定性远低于铅基。主要对策：

- **SnF₂ 添加剂**（约 10 mol%）：抑制 Sn²⁺ 氧化（Raddad et al., 2023，被引 77 次）；
- **惰性气氛制备**：全工艺在手套箱内进行，避免氧气接触；
- **抗氧化还原剂**：如羟胺盐、Sn 粉还原；
- **封装隔离**：严格的封装阻挡氧气侵入。

Sn 基钙钛矿是当前效率最高的无铅体系，但 Sn²⁺ 的氧化问题使其稳定性成为最大瓶颈。

## 8.4　Bi³⁺ 与 Sb³⁺ 基钙钛矿 A₃B₂X₉

Bi³⁺ 与 Sb³⁺ 因低毒性与 ns² 电子结构（与 Pb²⁺ 的 6s² 类似），是另一类无铅候选：

- **Cs₃Sb₂I₉**：效率约 2–3.25%（最高约 6.22%）；
- **Cs₃Bi₂I₉**：效率约 1–2.5%；
- **MA₃Bi₂I₉**：通常 < 1%（带隙大、激子结合能高，约 0.4 eV）。

A₃B₂X₉ 体系的根本局限是**二维层状结构**（非三维钙钛矿骨架）导致载流子传输差、激子结合能高。目前效率仍远低于 Sn 基与双钙钛矿。

## 8.5　无铅反钙钛矿

**反钙钛矿**（anti-perovskite）的结构与传统钙钛矿 ABX₃ 颠倒（阳离子与阴离子位置互换），如 LiMgH₃ 等。这类材料的研究处于非常早期阶段：

- **研究现状**：仅有少量第一性计算研究报道，实验数据稀缺；
- **优势**：理论预测部分反钙钛矿具有合适的带隙与高载流子迁移率；
- **局限**：合成困难、稳定性未知、无实际器件报道。

反钙钛矿目前主要是理论计算的兴趣方向，距器件应用尚远。

## 8.6　机器学习加速发现新型无铅钙钛矿材料

传统材料发现依赖"试错-实验"循环，效率低、成本高。**机器学习 + 第一性原理计算**的高通量筛选正在加速无铅钙钛矿的发现：

### 8.6.1　奠基性工作

- **Lu et al.（*Nat. Commun.*, 2018，被引 861 次）**：把机器学习与第一性原理计算结合，快速筛选稳定且无铅的杂化有机-无机钙钛矿（HOIP），筛选出多种潜在候选；
- **Sun et al.（*Joule*, 2019，被引 357 次）**：高通量合成结合机器学习诊断，加速钙钛矿衍生材料的开发与优化。

### 8.6.2　机器学习的方法学

机器学习加速材料发现的工作流：

1. **数据收集**：从 Materials Project、OQMD 等数据库收集已知钙钛矿的形成能、带隙、稳定性等数据；
2. **特征工程**：把 A/B/X 离子的属性（电负性、离子半径、价电子数等）编码为特征向量；
3. **模型训练**：用随机森林、梯度提升、神经网络等模型预测新组合的性质；
4. **高通量筛选**：对数百万虚拟组合预测，筛选出符合带隙、稳定性、无毒约束的候选；
5. **第一性验证**：对筛选结果做 DFT 精确计算，确认候选；
6. **实验合成**：对最有希望的候选做实验验证。

### 8.6.3　代表性研究组

- **Stanford（Karunadasa 组）**：双钙钛矿 Cs₂AgBiBr₆ 的奠基者，持续探索新型双钙钛矿；
- **Northwestern（Kanatzidis 组）**：锡基钙钛矿与硫族钙钛矿的权威；
- **NREL、LBNL**：高通量计算与材料基因组方法。

## 8.7　无铅钙钛矿的展望

无铅钙钛矿的现状与方向：

| 体系 | 效率 | 稳定性 | 主要瓶颈 |
|---|---|---|---|
| Sn 基（FASnI₃） | 14–16.6% | 差（氧化） | Sn²⁺ 氧化 |
| 双钙钛矿（Cs₂AgBiBr₆） | 6.4% | 优 | 间接带隙、效率低 |
| Bi³⁺/Sb³⁺ 基（A₃B₂X₉） | < 6% | 中 | 二维结构、激子结合能高 |
| 反钙钛矿 | 无器件 | 未知 | 合成困难 |

无铅钙钛矿距铅基（26.7%）仍有巨大差距，但 Sn 基（> 14%）已展示实用潜力。未来方向：

1. **Sn 氧化抑制**：抗氧化剂、惰性工艺、全无机 Sn 基钙钛矿；
2. **双钙钛矿带隙优化**：通过合金化把 Cs₂AgBiBr₆ 的间接带隙降至 < 1.7 eV；
3. **机器学习驱动**：加速发现全新的无铅钙钛矿体系；
4. **叠层兼容**：Sn 基窄带隙钙钛矿作为全钙钛矿叠层底电池（详见第 9 章）。

## 参考文献

1. Babayigit A., et al. Environment versus sustainable energy: The case of lead halide perovskite-based solar cells. *MRS Energy & Sustainability*, 2018. https://www.cambridge.org/core/journals/mrs-energy-and-sustainability/
2. Torrence L., et al. Environmental and health risks of perovskite solar modules. *Joule*, 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC9860350/
3. Abate A., et al. Perovskite solar cells go lead free. *Joule*, 2017. https://www.sciencedirect.com/science/article/pii/S2542435117300806
4. Slavney A. H., Hu T., Lindenberg A. M., Karunadasa H. I. A bismuth-halide double perovskite with long carrier recombination lifetime for photovoltaic applications. *J. Am. Chem. Soc.*, 2016. https://pubmed.ncbi.nlm.nih.gov/26853379/
5. McClure E. T., et al. Cs₂AgBiBr₆ performance-limiting factors. *ACS Energy Lett.* https://pubs.acs.org/doi/10.1021/acsenergylett.0c01020
6. Zhang W., et al. Hydrogenated Cs₂AgBiBr₆ for significantly improved solar cells. 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC9192601/
7. Jiang X., et al. FASnI₃ films for lead-free perovskite solar cells with over 14% efficiency. *ACS Energy Lett.*, 2022. https://pubs.acs.org/doi/10.1021/acsenergylett.2c00776
8. TaiyangNews. Lead-free perovskite solar cell reaches 16.65% efficiency. https://taiyangnews.info/amp/story/technology/queensland-university-lead-free-perovskites-solar-cell-16-65-efficiency-2
9. Raddad E. A., et al. Sn-based perovskite solar cells towards high stability. 2023. https://pmc.ncbi.nlm.nih.gov/articles/PMC10143209/
10. Lu S., et al. Accelerated discovery of stable lead-free hybrid organic-inorganic perovskites. *Nat. Commun.*, 2018. https://www.nature.com/articles/s41467-018-05761-w
11. Sun S., et al. High-throughput machine learning screening of perovskite derivatives. *Joule*, 2019. https://www.cell.com/joule/fulltext/S2542-4351(19)30257-0
12. Konstantakou M., Stergiopoulos T. A review on lead-free perovskites. *J. Mater. Chem. A*, 2017.
13. Giustino F., et al. Toward lead-free perovskite solar cells. *ACS Energy Lett.*, 2020.
14. Yang S., et al. Tin halide perovskite review. 2024. https://pubmed.ncbi.nlm.nih.gov/38779891/
15. Li X., et al. Cs₃Sb₂I₉ heterojunction solar cells. *Chemical Engineering Journal*. https://www.sciencedirect.com/science/article/abs/pii/S1385894721010123
