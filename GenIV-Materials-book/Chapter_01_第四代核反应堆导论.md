# 第 1 章　第四代核反应堆导论

> **核心命题**　第四代核能系统以更高出口温度、更长换料周期和更严苛的冷却剂环境，把结构材料推到了现役轻水堆从未触及的服役窗口——500–1000 ℃的高温、液态金属/熔盐/超临界水/高温氦等强腐蚀介质，以及百 dpa 量级的辐照剂量。本章建立全书"环境—材料—寿期"的分析框架，使后续各章的腐蚀机理、辐照损伤与材料选型得以归位。

---

## 1.1　引言：新一代核系统的需求

现役轻水反应堆（LWR）的工作介质相对温和：一回路水温约 290–330 ℃、压力 7–16 MPa、堆芯构件的累积辐照剂量通常不超过 10 dpa（位移每原子）。经过半个多世纪的发展，锆合金包壳、304/316 不锈钢堆内构件和低合金钢压力容器已经形成了成熟的工程体系。

进入 21 世纪后，全球核能界对反应堆提出了更高的期待：更高的热效率、更深的燃耗、更少的放射性废物、更强的固有安全性，以及更佳的防核扩散能力。2001 年成立的**第四代核能系统国际论坛**（Generation IV International Forum，GIF）把这些期待凝练为八条目标（可持续性、经济性、安全与可靠性、防扩散与实物保护），并在 2002 年的路线图中筛选出六类最有潜力的候选堆型。这就是今天我们通称的"第四代反应堆"。

实现这些目标的代价，是反应堆的工作环境全面超越现役轻水堆：

- **温度更高**：出口温度普遍 500–1000 ℃，热效率目标 43–50%（LWR 约 33%）；
- **冷却剂更苛刻**：液态金属、熔盐、超临界水或高温氦替代了普通水，腐蚀机理完全不同；
- **辐照剂量更深**：快中子堆的堆芯结构材料寿期内累积剂量可达 100–200 dpa，是轻水堆堆内构件的 10–20 倍。

这三重挑战构成了全书的主线。本章先勾勒六类堆型的工况轮廓，再归纳它们对结构材料的共性挑战，最后以"环境—材料—寿期"三角关系收束，为后续各章的深入讨论定坐标。

## 1.2　六类第四代候选堆型

GIF 在 2002 年从近百个概念中遴选出六类最具前景的候选堆型。2014 年路线图更新后，这六类被保留并重新评估。下表汇总了它们的主要工况参数。

| 堆型 | 冷却剂 | 中子能谱 | 出口温度（℃） | 工作压力（MPa） | 燃料循环 |
|---|---|---|---|---|---|
| VHTR 超高温堆 | 氦气 | 热中子 | 900–1000 | 7–15 | 开式 |
| GFR 气冷快堆 | 氦气 | 快中子 | 约 850 | 7–15 | 闭式 |
| SFR 钠冷快堆 | 液态钠 | 快中子 | 500–550 | 近大气压 | 闭式 |
| LFR 铅冷快堆 | 铅或铅铋 | 快中子 | 480–570（概念目标 800，尚无建成机组） | 近大气压 | 闭式 |
| MSR 熔盐堆 | 氟盐或氯盐 | 热中子或快中子 | 700–800 | 低压 | 闭式 |
| SCWR 超临界水冷堆 | 超临界水 | 热中子或快中子 | 510–625 | 约 25 | 开式或闭式 |

数据来源：GIF 2014 年技术路线图更新与 GIF 官方门户。这六类堆型并非齐头并进，研发优先级、工业成熟度差异显著，但它们共同界定了第四代堆结构材料的服役空间。

**钠冷快堆（SFR）** 是六类中最成熟的。液态钠在常压下沸点高达 883 ℃、热导率高（约 76 W/m·K），使得 SFR 可在低压下实现高功率密度与紧凑堆芯。俄罗斯别洛雅尔斯克 4 号机组 **BN-800**（电功率 880 MWe）一回路钠出口温度约 547 ℃，使用 MOX 燃料并于 2022 年完成全 MOX 堆芯装载，是目前在运功率最大的快堆。

