# 第 7 章　钙钛矿太阳电池的干法制备技术

> **核心命题**　真空蒸镀等干法工艺提供了与溶液法互补的另一条路径——无溶剂、界面更 sharp、与硅半导体工艺兼容、适合叠层电池的硅底电池集成。顺序真空蒸镀钙钛矿电池效率已达 24.42%（Li et al., *Sci. Adv.*, 2022），共蒸发的钙钛矿薄膜在 1000 小时连续光照下保持初始性能。干法是把钙钛矿嵌入主流半导体制造链的关键工艺。

---

## 7.1　真空蒸镀应用介绍

溶液法（旋涂、印刷）主导了实验室钙钛矿研究，但在产业化与高性能器件中，**真空干法工艺**（vacuum deposition）提供了不可替代的优势：

- **无溶剂**：避免 DMF/DMSO 等有毒溶剂，环保且与洁净室兼容；
- **界面 sharp**：层间无溶剂互溶，界面更清晰，适合叠层电池；
- **大面积均匀**：真空蒸镀的厚度均匀性优于溶液法（已证实的产业化能力，OLED 行业的标准）；
- **与硅工艺兼容**：可直接在晶硅电池上沉积钙钛矿顶电池，是钙钛矿/硅叠层的天然工艺；
- **化学计量比精确**：共蒸发可精确控制 A/B/X 比例。

主流真空干法包括：

- **热蒸发**（thermal evaporation）：电阻加热蒸发源；
- **电子束蒸发**（e-beam evaporation）：电子束轰击蒸发源；
- **共蒸发**（co-evaporation）：多源同时蒸发形成化合物；
- **反应磁控溅射**（reactive sputtering）：用于 NiOₓ 等无机传输层。

## 7.2　器件电荷传输层材料的选择和制备

### 7.2.1　电子传输层的干法沉积

- **C₆₀（富勒烯）**：热蒸发 C₆₀ 是 p-i-n 倒置结构的标准 ETL，沉积温度低、与钙钛矿界面良好。典型厚度 20–40 nm。
- **BCP（浴铜灵）**：在 C₆₀ 与金属电极之间作为修饰层，热蒸发，厚度约 6–8 nm。
- **SnO₂**：可通过原子层沉积（ALD）或反应溅射制备，致密无针孔，适合大面积。

### 7.2.2　空穴传输层的干法沉积

- **NiOₓ**：反应磁控溅射沉积，是 p-i-n 倒置结构的主流无机 HTL。NiOₓ 高稳定性（远超 spiro-OMeTAD）、高迁移率，但需精确控制氧分压获得合适的能级与化学计量；
- **CuSCN**：可热蒸发沉积，但与钙钛矿的界面反应需控制；
- **Spiro-OMeTAD**：理论上可热蒸发，但本征导电性差，仍以溶液旋涂为主（辅以 Li-TFSI 掺杂）。

干法 HTL 的优势是无机化（NiOₓ）带来的稳定性提升，这是高效率钙钛矿/硅叠层电池的标准配置。

## 7.3　热蒸发制备钙钛矿太阳电池

### 7.3.1　钙钛矿层的蒸镀方法

钙钛矿层的真空蒸镀主要有三种方法：

1. **顺序蒸镀（sequential evaporation）**：先蒸镀 PbI₂（或 PbCl₂），再蒸镀 MAI/FAI 有机盐，退火后反应形成钙钛矿。这是最成熟的方法，效率纪录 24.42% 即由 Li 等人（*Sci. Adv.* 8, eabo7422, 2022）实现；
2. **共蒸发（co-evaporation）**：PbI₂ 与 MAI/FAI 同时从两个源蒸发，直接形成钙钛矿。化学计量比控制更精确，但工艺窗口窄；
3. **单源蒸镀**：预先合成的钙钛矿粉末从单一源蒸发，适合无机钙钛矿（如 CsPbBr₃）。

### 7.3.2　顺序蒸镀的工艺要点

顺序蒸镀的关键工艺参数：

- **PbI₂ 层厚度**：典型 200–300 nm，过厚会导致有机盐渗透不完全；
- **有机盐蒸镀**：MAI/FAI 的蒸镀速率与总量需精确控制，过量导致表面残留、不足导致转化不完全；
- **退火**：100–150 ℃ 退火使 PbI₂ 与 MAI/FAI 完全反应，形成钙钛矿相；
- **两步法的优势**：PbI₂ 层致密平整，与界面层接触良好，适合大面积。

### 7.3.3　干法钙钛矿的器件性能

干法钙钛矿电池的效率纪录：

