# -*- coding: utf-8 -*-
"""
Pixar 台灯机器人（Luxo）— 平面多体动力学仿真，自研最小实现（仅依赖 numpy）
================================================================================
模型（sagittal 平面）：
    浮基座(底盘, 3 DOF: x/y/phi) + 肩关节 th1 + 肘关节 th2 + 颈关节 th3
    q = [x, y, phi, th1, th2, th3]
机构：底盘(含肩电机/电池/主控) — 下臂(含肘电机) — 上臂(含颈舵机) — 灯头(灯罩/摄像头/IMU)
    真实 Luxo 是双侧平行双臂，本平面模型取单侧等效。

局部坐标约定（所有刚体）: u = 沿体轴（站立时向上/沿连杆向远端）, v = 前方垂直分量。

动力学（已通过能量/动量/角动量守恒与有限差分交叉验证）：
    M(q) qdd + b(q, qd) = tau_gen + J_c^T F_contact
    - M = Σ m_i Jv_i^T Jv_i + I_i Jw_i^T Jw_i（COM 雅可比组装）
    - b 惯性项 = Σ m_i Jv_i^T a_bias_i，a_bias_i = -Σ_seg rotv(a_seg)*adot^2
      （平面链 qdd=0 时的纯向心偏置加速度；重力项 Σ m_i g Jv_i[1,:]）
    - 地面接触：足底两点 + 灯头鼻端；法向 Kelvin-Voigt 罚接触 + 正则化库仑摩擦
    - 关节弹簧（复刻 Luxo 平衡弹簧，静止位 θ=0 即伸展位，蹲下储能助跳）
    - 电机限制：峰值扭矩钳位 + 转速扭矩线性衰减 + 功率钳位
    - 关节阻尼（弹簧阻尼 + 控制器微分项）做隐式积分：(M + dt·D) q̇' = M q̇ + dt·Q
      ——浮基座小等效惯量下显式阻尼会数值失稳（MuJoCo 同样做法）
积分：速度半隐式 + 阻尼隐式。
"""
import numpy as np

G = 9.81
NQ = 6  # [x, y, phi, th1, th2, th3]


def rotv(alpha, u, v):
    sa, ca = np.sin(alpha), np.cos(alpha)
    return np.array([u * sa + v * ca, u * ca - v * sa])


def drotv(alpha, u, v):
    sa, ca = np.sin(alpha), np.cos(alpha)
    return np.array([u * ca - v * sa, -u * sa - v * ca])


def composite_body(points, rods):
    """points: [(m, u, v)]; rods: [(m, uc, half_len)] 沿 u 轴杆段。→ (m, com, I_com)"""
    m = sum(p[0] for p in points) + sum(r[0] for r in rods)
    cu = (sum(p[0] * p[1] for p in points) + sum(r[0] * r[1] for r in rods)) / m
    cv = sum(p[0] * p[2] for p in points) / m
    I = 0.0
    for pm, pu, pv in points:
        I += pm * ((pu - cu) ** 2 + (pv - cv) ** 2)
    for rm, ru, hl in rods:
        I += rm * ((ru - cu) ** 2 + (4.0 * hl ** 2) / 12.0)
    return m, np.array([cu, cv]), I


def default_bodies():
    """结构与质量预算 v1（总 1.291 kg）。底盘几何原点=足底平面中心；连杆原点=近端关节。"""
    bodies = []
    m0, c0, I0 = composite_body(
        points=[(0.120, 0.053, 0.000),   # 3D 打印半球外壳 + 饰件
                (0.317, 0.070, 0.000),   # 肩关节电机 DM-J4310-2EC-V2
                (0.175, 0.028, 0.000),   # 电池 6S 1000mAh (22.2V)
                (0.060, 0.055, 0.000),   # 主控 ESP32-S3 + CAN + 驱动板
                (0.030, 0.004, 0.000)],  # 橡胶足环
        rods=[])
    bodies.append(dict(m=m0, com=c0, I=I0, pivot_out=(0.085, 0.000),
                       contacts=[(0.0, 0.085), (0.0, -0.085)]))  # 17cm 足底(真实 Luxo ~23cm)
    m1, c1, I1 = composite_body(points=[(0.317, 0.170, 0.0)],
                                rods=[(0.060, 0.085, 0.085)])
    bodies.append(dict(m=m1, com=c1, I=I1, pivot_out=(0.170, 0.0), contacts=[]))
    m2, c2, I2 = composite_body(points=[(0.040, 0.160, 0.0)],
                                rods=[(0.060, 0.080, 0.080)])
    bodies.append(dict(m=m2, com=c2, I=I2, pivot_out=(0.160, 0.0), contacts=[]))
    # 灯头：灯罩按前后缘分布质量(更真实的转动惯量) + 摄像头 + 头部PCB/IMU + 支架
    m3, c3, I3 = composite_body(
        points=[(0.036, 0.012, 0.062), (0.024, 0.012, -0.002), (0.012, 0.000, 0.035),
                (0.020, -0.005, 0.010), (0.020, 0.000, 0.000)], rods=[])
    bodies.append(dict(m=m3, com=c3, I=I3, pivot_out=(0.0, 0.0),
                       contacts=[(0.005, 0.065)]))
    return bodies


