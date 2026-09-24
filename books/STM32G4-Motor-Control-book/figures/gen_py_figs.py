#!/usr/bin/env python3
"""本书全部 matplotlib 示意图生成脚本。
输出 PNG 到 ../images/，尺寸按物理英寸设计（宽 5.1 in ≈ 版心宽），
savefig dpi=300 写入 pHYs，Pandoc/LaTeX 按物理尺寸排版，不会溢出。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "images"
OUT.mkdir(exist_ok=True)

# —— 书籍配色（与 LaTeX 模板一致）——
ZHUSHA = "#9B2D20"   # 朱砂
MOHEI = "#1A1A1A"    # 墨黑
SHENHUI = "#555555"  # 深灰
LAN = "#1F4E79"      # 深蓝（主曲线）
HUANG = "#B8860B"    # 暗金（次曲线）
QING = "#2E7D6E"     # 青（第三曲线）

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["PingFang SC", "Heiti SC", "Songti SC", "Arial Unicode MS"],
    "axes.unicode_minus": False,
    "font.size": 8.5,
    "axes.linewidth": 0.6,
    "axes.edgecolor": SHENHUI,
    "xtick.color": SHENHUI, "ytick.color": SHENHUI,
    "axes.labelcolor": MOHEI,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})


def save(fig, name):
    fig.savefig(OUT / name, dpi=300)
    plt.close(fig)
    print("saved", name)


def despine(ax, bottom=True, left=True):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if not bottom:
        ax.spines["bottom"].set_visible(False)
    if not left:
        ax.spines["left"].set_visible(False)


# ============================================================
# 图 4-1 定时器 PWM：计数器 / CCR / 输出占空比
# ============================================================
def fig_pwm_duty():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.1, 3.1), sharex=True,
                                   constrained_layout=True)
    T, ARR = 1.0, 10.0
    t = np.linspace(0, 2 * T, 2000)
    cnt = (ARR * (t / T)) % ARR          # 边沿对齐：向上计数锯齿波
    ax1.plot(t, cnt, color=LAN, lw=1.2)
    # 前一周期 CCR=7（占空比 70%），后一周期 CCR=4（占空比 40%）
    for x0, ccr, c in [(0, 7, ZHUSHA), (T, 4, ZHUSHA)]:
        ax1.plot([x0, x0 + T], [ccr, ccr], color=c, lw=1.2, ls="--")
        ax1.text(x0 + 0.02, ccr + 0.5, f"CCR={ccr}", fontsize=7.5, color=ZHUSHA)
    ax1.set_ylabel("计数器 CNT")
    ax1.set_ylim(0, 11.5)
    ax1.set_yticks([0, 4, 7, 10])
    ax1.set_yticklabels(["0", "4", "7", "ARR=10"])
    ax1.set_title("CNT < CCR 期间输出高电平", fontsize=8.5, color=SHENHUI, pad=4)
    despine(ax1)

    # 输出 PWM
    for x0, ccr in [(0, 7), (T, 4)]:
        lvl = np.where((t >= x0) & (t < x0 + T), ((t - x0) / T * ARR) < ccr, np.nan)
        y = np.where(lvl, 1, 0)
        ax2.plot(t, y, color=MOHEI, lw=1.2)
        duty = int(round(ccr / ARR * 100))
        ax2.annotate(f"占空比 {duty}%", xy=(x0 + ccr / ARR * T / 2, 1.02),
                     fontsize=7.5, color=ZHUSHA, ha="center")
    ax2.set_ylabel("OC 输出")
    ax2.set_ylim(-0.25, 1.45)
    ax2.set_yticks([0, 1])
    ax2.set_xlabel("时间（2 个计数周期）")
    despine(ax2)
    save(fig, "fig_04_pwm_duty.png")


# ============================================================
# 图 4-2 互补 PWM 与死区
# ============================================================
def fig_deadtime():
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(5.1, 3.4), sharex=True,
                                        constrained_layout=True,
                                        gridspec_kw={"height_ratios": [1, 1, 1.5]})
    # 中央对齐计数器（三角波）
    T = 1.0
    t = np.linspace(0, 2.5 * T, 2500)
    tri = np.abs(2 * (t / T % 1.0) - 1) * 10
    ax1.plot(t, tri, color=LAN, lw=1.2)
    ax1.set_ylabel("CNT")
    ax1.set_yticks([])
    ax1.text(0.02, 8.2, "中央对齐计数（上数-下数）", fontsize=7.5, color=SHENHUI)
    despine(ax1)

    duty = 0.5
    # 上管 CH1：谷底两侧对称导通
    on = (np.abs(t / T % 1.0 - 0.5) < duty / 2)
    ax2.plot(t, on.astype(float), color=ZHUSHA, lw=1.2)
    ax2.set_ylabel("CH1\n上管")
    ax2.set_yticks([])
    despine(ax2)

    # 下管 CH1N：取反 + 死区
    dt = 0.06 * T
    off = (np.abs(t / T % 1.0 - 0.5) > duty / 2 + dt)
    ax3.plot(t, off.astype(float), color=QING, lw=1.2)
    ax3.set_ylabel("CH1N\n下管")
    ax3.set_yticks([])
    ax3.set_xlabel("时间（2.5 个 PWM 周期）")
    # 放大窗：标出死区
    for k in range(3):
        te = k * T + duty / 2 * T          # 下降沿时刻
        ax3.axvspan(te, te + dt, color=ZHUSHA, alpha=0.18, lw=0)
    ax3.annotate("死区：两管同时关断", xy=(0.5 * T + duty / 2 * T + dt / 2, 1.25),
                 fontsize=7.5, color=ZHUSHA, ha="center",
                 arrowprops=dict(arrowstyle="->", color=ZHUSHA, lw=0.8),
                 xytext=(1.35 * T, 1.45))
    ax3.set_ylim(-0.2, 1.7)
    despine(ax3)
    save(fig, "fig_04_deadtime.png")


# ============================================================
# 图 4-3 UART 帧格式（0x55）
# ============================================================
def fig_uart_frame():
    fig, ax = plt.subplots(figsize=(5.1, 1.9), constrained_layout=True)
    bits = [("空闲", 1, 0.9), ("起始", 0, 1), ("D0", 1, 1), ("D1", 0, 1), ("D2", 1, 1),
            ("D3", 0, 1), ("D4", 1, 1), ("D5", 0, 1), ("D6", 0, 1), ("D7", 0, 1),
            ("停止", 1, 1.2)]
    x = 0.0
    lvl = []
    for name, v, w in bits:
        lvl += [(x, v), (x + w, v)]
        ax.text(x + w / 2, 1.12, name, fontsize=7, ha="center", color=MOHEI)
        ax.axvline(x + w, color=SHENHUI, lw=0.3, alpha=0.5)
        x += w
    xs, ys = zip(*lvl)
    ax.step(xs, ys, where="post", color=LAN, lw=1.4)
    ax.annotate("数据 0x55 = 0b01010101\n低位 LSB 先发", xy=(2.5, 0.02),
                fontsize=7, color=ZHUSHA, ha="center", va="bottom")
    ax.set_ylim(-0.15, 1.5)
    ax.set_xlim(-0.1, x + 0.1)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["低", "高"])
    ax.set_xlabel("一位的宽度由波特率决定（如 115200 bit/s）")
    despine(ax)
    save(fig, "fig_04_uart_frame.png")


# ============================================================
# 图 4-4 DAC 输出：正弦查表 + 三角波
# ============================================================
def fig_dac_out():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.1, 2.1), constrained_layout=True)
    t = np.linspace(0, 2, 600)
    ideal = 1.65 + 1.2 * np.sin(2 * np.pi * t)
    # 12-bit DAC 阶梯（每半周期 16 个点）
    steps = np.repeat(ideal[:: len(t) // 60][:30], len(t) // 30)[: len(t)]
    ax1.plot(t, ideal, color=HUANG, lw=1.0, ls="--", label="理想正弦")
    ax1.step(t, steps, color=LAN, lw=1.1, where="post", label="DAC 阶梯输出")
    ax1.set_title("正弦查表输出（12-bit 分辨率）", fontsize=8)
    ax1.legend(fontsize=6.5, frameon=False, loc="lower left")
    ax1.set_xlabel("周期"); ax1.set_ylabel("输出电压 (V)")
    ax1.set_ylim(0, 3.4)
    despine(ax1)

    t2 = np.linspace(0, 2, 600)
    tri = 1.65 + 1.2 * (2 * np.abs((t2 * 1) % 1 - 0.5))
    ax2.plot(t2, tri, color=QING, lw=1.1)
    ax2.set_title("定时器触发 + DAC 三角波", fontsize=8)
    ax2.set_xlabel("周期"); ax2.set_ylim(0, 3.4)
    despine(ax2)
    save(fig, "fig_04_dac_out.png")


# ============================================================
# 图 5-1 六步换相全景：霍尔 / 相电流 / 梯形反电动势
# ============================================================
def _hall(theta):
    """霍尔信号：120° 电角间隔，每 360° 一个周期"""
    th = theta % 360
    out = np.zeros_like(th)
    # H_a 高电平 0-180, H_b 高 120-300, H_c 高 240-360+0-60
    for base in (0, 120, 240):
        d = (th - base) % 360
        out = np.where((d < 180), 1, 0) if base == 0 else np.where(d < 180, 1, out)
    return out


def _hall_x(theta, base):
    d = theta % 360
    return np.where((d - base) % 360 < 180, 1, 0)


def _phase_current(theta, base):
    """120° 导通 + 60° 断续的方波相电流，base 为该相正向导通起点（电角度）"""
    d = (theta - base) % 360
    return np.where(d < 120, 1.0, np.where(d < 180, 0.0,
                   np.where(d < 300, -1.0, 0.0)))


def _bemf(theta, base):
    """梯形反电动势：平顶 120° + 线性过渡 60°"""
    d = (theta - base) % 360
    y = np.zeros_like(d)
    y = np.where(d < 60, d / 60, y)
    y = np.where((d >= 60) & (d < 180), 1.0, y)
    y = np.where((d >= 180) & (d < 240), 1 - (d - 180) / 60, y)
    y = np.where((d >= 240) & (d < 300), 0.0, y)
    y = np.where(d >= 300, -(d - 300) / 60, y)
    y = np.where((d >= 300), -(d - 300) / 60, y)
    # 平底负半周
    y = np.where((d >= 300), -(d - 300) / 60, y)
    return y


def _bemf_full(theta, base):
    """梯形反电动势：+1 平顶 [base, base+120) 与该相正向导通区对齐，
    60° 斜边接 -1 平底 [base+180, base+300)，过零点在 base+150 与 base+330。"""
    d = (theta - base) % 360
    y = np.where(d < 120, 1.0, 0.0)                       # +1 平顶 120°
    y = np.where((d >= 120) & (d < 180), 1 - 2 * (d - 120) / 60, y)  # +1→-1
    y = np.where((d >= 180) & (d < 300), -1.0, y)         # -1 平底 120°
    y = np.where(d >= 300, -1 + 2 * (d - 300) / 60, y)    # -1→+1
    return y


def fig_sixstep():
    th = np.linspace(0, 720, 2400)
    fig, axes = plt.subplots(9, 1, figsize=(5.1, 6.2), sharex=True,
                             constrained_layout=True)
    rows = [
        ("$H_a$", [_0 := _hall_x(th, 0)], ZHUSHA),
        ("$H_b$", [_hall_x(th, 120)], HUANG),
        ("$H_c$", [_hall_x(th, 240)], QING),
        ("$i_a$", [_phase_current(th, 0)], ZHUSHA),
        ("$i_b$", [_phase_current(th, 120)], HUANG),
        ("$i_c$", [_phase_current(th, 240)], QING),
        ("$e_a$", [_bemf_full(th, 0)], ZHUSHA),
        ("$e_b$", [_bemf_full(th, 120)], HUANG),
        ("$e_c$", [_bemf_full(th, 240)], QING),
    ]
    for ax, (name, (y,), c) in zip(axes, rows):
        ax.plot(th, y, color=c, lw=1.1)
        ax.set_ylabel(name, rotation=0, labelpad=16, fontsize=9, color=MOHEI)
        ax.set_yticks([])
        lim = (-1.35, 1.35)
        if name.startswith("$i"):
            lim = (-1.25, 1.25)
        ax.set_ylim(*lim)
        despine(ax, left=False)
    # 60° 网格 + 换相标记
    for k in range(0, 13):
        for ax in axes:
            ax.axvline(k * 60, color=SHENHUI, lw=0.3, alpha=0.35)
    for k in range(12):
        axes[3].text(k * 60 + 30, 1.42, ["A+B-", "A+C-", "B+C-", "B+A-", "C+A-", "C+B-"][k % 6],
                     fontsize=6.5, ha="center", color=ZHUSHA)
    axes[-1].set_xlim(0, 720)
    axes[-1].set_xticks(range(0, 721, 60))
    axes[-1].set_xticklabels([f"{v}°" for v in range(0, 721, 60)], fontsize=6.5)
    axes[-1].set_xlabel("电角度（两个电周期）")
    save(fig, "fig_05_sixstep.png")


# ============================================================
# 图 5-2 无感过零检测原理
# ============================================================
def fig_zcd():
    th = np.linspace(0, 360, 1200)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.1, 3.2), sharex=True,
                                   constrained_layout=True)
    # 上：B 相电流（非导通相示例：换到 B 断续窗口观察 BEMF）
    iA = _phase_current(th, 0)
    iB = _phase_current(th, 120)
    iC = _phase_current(th, 240)
    ax1.plot(th, iA, color=ZHUSHA, lw=1.1, label="$i_a$")
    ax1.plot(th, iB, color=HUANG, lw=1.1, label="$i_b$")
    ax1.plot(th, iC, color=QING, lw=1.1, label="$i_c$")
    ax1.axhline(0, color=SHENHUI, lw=0.5)
    ax1.legend(fontsize=7, frameon=False, ncol=3, loc="upper right")
    ax1.set_ylabel("相电流")
    ax1.set_yticks([])
    despine(ax1, left=False)

    # 下：B 相端电压/反电动势 + 过零点 + 30° 延迟换相
    eB = _bemf_full(th, 120)
    ax2.plot(th, eB, color=LAN, lw=1.2, label="$e_b$（非导通相）")
    ax2.axhline(0, color=SHENHUI, lw=0.6, ls="--")
    for zc in (90, 270):   # B 相梯形波的两个过零点（base=120 → 过零 90/270）
        ax2.plot(zc, 0, "o", color=ZHUSHA, ms=4)
        ax2.annotate("过零点", xy=(zc, 0), xytext=(zc - 58, 0.75), fontsize=7,
                     color=ZHUSHA, arrowprops=dict(arrowstyle="->", color=ZHUSHA, lw=0.8))
        ax2.axvline(zc + 30, color=QING, lw=0.9, ls=":")
        ax2.text(zc + 40, 0.32, "延时 30°\n换相", fontsize=6.5, color=QING, va="bottom")
    ax2.set_ylabel("反电动势")
    ax2.set_yticks([])
    ax2.set_xlabel("电角度（°）")
    ax2.set_xlim(0, 360)
    despine(ax2, left=False)
    save(fig, "fig_05_zcd.png")


# ============================================================
# 图 6-1 七段式 SVPWM 一个周期内的门极信号
# ============================================================
def fig_svpwm_7seg():
    fig, axes = plt.subplots(3, 1, figsize=(5.1, 3.0), sharex=True,
                             constrained_layout=True)
    # 扇区 I：duty_a > duty_b = duty_c
    t = np.linspace(0, 1, 1000)
    d = [0.75, 0.5, 0.25]
    names = ["A 相上管 $S_1$", "B 相上管 $S_3$", "C 相上管 $S_5$"]
    segs = [0, 0.125, 0.3125, 0.4375, 0.5625, 0.6875, 0.875, 1.0]
    for ax, dd, nm in zip(axes, d, names):
        on = (np.abs(t - 0.5) < dd / 2)
        ax.plot(t, on.astype(float), color=LAN, lw=1.2)
        ax.set_ylabel(nm.replace(" ", "\n"), fontsize=7.5)
        ax.set_yticks([])
        ax.set_ylim(-0.25, 1.45)
        despine(ax, left=False)
    for s in segs:
        for ax in axes:
            ax.axvline(s, color=ZHUSHA, lw=0.4, ls=":", alpha=0.7)
    labs = ["000", "100", "110", "111", "110", "100", "000"]
    for i, lb in enumerate(labs):
        xm = (segs[i] + segs[i + 1]) / 2
        axes[0].text(xm, 1.18, lb, fontsize=6.5, ha="center", color=ZHUSHA)
    axes[2].set_xlim(0, 1)
    axes[2].set_xticks([0, 0.5, 1])
    axes[2].set_xlabel("一个 PWM 周期 $T_{PWM}$（中央对齐，七段对称）")
    save(fig, "fig_06_svpwm_7seg.png")


# ============================================================
# 图 6-2 SPWM 与 SVPWM 调制波对比
# ============================================================
def fig_spwm_vs_svpwm():
    th = np.linspace(0, 2 * np.pi, 1000)
    m = 1.0
    ua = m * np.sin(th)
    ub = m * np.sin(th - 2 * np.pi / 3)
    uc = m * np.sin(th + 2 * np.pi / 3)
    off = -(np.maximum(np.maximum(ua, ub), uc) + np.minimum(np.minimum(ua, ub), uc)) / 2
    sv = ua + off
    fig, ax = plt.subplots(figsize=(5.1, 2.6), constrained_layout=True)
    ax.plot(th / np.pi, ua, color=HUANG, lw=1.1, ls="--", label="SPWM：正弦参考")
    ax.plot(th / np.pi, sv, color=LAN, lw=1.2, label="SVPWM：马鞍波（共模注入后）")
    ax.axhline(1.0, color=SHENHUI, lw=0.5, ls=":")
    ax.axhline(-1.0, color=SHENHUI, lw=0.5, ls=":")
    ax.axhline(2 / np.sqrt(3), color=ZHUSHA, lw=0.6, ls=":")
    ax.annotate("线性区幅值上限 $2V_{dc}/3$（比 SPWM 高 15%）",
                xy=(0.62, 2 / np.sqrt(3)), xytext=(0.15, 1.45), fontsize=7,
                color=ZHUSHA, arrowprops=dict(arrowstyle="->", color=ZHUSHA, lw=0.8))
    ax.set_xlabel("电角度（π 为单位）")
    ax.set_ylabel("调制波（归一化）")
    ax.set_ylim(-1.35, 1.75)
    ax.legend(fontsize=7, frameon=False, loc="lower left")
    despine(ax)
    save(fig, "fig_06_spwm_vs_svpwm.png")


# ============================================================
# 图 6-3 电流环 PI 整定的阶跃响应对比
# ============================================================
def fig_pi_tuning():
    # 被控对象 dI/dt = (V - R I)/L，PI：V = Kp e + Ki ∫e
    R, L = 11.2, 0.02     # GBM2804H 量级（Ω, H）
    dt = 2e-5
    T = 12e-3
    n = int(T / dt)
    t = np.linspace(0, T, n)
    cases = [
        ("整定良好", 6.0, 3200, LAN),
        ("Kp 过小（爬行）", 1.2, 800, HUANG),
        ("Kp 过大（超调振荡）", 22.0, 2600, ZHUSHA),
    ]
    fig, ax = plt.subplots(figsize=(5.1, 2.6), constrained_layout=True)
    for name, kp, ki, c in cases:
        I, v, integ = 0.0, 0.0, 0.0
        y = np.zeros(n)
        for k in range(n):
            e = 1.0 - I
            integ += e * dt
            v = kp * e + ki * integ
            v = max(min(v, 24.0), 0.0)     # 12V 母线双极性上限
            I += (v - R * I) / L * dt
            y[k] = I
        ax.plot(t * 1e3, y, color=c, lw=1.2, label=name)
    ax.axhline(1.0, color=SHENHUI, lw=0.6, ls="--")
    ax.text(9.6, 1.02, "指令 $i_q^{*}$", fontsize=7, color=SHENHUI)
    ax.set_xlabel("时间 (ms)")
    ax.set_ylabel("电流 (A)")
    ax.legend(fontsize=7, frameon=False, loc="center right")
    ax.set_xlim(0, 12)
    despine(ax)
    save(fig, "fig_06_pi_tuning.png")


# ============================================================
# 图 7-1 Motor Profiler 测量过程示意
# ============================================================
def fig_profiler():
    fig, axes = plt.subplots(1, 3, figsize=(5.1, 1.95), constrained_layout=True)
    t = np.linspace(0, 1, 400)

    # 1 测 R：小占空比电压方波 → 稳态电流 I = V/R
    v = np.where(t < 0.08, 0, np.where(t < 0.75, 5.0, 0))
    I0 = 5 / 11.2
    i = I0 * (1 - np.exp(-(t - 0.08) / 0.05))
    i = np.where(t < 0.08, 0, np.where(t < 0.75, i, 0))
    axes[0].plot(t, v / 5, color=ZHUSHA, lw=1.0, ls="--", label="电压")
    axes[0].plot(t, i / I0, color=LAN, lw=1.2, label="电流")
    axes[0].set_title("① 直流脉冲测 $R_s$", fontsize=8)
    axes[0].legend(fontsize=6, frameon=False)
    despine(axes[0])

    # 2 测 L：电压阶跃初期电流上升率 di/dt = V/L
    i2 = np.clip((t - 0.1) * 8, 0, 1)
    axes[1].plot(t, np.where(t < 0.1, 0, 1), color=ZHUSHA, lw=1.0, ls="--", label="电压")
    axes[1].plot(t, i2, color=LAN, lw=1.2, label="电流")
    axes[1].annotate("斜率 ∝ V/L", xy=(0.3, 0.45), fontsize=6.5, color=MOHEI,
                     arrowprops=dict(arrowstyle="->", color=SHENHUI, lw=0.7),
                     xytext=(0.42, 0.2))
    axes[1].set_title("② 电流上升率测 $L_s$", fontsize=8)
    despine(axes[1])

    # 3 测磁链：恒压加速旋转，稳态电流幅值 → 反电动势/磁链
    w = 2 * np.pi * 3
    i3 = 0.25 + 0.15 * np.sin(w * t)
    i3 = np.where(t < 0.05, 0, i3)
    axes[2].plot(t, np.where(t > 0.05, 1, 0), color=ZHUSHA, lw=1.0, ls="--", label="电压矢量")
    axes[2].plot(t, i3, color=LAN, lw=1.2, label="电流幅值")
    axes[2].set_title("③ 加速旋转测 $\\lambda$", fontsize=8)
    despine(axes[2])

    for ax in axes:
        ax.set_xlabel("时间", fontsize=7)
        ax.set_xticks([])
        ax.set_yticks([])
    save(fig, "fig_07_profiler.png")


if __name__ == "__main__":
    fig_pwm_duty()
    fig_deadtime()
    fig_uart_frame()
    fig_dac_out()
    fig_sixstep()
    fig_zcd()
    fig_svpwm_7seg()
    fig_spwm_vs_svpwm()
    fig_pi_tuning()
    fig_profiler()
    print("all done")
