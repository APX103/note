# -*- coding: utf-8 -*-
"""
MuJoCo 3D 训练：圆片底盘 + 双连杆 + 圆台灯罩 的向前跳。
复用 2D 阶段的 JumpControllerV2(结构化策略)与参数空间，物理引擎换成 MuJoCo，
以 2D 训练结果热启动。 运行: 用 luxo_mujoco/.venv 的 python。
"""
import json
import os
import sys
import time
import numpy as np

import mujoco

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "sim"))
from lamp_sim import JumpControllerV2  # noqa: E402

XML = os.path.join(HERE, "lamp3d.xml")
RESULTS = os.path.join(HERE, "results")
os.makedirs(RESULTS, exist_ok=True)
HOP2D = os.path.join(HERE, "..", "sim", "results", "cem_hop.json")

BOUNDS = np.array([
    [0.15, 1.60], [0.80, 2.60], [-12.5, -2.0], [-12.5, -2.0],
    [0.0, 0.25], [0.0, 0.25], [0.0, 80.0], [0.0, 1.0],
    [0.8, 2.40], [0.80, 2.40], [0.4, 1.6], [0.45, 0.90],
    [0.10, 0.80], [0.20, 0.50], [0.0, 400.0], [0.0, 60.0], [-0.045, 0.045]])


def base_pitch(d):
    w, x, y, z = d.qpos[3:7]
    return np.arctan2(2 * (w * y + z * x), 1 - 2 * (y * y + x * x))


class Env:
    """MuJoCo 环境适配器: 暴露 JumpControllerV2 需要的最小接口。"""

    def __init__(self, seed=0):
        self.m = mujoco.MjModel.from_xml_path(XML)
        self.d = mujoco.MjData(self.m)
        self.rng = np.random.default_rng(seed)
        self.kp = np.array([60.0, 60.0, 2.0])
        self.kd = np.array([3.0, 3.0, 0.1])
        self.dt = self.m.opt.timestep
        self.stand_com = None

    def q_like(self):
        """[x, y, phi, th1, th2, th3] + 关节角速度, 供控制器使用。
        x 恒 0: COM 反馈全部在"臂体坐标系"(按 yaw 反旋转), 保证转向后策略方向不变。"""
        q = np.array([0.0, self.d.qpos[2], base_pitch(self.d),
                      self.d.qpos[8], self.d.qpos[9], self.d.qpos[10]])
        return q

    def qd_like(self):
        qd = np.zeros(6)
        qd[0], qd[1] = self.d.qvel[0], self.d.qvel[2]
        qd[2] = self.d.qvel[4]
        qd[3:] = self.d.qvel[7:10]
        return qd

    def com_pos(self, q):
        com = self.d.subtree_com[1]
        yaw = self.d.qpos[7]
        dx, dy = com[0] - self.d.qpos[0], com[1] - self.d.qpos[1]
        bx = np.cos(-yaw) * dx - np.sin(-yaw) * dy   # 臂体系 x 偏移
        return np.array([bx, com[2]])

    def com_vel(self, q, qd):
        v = self.d.subtree_linvel[1]
        return np.array([v[0], v[2]])

    def reset(self, crouch_noise=0.03, hover=0.030):
        """台灯初始化: 关节由位置PD力锁在站姿, 整体半悬浮 ~3cm 出生后落下弹性落定。"""
        mujoco.mj_resetDataKeyframe(self.m, self.d, 0)
        self.x0, self.y0 = self.d.qpos[0], self.d.qpos[1]
        self.d.qpos[8] += self.rng.normal(0, crouch_noise)
        self.d.qpos[9] += self.rng.normal(0, crouch_noise * 1.5)
        self.d.qpos[2] += hover + self.rng.normal(0, 0.006)
        mujoco.mj_forward(self.m, self.d)

    def run(self, p, T=None, record=False, task="leap"):
        if task == "travel":
            ctrl_ = JumpControllerV2(np.asarray(p, float), repeat=True, stop_t=4.2)
            T = T or 6.5
        else:
            ctrl_ = JumpControllerV2(np.asarray(p, float))
            T = T or 4.6
        self._last_ctrl = ctrl_
        self.reset()
        dt = self.m.opt.timestep
        n = int(T / dt)
        rec = dict(t=[], q=[], com=[], contact=[], phase=[]) if record else None
        # 指标
        mujoco.mj_forward(self.m, self.d)
        com0z = None
        apex_air = 0.0
        air_streak = 0
        registered = False
        in_air_prev = False
        air_t = 0.0
        com_apex = -9.9
        for i in range(n):
            q = self.q_like(); qd = self.qd_like()
            contact = self.d.ncon > 0 and any(
                self.d.contact[k].geom1 == 0 or self.d.contact[k].geom2 == 0 for k in range(self.d.ncon))
            tau, kd = ctrl_(i * dt, q, qd, contact, self)
            self.d.ctrl[0] = np.clip(tau[0] - kd[0] * qd[3], -12.5, 12.5)
            self.d.ctrl[1] = np.clip(tau[1] - kd[1] * qd[4], -12.5, 12.5)
            self.d.ctrl[2] = np.clip(tau[2] - kd[2] * qd[5], -1.2, 1.2)
            self.d.ctrl[3] = 0.0
            mujoco.mj_step(self.m, self.d)
            comz = self.d.subtree_com[1][2]
            in_air = self.d.qpos[2] > 0.0135
            if in_air and i * dt > 0.5:
                air_streak += 1
                if air_streak * dt > 0.02:
                    if not registered:
                        registered = True
                    air_t += dt
                    com_apex = max(com_apex, comz)
            else:
                air_streak = 0
            if record and i % 8 == 0:
                rec["t"].append(i * dt)
                rec["q"].append(self.q_like().tolist())
                rec["com"].append([self.d.subtree_com[1][0], comz])
                rec["contact"].append(not in_air)
                rec["phase"].append(ctrl_.phase)
        apex_at = max(0.0, com_apex - 0.150) if registered else 0.0   # 相对站立COM抬升
        qe = self.q_like()
        sp1, sp2, _ = JumpControllerV2.STAND_POSE
        upright = bool(abs(base_pitch(self.d)) < 0.30 and not in_air
                       and abs(qe[3] - sp1) < 0.45 and abs(qe[4] - sp2) < 0.60)
        lamp_pose = bool(abs(base_pitch(self.d)) < 0.25 and not in_air
                         and abs(qe[3] - sp1) < 0.30 and abs(qe[4] - sp2) < 0.45
                         and np.abs(self.d.qvel).max() < 0.8)
        fell = bool(abs(base_pitch(self.d)) > 1.2)
        yaw0 = 0.0
        disp = np.array([self.d.qpos[0] - self.x0, self.d.qpos[1] - self.y0])
        heading = np.array([np.cos(self.d.qpos[7]), np.sin(self.d.qpos[7])])
        info = dict(x_end=float(disp @ heading), apex_at=apex_at, air_t=air_t, lamp_pose=lamp_pose,
                    upright=upright, fell=fell, phase_end=ctrl_.phase,
                    pitch_end=float(base_pitch(self.d)))
        if record:
            info["rec"] = rec
        return info


