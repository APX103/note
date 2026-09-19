# 第 5 章　熔盐引起的腐蚀

> **核心命题**　熔盐堆中的腐蚀不是电化学驱动的氧化还原，而是由盐的氧化还原电位（Redox）直接驱动——UF₄ 把合金中的 Cr 选择性氧化溶解为 CrF₂。控制 U(IV)/U(III) 比率、净化含氧杂质、研发抗 Cr 浸出的新一代 Ni 基合金，是熔盐堆结构材料合格化的三大支柱。

---

## 5.1　熔盐堆的两条技术路线

熔盐堆（MSR）在 GIF 六类候选堆型中是化学最复杂的一类。它沿两条技术路线发展：

- **液态燃料 MSR**：把裂变燃料溶解在熔盐中，熔盐既是燃料载体又是冷却剂。鼻祖是 ORNL 于 1965–1969 年运行的 **MSRE**（Molten Salt Reactor Experiment，热功率 7.4 MWt），其燃料盐为 LiF-BeF₂-ZrF₄-UF₄ = 65-29.1-5-0.9 mol%，运行温度约 650 ℃，累计等效满功率运行 11555 小时。
- **固态燃料/氟盐冷却（FHR）**：使用 TRISO 等固态燃料，熔盐仅作冷却剂。代表是 Kairos Power 的 KP-FHR（Hermes 示范堆正在田纳西州 Oak Ridge 建设），采用低压 FLiBe（2LiF-BeF₂）冷却剂。

当前正在推进的项目还包括 TerraPower 在美国 INL 建设的 **MCRE**（世界首座快谱熔盐堆，氯盐燃料）、Moltex 的 SSR-W（使用回收乏燃料）、Flibe Energy 的 LFTR（钍基液态燃料），以及中科院上海应物所的 **TMSR** 项目（TMSR-LF1 已于 2023 年 10 月首次临界，并于 2024 年实现钍—铀转换）。

## 5.2　关键熔盐体系

不同的盐体系在熔点、热稳定性、腐蚀性、中子学等方面各有取舍：

| 盐体系 | 组成（mol%） | 熔点（℃） | 沸点（℃） | 主要用途 |
|---|---|---|---|---|
| FLiBe | 67LiF-33BeF₂ | 459 | 约 1430 | MSR 一回路、FHR 冷却剂 |
| FLiBe（共晶） | BeF₂ 略 >50% | 360 | 约 1430 | 实验研究 |
| FLiNaK | 46.5LiF-11.5NaF-42KF | 454 | 约 1570 | FHR 候选、腐蚀研究 |
| NaF-ZrF₄ | 59.5-40.5 | 约 500 | >1350 | 锆基燃料循环 |
| NaCl-KCl-UCl₃/₄ | — | — | — | 快谱 MSR（MCRE） |

**FLiBe**（66.7LiF-33.3BeF₂，形成化合物 Li₂BeF₄）是 MSRE 二回路冷却盐采用的体系。熔点 459 ℃，密度约 1.94 g/cm³。由于天然 Li 中 ⁶Li（约 7.5%）吸收中子生成 α + **氚（T）**，需用 **⁷Li 富集**；MSRE 二回路冷却盐使用 99.993% ⁷Li 的 FLiBe（Romatoski & Hu, *Ann. Nucl. Energy*, 2017，被引 230+）。

**FLiNaK**（46.5-11.5-42）熔点 454 ℃（实验测定的真实共晶温度；部分文献给出 462 ℃），沸点约 1570 ℃。优点是高体积热容、合理热导、低蒸气压、高温稳定，常用于 FHR 冷却剂候选及实验室腐蚀研究（Frandsen et al., *J. Nucl. Mater.*, 2020；Sohal et al., INL/EXT-10-18297，被引 534+）。

**氯盐体系**（如 NaCl-KCl-UCl₃/UCl₄、NaCl-MgCl₂）用于快谱 MSR。Ai 等人（上海应物所，*Nucl. Sci. Tech.*, 2023，被引 22）系统测试了 316H 在不纯 NaCl-KCl-MgCl₂ 中 1000 小时腐蚀深度达约 130 μm，并发生严重沿晶腐蚀；不同氯盐腐蚀性强弱排序为 NaCl-KCl < NaCl-MgCl₂ ≈ NaCl-KCl-MgCl₂。

## 5.3　腐蚀驱动力与 Redox 控制