class LampModel:
    def __init__(self, bodies=None):
        self.b = bodies if bodies is not None else default_bodies()
        self.nb = len(self.b)
        self.m = np.array([bd["m"] for bd in self.b])
        self.Ib = np.array([bd["I"] for bd in self.b])
        self.M_total = float(self.m.sum())
        segs = [[(0, self.b[0]["com"][0], self.b[0]["com"][1])]]
        for i in range(1, self.nb):
            path = [(0, self.b[0]["pivot_out"][0], self.b[0]["pivot_out"][1])]
            for k in range(1, i):
                path.append((k, self.b[k]["pivot_out"][0], self.b[k]["pivot_out"][1]))
            path.append((i, self.b[i]["com"][0], self.b[i]["com"][1]))
            segs.append(path)
        self.segs = segs
        self.contact_pts = []
        for i, bd in enumerate(self.b):
            for (u, v) in bd["contacts"]:
                self.contact_pts.append((i, u, v))
        self.Jw = np.zeros((self.nb, NQ))
        for i in range(self.nb):
            self.Jw[i, 2] = 1.0
            self.Jw[i, 3:3 + i + 1] = 1.0
        # 展平路径段: [body, alpha_idx, u, v]
        seg_rows = []
        for i in range(self.nb):
            for (ai, u, v) in segs[i]:
                seg_rows.append((i, ai, u, v))
        self.seg_body = np.array([r[0] for r in seg_rows])
        self.seg_alpha = np.array([r[1] for r in seg_rows])
        self.seg_u = np.array([r[2] for r in seg_rows], dtype=float)
        self.seg_v = np.array([r[3] for r in seg_rows], dtype=float)
        self.seg_body_starts = np.searchsorted(self.seg_body, np.arange(self.nb))

    def fk(self, q, qd=None):
        """各刚体: 绝对角 alpha, COM 世界位置 P(nb,2), 雅可比 J(nb,2,6), 偏置加速度 a_bias。(向量化)"""
        A = np.empty(self.nb)
        A[0] = q[2]
        for i in range(1, self.nb):
            A[i] = A[i - 1] + q[2 + i]
        W = np.zeros(self.nb) if qd is None else np.cumsum(qd[2:])
        sa, ca = np.sin(A[self.seg_alpha]), np.cos(A[self.seg_alpha])
        u, v = self.seg_u, self.seg_v
        # rotv / drotv 批量
        off = np.stack([u * sa + v * ca, u * ca - v * sa], axis=1)        # (nseg,2)
        doff = np.stack([u * ca - v * sa, -u * sa - v * ca], axis=1)      # (nseg,2)
        w2 = W[self.seg_alpha] ** 2
        P = np.zeros((self.nb, 2))
        J = np.zeros((self.nb, 2, NQ))
        a_bias = np.zeros((self.nb, 2))
        np.add.at(P, self.seg_body, off)
        np.add.at(a_bias, self.seg_body, -off * w2[:, None])
        np.add.at(J[:, :, 2], self.seg_body, doff)
        for j in range(1, self.nb):
            mask = self.seg_alpha >= j
            np.add.at(J[:, :, 2 + j], self.seg_body[mask], doff[mask])
        J[:, 0, 0] = 1.0
        J[:, 1, 1] = 1.0
        P += np.array([q[0], q[1]])
        return list(A), P, J, a_bias

    def mass_bias(self, q, qd):
        """返回 (M, bias, P)。bias 含向心项与重力，不含关节扭矩。(einsum 向量化)"""
        alphas, P, J, a_bias = self.fk(q, qd)
        M = np.einsum('nra,nrb,n->ab', J, J, self.m) \
            + np.einsum('na,nb,n->ab', self.Jw, self.Jw, self.Ib)
        bias = np.einsum('nra,nr,n->a', J, a_bias, self.m) + G * np.einsum('na,n->a', J[:, 1, :], self.m)
        return M, bias, P


