# 永磁同步电机控制技术

> **核心命题**　PMSM 的磁场定向控制（FOC）做了一件事：换坐标系。Clarke 变换把三相交流降维成两相静止量，Park 变换再跟着转子旋转，于是"控制三个错相的正弦波"变成"控制两个直流量"——两个 PI 电流环的故事。执行端由 SVPWM 用八个离散电压矢量"平均出"任意目标矢量。本章从几何直觉讲到可落地的公式与框图，是第 7 章所有 SDK 配置项的理论出处。

---

## 三相 PMSM 的结构

永磁同步电机与 BLDC 在结构上是近亲：定子三相绕组、转子永磁体，区别在**绕组设计目标**——PMSM 追求**正弦反电动势**，BLDC 追求梯形反电动势。GBM2804H-100T 这类云台电机的反电动势正弦度相当好，当 BLDC 用（方波）或当 PMSM 用（正弦）都行，正好一鱼两吃。

按转子磁路分两类：

- **表贴式（SPM）**：磁铁贴在转子表面，交直轴电感近似相等（$L_d = L_q$），转矩严格正比于 $i_q$——本书电机与大多数云台/无人机电机都是这类，控制最简单；
- **内嵌式（IPM）**：磁铁埋入转子铁芯，$L_q > L_d$，除永磁转矩外还有磁阻转矩，高速弱磁性能好，控制要精细得多（利用 $L_d \ne L_q$ 的转矩公式），本书不展开。

## 三相 PMSM 的数学模型

### 三相 PMSM 的坐标变换

**为什么变**：三相电流是三个时间上错开 120° 的正弦量，直接闭环控制它们，控制器必须在每个瞬间同时算三笔相位相关的账。坐标变换的洞见：三个正弦量其实是同一个旋转矢量在三个轴上的投影——**控制一个矢量，比控制三个正弦量干净**。

三个坐标系的几何关系是本章的"地图"（图 6.1）：

- **abc 系**：三相静止轴，互差 120°（电角），A 相轴与 α 轴重合；
- **αβ 系**：两相静止轴，α 对齐 A 相轴，β 超前 90°——Clarke 变换的目的地；
- **dq 系**：两相旋转轴，d 轴对准转子磁场（永磁体磁链方向），q 轴超前 90°——Park 变换的目的地，FOC 的作战地图。

![坐标系与矢量图：同一个定子电流矢量，在 abc 三相轴、αβ 静止轴、dq 旋转轴上各有投影；θe 为转子电角，FOC 的目标是让电流矢量始终贴着 q 轴（γ = 90°）](images/fig_06_frames.pdf)

**Clarke 变换**（abc $\rightarrow$ αβ，等幅值形式）：

$$i_\alpha = \frac{2}{3}\Big(i_a - \frac{1}{2} i_b - \frac{1}{2} i_c\Big), \qquad i_\beta = \frac{2}{3}\Big(\frac{\sqrt{3}}{2} i_b - \frac{\sqrt{3}}{2} i_c\Big)$$

工程上常用"采两相"版本（$i_c = -i_a - i_b$ 代入）：

$$i_\alpha = i_a, \qquad i_\beta = \frac{i_a + 2 i_b}{\sqrt{3}}$$

**Park 变换**（αβ $\rightarrow$ dq）：

$$\begin{cases} i_d = \;\;\, i_\alpha \cos\theta_e + i_\beta \sin\theta_e \\ i_q = -\, i_\alpha \sin\theta_e + i_\beta \cos\theta_e \end{cases}$$

**反 Park 变换**（dq $\rightarrow$ αβ）：

$$v_\alpha = v_d \cos\theta_e - v_q \sin\theta_e, \qquad v_\beta = v_d \sin\theta_e + v_q \cos\theta_e$$

整个 FOC 只需要一对 $\sin\theta_e / \cos\theta_e$——这正是第 1 章 CORDIC 协处理器登场的地方。

### 同步旋转坐标系（d-q 坐标系）下的数学模型

站在随转子旋转的 dq 系里看，所有正弦量都静止了，电压方程变成两个**直流量**的方程（SPM，$L_d = L_q = L_s$）：

$$\begin{cases} v_d = R_s i_d + L_s \dfrac{\mathrm{d}i_d}{\mathrm{d}t} - \omega_e L_s i_q \\[6pt] v_q = R_s i_q + L_s \dfrac{\mathrm{d}i_q}{\mathrm{d}t} + \omega_e L_s i_d + \underbrace{\omega_e \lambda_f}_{\text{反电动势}} \end{cases}$$

