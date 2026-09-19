# 第 9 章　SMR 防扩散和实物保护

> **核心命题**　PR&PP（Proliferation Resistance and Physical Protection）评估是衡量反应堆"3S"安全中安保与保障监督维度的重要方法。SMR 在"少人值守 + 长换料周期 + 整体回收"等特征下，对 PR&PP 提出新的评估框架。

---

## 9.1　引言

核能的扩散风险（proliferation）和实物保护（physical protection）一直是国际核能治理的核心议题。IAEA 提出 **PR&PP 评估方法学**作为对反应堆设计进行系统评估的工具。SMR 因其紧凑性、可能的"少人值守"、模块化运输、长换料周期、海上部署等特点，PR&PP 评估与传统大型核电站有显著差异：

- 一次装入堆芯的核材料量少，但**比功率高、富集度高（部分先进 SMR 用 HALEU 或 HALEU+）**；
- 多模块厂址 + 整体运输增加运输路径上的安保风险；
- 海上 / 海外部署涉及**国际保障监督（safeguards）**的复杂性；
- 长换料周期（> 5 年）意味着核查频率低，核查技术需革新。

## 9.2　分析方法

PR&PP 评估方法学由 IAEA 和 GEN-IV 国际论坛（GIF）联合开发，是结构化、可追溯的评估框架。

### 9.2.1　PR（防扩散）评估要素

- **核材料特征**：核材料吸引力级别（MAGAT、LEU、HEU、Pu 等）；
- **固有 PR 特征**：反应堆设计本身减少吸引力、提高获取难度；
- **外在 PR 措施**：保障监督、物质保护、出口管制；
- **威胁场景**：国家型扩散威胁（State Level）、非国家型威胁（NSN）。

### 9.2.2　PP（实物保护）评估要素

- **设计基准威胁（DBT）**：武装袭击、爆炸、网络、内部威胁；
- **目标识别**：核材料、关键设备、辐射源；
- **物理保护系统**：探测、延迟、响应；
- **后果评估**：辐射释放、社会影响。

### 9.2.3　评估方法

```
[识别威胁] → [识别目标] → [设计攻击路径] 
       → [计算路径指标（时间、检测概率、所需专业知识）] 
       → [评估后果] → [设计改进]
```

通常用以下指标：

- ** proliferation time**：完成核材料分离所需时间；
- **detection probability**：被发现的概率；
- **material quantity**：可获取的核材料量。

## 9.3　系统响应和结果

### 9.3.1　典型 SMR 的 PR 评估结果

- **轻水 SMR（NuScale、ACP100）**：核材料与传统 PWR 相同（LEU），固有 PR 与大型 PWR 相当；长换料周期和整体运输增强 PR。
- **气冷 SMR（HTR-PM、Xe-100）**：TRISO 燃料难以后处理（颗粒坚硬、需破碎），PR 较高；但燃耗深，钚同位素组成（²⁴⁰Pu 比例）影响 Pu 吸引力。
- **液态金属快堆**：闭式燃料循环涉及 Pu 分离，PR 较低；需配套先进后处理（如 PUREX 替代方案、UREX+、GANEX）。
- **熔盐堆**：在线化学处理增加扩散风险；需设计防止分离。

### 9.3.2　典型 SMR 的 PP 评估结果

- **陆基地下 SMR**：物理保护优于地上电站；
- **海上 SMR**：海上环境复杂，海盗、撞击、潜艇干扰都是新威胁；
- **可移动 SMR**：运输路径上的安保风险最高，需全程护卫；
- **远程 / 无人值守 SMR**：内部威胁降低，但网络攻击风险上升。

### 9.3.3　SMR 的 PR&PP 优势与劣势