class Sim:
    def __init__(self, model=None, dt=4e-4,
                 k_n=3.0e4, d_n=90.0, mu=0.65, k_f=1.5e4,
                 tau_peak=(12.5, 12.5, 1.2), omega_max=(21.0, 21.0, 30.0),
                 p_cap=(100.0, 100.0, 15.0),
                 kp=(60.0, 60.0, 2.0), kd=(3.0, 3.0, 0.1),
                 k_spring=(0.0, 0.0, 0.0), c_spring=(0.05, 0.05, 0.02), spring_rest=0.0,
                 joint_friction=(0.15, 0.15, 0.05)):
        self.model = model if model is not None else LampModel()
        self.dt = dt
        self.k_n, self.d_n, self.mu, self.k_f = k_n, d_n, mu, k_f
        self.tau_peak, self.omega_max, self.p_cap = (np.array(tau_peak), np.array(omega_max), np.array(p_cap))
        self.kp, self.kd = np.array(kp), np.array(kd)
        self.k_spring, self.c_spring, self.spring_rest = (np.array(k_spring), np.array(c_spring), spring_rest)
        self.joint_friction = np.array(joint_friction)
        self.ground_y = 0.0
        # 隐式关节阻尼系数（被动阻尼 + 控制器 D 增益统一走隐式；
        # 颈关节 0.02 N·m·s/rad 对应小舵机变速箱粘滞，抑制无物理意义的鞭梢效应）
        self.D = np.diag([0.0, 0.0, 0.0, c_spring[0] + kd[0], c_spring[1] + kd[1], c_spring[2] + kd[2]])

    # ---------- 扭矩模型 ----------
    def motor_limit(self, tau, qd):
        """电机指令扭矩限制：峰值 × 转速线性衰减 × 功率钳位。"""
        w = qd[3:]
        cap = self.tau_peak * np.clip(1.0 - np.abs(w) / self.omega_max, 0.0, 1.0)
        cap = np.minimum(cap, self.p_cap / np.maximum(np.abs(w), 1e-3))
        return np.clip(tau, -cap, cap)

    def spring_stiffness(self, q):
        """弹簧保守扭矩（不经过电机限幅；阻尼部分在积分器隐式处理）。"""
        return -self.k_spring * (q[3:6] - self.spring_rest)

    def joint_torques(self, q, qd, tau_cmd):
        """总关节扭矩（遥测/能量审计用）。"""
        th = np.tanh(qd[3:6] / 0.1)
        return (self.motor_limit(np.asarray(tau_cmd, float), qd) + self.spring_stiffness(q)
                - self.c_spring * qd[3:6] - self.joint_friction * th)

    # ---------- 接触 ----------
    def contact_states(self, q, qd, alphas, P, J):
        out = []
        for (bi, u, v) in self.model.contact_pts:
            du, dv = u - self.model.b[bi]["com"][0], v - self.model.b[bi]["com"][1]
            if bi == 0:
                Jc = np.zeros((2, NQ))
                Jc[:, 0] = [1, 0]
                Jc[:, 1] = [0, 1]
                Jc[:, 2] = drotv(alphas[0], u, v)
                p = np.array([q[0], q[1]]) + rotv(alphas[0], u, v)
            else:
                Jc = J[bi].copy()
                Jc[:, 2] += drotv(alphas[bi], du, dv)
                for j in range(1, bi + 1):
                    Jc[:, 2 + j] += drotv(alphas[bi], du, dv)
                p = P[bi] + rotv(alphas[bi], du, dv)
            out.append((p, Jc @ qd, Jc))
        return out

    def contact_forces(self, q, qd, alphas, P, J):
        F_gen = np.zeros(NQ)
        cF = []
        for (p, v, Jc) in self.contact_states(q, qd, alphas, P, J):
            pen = p[1] - self.ground_y
            if pen < 0:
                Fn = min(600.0, max(0.0, -self.k_n * pen - self.d_n * v[1]))
                Ft = -np.clip(self.k_f * v[0], -self.mu * Fn, self.mu * Fn)
            else:
                Fn, Ft = 0.0, 0.0
            cF.append((p, v, Fn, Ft))
            F_gen += Jc.T @ np.array([Ft, Fn])
        return F_gen, cF

    def qdd_no_damp(self, q, qd, tau_cmd):
        """无关节阻尼的显式动力学（阻尼在 step() 中隐式积分）。"""
        alphas, P, J, a_bias = self.model.fk(q, qd)
        M, bias, _ = self.model.mass_bias(q, qd)
        F_gen, cF = self.contact_forces(q, qd, alphas, P, J)
        tau_gen = np.zeros(NQ)
        tau_gen[3:] = self.motor_limit(np.asarray(tau_cmd, float), qd) + self.spring_stiffness(q)
        qdd = np.linalg.solve(M, tau_gen + F_gen - bias)
        return qdd, M, bias, cF

    def _friction_lin(self, qd):
        """库仑摩擦(线性化隐式用): 返回 (τ_fric(qd), 斜率 dτ/dω)。"""
        th = np.tanh(qd[3:6] / 0.1)
        tau_f = -self.joint_friction * th
        slope = (self.joint_friction / 0.1) * (1.0 - th ** 2)
        return tau_f, slope

    def _implicit_damp(self, q, qd, tau_cmd, kd_ctrl, h):
        qdd, M, bias, cF = self.qdd_no_damp(q, qd, tau_cmd)
        tau_f, slope = self._friction_lin(qd)
        Dv = np.array([0.0, 0.0, 0.0,
                       self.c_spring[0] + (kd_ctrl[0] if kd_ctrl is not None else 0.0) + slope[0],
                       self.c_spring[1] + (kd_ctrl[1] if kd_ctrl is not None else 0.0) + slope[1],
                       self.c_spring[2] + (kd_ctrl[2] if kd_ctrl is not None else 0.0) + slope[2]])
        Q = M @ (qd + qdd * h)
        Q[3:6] -= h * (tau_f + slope * qd[3:6])   # 摩擦隐式残差
        qd_new = np.linalg.solve(M + h * np.diag(Dv), Q)
        q_new = q + qd_new * h
        return q_new, qd_new, cF, qdd

    def _euler(self, q, qd, tau_cmd, kd_ctrl, h):
        return self._implicit_damp(q, qd, tau_cmd, kd_ctrl, h)

    def step(self, q, qd, tau_cmd, kd_ctrl=None, depth=0):
        """一步积分：阻尼隐式、其余显式；位置半隐式。
        刚性瞬态(反奇异/高速触地)自动 8 子步细分，避免定步长崩溃。"""
        qdd, M, bias, cF = self.qdd_no_damp(q, qd, tau_cmd)
        v_cmax = max((abs(c[1][1]) for c in cF), default=0.0)
        stiff = (np.abs(qdd).max() > 5.0e4) or (v_cmax > 12.0)
        if stiff and depth < 3 and self.dt > 4e-5:
            n = 6
            for _ in range(n):
                q, qd, cF, _ = self._euler(q, qd, tau_cmd, kd_ctrl, self.dt / n)
            return q, qd, cF
        q_new, qd_new, _, _ = self._implicit_damp(q, qd, tau_cmd, kd_ctrl, self.dt)
        return q_new, qd_new, cF

    # ---------- COM 工具 ----------
    def com_pos(self, q):
        alphas, P, J, ab = self.model.fk(q)
        return (self.model.m[:, None] * P).sum(0) / self.model.M_total

    def com_vel(self, q, qd):
        alphas, P, J, ab = self.model.fk(q, qd)
        vc = np.zeros(2)
        for i in range(self.model.nb):
            vc += self.model.m[i] * (J[i] @ qd)
        return vc / self.model.M_total

    # ---------- 仿真主循环 ----------
    def run(self, controller, T, q0=None, qd0=None, record_every=5):
        q = np.zeros(NQ) if q0 is None else np.array(q0, dtype=float)
        qd = np.zeros(NQ) if qd0 is None else np.array(qd0, dtype=float)
        n = int(round(T / self.dt))
        hist = dict(t=[], q=[], qd=[], contact=[], Fn=[], com=[], tau=[], cycles=0)
        standing_com = self.com_pos(np.zeros(NQ))[1]
        best = dict(apex=0.0, apex_at=0.0, com_apex=-9.9, peak_Fn=0.0, peak_tau=np.zeros(3),
                    air_t=0.0, touchdown_v=0.0, takeoff=None, v_takeoff=0.0)
        contact_prev = True
        air_streak = 0
        registered = False
        in_air_real_prev = False
        t = 0.0
        diverged = False
        for step_i in range(n):
            if not (np.all(np.isfinite(q)) and np.all(np.isfinite(qd))):
                diverged = True
                break
            if np.abs(qd).max() > 90.0 or abs(q[0]) > 8.0 or q[1] > 4.0 or q[1] < -1.0:
                diverged = True
                break
            out = controller(t, q, qd, contact_prev, self)
            if isinstance(out, tuple):
                tau_cmd, kd_ctrl = np.asarray(out[0], float), np.asarray(out[1], float)
            else:
                tau_cmd, kd_ctrl = np.asarray(out, float), np.zeros(3)
            q, qd, cF = self.step(q, qd, tau_cmd, kd_ctrl)
            Fn_tot = sum(c[2] for c in cF)
            contact = Fn_tot > 1e-6
            cx, cy = self.com_pos(q)
            if step_i % record_every == 0:
                hist["t"].append(t); hist["q"].append(q.copy()); hist["qd"].append(qd.copy())
                hist["contact"].append(contact); hist["Fn"].append(Fn_tot)
                hist["com"].append((cx, cy))
                hist["tau"].append(self.joint_torques(q, qd, tau_cmd))
            best["peak_Fn"] = max(best["peak_Fn"], Fn_tot)
            # 接触去抖: 连续离地 >20ms 才认定为起飞(罚接触微抖不算)
            if not contact:
                air_streak += 1
                if air_streak * self.dt > 0.02:
                    if not best.get("in_air_real") and not registered:
                        vc = self.com_vel(q, qd)
                        best["takeoff"] = dict(t=t, vx=vc[0], vy=vc[1])
                        best["v_takeoff"] = vc[1]
                        best["takeoff_com_y"] = cy
                        registered = True
                    best["air_t"] += self.dt
                    best["com_apex"] = max(best["com_apex"], cy)
                    in_air_real_prev = True
            else:
                if in_air_real_prev and registered:
                    best["touchdown_v"] = self.com_vel(q, qd)[1]
                air_streak = 0
                in_air_real_prev = False
            best["peak_tau"] = np.maximum(best["peak_tau"], np.abs(self.joint_torques(q, qd, tau_cmd)))
            contact_prev = contact
            t += self.dt
        best["apex"] = best["com_apex"] - standing_com
        if best.get("takeoff_com_y") is not None:
            best["apex_at"] = best["com_apex"] - best["takeoff_com_y"]
        else:
            best["apex_at"] = -1.0
        hist["q_end"] = q.copy(); hist["qd_end"] = qd.copy()
        hist["best"] = best
        hist["standing_com_y"] = standing_com
        hist["T"] = t
        hist["diverged"] = diverged
        if hasattr(controller, "cycles"):
            hist["cycles"] = controller.cycles
        return hist