- $\omega_e$ 为电角速度（$\omega_e = p \omega_m$），$\lambda_f$ 为转子磁链；
- $\omega_e L_s i$ 项是**交叉耦合**：转速越高，d/q 两轴通过电感互相串扰越强；
- $\omega_e \lambda_f$ 项就是反电动势在 q 轴上的化身。

**转矩方程**（SPM）：

$$T_e = \frac{3}{2} p \, \lambda_f \, i_q$$

只由 $i_q$ 决定！这就是 FOC 的操作指南：**把 $i_d$ 压到零（不励磁不浪费），用 $i_q$ 当转矩旋钮**。速度环的输出就是 $i_q$ 指令，力矩控制退化为直流量控制——FOC 把 PMSM 变成了一台"解耦的直流电机"。

### 静止坐标系（α-β 坐标系）下的数学模型

不做 Park 变换、直接在两相静止系建模（无感观测器喜欢在这里工作，因为不需要转子角度）：

$$\begin{cases} v_\alpha = R_s i_\alpha + L_s \dfrac{\mathrm{d}i_\alpha}{\mathrm{d}t} + e_\alpha \\[4pt] v_\beta = R_s i_\alpha + L_s \dfrac{\mathrm{d}i_\beta}{\mathrm{d}t} + e_\beta \end{cases}$$

反电动势两个分量 $e_\alpha = -\omega_e \lambda_f \sin\theta_e$、$e_\beta = \omega_e \lambda_f \cos\theta_e$——**藏着转子的角度信息**。STO 观测器（7.1 节）的原理就是：由已知的 $v_{\alpha\beta}$、测得的 $i_{\alpha\beta}$ 和电机参数 $R_s$、$L_s$ 反解出 $e_{\alpha\beta}$，再 $\theta_e = \mathrm{atan2}(-e_\alpha, e_\beta)$ 拿到转子角。无感 FOC 的全部魔法就这一段。

### 用传统测量方法获取电机参数

没有 Motor Profiler 的年代，参数靠仪器（现在仍是校验工具的好方法）：

| 参数 | 传统方法 | 要点 |
| --- | --- | --- |
| 相电阻 $R_s$ | 万用表 / 电桥测线电阻 | 星接：线电阻 = 2 倍相电阻，除 2 |
| 相电感 $L_s$ | LCR 表测线电感（1 kHz 挡） | 同上除 2；位置不同读数略异取均值 |
| 磁链 $\lambda_f$ | 外部原动机拖动电机，示波器测开路线电压峰值 $U_{pk}$ | $\lambda_f = U_{pk} / (\sqrt{3} \, \omega_e)$（线反电动势峰值换算） |
| 极对数 $p$ | 数磁铁 / 感受每次全转的磁阻卡点数 | $p$ = 卡点数；或手动转一圈数霍尔脉冲数除 12 |

### ST-MC-SDK Motor Profiler 测量电机参数的原理

Motor Profiler（3.6.3 节的操作）每一步都严格对应 6.2 节模型的一项：

1. **测 $R_s$**：注入小幅直流电压矢量（转子静止），稳态时电感项为零、反电动势为零，$R_s = V / I$；
2. **测 $L_s$**：观察施加电压矢量初期电流的上升斜率，$\mathrm{d}i/\mathrm{d}t = (V - R_s i)/L_s$，拟合出 $L_s$；
3. **测 $\lambda_f$ 与 $p$**：以已知电压矢量开环拖动电机旋转，稳态下从电压方程扣除 $R_s i$ 与 $L_s\,\mathrm{d}i/\mathrm{d}t$，剩下的就是反电动势项 $\omega_e \lambda_f$；由指令频率与实测转速的关系同时校出 $p$；
4. **测 $J$、$B$**：撤去驱动让电机自由减速，$\mathrm{d}\omega/\mathrm{d}t = -(T_L + B\omega)/J$，由减速曲线拟合。

所以 Profiler 不是黑魔法，而是把 5.2 节的方程逐项反解的自动化脚本——输出的每个数都能用手动方法复核。

## SVPWM 控制技术

### 三相电压的空间矢量表示

反 Park 变换给出了目标电压 $(v_\alpha, v_\beta)$——一个在 αβ 平面上旋转的矢量。但三相逆变桥只有 8 种开关状态（三个上管的开/关组合），只能输出 8 个离散的电压矢量：6 个**有效矢量** $\vec{V}_1 \ldots \vec{V}_6$（幅值 $2V_{dc}/3$，方向互差 60°，对应 100/110/010/011/001/101）和 2 个**零矢量** $\vec{V}_0(000)$、$\vec{V}_7(111)$（三相短接到同一点，输出电压为零）。