| 优势 | 劣势 |
|---|---|
| 单堆核材料量少 | 多机组叠加后总量可观 |
| 整体回收、现场不留乏燃料 | 运输路径暴露 |
| 长换料周期减少核查中断 | 长周期核查技术不成熟 |
| 部分先进燃料（TRISO、金属合金）难后处理 | 闭式燃料循环（液态金属堆）涉及 Pu 分离 |
| 地下、模块化设计 PP 好 | 海上、移动式 PP 难 |

## 9.4　第四代核能系统国际论坛（GIF）评估步骤

GIF（Generation IV International Forum）把 PR&PP 作为评价六种第四代反应堆（GFR、LFR、MSR、SFR、SCWR、VHTR）的关键指标之一。评估步骤如下：

1. **威胁定义**：基于 GIF PR&PP 方法论（白皮书）；
2. **目标识别**：识别所有可被攻击 / 利用为扩散的核材料、设备、信息；
3. **路径识别**：列出潜在攻击 / 扩散路径；
4. **指标计算**：对每条路径计算时间、检测、专业度、成本；
5. **方案对比**：不同设计或运行模式对比；
6. **设计改进**：反馈到设计；
7. **迭代**：与设计周期同步迭代。

## 9.5　PR&PP 经验总结

从过去 20 年评估实践，可总结：

1. **没有"绝对不扩散"的设计**，但通过设计 + 外在措施可显著降低风险；
2. **固有 PR 比外在 PR 更稳健**（不易被绕过）；
3. **整堆更换 + 整体运输**是 SMR 提升 PR/PP 的关键技术路径，但要解决运输安保；
4. **国际保障监督技术**需要为 SMR 专门研发（远程核查、连续监测、加密通信）；
5. **核材料衡算（Material Accountancy）**对长换料周期堆（5–20 年）有挑战，需"基于过程"而非"基于库存"的新方法；
6. **跨学科团队**（核工程、保障监督、安保、政策）的协作是 PR&PP 评估成功的关键。

## 9.6　未来趋势

1. **数字保障监督**：基于 IoT、区块链、AI 的连续核查；
2. **小批量核查技术**：中子多重性、γ 谱、热量计 + 改进算法；
3. **可机读核材料标签**：基于物理不可克隆函数（PUF）；
4. **海上 SMR 国际公约**：类似 MARPOL，规范海上核安全、保障监督、安保；
5. **核燃料银行**：IAEA 推动低浓铀燃料银行（LEU Bank）为 SMR 提供燃料供应安全；
6. **新型燃料形式**：TRISO、金属合金、氮化物、硅化物燃料继续提升 PR；
7. **AI 用于安保**：异常检测、视频分析、行为识别。

## 9.7　信息来源和建议

- IAEA *International Nuclear Safeguards*（Safeguards Implementation Report）年度报告；
- GIF PR&PP 工作组白皮书（Revised Approach to Proliferation Resistance and Physical Protection Assessment*，2018）；
- OECD/NEA 报告 *Proliferation Resistance and Physical Protection*；
- 国际核保障监督暑期学校（INSSS）、IAEA Safeguards Traineeship；
- 各国监管机构公开的 PR&PP 评估报告。

## 9.8　参考文献

1. GIF. *Evaluation Methodology for Proliferation Resistance and Physical Protection of Generation IV Nuclear Energy Systems*, Rev. 6, 2018.
2. IAEA. *International Target Values 2010 for Measurement Uncertainties in Safeguarding Nuclear Materials*.
3. Charlton W. S. et al. "Proliferation Resistance Assessment Methodology." *Nucl. Tech.*, 2007.
4. Bari R. et al. "PR&PP Evaluations of Sodium-Cooled Fast Reactors." *Nucl. Tech.*, 2009.
5. Whitlock J. J. et al. "SMR Proliferation Resistance." *Trans. ANS*, 2013.
6. IAEA. *Safeguards Implementation Report* (SIR), 年度。
7. NNSA. *Proliferation Resistance Assessment*. NNSA Office of Nonproliferation and Arms Control.
8. Zentner M. D. et al. "Proliferation Resistance Methodology." PNNL, 2009.