def reward_leap(info):
    # 目标: 稳稳向前跳 10cm(前方=肘弯开口方向): 10cm 处峰值、两侧衰减; 直立落地为硬要求
    x = max(0.0, info["x_end"])
    r = 600.0 * max(0.0, 1.0 - abs(x - 0.10) / 0.08) \
        + (120.0 if info["upright"] else 0.0) - (80.0 if info["fell"] else 0.0) \
        - 30.0 * abs(info["pitch_end"]) + 8.0 * min(info["apex_at"], 0.05) \
        + (80.0 if info["air_t"] > 0.06 else 0.0) - (40.0 if info["air_t"] < 0.03 and x > 0.02 else 0.0)
    if info["apex_at"] > 1.0 or abs(info["x_end"]) > 3.0:
        return -500.0
    return r


def reward_travel(info, ctrl=None):
    # 指令窗口(4.2s)连续挪动: 总位移 + 终态必须是台灯站姿(瘫蹲重罚) + 腾空
    x = max(0.0, info["x_end"])
    n_hops = max(1, getattr(ctrl, "cycles", 1) if ctrl is not None else 1)
    per_hop = min(x / n_hops / 0.10, 1.0)
    r = (400.0 * min(x, 0.60) + (150.0 if info.get("lamp_pose") else -120.0)
         - (100.0 if info["fell"] else 0.0) - 30.0 * abs(info["pitch_end"])
         + 60.0 * min(info["air_t"], 0.30) / 0.30 + 20.0 * per_hop
         - (250.0 if info["air_t"] < 0.12 and x > 0.05 else 0.0)      # 蹭地挪动=作弊
         - 600.0 * max(0.0, info["apex_at"] - 0.10))                  # 温和跳: 单跳腾空<10cm
    if info["apex_at"] > 1.0 or x > 3.0:
        return -500.0
    return r


_G = {}


def _worker_init():
    np.seterr(all="ignore")
    _G["env"] = Env()


_TASK = "leap"


