# -*- coding: utf-8 -*-
"""
实验与图表：频闪图 / 遥测图 / 学习曲线 / 扭矩-弹簧余量分析。
用法:
  python3 experiments.py strobe   # 用 CEM 最优参数画跳跃频闪图(无结果时用基线参数)
  python3 experiments.py telemetry
  python3 experiments.py learning
  python3 experiments.py margin   # 训练完成后: 电机扭矩/弹簧刚度余量分析
  python3 experiments.py all
"""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lamp_sim import Sim, JumpControllerV2, FlipController, NQ, rotv, energy

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")

plt.rcParams.update({
    "font.size": 11, "axes.grid": True, "grid.alpha": 0.22, "grid.color": "#4b5563",
    "figure.facecolor": "#1a1a1f", "axes.facecolor": "#1a1a1f", "savefig.facecolor": "#1a1a1f",
    "text.color": "#e8e8ec", "axes.labelcolor": "#e8e8ec", "xtick.color": "#9ca3af",
    "ytick.color": "#9ca3af", "axes.edgecolor": "#4b5563",
    "axes.spines.top": False, "axes.spines.right": False,
    "font.sans-serif": ["PingFang SC", "Hiragino Sans GB", "Arial Unicode MS", "DejaVu Sans"],
    "axes.unicode_minus": False,
})
C_BODY, C_ARM, C_HEAD, C_COM = "#e8e8ec", "#9ca3af", "#f9fafb", "#f87171"


# ---------------------------------------------------------------- 造型渲染
def lamp_points(q):
    """返回绘制用的关键点: 足角[(x,y)x2], 肩, 肘, 颈, 灯罩鼻/后缘, COM。"""
    phi, th1, th2, th3 = q[2], q[3], q[4], q[5]
    a1, a2, a3 = phi + th1, phi + th1 + th2, phi + th1 + th2 + th3
    origin = np.array([q[0], q[1]])
    shoulder = origin + rotv(phi, 0.085, 0.0)
    elbow = shoulder + rotv(a1, 0.17, 0.0)
    neck = elbow + rotv(a2, 0.16, 0.0)
    nose = neck + rotv(a3, 0.010, 0.068)
    back_top = neck + rotv(a3, 0.030, -0.030)
    back_bot = neck + rotv(a3, -0.010, -0.030)
    toe = origin + rotv(phi, 0.0, 0.085)
    heel = origin + rotv(phi, 0.0, -0.085)
    dome_l = origin + rotv(phi, 0.020, 0.083)
    dome_r = origin + rotv(phi, 0.020, -0.083)
    return dict(origin=origin, shoulder=shoulder, elbow=elbow, neck=neck,
                nose=nose, back_top=back_top, back_bot=back_bot,
                toe=toe, heel=heel, dome_l=dome_l, dome_r=dome_r)


def draw_lamp(ax, q, alpha=1.0, lw=3.0, color=None, com=None):
    p = lamp_points(q)
    c = color or C_BODY
    # 底盘
    ax.plot([p["heel"][0], p["toe"][0]], [p["heel"][1], p["toe"][1]],
            color=c, lw=lw + 2, alpha=alpha, solid_capstyle="round")
    dome = plt.Polygon([p["heel"], p["dome_r"], p["shoulder"], p["dome_l"], p["toe"]],
                       closed=True, fill=True, fc=c, ec="none", alpha=alpha * 0.85)
    ax.add_patch(dome)
    # 双臂
    ax.plot([p["shoulder"][0], p["elbow"][0]], [p["shoulder"][1], p["elbow"][1]],
            color=c, lw=lw, alpha=alpha, solid_capstyle="round")
    ax.plot([p["elbow"][0], p["neck"][0]], [p["elbow"][1], p["neck"][1]],
            color=c, lw=lw * 0.8, alpha=alpha, solid_capstyle="round")
    # 灯罩(梯形)
    shade = plt.Polygon([p["neck"], p["back_top"], p["nose"], p["back_bot"]],
                        closed=True, fc=C_HEAD, ec="none", alpha=alpha * 0.9)
    ax.add_patch(shade)
    # 关节点
    for key in ("shoulder", "elbow", "neck"):
        ax.plot(*p[key], "o", color="#1a1a1f", mec=c, mew=1.6, ms=lw * 1.6, alpha=alpha, zorder=5)
    if com is not None:
        ax.plot(com[0], com[1], "*", color=C_COM, ms=13, alpha=alpha, zorder=6)


def load_params(task="hop"):
    f = os.path.join(RESULTS, f"cem_{task}.json")
    if os.path.exists(f):
        with open(f) as fh:
            data = json.load(fh)
        return np.array(list(data["params"].values())), data
    from train_es import SPACE
    return SPACE["hop" if task != "flip" else "flip"]["p0"].copy(), None