class JumpController:
    """阶段机 SETTLE(蹲) -> FIRE(爆发伸展) -> FLIGHT(空中收腿备降) -> LAND(缓冲)。
    p = [th1c, th2c, tau1, tau2, th1s, th2s, th1l, th2l, t_wait, fire_tmax]
    微分项不在控制器里 —— 统一由 Sim 以隐式阻尼实现（sim.kd）。"""

    PHASE_SETTLE, PHASE_FIRE, PHASE_FLIGHT, PHASE_LAND = 0, 1, 2, 3

    def __init__(self, p, repeat=False, land_kp_scale=0.8):
        self.p0 = np.array(p, dtype=float)
        self.p = self.p0.copy()
        self.repeat = repeat
        self.land_kp_scale = land_kp_scale
        self.reset()

    def reset(self):
        self.phase = self.PHASE_SETTLE
        self.t0 = 0.0
        self.cycles = 0
        self.p = self.p0.copy()

    def _pd(self, sim, q, tgt, scale=1.0):
        return sim.kp * scale * (np.array(tgt) - q[3:6]), sim.kd * scale

    def __call__(self, t, q, qd, contact, sim):
        (th1c, th2c, tau1, tau2, th1s, th2s, th1l, th2l, t_wait, fire_tmax) = self.p
        dt_p = t - self.t0
        s3 = self.STAND_POSE[2]
        if self.phase == self.PHASE_SETTLE:
            tau, kd = self._pd(sim, q, (th1c, th2c, s3))
            if dt_p > t_wait:
                self.phase = self.PHASE_FIRE; self.t0 = t
            return tau, kd
        if self.phase == self.PHASE_FIRE:
            if (q[3] < th1s and q[4] > th2s) or dt_p > fire_tmax:
                self.phase = self.PHASE_FLIGHT; self.t0 = t
            return np.array([tau1, tau2, 0.0]), np.zeros(3)
        if self.phase == self.PHASE_FLIGHT:
            tau, kd = self._pd(sim, q, (th1l, th2l, self.STAND_POSE[2]), 0.6)
            if contact:
                self.phase = self.PHASE_LAND; self.t0 = t
            return tau, kd
        tau, kd = self._pd(sim, q, (th1c, th2c, 0.0), self.land_kp_scale)
        settled = dt_p > 0.2 and abs(qd[2]) < 0.4 and contact
        if self.repeat and (settled or dt_p > 0.9):
            self.phase = self.PHASE_SETTLE; self.t0 = t; self.cycles += 1
            self.p[8] = np.clip(self.p[8], 0.10, 0.30)
        return tau, kd