- **顺序蒸镀**：24.42%（Li et al., *Sci. Adv.* 8, eabo7422, 2022）；
- **共蒸发钙钛矿/硅叠层**：共蒸发的钙钛矿薄膜在 1000 小时连续光照下保持初始性能（Roß et al., *Adv. Energy Mater.* 11, 2101460, 2021）；
- **干法 + 溶液法混合**：传输层干法 + 钙钛矿层溶液法的混合工艺，是产业化的折中方案。

干法钙钛矿电池的效率略低于溶液法（26.7%），但稳定性与大面积均匀性更优，是产业化的重要路径。

### 7.3.4　干法在叠层电池中的优势

干法在钙钛矿/硅叠层电池中具有独特优势：

- **硅底电池兼容**：可直接在绒面晶硅电池上蒸镀钙钛矿顶电池，无需溶液法的水/溶剂侵入风险；
- **界面 sharp**：钙钛矿/传输层界面无溶剂互溶，适合薄层（< 50 nm）的高质量沉积；
- **Oxford PV 的产业化路径**：钙钛矿/硅叠层商业组件（24.5%，2024 年首批交付）即采用干法 + 湿法混合工艺。

理论建模表明，全干法钙钛矿/硅叠层的效率潜力可达 **37.6%**，远超当前纪录（34.6%）。

## 7.4　钙钛矿太阳电池干法制备的稳定性

干法钙钛矿电池的稳定性优势：

- **无残留溶剂**：避免了 DMF/DMSO 残留导致的长期退化；
- **致密薄膜**：蒸镀薄膜致密度高，水氧侵入路径少；
- **无机传输层**：NiOₓ、SnO₂ 等无机层稳定性远超 spiro-OMeTAD；
- **共蒸发模块的稳定性**：共蒸发的钙钛矿薄膜在 1000 小时连续光照下保持初始性能（Roß et al., 2021），是干法稳定性的关键证据。

干法器件在 IEC 61215 湿热测试（85 ℃ / 85% RH）中的表现普遍优于溶液法器件。

## 7.5　小结

干法制备是钙钛矿电池从溶液法主导的实验室研究走向产业化可靠性的另一条路径。顺序真空蒸镀效率已达 24.42%（Li et al., 2022），共蒸发的钙钛矿薄膜在 1000 小时连续光照下保持初始性能（Roß et al., 2021）。干法的核心优势是无溶剂、界面 sharp、与硅工艺兼容、稳定性优——使其特别适合钙钛矿/硅叠层电池（Oxford PV、LONGi 的产业化路径）。湿法与干法的混合工艺（传输层干法 + 钙钛矿层湿法或反之）是当前产业化的折中方案。干法是把钙钛矿嵌入主流半导体制造链的关键工艺。

## 参考文献

1. Longo G., et al. Vacuum-evaporated perovskite solar cells. *Joule*, 2018.
2. Li H., et al. Sequential vacuum-evaporated perovskite solar cells with 24.42% efficiency. *Sci. Adv.*, 2022, 8: eabo7422. https://www.science.org/doi/10.1126/sciadv.abo7422
3. Roß M., et al. Co-evaporated formamidinium lead iodide based perovskites with 1000 h stability. *Adv. Energy Mater.*, 2021, 11: 2101460.
4. Oxford PV. First commercial perovskite-silicon tandem modules. 2024-09. https://www.oxfordpv.com/press-releases
5. Bush K. A., et al. 23.6%-efficient monolithic perovskite/silicon tandem solar cells. *Nat. Energy*, 2017.
6. Werner J., et al. Efficient monolithic perovskite/silicon tandem solar cell. *ACS Energy Lett.*, 2016.
7. Momblona C., et al. Efficient vacuum-deposited p-i-n perovskite solar cells. *Adv. Electron. Mater.*, 2019.
8. Saliba M., et al. Cesium-containing triple cation perovskite solar cells. *Energy Environ. Sci.*, 2016.
9. Al-Ashouri A., et al. Monolithic perovskite/silicon tandem with 29% efficiency. *Science*, 2020.
10. Liu Z., et al. Vapor-deposited inorganic perovskite solar cells. *Adv. Mater.*, 2023.
11. Wang S., et al. Vacuum-deposited NiOₓ hole transport layer. *Sol. RRL*, 2022.
12. Tress W., et al. Performance of vacuum-deposited perovskite solar cells. *Nat. Energy*, 2024.
13. Li Z., et al. Scalable vacuum deposition for perovskite solar modules. *Joule*, 2023.
14. Green M. A., et al. Solar cell efficiency tables. *Prog. Photovolt.*, 2024. https://onlinelibrary.wiley.com/doi/full/10.1002/pip.3831
15. NREL. Best Research-Cell Efficiency Chart. https://www.nrel.gov/pv/cell-efficiency.html