熔盐腐蚀的核心驱动力与液态金属或超临界水都不同——它是**热力学氧化还原驱动**的，由盐的氧化还原电位直接决定。

### 5.3.1　Cr 的选择性溶解

在所有候选结构材料中，**Cr 是被熔盐选择性浸出的关键元素**（Cr → CrF₂ 溶解）。UF₄ 将合金表面 Cr 氧化溶解：

```
Cr (s) + 2 UF₄ ⇌ CrF₂ + 2 UF₃
```

因此 **U(IV)/U(III) 比率**（即 [UF₄]/[UF₃]）是控制氧化电位/腐蚀驱动力的核心参数。Chan（*npj Mater. Degrad.*, 2022，被引 44；*J. Electrochem. Soc.*, 2023）在 FLiNaK 中系统研究了 Cr 的腐蚀热力学与电化学行为。

### 5.3.2　Redox 控制的临界阈值

Surenkov 等人（*EPJ Nucl. Sci. Technol.*, 2020，被引 18）给出了关键阈值：当 **[U(IV)]/[U(III)] < 30–40** 时（温度至 760 ℃），可将选择性 Cr 腐蚀降至可接受水平。

Te 致沿晶开裂（IGC）同样受该比率控制，具体数据如下：

- 比率 = 42、760 ℃：金属学检查无 IGC，表面 Cr 降至 3.5 wt%；
- 比率 = 60、760 ℃：出现强 IGC；
- 比率 = 85、780–800 ℃：最大裂纹深度 Lmax = 148 μm，表面 Cr 降至 1.7 wt%；800 ℃、比率 85 的腐蚀失重速率比 760 ℃、比率 42 高 2 倍以上。

ORNL 在 MSRE 后续检查中发现裂变产物 Te 沿晶界形成深度 100–250 μm 的微裂纹——这是历史上首次揭示的 Te 致开裂现象。

### 5.3.3　盐化学净化：HF/H₂ 氢氟化

含氧杂质（氧化物、水分）会显著加剧腐蚀，必须通过**氢氟化法**（H₂–HF 方法）去除：典型流程向熔盐中鼓泡通入 HF/H₂ 混合气，HF 还原氧化物和金属杂质（Zhang et al., *Corrosion Science*, 2018，被引 272；Kelleher et al., ASME, 2015）。净化后残留的溶解 HF 会设定不希望的氧化还原电位，需后续 H₂ 鼓泡 + 过滤调整。FLiBe 体系中常通过添加 **Be 金属** 控制氧化还原电位（Be 与 NiF₂、FeF₂ 反应生成稳定 BeF₂）。

## 5.4　Hastelloy N 与新一代 Ni 基合金

### 5.4.1　Hastelloy N 的诞生与局限

Hastelloy N（UNS N10003，标准成分 **Ni-16Mo-7Cr-5Fe**，另含约 0.5% Si、约 0.05% C）由 ORNL 为 MSRE 专门开发（McCoy, ORNL-TM-5920, 1978，被引 129）。MSRE 中所有与盐接触的金属部件均由 Hastelloy N 制造。Mo 提供抗氟盐腐蚀能力。

但 MSRE 运行暴露了 Hastelloy N 的两大缺陷：**(1) 辐照致脆**、**(2) Te 致沿晶开裂**。Te 沿晶界扩散生成不稳定碲化物相（Ni₃Te₂、CrTe、MoTe₂），扩散深度约 50 μm，导致开裂（Cheng et al., *J. Nucl. Mater.*, 2015，被引 48；Chu et al., *Nucl. Sci. Tech.*, 2017）。

### 5.4.2　中国 GH3535

中国 TMSR 项目对应牌号 **GH3535**（Ni-16Mo-7Cr-4Fe）正在研究添加 La（镧）等元素以降低 Te 扩散深度、改善抗沿晶开裂能力。

### 5.4.3　SiC/SiC 陶瓷与新方向

CVD 单晶 SiC 在氟盐中呈相对均匀、低速率腐蚀；但 CVI SiC_f/SiC 复合材料呈非均匀腐蚀——这是陶瓷复合材料的关注点（Lee et al., 2019，被引 42；Koyanagi et al., *Corrosion Science*, 2023）。