# ---------------------------------------------------------------- 图: 频闪
def fig_strobe(task="hop", n_frames=14, T=None, fname=None):
    p, data = load_params(task)
    sim = Sim(k_spring=(1.5, 1.5, 0.0))
    if task == "flip":
        ctrl = FlipController(p); T = T or 2.6
    else:
        ctrl = JumpControllerV2(p, repeat=(task == "travel"))
        T = T or (3.5 if task == "travel" else (2.6 if task == "leap" else 2.2))
    q0 = np.zeros(NQ); q0[1] = 0.0005
    h = sim.run(ctrl, T, q0, np.zeros(NQ))
    ts = np.array(h["t"])
    # 频闪窗口: 以"腾空段质心最高点"为中心, 覆盖 蹲→起跳→顶点→落地
    com_y = np.array([c[1] for c in h["com"]])
    airborne = np.array(h["contact"]) == False
    valid = np.where(airborne, com_y, -9.9)
    i_apex = int(np.argmax(valid)) if valid.max() > 0 else len(ts) // 2
    t0 = max(0.0, ts[i_apex] - 0.35)
    idx = [int(np.argmin(np.abs(ts - (t0 + i * 0.045)))) for i in range(n_frames)]
    xs = [h["q"][i][0] for i in idx]
    xmin, xmax = min(xs) - 0.30, max(xs) + 0.30
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    ax.fill_between([xmin, xmax], -1, 0, color="#4b5563", alpha=0.9, lw=0, zorder=0)
    ax.text(xmin + 0.03, 0.015, "地面", color="#9ca3af", fontsize=9)
    for k, i in enumerate(idx):
        fade = 0.35 + 0.65 * k / max(1, len(idx) - 1)
        draw_lamp(ax, h["q"][i], alpha=fade, com=h["com"][i])
    b = h["best"]
    dx = (h["q_end"][0] - h["q"][0][0]) * 100
    labels = dict(hop="原地跳", leap="定向跳", travel="连续跳", flip="翻身跳(尝试)")
    ttl = (f"Pixar 台灯{labels.get(task,'')}频闪（每帧 45 ms）  "
           f"腾空 {b['apex_at']*100:.1f} cm  $v_0$={np.sqrt(2*9.81*max(0,b['apex_at'])):.2f} m/s")
    if abs(dx) > 3:
        ttl += f"  水平位移 {abs(dx):.0f} cm"
    ax.set_title(ttl)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(-0.035, 0.62)
    ax.set_aspect("equal"); ax.set_xlabel("x [m]"); ax.set_ylabel("y [m]")
    out = fname or os.path.join(RESULTS, f"fig_strobe_{task}.png")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)
    print("saved", out, "| apex_at=%.1fcm dx=%.1fcm" % (b["apex_at"]*100, dx))
    return h


def load_params(task="hop"):
    f = os.path.join(RESULTS, f"cem_{task}.json")
    if os.path.exists(f):
        with open(f) as fh:
            data = json.load(fh)
        return np.array(list(data["params"].values())), data
    from train_es import SPACE
    return SPACE["hop" if task != "flip" else "flip"]["p0"].copy(), None


# ---------------------------------------------------------------- 图: 频闪


# ---------------------------------------------------------------- 图: 遥测
def fig_telemetry(task="hop", fname=None):
    p, _ = load_params(task)
    sim = Sim(k_spring=(1.5, 1.5, 0.0))
    h = sim.run(JumpControllerV2(p, repeat=(task == "travel")),
                3.5 if task == "travel" else 2.2,
                np.concatenate([np.zeros(5), [0.0005], np.zeros(0)]), np.zeros(NQ)) \
        if False else sim.run(JumpControllerV2(p, repeat=(task == "travel")),
                              3.5 if task == "travel" else 2.2,
                              np.r_[0, 0.0005, 0, 0, 0, 0], np.zeros(NQ))
    t = np.array(h["t"])
    fig, axes = plt.subplots(3, 1, figsize=(9.5, 7.2), sharex=True)
    axes[0].plot(t, [c[1] for c in h["com"]], color="#2563eb", lw=2)
    axes[0].axhline(h["standing_com_y"], ls="--", color="#9ca3af", lw=1)
    axes[0].set_ylabel("COM 高度 [m]"); axes[0].legend(["COM", "站立参考"])
    axes[1].plot(t, h["Fn"], color="#dc2626", lw=1.6)
    axes[1].set_ylabel("地面法向力 [N]")
    axes[1].axhline(sim.model.M_total * 9.81, ls="--", color="#9ca3af", lw=1)
    tau = np.array(h["tau"])
    axes[2].plot(t, tau[:, 0], lw=1.6, color="#7c3aed")
    axes[2].plot(t, tau[:, 1], lw=1.6, color="#059669")
    axes[2].axhline(12.5, ls=":", color="#9ca3af"); axes[2].axhline(-12.5, ls=":", color="#9ca3af")
    axes[2].set_ylabel("关节扭矩 [N·m]"); axes[2].set_xlabel("t [s]")
    axes[2].legend(["肩 τ1(含弹簧)", "肘 τ2(含弹簧)", "电机峰值 ±12.5"])
    fig.suptitle("跳跃遥测：COM 高度 / 地面反力 / 关节扭矩")
    out = fname or os.path.join(RESULTS, f"fig_telemetry_{task}.png")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)
    print("saved", out)
    return h


