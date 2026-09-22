# 第 10 章　杂化钙钛矿室内光伏器件

> **核心命题**　室内弱光（100–1000 lux）是一个被传统光伏忽视的巨大市场。钙钛矿的带隙可调性使其与 LED/荧光灯光谱高度匹配——室内光伏最优带隙约 1.9 eV，远高于室外（1.34 eV），钙钛矿可精确匹配。室内光伏钙钛矿组件在 1000 lux 下效率已达 **36.36%**（认证，Zhang et al., 2022），全无机 CsPbI₃ 室内电池达 **41.21%**（*APL*, 2025）——远超任何室外单结效率。

---

## 10.1　室内光伏的发展前景

### 10.1.1　室内光伏技术

室内光伏（indoor photovoltaics）是为室内环境（100–1000 lux，远低于室外 AM1.5G 的 100,000 lux）设计的微型光伏器件。其核心应用是为物联网（IoT）传感器、智能家居设备、可穿戴电子产品供电，替代或补充纽扣电池。

室内光伏的关键差异：

- **光强极弱**：1000 lux 约对应总辐照度 **8.6 W/m²**（Michael et al., 2020，被引 320 次），约为 AM1.5G（1000 W/m²）的百分之一量级（约 1/116）；
- **光谱不同**：LED 与荧光灯的光谱集中在 400–700 nm（可见光），无红外成分；
- **最优带隙不同**：室内最优带隙约 **1.9 eV**（Jagadamma et al., 2021，被引 56 次），远高于室外 1.34 eV。

### 10.1.2　室内光伏设计

室内光伏器件设计的核心考虑：

- **带隙匹配**：带隙需调到约 1.8–1.9 eV 以匹配 LED/荧光灯光谱；
- **低光强下的串联电阻**：弱光下电流小，串联电阻损失相对放大，需高 shunt 电阻；
- **V_oc 优化**：弱光下 V_oc 下降明显，需宽带隙保证足够电压；
- **大面积与图案化**：IoT 应用需要定制化形状与面积。

### 10.1.3　室内光伏的未来市场

室内光伏的市场潜力巨大：

- **IoT 传感器**：全球部署的 IoT 传感器预计 2030 年超百亿台，每台需独立电源；
- **市场规模**：IDTechEx 预测全球钙钛矿光伏市场到 **2037 年达 193 亿美元**（CAGR > 60%），明确将"室内 IoT"列为关键应用；
- **替代纽扣电池**：室内光伏可替代 CR2032 等纽扣电池，避免维护与回收问题；
- **无缝集成**：钙钛矿的柔性、半透明、可调色使其可集成到墙面、桌面、设备外壳。

## 10.2　室内光伏的研究现状

### 10.2.1　硅基光伏器件

非晶硅（a-Si）是最早的室内光伏技术，效率约 5–14%。其优势是成本低、工艺成熟；劣势是带隙约 1.7 eV 偏窄于室内最优 1.9 eV、弱光下 V_oc 低（< 0.7 V）。晶硅因带隙 1.12 eV 远偏离室内最优、弱光性能差，基本不用于室内。

### 10.2.2　染料敏化光伏器件

染料敏化电池（DSSC）的染料吸收峰可调到可见光区，与室内光谱匹配良好，效率约 10–20%。其优势是半透明、可调色、柔性；劣势是液态电解质的封装与长期稳定性问题。

### 10.2.3　III-V 族化合物光伏器件

GaInP 等 III-V 化合物（带隙约 1.8–1.9 eV）在室内光伏中性能优异：Fraunhofer ISE 的 GaInP 电池在 100 lux 下效率 **37.5%**，1000 lux 下峰值 **41.4%**。其优势是带隙精确匹配、载流子质量极高；劣势是成本极高（MOCVD 工艺），仅适合航空航天或高端 IoT。

### 10.2.4　有机光伏器件

有机太阳能电池（OPV）的带隙可通过分子设计调节到 1.8–2.0 eV，室内效率约 10–15%。其优势是柔性、半透明、可溶液加工；劣势是稳定性差（光氧化）、载流子迁移率低。宽带隙 OPV 在室内性能优于硅基室内光伏（Muhammad et al., 2022，被引 103 次）。

### 10.2.5　钙钛矿光伏器件

钙钛矿是室内光伏的明星技术：

- **带隙完美匹配**：通过 Br/I 调节到 1.8–1.9 eV，与 LED/荧光灯光谱高度匹配；
- **弱光性能优异**：高 shunt 电阻、低缺陷密度使弱光下 V_oc 损失小；
- **效率纪录**：
  - 经 KI 处理修复 Br 空位的钙钛矿室内组件，1000 lux TL84 光源下认证效率 **36.36%**（Zhang et al., *Advanced Science*, 2022，被引 71 次），最优带隙 1.82 eV；
  - 全无机 CsPbI₃（1.73 eV）室内电池在 1062 lux WLED 下效率 **41.21%**（V_oc = 1.07 V，*APL*, 2025），为钙钛矿室内最高报道之一；
  - UCL 团队在 1000 lux 下转换 **37.6%** 室内光为电能（宽带隙 1.75 eV，2025）。