新一代合金方向包括 **Ni-20Cr** 模型合金、**Ni-20Cr-18W** 高温抗热腐蚀合金等。2025 年最新研究发现，Ni-20Cr 在质子辐照下沿晶腐蚀反而被延缓（辐照—腐蚀协同效应）——这对核 MSR 结构材料具有重要意义（Zhou et al., 2020，被引 150；Bawane et al., 2021，被引 45）。

## 5.5　小结

熔盐腐蚀由盐的氧化还原电位直接驱动，Cr 的选择性溶解是主因。把 [U(IV)]/[U(III)] 比率控制在 <30–40 是抑制 Cr 浸出与 Te 致开裂的关键。Hastelloy N 是历史上唯一经过反应堆辐照验证的熔盐结构材料，但 Te 致沿晶开裂与辐照致脆是其根本局限。新一代 Ni-Cr-W 合金、GH3535 改进型与 SiC/SiC 陶瓷正在多个国家实验室评估中。氯盐快谱熔盐堆的腐蚀挑战比氟盐更严苛，316H 等常规奥氏体钢在氯盐中腐蚀深度可达 130 μm/1000h。

## 参考文献

1. McCoy H. E. *Status of Materials Development for Molten Salt Reactors*. ORNL-TM-5920, 1978. https://moltensalt.org/references/static/downloads/pdf/ORNL-TM-5920.pdf
2. ORNL. *MSRE Design and Operations Report (ORNL-4396)*. https://moltensalt.org/references/static/downloads/pdf/ORNL-4396.pdf
3. Romatoski R. R., Hu L. W. Fluoride salt coolant properties for nuclear reactor applications: A review. *Annals of Nuclear Energy*, 2017. https://www.sciencedirect.com/science/article/am/pii/S0306454917301391
4. Sohal M. S., et al. *Engineering Database of Fluoride Salt (FLiNaK) Properties*. INL/EXT-10-18297, 2013. https://inldigitallibrary.inl.gov/sites/sti/sti/5698704.pdf
5. Williams D. F. *Assessment of Candidate Molten Salt Coolants for the AHTR*. ORNL/TM-2006-12, 2006. https://moltensalt.org/references/static/downloads/pdf/ORNL-TM-2006-12.pdf
6. Ai H., et al. Corrosion of 316H in molten chloride salts. *Nuclear Science and Techniques*, 2023, 34: 191. https://ui.adsabs.harvard.edu/abs/2023NuScT..34..191A/abstract
7. Chan J. Thermodynamics of chromium corrosion in molten FLiNaK. *npj Materials Degradation*, 2022. https://www.nature.com/articles/s41529-022-00251-3
8. Surenkov A. L., et al. Corrosion of Hastelloy N in molten salts under controlled redox. *EPJ Nuclear Sciences & Technologies*, 2020. https://www.epj-n.org/articles/epjn/full_html/2020/01/epjn190003/epjn190003.html
9. Zhang J. A review of steel corrosion in molten fluoride salts. *Corrosion Science*, 2018. https://www.sciencedirect.com/science/article/am/pii/S0010938X18307078
10. Cheng W., et al. Tellurium embrittlement of Ni-16Mo-7Cr alloy. *Journal of Nuclear Materials*, 2015. https://www.sciencedirect.com/science/article/abs/pii/S0022311515000641
11. Chu S., et al. Tellurium diffusion in Ni-16Mo-7Cr-4Fe. *Nuclear Science and Techniques*, 2017. https://link.springer.com/article/10.1007/s41365-017-0330-8
12. Lee J. J., et al. *Materials compatibility of SiC and FHR fluoride salts*. OSTI, 2019. https://www.osti.gov/servlets/purl/1531263
13. Koyanagi T., et al. *Single crystal SiC corrosion in Be-containing fluoride salt*. *Corrosion Science*, 2023. https://www.sciencedirect.com/science/article/abs/pii/S0010938X23003438
14. Zhou W., et al. *Proton irradiation delays intergranular corrosion of Ni-20Cr*. eScholarship, 2020. https://escholarship.org/content/qt0jb47414/qt0jb47414_noSplash_49f3e21d49ff468c463998b74034d0d5.pdf
15. Wikipedia. *Molten-Salt Reactor Experiment*. https://en.wikipedia.org/wiki/Molten-Salt_Reactor_Experiment
16. Wikipedia. *TMSR (Chinese reactor project)*. https://en.wikipedia.org/wiki/TMSR_(Chinese_reactor_project)