![SVPWM 空间矢量图：六个有效矢量构成正六边形，六个扇区 I ~ VI；目标矢量在扇区 I 内由相邻矢量按 T1/T2 时间加权合成；虚线圆为线性区边界](images/fig_06_svpwm_hex.pdf)

### SVPWM 算法的合成原理

**核心思想**：在一个 PWM 周期 $T$ 内，用相邻两个有效矢量加零矢量按时间加权"平均出"目标矢量（设目标矢量落在扇区 I，相邻矢量为 $\vec{V}_1$、$\vec{V}_2$）：

$$\vec{U}_{ref} \, T = \vec{V}_1 T_1 + \vec{V}_2 T_2 + \vec{V}_{0/7} T_0, \qquad T_1 + T_2 + T_0 = T$$

由平行四边形法则解出（$\theta$ 为矢量在本扇区内偏离 $\vec{V}_1$ 的角度，$|\vec{U}_{ref}| = U$）：

$$T_1 = \frac{\sqrt{3} \, U \, T}{V_{dc}} \sin(60° - \theta), \qquad T_2 = \frac{\sqrt{3} \, U \, T}{V_{dc}} \sin\theta$$

**七段式排布**：把 $T_1$、$T_2$ 对半拆开对称放置，零矢量分到两端与中央（000-100-110-111-110-100-000），使一个周期内开关次数最少、谐波最小：

![七段式 SVPWM 一个 PWM 周期内的三相上管门极信号（扇区 I 情形）：A 相最宽、B/C 相居中对称，中央对齐排布](images/fig_06_svpwm_7seg.png)

**线性区与母线利用率**：六边形内切圆半径 $V_{dc}/\sqrt{3}$ 是线性调制上限，比正弦 PWM（SPWM）的 $V_{dc}/2$ 高出 $2/\sqrt{3} \approx 1.155$ 倍——同样母线电压多出约 15\% 的电压利用率，这是 SVPWM 在电机驱动中一统江湖的直接原因。从调制波形看，SVPWM 等效于在正弦参考上叠加零序分量，形成"马鞍波"：

![SPWM 与 SVPWM 调制波对比：SVPWM 的马鞍波峰值可达 2Vdc/3（比 SPWM 高 15\%），意味着同样的相电流能力下母线电压利用更充分](images/fig_06_spwm_vs_svpwm.png)

### SVPWM 算法的实现

教科书流程（判扇区 $\rightarrow$ 套 $T_1/T_2$ 公式 $\rightarrow$ 七段排布）分支多；嵌入式实现的标准姿势是数学等价的**最小最大值注入法（min-max injection）**——无分支、四次乘法完事：

$$\begin{cases} V_a = v_\alpha \\[2pt] V_b = \dfrac{-v_\alpha + \sqrt{3}\, v_\beta}{2} \\[4pt] V_c = \dfrac{-v_\alpha - \sqrt{3}\, v_\beta}{2} \end{cases} \qquad V_{off} = -\frac{\max(V_a, V_b, V_c) + \min(V_a, V_b, V_c)}{2}$$

$$\mathrm{duty}_x = \frac{1}{2} + \frac{V_x + V_{off}}{V_{dc}} \quad (x = a, b, c)$$

`duty_x` 直接写入 TIM1 三个通道的 CCR 寄存器。三行代码的物理含义：三相调制波的共模平移（注入 $V_{off}$）不改变线电压，却把波形中心拉回 PWM 的线性范围中央——这正是七段式的代数化身。

## 三相永磁同步电机的矢量控制

### PMSM 矢量控制基本原理

把 6.2 的模型与 6.3 的执行器组装起来，就是完整的 FOC 控制框图（图 6.5）——**这张图值得盯到能默画**：

![FOC 级联控制框图：速度环输出 iq*，与 id* = 0 一起进入两个电流环 PI；输出 vd/vq 经反 Park、SVPWM 变成三相占空比驱动逆变桥；反馈链为电流采样 → Clarke → Park；θe 来自编码器或无感观测器](images/fig_06_foc_loop.pdf)

按信号流走一遍：

1. 速度指令 $\omega^{*}$ 与反馈速度之差进**速度环 PI**，输出 $i_q^{*}$（转矩指令）；
2. $i_q^{*}$ 与 $i_d^{*} = 0$ 分别进两个**电流环 PI**，输出 $v_d$、$v_q$（含限幅与抗饱和）；
3. 反 Park 变换转回 $\alpha\beta$ 平面，SVPWM 生成三相占空比，写入 TIM1；
4. 每个 PWM 周期采样两相电流 $\rightarrow$ Clarke $\rightarrow$ Park 得到 $i_d$、$i_q$ 反馈；
5. $\theta_e$ 来自编码器/霍尔（有感）或观测器（无感），同时喂给 Park 与反 Park。

