# 附录 C　均衡器推导

## C.1　线性均衡器

设收发信机模型中，信息源产生施加于无限冲激串的幅度值 $I_n$；即

$$s(t)=\sum_{n=-\infty}^{\infty}I_n\delta(t-nT),$$

其中 $\delta(t)$ 是狄拉克冲激函数。对信息信号 $s(t)$ 施加发射脉冲成形滤波器 $h_T(t)$，得到发射机输出信号：

$$v(t)=\sum_{n=-\infty}^{\infty}I_nh_T(t-nT),$$

它随后经过由信道滤波器 $h_C(t)$ 与加性高斯白噪声信号 $z(t)$ 描述的传播信道。信道滤波器的输出为：

$$p(t)=\sum_{n=-\infty}^{\infty}I_nh(t-nT),$$

其中 $h(t)=h_T(t)\ast h_C(t)$ 是信道冲激响应。接收机截获的信号表示为

$$r(t)=p(t)+z(t)=\sum_{n=-\infty}^{\infty}I_nh(t-nT)+z(t).$$

在接收端，我们想找到均方误差（MSE）的表达式并将其最小化。为此选择接收滤波器 $h_R(t)$ 与 $h(t)$ 匹配，得到最优结果：

$$h_R(t)=h^{\ast}(-t),$$

这使得接收滤波器的输出等于

$$y(t)=p(t)\ast h^{\ast}(-t)+z(t)\ast h^{\ast}(-t)=\sum_{n=-\infty}^{\infty}I_ng(t-nT)+z(t)\ast h^{\ast}(-t),$$

其中 $g(t)=h(t)\ast h_R(t)$，且

$$x(t)=\varphi_h(t)=h(t)\ast h^{\ast}(-t)=\int_{-\infty}^{\infty}h(t+\tau)h^{\ast}(\tau)d\tau.$$

设 $v(t)=z(t)\ast h^{\ast}(-t)$，则得到：

$$y(t)=\sum_{n=-\infty}^{\infty}I_nx(t-nT)+v(t).$$

现在对接收滤波器的输出采样，使得

$$y_k=y(kT)=\sum_{n=-\infty}^{\infty}I_nx((k-n)T)+v(kT)=\sum_{n=-\infty}^{\infty}I_nx_{k-n}+v_k.$$

注意 $x_k$ 称为信道自相关。此外，由于经过 $h^{\ast}(t)$ 滤波，$v_k$ 采样不是白的——即 $E\{v_kv_{k+n}\}\neq\delta(n)$。处理这种有色噪声有几条路。第一种是求噪声序列 $v_k$ 的 $E\{v_kv^{\ast}_l\}$。此法中我们知道 $v_k(t)$ 是高斯的（因为 $z(t)$ 是高斯的）；还知道 $z(t)$ 是白的，即 $S_z(f)=N_0$。于是若 $E\{z^{\ast}(s)z(t)\}=N_0\delta(t-s)$，可解 $E\{v_kv^{\ast}_l\}$：

$$\begin{aligned}
E\{v_kv^{\ast}_l\}&=\int_{-\infty}^{\infty}\!\!\int_{-\infty}^{\infty}h(t-lT)h^{\ast}(s-kT)E\{z^{\ast}(s)z(t)\}\,ds\,dt\\
&=N_0\int_{-\infty}^{\infty}h(t-lT)h^{\ast}(t-kT)\,dt\\
&=N_0\int_{-\infty}^{\infty}h(t+|k-l|T)h^{\ast}(t)\,dt.
\end{aligned}$$

由于

$$x_k=\int_{-\infty}^{\infty}h^{\ast}(t)h(t+kT)\,dt,$$

这给出 $E\{v_kv^{\ast}_l\}$ 的表达式：

$$E\{v_kv^{\ast}_l\}=N_0x_{k-l},$$

可以写成 $v_k$ 的自相关函数与功率谱密度；即