钙钛矿室内光伏的效率已超过所有竞争技术（除昂贵的 III-V），且具备低成本、柔性、可调色的产业化优势。

### 10.2.6　钙钛矿室内光伏存在的问题

钙钛矿室内光伏的挑战：

- **稳定性**：IoT 应用要求 5–10 年寿命，钙钛矿的长期稳定性仍需验证；
- **大面积均匀性**：实验室小面积（< 0.1 cm²）效率高，放大到 cm² 级效率下降；
- **铅毒性**：室内 IoT 的铅泄漏风险敏感，无铅化（见第 8 章）尤为重要；
- **光谱与照度标准化**：不同 LED/荧光灯的光谱与照度差异大，效率报告缺乏可比性。

## 10.3　室内光伏测量存在的问题和解决方案

室内光伏的效率测量缺乏统一标准，是领域的主要障碍：

**问题**：

- **光谱差异**：LED（460 nm 蓝、550 nm 绿、650 nm 红）与荧光灯（多峰）的光谱差异大，同一器件在不同光源下效率不同；
- **照度换算**：lux（光照度，与人眼响应加权）与 W/m²（辐照度）的换算依赖光源光谱；
- **面积定义**：小面积器件的有效面积（孔径 vs 总面积）定义不统一；
- **无标准光源**：实验室常用不同 LED/荧光灯，结果难比较。

**解决方案**：

- **标准化光源**：建议采用标准 LED（如 TL84、WLED 5500K）作为测试光源；
- **照度计校准**：用 NIST 可溯源的照度计校准测试光强；
- **光谱修正**：报告测试光源的光谱分布与器件 EQE，便于换算到其他光源；
- **ISOS-I 协议**：ISOS 已发布室内光伏测试指南（ISOS-I），建议遵循。

## 10.4　展望

室内光伏钙钛矿的未来方向：

1. **稳定性突破**：通过封装、二维钙钛矿、无机传输层（NiOₓ、SnO₂）提升 IoT 所需的 5–10 年寿命；
2. **无铅化**：Sn 基或双钙钛矿室内电池（见第 8 章）规避铅泄漏风险；
3. **大面积制备**：狭缝涂布、喷墨打印（见第 6 章）实现 cm² 级高效器件；
4. **集成方案**：与 IoT 传感器、MCU、无线通信芯片的封装级集成；
5. **标准化**：推动 ISOS-I 成为国际标准，提升效率报告的可比性。

室内光伏是钙钛矿最容易实现商业化的应用场景之一——市场规模大、效率要求低于室外、可调色与柔性是独特优势。预计 2025–2030 年，钙钛矿室内光伏将在 IoT 传感器市场实现规模化应用。

## 参考文献

1. Michael K., et al. A conversion guide: solar irradiance and lux illuminance. 2020. https://www.extrica.com/article/21667
2. Jagadamma L. K., et al. Wide-bandgap halide perovskites for indoor photovoltaics. 2021. https://pmc.ncbi.nlm.nih.gov/articles/PMC8032892/
3. Zhang Y., et al. Perovskite indoor photovoltaic module with 36.36% efficiency. *Advanced Science*, 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC9685472/
4. Applied Physics Letters. CsPbI₃ indoor photovoltaic cell with 41.21% efficiency. 2025. https://pubs.aip.org/aip/apl/article/127/4/040502/3356962/
5. UCL News. New solar cells could power devices with indoor light. 2025-08. https://www.ucl.ac.uk/news/2025/aug/new-solar-cells-could-power-devices-indoor-light
6. Mathew P. S., Samukkawa S. Light sources comparison for indoor photovoltaics. *ACS Appl. Energy Mater.* https://pubs.acs.org/doi/10.1021/acsaem.3c01274
7. Muhammad F. Y., et al. Indoor photovoltaic technologies review. 2022. https://www.sciencedirect.com/science/article/abs/pii/S2468606921002720
8. IDTechEx. Perovskite Photovoltaics 2027-2037. https://www.idtechex.com/en/research-report/perovskite-photovoltaics/1158
9. Freitag M., et al. Perovskite indoor photovoltaics. *Nat. Photonics*, 2017.
10. Chen B., et al. Efficient perovskite indoor photovoltaic cells. *Joule*, 2024.
11. ISOS-I. Indoor photovoltaic testing protocols.
12. Cheng Y., et al. Sn-based perovskite indoor photovoltaics. *Adv. Mater.*, 2024.
13. Chen Y., et al. Lead-free perovskite indoor cells. *Energy Environ. Sci.*, 2025.
14. He X., et al. Large-area perovskite indoor modules. *Nat. Energy*, 2024.
15. Cui P., et al. Stability of perovskite indoor photovoltaics. *Adv. Energy Mater.*, 2025.