**与六步方波对比**：方波每 60° 电角"跳一档"，电流矢量方向在 ±30° 间摆动；FOC 每一个 PWM 周期（几十微秒）都把电流矢量钉在 q 轴上——转矩恒定、电流利用率最高、低速平稳、无换相噪声。代价是计算量与对电流采样/角度质量的要求。

### PMSM 的电流环 PI 控制

**被控对象**：6.2.2 节 dq 方程忽略交叉耦合后，d、q 轴各是一个一阶 RL 惯性环节（传递函数 $1/(L_s s + R_s)$）——这是 PI 控制器的教科书对象。

**带宽整定法**（把闭环带宽直接设计为 $f_{bw}$，极点对消）：

$$K_P = 2\pi f_{bw} L_s, \qquad K_I = 2\pi f_{bw} R_s$$

$f_{bw}$ 取 PWM 频率的 1/10 \textasciitilde{} 1/20（20 kHz PWM $\rightarrow$ 电流环带宽 1 \textasciitilde{} 2 kHz 量级）。$R_s$、$L_s$ 就来自 6.2.4/6.2.5 的测量——**参数辨识 $\rightarrow$ PI 整定 $\rightarrow$ 性能**，链条在这里闭合。

![电流环阶跃响应仿真（GBM2804H 量级参数）：整定良好时快速无超调；Kp 过小时缓慢爬行；Kp 过大时超调振荡——虚线为电流指令](images/fig_06_pi_tuning.png)

**工程细节**（SDK 里都有对应参数项）：

- **输出限幅**：$\sqrt{v_d^2 + v_q^2} \le V_{dc}/\sqrt{3}$（SVPWM 线性区圆）；
- **抗积分饱和**：限幅的同时钳住积分器（反计算或钳位法），否则超调恢复极慢；
- **交叉解耦前馈**（可选）：补偿 $\pm\omega_e L_s i$ 项，高速时改善动态；云台电机低速场景常省略，由 PI 积分顶住。

### PMSM 的速度环 PI 控制

速度环套在电流环外面，被控对象近似为"电流环（一阶惯性）+ 转矩常数 + 机械惯量"的积分环节：

$$J \frac{\mathrm{d}\omega_m}{\mathrm{d}t} = \frac{3}{2} p \lambda_f i_q - T_L \;\; \Rightarrow \;\; \omega_m(s) = \frac{K_t}{J s} i_q(s) + \ldots$$

**整定原则**：

1. **带宽分离**：速度环带宽取电流环的 1/5 \textasciitilde{} 1/10，内外环才不打架（内环对外环近似" instantaneous"）；
2. 速度反馈在无感方案里来自观测器，噪声较大——加低通或用 FMAC 硬件滤波（第 1 章），但注意滤波延迟也在吃相位裕度；
3. 速度环输出 $i_q^{*}$ 要限幅（最大相电流），堵转时这层限幅就是电机的热保护。

**级联结构的意义**：速度环不必关心电流怎么跟上，电流环不必关心电压怎么合成——每层只对一层负责。这个"分而治之"的框架从 0.5 Hz 的位置环到 20 kHz 的电流环通吃，是运动控制领域近百年沉淀下来的标准答案。

## 本章小结

- 坐标变换把"三相交流"变成"两个直流"：Clarke（abc$\rightarrow$αβ）降维，Park（αβ$\rightarrow$dq）换到转子视角；FOC 目标是 $i_d = 0$、$i_q$ 出力；
- dq 模型给出电压方程与转矩方程 $T_e = \frac{3}{2} p \lambda_f i_q$；αβ 模型藏着无感观测器的钥匙；
- SVPWM 用 8 个离散矢量时间加权合成任意矢量，七段式谐波最优，min-max 注入法三行代码实现，比 SPWM 多 15\% 母线利用率；
- 电流环带宽法整定 $K_P = 2\pi f_{bw} L_s$、$K_I = 2\pi f_{bw} R_s$，速度环带宽低于电流环 5 \textasciitilde{} 10 倍；
- 第 7 章把这些公式全部"对号入座"到 MC SDK 的配置界面与 API 上。

## 本章参考

- 电机控制通行教材中 PMSM 矢量控制与 SVPWM 章节（坐标变换与七段式推导）
- RM0440（CORDIC/FMAC 章节：三角函数与滤波加速）
- X-CUBE-MCSDK 5.x 文档（电流环整定建议与观测器原理章节）