# ---------------------------------------------------------------- 图: 学习曲线
def fig_learning(task="hop", fname=None):
    f = os.path.join(RESULTS, f"cem_{task}.json")
    if not os.path.exists(f):
        print("无训练结果"); return
    with open(f) as fh:
        data = json.load(fh)
    hist = data["history"]
    it = [x["iter"] for x in hist]
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    ax.plot(it, [x["best"] for x in hist], "o-", ms=3.5, color="#2563eb", label="种群最优")
    ax.plot(it, [x["elite_mean"] for x in hist], "-", color="#7c3aed", label="精英均值")
    ax.plot(it, [x["mu"] for x in hist], "-", color="#9ca3af", label="均值策略")
    ax2 = ax.twinx()
    ax2.plot(it, [x["info"]["apex_at"] * 100 for x in hist], "--", color="#dc2626", label="腾空高度(cm)")
    ax2.set_ylabel("腾空高度 [cm]", color="#dc2626"); ax2.grid(False)
    ax.set_xlabel("CEM 迭代"); ax.set_ylabel("回报")
    ax.set_title(f"CEM 训练曲线（{task}，pop=40，CPU {data['wall_s']:.0f}s）")
    ax.legend(loc="upper left"); ax2.legend(loc="lower right")
    out = fname or os.path.join(RESULTS, f"fig_learning_{task}.png")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)
    print("saved", out)


# ---------------------------------------------------------------- 余量分析
def fig_margin(task="hop", fname=None):
    """训练完成后: 用最优策略参数在降扭矩/变弹簧下的表现 -> 硬件余量。"""
    p, _ = load_params(task)
    taus = [4.0, 6.0, 8.0, 10.0, 12.5, 15.0]
    springs = [0.0, 0.75, 1.5, 3.0, 4.5]
    rows = []
    for tc in taus:
        for ks in springs:
            rs, aps = [], []
            for seed in range(3):
                sim = Sim(k_spring=(ks, ks, 0.0))
                sim.tau_peak = np.array([tc, tc, 1.2])
                ctrl = JumpControllerV2(p.copy())
                h = sim.run(ctrl, 2.2, np.r_[0, 0.0005, 0, 0, 0, 0], np.zeros(NQ))
                b = h["best"]; qe = h["q_end"]
                if h.get("diverged") or b["apex_at"] > 1.0:
                    rs.append(-500.0); aps.append(0.0); continue
                upright = abs(qe[2]) < 0.30 and h["contact"][-1]
                rs.append(100 * b["apex_at"] + (40 if upright else 0.0))
                aps.append(b["apex_at"] * 100)
            rows.append((tc, ks, float(np.mean(rs)), float(np.mean(aps))))
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3))
    sel = [(r[0], r[3]) for r in rows if abs(r[1] - 1.5) < 1e-9]
    axes[0].plot([s[0] for s in sel], [s[1] for s in sel], "o-", color="#2563eb")
    axes[0].set_xlabel("电机峰值扭矩 [N·m]"); axes[0].set_ylabel("腾空高度 [cm]")
    axes[0].set_title("扭矩余量（弹簧 1.5 N·m/rad）")
    sel = [(r[1], r[3]) for r in rows if abs(r[0] - 12.5) < 1e-9]
    axes[1].plot([s[0] for s in sel], [s[1] for s in sel], "s-", color="#059669")
    axes[1].set_xlabel("关节弹簧刚度 [N·m/rad]"); axes[1].set_ylabel("腾空高度 [cm]")
    axes[1].set_title("弹簧贡献（扭矩 12.5 N·m）")
    out = fname or os.path.join(RESULTS, "fig_margin.png")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)
    with open(os.path.join(RESULTS, "margin.json"), "w") as f:
        json.dump([r[:3] for r in rows], f)
    print("saved", out)


if __name__ == "__main__":
    import sys
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    os.makedirs(RESULTS, exist_ok=True)
    if what in ("strobe", "all"):
        fig_strobe("hop")
    if what in ("telemetry", "all"):
        fig_telemetry("hop")
    if what in ("learning", "all"):
        fig_learning("hop")
    if what in ("margin", "all"):
        fig_margin("hop")