def energy(sim, q, qd):
    """机械能（动能 + 重力势能 + 弹簧势能；阻尼与接触会耗散）。"""
    alphas, P, J, ab = sim.model.fk(q, qd)
    T = 0.0
    for i in range(sim.model.nb):
        v = J[i] @ qd
        T += 0.5 * sim.model.m[i] * (v @ v) + 0.5 * sim.model.b[i]["I"] * (sim.model.Jw[i] @ qd) ** 2
    V = G * float((sim.model.m * P[:, 1]).sum())
    Es = 0.5 * float((sim.k_spring * (q[3:6] - sim.spring_rest) ** 2).sum())
    return T + V + Es


if __name__ == "__main__":
    np.set_printoptions(precision=6, suppress=True)
    mdl = LampModel()
    print(f"总质量 = {mdl.M_total:.3f} kg, 各体 = {mdl.m}")
    for i, bd in enumerate(mdl.b):
        print(f"  body{i}: m={bd['m']:.3f} com=(u{bd['com'][0]:+.3f},v{bd['com'][1]:+.3f}) I={bd['I']:.2e}")
    sim = Sim()
    print(f"站立 COM 高度 = {sim.com_pos(np.zeros(NQ))[1]:.4f} m")

    # T1a 能量守恒（无接触、含弹簧、阻尼为 0）
    sim1 = Sim(k_spring=(1.5, 1.5, 0.0), c_spring=(0.0, 0.0, 0.0))
    sim1.D = sim1.D * 0.0
    sim1.ground_y = -100.0
    q0 = np.array([0, 0, 0.1, 1.2, -2.0, 0.3]); qd0 = np.array([0.3, 1.1, 0.5, -0.7, 0.9, 0.2])
    h = sim1.run(lambda *a: np.zeros(3), 1.5, q0, qd0)
    E0, E1 = energy(sim1, q0, qd0), energy(sim1, h["q_end"], h["qd_end"])
    print(f"T1a 能量守恒: {E0:.6f} -> {E1:.6f} J (漂移 {100*(E1-E0)/abs(E0):+.4f}%)")

    # T1b 自由落体构形不变性（无弹簧）
    sim1c = Sim(c_spring=(0.0, 0.0, 0.0)); sim1c.D = sim1c.D * 0.0; sim1c.ground_y = -100.0
    h = sim1c.run(lambda *a: (np.zeros(3), np.zeros(3)), 1.0, np.array([0, 0, 0.05, 0.3, -0.5, 0.1]), np.zeros(NQ))
    print(f"T1b 自由落体构形漂移: {np.abs(h['q_end'][2:] - np.array([0.05, 0.3, -0.5, 0.1])).max():.2e}")

    # T2 静立支撑
    sim2 = Sim()
    hold = lambda t, q, qd, c, s: (np.array([60.0 * (0.15 - q[3]), 60.0 * (-0.3 - q[4]), 0.0]), np.array([3.0, 3.0, 0.1]))
    h = sim2.run(hold, 1.5, np.array([0, 0.002, 0, 0.15, -0.3, 0]), np.zeros(NQ))
    print(f"T2 静立: y_end={h['q_end'][1]:+.5f} Fn_end={h['Fn'][-1]:.2f} N "
          f"(mg={mdl.M_total*G:.2f}) phi_end={h['q_end'][2]:+.5f}")

    # T3 手调开环跳（不同弹簧刚度）
    p = np.array([1.5, -2.4, -9.0, 9.0, 0.25, -0.35, 0.9, -1.4, 0.7, 0.35])
    for ks in [(0.0, 0.0, 0.0), (1.5, 1.5, 0.0), (3.0, 3.0, 0.0)]:
        sim3 = Sim(k_spring=ks)
        h = sim3.run(JumpController(p), 2.0)
        b = h["best"]
        print(f"T3 开环跳 k={ks[0]:.1f}: 跳高={b['apex']*100:5.1f} cm 滞空={b['air_t']:.3f}s "
              f"峰值Fn={b['peak_Fn']:5.1f}N 峰值tau={np.round(b['peak_tau'][:2],1)} "
              f"落地|phi|={abs(h['q_end'][2]):.2f}rad")