def _worker_eval(args):
    p, seed = args
    try:
        env = _G["env"]
        info = env.run(p, task=_TASK)
        r = reward_travel(info, getattr(env, "_last_ctrl", None)) if _TASK == "travel" else reward_leap(info)
        return r, info
    except Exception:
        return -500.0, None


def cem_leap(iters=60, pop=64, elites=12, seeds=3, workers=6, out=None, init=None, sig_scale=0.12,
             task="leap"):
    global _TASK
    _TASK = task
    from multiprocessing import get_context
    lo, hi = BOUNDS[:, 0], BOUNDS[:, 1]
    # 天鹅颈几何从头学(与旧折叠方向不兼容)
    p0 = np.array([1.0, 1.8, -8.0, -8.0, 0.02, 0.08, 30.0, 0.3,
                   1.2, 1.8, 0.8, 0.70, 0.30, 0.35, 200.0, 20.0, -0.005])
    mu = np.array(init) if init is not None else p0
    if task == "travel":
        for fn in ("mj_travel.json", "mj_leap.json"):
            lf = os.path.join(RESULTS, fn)
            if os.path.exists(lf):
                with open(lf) as f:
                    mu = np.array(json.load(f)["params"])
                break
    sig = 0.15 * (hi - lo)
    rng = np.random.default_rng(11)
    hist = []
    best = (-1e9, mu.copy())
    t0 = time.time()
    ctx = get_context("spawn")
    with ctx.Pool(workers, initializer=_worker_init) as pool:
        for it in range(iters):
            cand = np.clip(mu + sig * rng.standard_normal((pop - 1, len(mu))), lo, hi)
            batch = [(p, s) for p in cand for s in range(seeds)] + [(mu, s) for s in range(seeds)]
            rs = pool.map(_worker_eval, batch)
            scores = np.array([r for r, _ in rs])
            cand_sc = scores[:-seeds].reshape(pop - 1, seeds).mean(1)
            mu_sc = scores[-seeds:].mean()
            order = np.argsort(-cand_sc)[:elites]
            ep = cand[order]
            mu = np.clip(ep.mean(0), lo, hi)
            sig = np.clip(ep.std(0) + 0.02 * (hi - lo), 0.02 * (hi - lo), 0.5 * (hi - lo))
            bi = int(order[0]) if cand_sc.max() >= mu_sc else -1
            bp = cand[bi] if bi >= 0 else mu.copy()
            _, binfo = _G_bench(bp, task)
            if cand_sc.max() >= mu_sc and cand_sc[bi] > best[0]:
                best = (cand_sc[bi], bp.copy())
            hist.append(dict(iter=it, best=float(max(cand_sc.max(), mu_sc)), mu=float(mu_sc),
                             info={k: binfo[k] for k in ("x_end", "apex_at", "upright", "air_t")}))
            print(f"[mj-{_TASK}] it{it:02d} best={max(cand_sc.max(), mu_sc):7.2f} mu={mu_sc:7.2f} "
                  f"x={binfo['x_end']:+.3f} apex={binfo['apex_at']*100:5.1f}cm upright={binfo['upright']}",
                  flush=True)
    # 最终: 均值 vs 历史最优
    env = Env()
    r_mu = reward_travel(env.run(mu, task=task), env._last_ctrl) if task == "travel" else reward_leap(env.run(mu, task=task))
    r_best = reward_travel(env.run(best[1], task=task), env._last_ctrl) if task == "travel" else reward_leap(env.run(best[1], task=task))
    use_best = r_best > r_mu
    final_p = best[1] if use_best else mu
    info = env.run(final_p, record=True, task=task)
    data = dict(params=final_p.tolist(), reward=max(r_mu, r_best), info={k: v for k, v in info.items() if k != "rec"},
                rec=info["rec"], history=hist, wall_s=time.time() - t0,
                note=f"MuJoCo 3D {task}; final={'best' if use_best else 'mu'}")
    out = out or os.path.join(HERE, "results", "mj_leap.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(data, f)
    print(f"saved -> {out} | x_end={info['x_end']:+.3f} apex={info['apex_at']*100:.1f}cm upright={info['upright']}")


def _G_bench(p, task="leap"):
    env = _G.get("env") or Env()
    return 0.0, env.run(p, task=task)


if __name__ == "__main__":
    iters = int(sys.argv[1]) if len(sys.argv) > 1 else 45
    task = sys.argv[2] if len(sys.argv) > 2 else "leap"
    if task == "travel":
        cem_leap(iters=iters, out=os.path.join(RESULTS, "mj_travel.json"), task="travel")
    else:
        cem_leap(iters=iters)
