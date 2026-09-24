# -*- coding: utf-8 -*-
"""
render.py — 训练结果的"录像级"渲染：站姿肖像 / 帧序列大图 / GIF 动画 / 转向+前跳演示。
用法: python3 render.py all   （或 portrait / filmstrip / gif / turn）
所有输出到 results/，仅依赖 numpy + matplotlib。
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse, FancyArrowPatch, Wedge
from matplotlib.colors import LinearSegmentedColormap

from lamp_sim import Sim, JumpControllerV2, NQ, rotv
from experiments import load_params

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")

plt.rcParams.update({
    "font.sans-serif": ["PingFang SC", "Hiragino Sans GB", "Arial Unicode MS", "DejaVu Sans"],
    "axes.unicode_minus": False,
})

# ------- Luxo 视觉语言 -------
BG = "#0b0b10"          # 演播室深底
FLOOR = "#1b1b24"
BODY = "#23232c"         # 亚光黑本体
BODY_EDGE = "#8f93a3"    # 轮廓高光
CHROME = "#c9d1e0"       # 镀铬关节
ACCENT = "#10b981"       # 弹簧(青绿)
WARM = "#ffd9a0"         # 暖光
GLOW = "#ff9d2e"
CAM_LENS = "#f97316"


def _norm(v):
    return np.array(v) / (np.linalg.norm(v) + 1e-12)


def draw_lamp_pretty(ax, q, shadow=True, light=True, lw_scale=1.0):
    """按 Luxo 造型渲染一帧。局部系: u 沿体轴, v 前方。"""
    phi, th1, th2, th3 = q[2], q[3], q[4], q[5]
    a1, a2, a3 = phi + th1, phi + th1 + th2, phi + th1 + th2 + th3
    O = np.array([q[0], q[1]])
    def W(alpha, u, v):
        return O + rotv(alpha, u, v)
    toe, heel = W(phi, 0.0, 0.085), W(phi, 0.0, -0.085)
    shoulder = W(phi, 0.085, 0.0)
    elbow = shoulder + rotv(a1, 0.17, 0.0)
    neck = elbow + rotv(a2, 0.16, 0.0)
    # 地面投影(高度越高越小越淡)
    if shadow:
        com_h = O[1] + 0.0
        w = 0.16 * np.clip(1.15 - 0.55 * max(0.0, O[1]), 0.25, 1.15)
        al = 0.38 * np.clip(1.1 - 0.8 * max(0.0, O[1]), 0.15, 0.5)
        ax.add_patch(Ellipse((O[0], 0.006), w, 0.016, color="#000000", alpha=al, zorder=1))
    # ---- 底盘: 半球 ----
    dome_pts = [heel]
    for tdeg in range(-85, 86, 5):
        ang = np.radians(tdeg)
        dome_pts.append(O + rotv(phi, 0.088 * np.cos(ang * 0.92), 0.085 * np.sin(ang * 0.92)))
    dome_pts.append(toe)
    ax.add_patch(Polygon(dome_pts, closed=True, fc=BODY, ec=BODY_EDGE, lw=1.6 * lw_scale, zorder=3))
    ax.plot([heel[0], toe[0]], [heel[1], toe[1]], color="#3a3a46", lw=8.5 * lw_scale,
            solid_capstyle="round", zorder=4)                      # 橡胶足环
    ax.plot([heel[0], toe[0]], [heel[1], toe[1]], color=CHROME, lw=1.2 * lw_scale,
            alpha=0.55, zorder=4.5)
    # 底盘高光弧
    hl = [O + rotv(phi, 0.088 * np.cos(np.radians(t) * 0.9), 0.085 * np.sin(np.radians(t) * 0.9))
          for t in range(15, 65, 6)]
    ax.plot([p[0] for p in hl], [p[1] for p in hl], color="#ffffff", lw=1.1 * lw_scale,
            alpha=0.16, zorder=5)
    # ---- 双平行臂(后侧臂淡影 + 主臂) ----
    for (alpha_arm, width, color, zo) in [(0.7, 5.5, "#4b4b58", 3.5), (1.0, 8.0, BODY, 4.5)]:
        off1, off2 = 0.012 * alpha_arm, 0.012 * alpha_arm
        ax.plot([shoulder[0] + off1, elbow[0] + off2], [shoulder[1], elbow[1]],
                color=color, lw=width * lw_scale, solid_capstyle="round", zorder=zo)
        ax.plot([elbow[0] + off2, neck[0]], [elbow[1], neck[1]],
                color=color, lw=width * 0.8 * lw_scale, solid_capstyle="round", zorder=zo)
    # 弹簧(下臂上方, 伸缩锯齿)
    n_z = 7
    s0 = shoulder + rotv(a1, 0.030, 0.012)
    s1 = elbow + rotv(a1, -0.028, 0.012)
    along = _norm(s1 - s0); perp = np.array([-along[1], along[0]]) * 0.014
    zz = [s0]
    for i in range(1, n_z):
        frac = i / n_z
        zz.append(s0 + (s1 - s0) * frac + (perp if i % 2 else -perp))
    zz.append(s1)
    ax.plot([p[0] for p in zz], [p[1] for p in zz], color=ACCENT, lw=1.6 * lw_scale,
            alpha=0.95, zorder=5)
    # ---- 镀铬关节 ----
    for pt, r in [(shoulder, 0.023), (elbow, 0.018), (neck, 0.011)]:
        ax.add_patch(Circle(pt, r, fc=CHROME, ec="#6b7280", lw=0.8 * lw_scale, zorder=6))
        ax.add_patch(Circle(pt + np.array([r * 0.3, r * 0.3]), r * 0.3, fc="#ffffff",
                            ec="none", alpha=0.8, zorder=6.5))
    # ---- 灯罩(圆锥) ----
    shade = [neck,
             neck + rotv(a3, 0.040, -0.030),
             neck + rotv(a3, 0.006, 0.096),     # 开口鼻端
             neck + rotv(a3, -0.016, -0.026)]
    ax.add_patch(Polygon(shade, closed=True, fc=BODY, ec=BODY_EDGE, lw=1.4 * lw_scale, zorder=6))
    # 罩口暖光内缘
    rim = [neck + rotv(a3, 0.006, 0.096), neck + rotv(a3, -0.016, -0.026)]
    ax.plot([rim[0][0], rim[1][0]], [rim[0][1], rim[1][1]], color=WARM, lw=3.6 * lw_scale,
            alpha=1.0, zorder=7, solid_capstyle="round")
    # 摄像头镜片
    lens = neck + rotv(a3, 0.007, 0.064)
    ax.add_patch(Circle(lens, 0.0075, fc=CAM_LENS, ec="#7c2d12", lw=0.8 * lw_scale, zorder=7.5))
    # 灯泡光晕 + 光锥
    if light:
        bulb = neck + rotv(a3, 0.005, 0.040)
        for r, al in [(0.060, 0.13), (0.038, 0.20), (0.019, 0.38)]:
            ax.add_patch(Circle(bulb, r, fc=GLOW, ec="none", alpha=al, zorder=6.8))
        dirv = _norm(rotv(a3, 0.0, 1.0))          # 光锥朝罩口方向
        far = bulb + dirv * 0.55
        side = np.array([-dirv[1], dirv[0]]) * 0.16
        ax.add_patch(Polygon([bulb, far + side, far - side], closed=True,
                             fc=GLOW, ec="none", alpha=0.075, zorder=2))


def studio_axes(ax, xlim, ylim=(-0.06, 0.62), title=None):
    ax.set_facecolor(BG)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Polygon([(xlim[0] - 1, 0), (xlim[1] + 1, 0), (xlim[1] + 1, -1), (xlim[0] - 1, -1)],
                         closed=True, fc=FLOOR, ec="none", zorder=0.5))
    ax.plot([xlim[0] - 1, xlim[1] + 1], [0, 0], color="#3d3d4a", lw=1.2, zorder=2)
    if title:
        ax.set_title(title, color="#e8e8ec", fontsize=12.5, pad=10)


# ---------------------------------------------------------------- 素材获取
class _PhaseRecorder:
    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.phases = []
    def __call__(self, t, q, qd, contact, sim):
        out = self.ctrl(t, q, qd, contact, sim)
        self.phases.append(self.ctrl.phase)
        return out


def rollout(task="hop", T=None):
    p, _ = load_params(task)
    sim = Sim(k_spring=(1.5, 1.5, 0.0))
    if task == "flip":
        from lamp_sim import FlipController
        ctrl = FlipController(p); T = T or 2.6
    else:
        ctrl = JumpControllerV2(p)
        T = T or (4.6 if task in ("leap", "hop") else 2.6)
    rec = _PhaseRecorder(ctrl)
    q0 = np.zeros(NQ); q0[1] = 0.0005
    h = sim.run(rec, T, q0, np.zeros(NQ))
    h["phase"] = list(np.array(rec.phases[::5][:len(h["t"])]))
    return h


def _apex_idx(h):
    com_y = np.array([c[1] for c in h["com"]])
    air = np.array(h["contact"]) == False
    valid = np.where(air, com_y, -9.9)
    return int(np.argmax(valid)) if valid.max() > 0 else len(com_y) // 2


# ---------------------------------------------------------------- 1. 站姿肖像
def portrait(fname="view_portrait.png"):
    q = np.zeros(NQ); q[3], q[4] = 0.12, -0.22      # 自然微弯站姿
    fig, ax = plt.subplots(figsize=(7.2, 8.2), dpi=130)
    fig.patch.set_facecolor(BG)
    studio_axes(ax, (-0.42, 0.42), (-0.07, 0.60))
    # 背景径向微光
    ax.add_patch(Circle((0.02, 0.30), 0.45, fc="#1a1a2e", ec="none", alpha=0.5, zorder=0))
    draw_lamp_pretty(ax, q)
    ax.text(0.0, 0.575, "Pixar 台灯机器人 · v1 造型", ha="center", color="#e8e8ec",
            fontsize=15, fontweight="bold")
    ax.text(0.0, 0.552, "总质量 1.291 kg · 站立全高 ~47 cm · DM-J4310-V2 ×2 + 平衡弹簧",
            ha="center", color="#9ca3af", fontsize=10.5)
    out = os.path.join(RESULTS, fname)
    fig.savefig(out, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    print("saved", out)


# ---------------------------------------------------------------- 2. 帧序列大图
def _lamp_extent(q):
    from experiments import lamp_points
    pts = lamp_points(q)
    xs = [p[0] for p in pts.values()]; ys = [p[1] for p in pts.values()]
    return min(xs), max(xs), min(min(ys), 0.0), max(ys)


def filmstrip(task="hop", n=20, fname=None):
    h = rollout(task)
    ts = np.array(h["t"])
    ph = np.array(h["phase"])
    i_apex = _apex_idx(h)
    t0 = max(0.0, ts[i_apex] - 0.55)
    span = 0.17
    times = list(t0 + np.arange(n) * span)
    idx = [int(np.argmin(np.abs(ts - t))) for t in times]
    # 相位感知: 保证含"点火蹬伸"(phase==1)与腾空
    fire_idx = np.where(ph == 1)[0]
    if len(fire_idx) and not any(ph[i] == 1 for i in idx):
        pos = 3 if ph[idx[3]] in (0,) else 3
        idx[pos] = int(fire_idx[len(fire_idx) // 2])
    idx[-1] = len(ts) - 1                      # 末帧 = 终态(站立)
    labels = {0: "下蹲蓄力", 1: "点火蹬伸", 2: "腾空", 3: "落地缓冲", 4: "起身站立"}
    rows, cols = 4, 5
    fig, axes = plt.subplots(rows, cols, figsize=(19.5, 10.4), dpi=105)
    fig.patch.set_facecolor(BG)
    for k, (ax, i) in enumerate(zip(axes.flat, idx)):
        ax.set_facecolor(BG)
        q = h["q"][i]
        x0, x1, y0, y1 = _lamp_extent(q)
        cx = 0.5 * (x0 + x1)
        halfw = max(0.5 * (x1 - x0) + 0.05, 0.13)
        ax.set_xlim(cx - halfw, cx + halfw)
        ax.set_ylim(-0.05, max(y1 + 0.10, 0.35))
        ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#2a2a35")
        ax.plot([cx - halfw - 0.05, cx + halfw + 0.05], [0, 0], color="#3d3d4a", lw=1.0, zorder=2)
        ax.add_patch(Polygon([(cx - halfw - 0.05, 0), (cx + halfw + 0.05, 0),
                              (cx + halfw + 0.05, -0.06), (cx - halfw - 0.05, -0.06)],
                             closed=True, fc=FLOOR, ec="none", zorder=0.5))
        draw_lamp_pretty(ax, q, lw_scale=0.82)
        ax.set_title(f"t = {ts[i]:.2f} s", color="#9ca3af", fontsize=9, pad=2)
        ax.text(0.03, 0.955, labels.get(int(ph[i]), "—"), color="#a5b4fc",
                fontsize=10, transform=ax.transAxes, va="top")
    b = h["best"]
    fig.suptitle(f"Pixar 台灯 · {'定向跳' if task=='leap' else '原地跳'} 帧序列（相机跟拍）    "
                 f"腾空 {b['apex_at']*100:.1f} cm · $v_0$ = {np.sqrt(2*9.81*max(0,b['apex_at'])):.2f} m/s · "
                 f"水平位移 {abs(h['q_end'][0]-h['q'][0][0])*100:.0f} cm · 末帧站立收势",
                 color="#e8e8ec", fontsize=13.5)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    out = fname or os.path.join(RESULTS, f"view_filmstrip_{task}.png")
    fig.savefig(out, facecolor=BG)
    plt.close(fig)
    print("saved", out)


# ---------------------------------------------------------------- 3. GIF 动画
def gif(task="hop", fname=None, follow=True):
    from matplotlib.animation import FuncAnimation, PillowWriter
    h = rollout(task)
    ts = np.array(h["t"])
    i_apex = _apex_idx(h)
    t0 = max(0.0, ts[i_apex] - 0.55)
    sel = [i for i, t in enumerate(ts) if t0 - 0.05 <= t <= t0 + 2.75]
    sel = sel[::4]                                    # ~40ms/帧
    fig, ax = plt.subplots(figsize=(7.6, 5.6), dpi=100)
    fig.patch.set_facecolor(BG)
    trail_x, trail_y = [], []

    def draw_frame(k):
        ax.clear(); ax.set_facecolor(BG)
        i = sel[k]
        q = h["q"][i]
        xw = 0.34
        xlim = (q[0] - xw, q[0] + xw) if follow else (-0.45, 0.45)
        studio_axes(ax, xlim, (-0.05, 0.60))
        # 质心轨迹尾迹
        trail_x.append(h["com"][i][0]); trail_y.append(h["com"][i][1])
        ax.plot(trail_x[-40:], trail_y[-40:], color="#f87171", lw=1.8, alpha=0.75,
                zorder=2.5, ls="--")
        draw_lamp_pretty(ax, q)
        ax.plot(h["com"][i][0], h["com"][i][1], "*", color="#f87171", ms=13, zorder=8)
        b = h["best"]
        ax.text(xlim[0] + 0.05, 0.575, f"t = {ts[i]:.2f} s", color="#e8e8ec", fontsize=12)
        ax.text(xlim[0] + 0.05, 0.55, f"腾空 {b['apex_at']*100:.1f} cm · "
                f"$v_0$ = {np.sqrt(2*9.81*max(0,b['apex_at'])):.2f} m/s", color="#9ca3af", fontsize=10)
        air = not h["contact"][i]
        ax.text(xlim[1] - 0.05, 0.575, "滞空" if air else "支撑", ha="right",
                color="#10b981" if air else "#9ca3af", fontsize=11)

    ani = FuncAnimation(fig, draw_frame, frames=len(sel), interval=33)
    out = fname or os.path.join(RESULTS, f"view_{task}.gif")
    ani.save(out, writer=PillowWriter(fps=30))
    plt.close(fig)
    print("saved", out, f"({len(sel)} 帧)")


# ---------------------------------------------------------------- 4. 转向 + 前跳
def turn_jump_gif(fname="view_turn_jump.gif"):
    """场景A: 俯视底盘转向90°; 场景B: 侧视前跳。演示"任何方向 = 转身 + 前跳"。"""
    from matplotlib.animation import FuncAnimation, PillowWriter
    h = rollout("leap")
    ts = np.array(h["t"])
    i_apex = _apex_idx(h)
    t0 = max(0.0, ts[i_apex] - 0.55)
    sel = [i for i, t in enumerate(ts) if t0 - 0.05 <= t <= t0 + 2.55][::4]

    n_turn = 26
    frames_total = n_turn + len(sel)
    fig, ax = plt.subplots(figsize=(7.6, 5.6), dpi=100)
    fig.patch.set_facecolor(BG)
    trail_x, trail_y = [], []
    head0 = np.deg2rad(90.0)     # 初始朝向(俯视: +y 北)

    def draw_top(psi, k):
        ax.clear(); ax.set_facecolor(BG)
        ax.set_xlim(-0.5, 0.5); ax.set_ylim(-0.5, 0.5)
        ax.set_aspect("equal"); ax.axis("off")
        # 指南环
        ax.add_patch(Circle((0, 0), 0.42, fill=False, ec="#2a2a35", lw=1.4))
        for ang, lab in [(90, "北 N"), (0, "东 E"), (-90, "南 S"), (180, "西 W")]:
            a = np.radians(ang)
            p = 0.44 * np.array([np.cos(a), np.sin(a)])
            ax.text(p[0], p[1], lab, ha="center", va="center", color="#6b7280", fontsize=9)
        # 目标方向(东)
        tgt = np.deg2rad(0.0)
        ax.add_patch(FancyArrowPatch((0.30 * np.cos(tgt), 0.30 * np.sin(tgt)),
                                     (0.41 * np.cos(tgt), 0.41 * np.sin(tgt)),
                                     arrowstyle="-|>", mutation_scale=16,
                                     color="#f97316", lw=2.2))
        ax.text(0.30, 0.335, "目标方向", color="#f97316", fontsize=10, ha="center")
        # 底盘圆 + 双臂投影 + 灯罩投影
        ax.add_patch(Circle((0, 0), 0.145, fc=BODY, ec=CHROME, lw=2.2))
        for r in (0.30, 0.46):
            ax.add_patch(Circle(r * np.array([np.cos(psi), np.sin(psi)]), 0.052,
                                fc="#3a3a46", ec="#6b7280", lw=1.0))
        ax.plot([0, 0.30 * np.cos(psi)], [0, 0.30 * np.sin(psi)], color=BODY_EDGE, lw=4.5)
        ax.plot([0.30 * np.cos(psi), 0.46 * np.cos(psi)], [0.30 * np.sin(psi), 0.46 * np.sin(psi)],
                color=BODY_EDGE, lw=3.6)
        ax.add_patch(FancyArrowPatch(0.18 * np.array([np.cos(psi + 0.55), np.sin(psi + 0.55)]),
                                     0.30 * np.array([np.cos(psi + 0.75), np.sin(psi + 0.75)]),
                                     arrowstyle="-|>", mutation_scale=13,
                                     color="#10b981", lw=2.0))
        ax.text(0, 0.495, "① 底盘转向（Z 轴偏航自由度, 与跳跃动力学解耦）",
                ha="center", color="#e8e8ec", fontsize=12)
        ax.text(0, -0.475, f"航向 {np.degrees((psi - head0 + np.pi) % (2*np.pi) - np.pi):.0f}° / 目标 90°",
                ha="center", color="#9ca3af", fontsize=10.5)

    def draw_side(k):
        i = sel[k]
        ax.clear(); ax.set_facecolor(BG)
        q = h["q"][i]
        xlim = (q[0] - 0.34, q[0] + 0.34)
        studio_axes(ax, xlim, (-0.05, 0.60))
        trail_x.append(h["com"][i][0]); trail_y.append(h["com"][i][1])
        ax.plot(trail_x[-40:], trail_y[-40:], color="#f87171", lw=1.8, alpha=0.75,
                zorder=2.5, ls="--")
        draw_lamp_pretty(ax, q)
        ax.plot(h["com"][i][0], h["com"][i][1], "*", color="#f87171", ms=13, zorder=8)
        b = h["best"]
        ax.text(xlim[0] + 0.05, 0.575, f"② 朝新航向前跳  t = {ts[i]:.2f} s", color="#e8e8ec", fontsize=12)
        ax.text(xlim[0] + 0.05, 0.55,
                f"腾空 {b['apex_at']*100:.1f} cm · 位移 {abs(h['q_end'][0]-h['q'][0][0])*100:.0f} cm",
                color="#9ca3af", fontsize=10)
        ax.text(xlim[1] - 0.05, 0.575, "前 = 已转向方向", ha="right", color="#10b981", fontsize=10.5)

    def frame(k):
        if k < n_turn:
            frac = min(1.0, k / (n_turn - 6))
            psi = head0 + np.pi / 2 * (frac * frac * (3 - 2 * frac))   # smoothstep
            draw_top(psi, k)
        else:
            draw_side(k - n_turn)
        return []

    ani = FuncAnimation(fig, frame, frames=frames_total, interval=33)
    out = os.path.join(RESULTS, fname)
    ani.save(out, writer=PillowWriter(fps=30))
    plt.close(fig)
    print("saved", out, f"({frames_total} 帧)")


def directions_png(fname="view_directions.png"):
    """顶视图: 圆形底盘的"全向 = 前跳"概念图(8 个航向)。"""
    fig, ax = plt.subplots(figsize=(7.6, 7.6), dpi=120)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-0.75, 0.75); ax.set_ylim(-0.78, 0.82)
    ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Circle((0, 0), 0.66, fill=False, ec="#23232e", lw=1.2))
    for ang in np.linspace(0, 2 * np.pi, 9)[:-1]:
        d = np.array([np.cos(ang), np.sin(ang)])
        # 每个方向: 弧形跳跃轨迹 + 台灯小图标
        for rr, aa in [(0.20, 0.0), (0.33, 0.35), (0.46, 0.55), (0.56, 0.0)]:
            pass
        trail = [t * d + np.array([0, 0.09 * np.sin(np.pi * t / 0.56)]) for t in np.linspace(0.16, 0.56, 24)]
        ax.plot([p[0] for p in trail], [p[1] for p in trail], color="#f87171", lw=1.6,
                alpha=0.85, ls="--")
        ax.add_patch(Circle(0.60 * d, 0.028, fc="#f97316", ec="none"))
    ax.add_patch(Circle((0, 0), 0.145, fc=BODY, ec=CHROME, lw=2.4))
    ax.plot([0, 0.0], [0, 0], lw=0)
    ax.text(0, 0.70, "全向移动 = 底盘偏航旋转 + 同一个「前跳」策略", ha="center",
            color="#e8e8ec", fontsize=13.5, fontweight="bold")
    ax.text(0, -0.72, "圆形底盘：偏航与矢状面动力学解耦，转身无重心代价，任意方向皆是向前",
            ha="center", color="#9ca3af", fontsize=10.5)
    out = os.path.join(RESULTS, fname)
    fig.savefig(out, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    print("saved", out)


if __name__ == "__main__":
    import sys
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    os.makedirs(RESULTS, exist_ok=True)
    if what in ("portrait", "all"):
        portrait()
    if what in ("filmstrip", "all"):
        filmstrip("hop"); filmstrip("leap")
    if what in ("gif", "all"):
        gif("hop"); gif("leap")
    if what in ("turn", "all"):
        turn_jump_gif(); directions_png()