class JumpControllerV2:
    """V2 跳跃控制器：点火时序(肩/肘延迟) + 肩部姿态反馈 + 参数化备降。
    站姿常量: 台灯形态(连杆弯折、灯罩斜朝地面), 也是落地后起身的目标。
    p = [th1c, th2c, tau1, tau2, d1, d2, kphi, kdphi,
         th1l, th2l, kp_land, t_wait, stop2, t_fire_max, kx, kdx]
    FIRE: tau_j(t) = tau_j·H(t-t0-d_j)（10ms 斜坡），肩部叠加姿态反馈
          kphi·(0-phi) - kdphi·phid —— 把内旋转动量导回竖直推程。
    repeat=True: 落地稳定后自动进入下一跳(移动任务)。"""

    PHASE_SETTLE, PHASE_FIRE, PHASE_FLIGHT, PHASE_LAND, PHASE_STAND, PHASE_HOLD = 0, 1, 2, 3, 4, 5
    STAND_POSE = (-0.65, 1.466, 0.034)  # ★冻结★ 见 ../INIT_POSE.json: 竖臂后仰37°/灯头32cm/罩口朝下前

    def __init__(self, p, repeat=False, stand_after=True, stop_t=None):
        self.p0 = np.array(p, dtype=float)
        self.p = self.p0.copy()
        self.repeat = repeat
        self.stop_t = stop_t          # 指令窗口: t<stop_t 连续跳, 之后定住保持台灯站姿
        self.stand_after = stand_after
        self.reset()

    def reset(self):
        self.phase = self.PHASE_SETTLE
        self.t0 = 0.0
        self.t_fire = 0.0
        self.cycles = 0
        self.p = self.p0.copy()
        self._cmd = 1
        self._hold_tgt = None

    def set_cmd(self, c, q, t):
        """指令位: 1=向前挪(状态机), 0=软着陆并归位到台灯站姿(定住)。"""
        if int(c) == 0 and self._cmd != 0:
            self._hold_tgt = np.array(JumpControllerV2.STAND_POSE)
            if self.phase in (self.PHASE_FIRE, self.PHASE_FLIGHT):
                self.phase = self.PHASE_LAND   # 运动中收到0: 软着陆后归位台灯站姿
            else:
                self.phase = self.PHASE_HOLD    # 静止中收到0: 平衡反馈直接锁台灯站姿
            self.t0 = t
        elif int(c) == 1 and self._cmd != 1 and self.phase in (self.PHASE_HOLD, self.PHASE_STAND, self.PHASE_LAND):
            self.phase = self.PHASE_SETTLE
            self.t0 = t
        self._cmd = int(c)

    def _pd(self, sim, q, tgt, scale=1.0):
        return sim.kp * scale * (np.array(tgt) - q[3:6]), sim.kd * scale

    def __call__(self, t, q, qd, contact, sim):
        (th1c, th2c, tau1, tau2, d1, d2, kphi, kdphi,
         th1l, th2l, kp_land, t_wait, stop2, t_fire_max, kx, kdx, com_ref) = \
            np.pad(self.p, (0, 17 - len(self.p)), constant_values=0.0)
        dt_p = t - self.t0
        s3 = self.STAND_POSE[2]
        if self.phase == self.PHASE_SETTLE:
            tau, kd = self._pd(sim, q, (th1c, th2c, s3))
            com = sim.com_pos(q); comv = sim.com_vel(q, qd)
            # 下蹲保持阶段的平衡反馈: 把 COM 控制到 com_ref(方向指令: 前倾=向前跳)
            com_rx = com[0] - q[0]        # COM 相对底盘足心(实机由编码器+IMU 得到)
            tau[0] += kx * (com_ref - com_rx) - kdx * comv[0] - kdphi * qd[2]
            if dt_p > t_wait and t > 0.35 and abs(com_rx - com_ref) < 0.035 and abs(qd[2]) < 0.6:
                self.phase = self.PHASE_FIRE; self.t_fire = t
            return tau, kd
        if self.phase == self.PHASE_FIRE:
            e = t - self.t_fire
            r1 = np.clip((e - d1) / 0.01, 0.0, 1.0)
            r2 = np.clip((e - d2) / 0.01, 0.0, 1.0)
            com = sim.com_pos(q); comv = sim.com_vel(q, qd)
            com_rx = com[0] - q[0]
            fb = kphi * (0.0 - q[2]) - kdphi * qd[2] + kx * (com_ref - com_rx) - kdx * comv[0]
            tau = np.array([tau1 * r1 + fb, tau2 * r2, 0.0])
            if (q[4] < stop2) or (e > t_fire_max):   # 正向折叠: 伸展=θ2 降到 stop2
                self.phase = self.PHASE_FLIGHT; self.t0 = t
            return tau, np.array([0.0, 0.0, 0.0])
        if self.phase == self.PHASE_FLIGHT:
            tau, kd = self._pd(sim, q, (th1l, th2l, self.STAND_POSE[2]), 0.6)
            if contact:
                self.phase = self.PHASE_LAND; self.t0 = t
            return tau, kd
        if self.phase == self.PHASE_STAND:
            self.t_stand = getattr(self, "t_stand", 0.0) + sim.dt
            return self._stand(sim, q, qd, dt_stand=self.t_stand)
        if self.phase == self.PHASE_HOLD:
            tau, kd = self._pd(sim, q, self._hold_tgt, 1.6)   # 软簧后主动刚度顶上
            com = sim.com_pos(q); comv = sim.com_vel(q, qd)
            fb = kx * (0.0 - (com[0] - q[0])) - kdx * comv[0] - 3.0 * qd[2]
            tau[0] += float(np.clip(fb, -12.5, 12.5))
            return tau, kd
        com_now = sim.com_pos(q)
        calm = abs(com_now[0] - q[0] - com_ref) < 0.07 and np.abs(qd).max() < 1.5
        if self.stand_after and dt_p > 0.9 and contact and abs(q[2]) < 0.30 and calm:
            self.phase = self.PHASE_STAND; self.t0 = t; self.t_stand = 0.0
            return self._stand(sim, q, qd, dt_stand=0.0)
        tau, kd = self._pd(sim, q, (th1c, th2c, self.STAND_POSE[2]), kp_land)
        settled = dt_p > 0.25 and abs(qd[2]) < 0.5 and contact
        if self.repeat and (settled or dt_p > 1.0):
            if self.stop_t is None or t < self.stop_t:
                self.phase = self.PHASE_SETTLE; self.t0 = t; self.cycles += 1
                self.p[11] = np.clip(self.p[11], 0.35, 0.65)  # 后续循环: 蹲深蓄满再跳
        return tau, kd

    def _stand(self, sim, q, qd, dt_stand=0.0):
        """落地缓冲后回到自然站立(演示收尾): 缓坡目标 + SETTLE 平衡结构(训练过的增益)。"""
        (th1c, th2c, tau1, tau2, d1, d2, kphi, kdphi,
         th1l, th2l, kp_land, t_wait, stop2, t_fire_max, kx, kdx, com_ref) = \
            np.pad(self.p, (0, 17 - len(self.p)), constant_values=0.0)
        # 准静态起身: 目标从蹲姿 1s 线性插值到台灯站姿, 反应扭矩足够小
        mix = float(np.clip(dt_stand / 1.0, 0.0, 1.0))
        s1, s2, s3 = self.STAND_POSE
        tgt = np.array([th1c + (s1 - th1c) * mix, th2c + (s2 - th2c) * mix, s3 * mix])
        tau, kd = self._pd(sim, q, tgt, 0.8)
        com = sim.com_pos(q); comv = sim.com_vel(q, qd)
        fb = kx * (0.0 - (com[0] - q[0])) - kdx * comv[0] - kdphi * qd[2]
        tau[0] += float(np.clip(fb, -8.0, 8.0))
        return tau, kd