$$R_v(k)=E\{v_nv^{\ast}_{k+n}\}=N_0x_k,\qquad S_v(z)=\mathcal{Z}\{R_v(k)\}=N_0X(z).$$

处理有色噪声的第二种方法是实现所谓的**白化滤波器**。此时我们试图逆转接收滤波器对噪声信号 $z(t)$ 的影响。换言之：既然 $v_k$ 的功率谱密度为 $S_v(z)=N_0X(z)$，我们最终想让白化后的噪声功率谱密度只等于 $N_0$。为此假设 $x_k$ 的 z 变换 $X(z)$ 可表示为：

$$X(z)=F(z)F^{\ast}(1/z^{\ast}).$$

于是，用传递函数为 $1/F^{\ast}(1/z^{\ast})$ 的白化滤波器，输出的功率谱密度应为：

$$S_n(z)=\frac{1}{F(z)F^{\ast}(1/z^{\ast})}S_v(z)=\frac{1}{X(z)}N_0X(z)=N_0,$$

产生白色的输出噪声信号。

## C.2　迫零均衡器

设接收机的离散时间模型为：

$$w_k=\sum_{n=-\infty}^{\infty}I_nf_{k-n}+n_k,\tag{C.20}$$

其中 $w_k$ 是白化滤波器的输出信号、$f_k$ 是白化滤波器的冲激响应、$n_k$ 是功率谱密度为 $N_0$ 的白化噪声信号。

在**迫零均衡器**（ZFE）中，我们选择传递函数 $C(z)$ 使每个 ISI 补偿项 $q_k=\delta_k$——意味着不存在 ISI，均衡后的输出 $I_k+n'_k$ 随后被量化，对 $I_k=\pm1$ 产生差错概率 $P_e=Q(1/\sigma')$。虽然 $P_e$ 常用作通信系统性能度量，但均衡器设计场合我们将用最小均方误差（MMSE）作度量，即 $E\{|I_k-\hat{I}_k|^2\}$。

取 (C.20) 的 z 变换得到：

$$W(z)=I(z)F(z)+N(z)$$

经 ZFE 均衡器滤波后，输出等于

$$W(z)C(z)=I(z)F(z)C(z)+N(z)C(z),$$

其中 $Q(z)=F(z)C(z)$。ZFE 的目标是产生输出

$$\mathcal{Z}^{-1}\{W(z)C(z)\}=I_k\ast q_k+n'_k,$$

其中 $q_k=\delta_k$（信号无 ISI）。因此该表达式中的 ISI 项是 $F(z)C(z)$，我们希望它等于 $Q(z)=F(z)C(z)=1$（对应 $q_k=\delta_k$）。整理得 ZFE 应为 $C(z)=1/F(z)$。

## C.3　判决反馈均衡器

虽然 ZFE 滤波器概念上直接，但几乎总有无限多个抽头——使现实应用中无法实现。此外，白化滤波器输出经 ZFE 均衡后，均衡信号中包含的任何噪声贡献都不再是白的。于是存在更容易在硬件中实现的其他均衡器设计。其中之一是**判决反馈均衡器**（DFE）——由两个滤波器组成：前向滤波器 $a(z)$ 与反馈滤波器 $b(z)-1$。

前向滤波器 $a(z)$ 是反因果的，形式如下：

$$a(z)=a_{-1}z+a_{-2}z^2+a_{-3}z^3+a_{-4}z^4+\ldots,$$

而反馈滤波器 $b(z)$ 是因果滤波器，形式为：

$$b(z)-1=b_1z^{-1}+b_2z^{-2}+b_3z^{-3}+b_4z^{-4}+\ldots$$

于是可以设计 $a(z)$ 与 $b(z)$ 使得

$$a(z)=CF^{\ast}(1/z^{\ast})$$

$$b(z)=F(z)$$

$$F(z)F^{\ast}(1/z^{\ast})=X(z)+N_0.$$