**铅冷快堆（LFR）** 用液态铅或铅铋共晶（LBE，44.5Pb-55.5Bi，熔点约 124 ℃）作冷却剂。铅/铅铋化学惰性、低压运行，但密度大（约 10.5 g/cm³）带来流致冲击与腐蚀难题。俄罗斯正在西伯利亚化工联合企业建设 **BREST-OD-300** 铅冷示范堆（300 MWt），业界分析其投运时间已从原定 2026 年推迟至 2028–2029 年。

**熔盐堆（MSR）** 把燃料溶解或悬浮在熔盐中（液态燃料）或用熔盐仅作冷却剂（固态燃料，FHR 概念）。最具历史意义的是橡树岭国家实验室（ORNL）于 1965–1969 年运行的 **MSRE**（熔盐实验堆，7.4 MWt），其燃料盐为 LiF-BeF₂-ZrF₄-UF₄，运行温度约 650 ℃。当前正在推进的项目包括 TerraPower 在美国 INL 建设的 **MCRE**（世界首座快谱熔盐堆）、Kairos Power 的 **Hermes**（FLiBe 冷却高温堆）以及中科院上海应物所的 **TMSR-LF1**（2 MWt 液态燃料钍基熔盐堆，2023 年 10 月首次临界）。

**超临界水冷堆（SCWR）** 把水的工作参数推到临界点（374 ℃、22.1 MPa）以上，在约 25 MPa 下运行，出口温度 510–625 ℃，热效率目标 43–48%。代表性的概念有加拿大压力管式 SCWR（出口 625 ℃、效率 48%）、欧洲 HPLWR、日本 Super LWR 与中国 CSR1000。

**超高温堆（VHTR）** 与 **气冷快堆（GFR）** 共用氦冷剂。VHTR 出口温度可达 900–1000 ℃，主要用于高温工艺热与制氢；GFR 用氦冷快谱堆芯实现闭式燃料循环。中国山东石岛湾的 **HTR-PM**（球床模块式高温气冷堆，电功率 200 MWe，出口 750 ℃）于 2023 年 12 月投入商业运行，被誉为世界首个进入商运的第四代反应堆。

## 1.3　结构材料的共性挑战

尽管六类堆型的冷却剂、能谱与温度各不相同，它们对结构材料提出了三重叠加的共性挑战。把这三重挑战放在同一张图上，就能理解为什么第四代堆的材料研发会持续二十年仍未完成——任何一类候选材料都必须同时在这三个维度上达标。

**高温挑战**　第四代堆的运行温度区间为 500–1000 ℃，远超现役 LWR 的 300 ℃。在 500 ℃ 以上，奥氏体不锈钢和铁素体-马氏体钢都会出现显著的**时间相关蠕变**：在恒定应力下，材料随时间缓慢变形并最终断裂。蠕变断裂强度随温度呈指数下降，温度每升高 50 ℃，10⁵ 小时的蠕变断裂应力往往下降 30–50%。因此 ASME 锅炉与压力容器规范（BPVC）专门为高温服役设立了第 III 卷第 5 分卷（Section III Division 5），用许用应力曲线与时变损伤评估程序来约束设计。

**腐蚀挑战**　液态金属、熔盐、超临界水和高温含杂质氦，每一种介质都有自己独特的腐蚀机理：液态金属中的元素选择性溶解与质量迁移；熔盐中由氧化还原电位驱动的 Cr 选择性浸出；超临界水中由介电常数骤变带来的从离子化学到自由基化学的转变；高温氦气中由 ppm 量级杂质比例决定的氧化/渗碳/脱碳平衡。第 2–5 章将分别深入这些机理。

**辐照挑战**　快中子堆的堆芯结构材料要在寿期内承受 100–200 dpa 的累积位移损伤（部分高注量部件的目标值），远超 LWR 堆内构件的 10 dpa 量级。辐照会带来硬化与脆化、辐照肿胀、辐照蠕变、辐照诱发偏析（RIS）与析出（RIP）等一系列效应，每一种都会削弱材料的服役裕度。IAEA 与 INL 的综合评估表明，第四代堆结构材料面临的典型辐照条件是"在 500–1000 ℃ 下累积 30–100 dpa"。