class FlipController:
    """翻身跳控制器：不对称起跳产生角动量 → 空中收拢加速旋转 → 转够展开 → 落地。
    p = [th1c, th2c, tau1, tau2, bias, kphi,
         th1t, th2t, t_tuck, rot_ext, th1l, th2l, kp_land, t_wait]
    bias: FIRE 时肩部前倾偏置(正=向前翻); t_tuck: 离地后收拢延迟; rot_ext: 展开触发角。"""

    PHASE_SETTLE, PHASE_FIRE, PHASE_FLIGHT, PHASE_TUCK, PHASE_EXTEND, PHASE_LAND = range(6)

    def __init__(self, p, kx=250.0, kdx=25.0):
        self.p0 = np.array(p, dtype=float)
        self.kx, self.kdx = kx, kdx
        self.reset()

    def reset(self):
        self.phase = self.PHASE_SETTLE
        self.t0 = 0.0
        self.t_fire = 0.0
        self.t_takeoff = None
        self.rot_unwrap = 0.0
        self.phi_prev = 0.0
        self.cycles = 0

    def _pd(self, sim, q, tgt, scale=1.0):
        return sim.kp * scale * (np.array(tgt) - q[3:6]), sim.kd * scale

    def __call__(self, t, q, qd, contact, sim):
        (th1c, th2c, tau1, tau2, bias, kphi,
         th1t, th2t, t_tuck, rot_ext, th1l, th2l, kp_land, t_wait) = self.p0
        # 展开累计角
        dphi = q[2] - self.phi_prev
        if abs(dphi) < np.pi:
            self.rot_unwrap += dphi
        self.phi_prev = q[2]
        dt_p = t - self.t0
        s3 = self.STAND_POSE[2]
        if self.phase == self.PHASE_SETTLE:
            tau, kd = self._pd(sim, q, (th1c, th2c, s3))
            com = sim.com_pos(q); comv = sim.com_vel(q, qd)
            tau[0] += self.kx * (0.0 - com[0]) - self.kdx * comv[0]
            if dt_p > t_wait and abs(com[0]) < 0.03 and abs(qd[2]) < 0.6:
                self.phase = self.PHASE_FIRE; self.t_fire = t
            return tau, kd
        if self.phase == self.PHASE_FIRE:
            tau = np.array([tau1 + bias, tau2, 0.0])
            if not contact:
                if self.t_takeoff is None:
                    self.t_takeoff = t
                if t - self.t_takeoff > t_tuck:
                    self.phase = self.PHASE_TUCK; self.t0 = t
            elif self.t_takeoff is not None and t - self.t_takeoff > 0.05:
                self.phase = self.PHASE_LAND; self.t0 = t   # 没跳起来
            elif t - self.t_fire > 0.45:
                self.phase = self.PHASE_FLIGHT; self.t0 = t
            return tau, np.zeros(3)
        if self.phase == self.PHASE_FLIGHT:  # 起跳失败残留
            tau, kd = self._pd(sim, q, (th1l, th2l, 0.0), 0.5)
            if contact:
                self.phase = self.PHASE_LAND; self.t0 = t
            return tau, kd
        if self.phase == self.PHASE_TUCK:
            tau, kd = self._pd(sim, q, (th1t, th2t, 0.0), 1.5)
            if abs(self.rot_unwrap) > rot_ext:
                self.phase = self.PHASE_EXTEND; self.t0 = t
            return tau, kd
        if self.phase == self.PHASE_EXTEND:
            tau, kd = self._pd(sim, q, (th1l, th2l, 0.0), 0.8)
            if contact:
                self.phase = self.PHASE_LAND; self.t0 = t
            return tau, kd
        tau, kd = self._pd(sim, q, (th1c, th2c, self.STAND_POSE[2]), kp_land)
        com = sim.com_pos(q); comv = sim.com_vel(q, qd)
        if dt_p > 0.1:
            tau[0] += self.kx * (0.0 - com[0]) - self.kdx * comv[0]
        return tau, kd