## 1.4　"环境—材料—寿期"的分析框架

把上述三重挑战抽象成一个三角关系，就得到了贯穿全书的分析框架：

- **环境（Environment）**：冷却剂化学、温度、压力、辐照谱——这是材料必须承受的输入；
- **材料（Material）**：化学成分、微观组织、加工状态——这是设计师可以调节的变量；
- **寿期（Lifetime）**：在给定环境下特定材料能维持设计裕度的时间或剂量——这是输出的约束。

后续每一章都可以套进这个框架。例如第 2 章研究液态钠环境对 316 不锈钢的腐蚀，第 7 章讨论辐照如何改变奥氏体钢的微观组织，第 9 章讨论铁素体-马氏体钢如何把肿胀阈值从奥氏体钢的 50 dpa 推高到 150 dpa 以上。读者若能把每一章定位在这个三角上，就能形成系统而非碎片化的理解。

第四代堆的工程化仍在推进中。GIF 的三阶段框架（可行性 → 性能 → 示范）预期某些设计在 2030 年起进入商业化部署。对中国读者而言，HTR-PM 已率先示范了球床高温堆技术，TMSR-LF1 验证了钍基液态燃料熔盐路线，CFR600 钠冷快堆正在建设中。这些示范项目不仅验证了系统设计，也在持续检验结构材料数据库的完备程度。

## 1.5　小结

第四代反应堆用更高的温度、更苛刻的冷却剂和更深的辐照剂量，换取更高的热效率、更深的燃耗和更少的废物。代价是结构材料必须在"高温—腐蚀—辐照"三重叠加的服役窗口中长期保持设计裕度。本章建立的三重挑战框架与"环境—材料—寿期"分析视角，将贯穿后续 17 章。第二至五章聚焦腐蚀环境，第六至七章聚焦力学与辐照，第八至十八章逐类讨论候选材料体系。

## 参考文献

1. Generation IV International Forum. *Technology Roadmap Update for Generation IV Nuclear Energy Systems*. GIF, 2014. https://www.gen-4.org/resources/reports/technology-roadmap-update-generation-iv-nuclear-energy-systems-gif-2014
2. Generation IV International Forum. *R&D Outlook for Generation IV Nuclear Energy Systems, 2018 Update*. GIF, 2018. https://www.gen-4.org/gif/upload/docs/application/pdf/2021-11/gif_rd_outlook_for_generation_iv_nuclear_energy_systems__2018_update_new_cover.pdf
3. Generation IV International Forum. Generation IV Criteria and Technologies Portal. https://www.gen-4.org/generation-iv-criteria-and-technologies
4. World Nuclear Association. *Generation IV Nuclear Reactors*. https://world-nuclear.org/information-library/nuclear-power-reactors/other/generation-iv-nuclear-reactors
5. Aitkaliyeva A., et al. *Irradiation Effects in Generation IV Nuclear Reactor Materials*. INL, 2017. https://inldigitallibrary.inl.gov/sites/sti/sti/Sort_7379.pdf
6. IAEA. *Development of Radiation Resistant Reactor Core Structural Materials*. GC51INF-3. https://www.iaea.org/sites/default/files/gc/gc51inf-3-att7_en.pdf
7. Zinkle S. J., Busby J. T. Structural materials for fission & fusion energy. *Materials Today*, 2009, 12(11): 12–19. https://www.sciencedirect.com/science/article/pii/S1369702109702949
8. Wikipedia. *HTR-PM*. https://en.wikipedia.org/wiki/HTR-PM
9. Wikipedia. *BN-800 reactor*. https://en.wikipedia.org/wiki/BN-800_reactor
10. Wikipedia. *Molten-Salt Reactor Experiment*. https://en.wikipedia.org/wiki/Molten-Salt_Reactor_Experiment
11. Wikipedia. *TMSR-LF1*. https://en.wikipedia.org/wiki/TMSR-LF1
