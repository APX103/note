# -*- coding: utf-8 -*-
"""
MuJoCo 3D 训练（完整版）：天鹅颈台灯的三个任务。
  leap   单次向前跳 ~10cm（前方=肘弯开口方向）
  travel 指令窗口(4.2s)连续挪动 → 定住保持台灯站姿
  gated  指令位 50/50: 1=向前挪+天鹅颈, 0=定住抗外力侵扰(随机推力)
运行: 用 luxo_mujoco/.venv 的 python。 用法: python3 mujoco_train.py <iters> [leap|travel|gated]
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

BOUNDS = np.array([
    [-0.85, 0.10], [0.90, 2.00], [-12.5, 12.5], [-12.5, 12.5],
    [0.0, 0.25], [0.0, 0.25], [0.0, 300.0], [0.0, 3.0],
    [-0.7, 0.3], [0.90, 2.00], [0.4, 1.6], [0.45, 0.90],
    [0.05, 0.80], [0.20, 0.60], [0.0, 500.0], [0.0, 80.0], [-0.045, 0.045]])


def base_pitch(d):
    w, x, y, z = d.qpos[3:7]
    return np.arctan2(2 * (w * y + z * x), 1 - 2 * (y * y + x * x))


class Env:
    def __init__(self, seed=0):
        self.m = mujoco.MjModel.from_xml_path(XML)
        self.d = mujoco.MjData(self.m)
        self.rng = np.random.default_rng(seed)
        self.kp = np.array([60.0, 60.0, 2.0])
        self.kd = np.array([3.0, 3.0, 0.1])
        self.dt = self.m.opt.timestep

    # ---- 观测(控制器接口, 臂体坐标系) ----
    def q_like(self):
        return np.array([0.0, self.d.qpos[2], base_pitch(self.d),
                         self.d.qpos[8], self.d.qpos[9], self.d.qpos[10]])

    def qd_like(self):
        qd = np.zeros(6)
        qd[0], qd[1], qd[2] = self.d.qvel[0], self.d.qvel[2], self.d.qvel[4]
        qd[3:] = self.d.qvel[7:10]
        return qd

    def com_pos(self, q):
        com = self.d.subtree_com[1]
        yaw = self.d.qpos[7]
        dx, dy = com[0] - self.d.qpos[0], com[1] - self.d.qpos[1]
        bx = np.cos(-yaw) * dx - np.sin(-yaw) * dy
        return np.array([bx, com[2]])

    def com_vel(self, q, qd):
        v = self.d.subtree_linvel[1]
        return np.array([v[0], v[2]])

    def reset(self, crouch_noise=0.03, hover=0.030):
        mujoco.mj_resetDataKeyframe(self.m, self.d, 0)
        self.x0, self.y0 = self.d.qpos[0], self.d.qpos[1]
        self.d.qpos[8] += self.rng.normal(0, crouch_noise)
        self.d.qpos[9] += self.rng.normal(0, crouch_noise * 1.5)
        self.d.qpos[2] += hover + self.rng.normal(0, 0.006)
        mujoco.mj_forward(self.m, self.d)

    # ---- 主循环 ----
    def run(self, p, T=None, record=False, task="leap", cmd_schedule=None):
        if task == "travel":
            ctrl_ = JumpControllerV2(np.asarray(p, float), repeat=True, stop_t=4.2)
            T = T or 6.5
        elif task == "gated":
            ctrl_ = JumpControllerV2(np.asarray(p, float), repeat=True, stop_t=99.0)
            T = T or 7.0
        else:
            ctrl_ = JumpControllerV2(np.asarray(p, float))
            T = T or 4.6
        self._last_ctrl = ctrl_
        self.reset()
        dt = self.dt
        n = int(T / dt)

        # 指令调度(50/50)与随机推力
        if task == "gated":
            if cmd_schedule is None:
                t_off = float(self.rng.uniform(1.5, 4.0)) if self.rng.random() < 0.5 else 0.0
                cmd_schedule = (0.0, t_off)
            self._pushes = []
            for _ in range(int(self.rng.integers(1, 4))):
                t0p = float(self.rng.uniform(max(cmd_schedule[1], 0.9) + 0.15, T - 0.8))
                dur = float(self.rng.uniform(0.10, 0.25))
                fx = float(self.rng.uniform(2.0, 5.0)) * (-1 if self.rng.random() < 0.5 else 1)  # 戳(2-5N): 9N推翻力矩超底盘裕度
                fz = float(self.rng.uniform(-2.0, 2.0))
                self._pushes.append((t0p, dur, fx, fz))
        else:
            self._pushes = []
        head_bid = mujoco.mj_name2id(self.m, mujoco.mjtObj.mjOBJ_BODY, "head")

        rec = dict(t=[], q=[], com=[], contact=[], phase=[]) if record else None
        air_streak, registered, air_t, com_apex = 0, False, 0.0, -9.9
        hold_err_sum, hold_n, x_cmd = 0.0, 0, 0.0
        flip_rot = 0.0            # 单次滞空内的最大俯仰摆动(翻转度量)
        pitch_at_lift = 0.0
        pose_dev_sum, pose_dev_n = 0.0, 0   # 全程偏离冻结姿态(时间平均)
        for i in range(n):
            t_now = i * dt
            q, qd = self.q_like(), self.qd_like()
            contact = self.d.ncon > 0
            if task == "gated":
                c = 1 if (cmd_schedule[0] <= t_now < cmd_schedule[1]) else 0
                ctrl_.set_cmd(c, q, t_now)
                if c == 1:
                    x_cmd = float(self.d.qpos[0])
                if c == 0 and ctrl_._hold_tgt is not None and t_now > 0.8:
                    hold_err_sum += float(np.abs(np.array(q[3:6]) - ctrl_._hold_tgt).sum())
                    hold_n += 1
            tau, kd = ctrl_(t_now, q, qd, contact, self)
            self.d.ctrl[0] = np.clip(tau[0] - kd[0] * qd[3], -12.5, 12.5)
            self.d.ctrl[1] = np.clip(tau[1] - kd[1] * qd[4], -12.5, 12.5)
            self.d.ctrl[2] = np.clip(tau[2] - kd[2] * qd[5], -1.2, 1.2)
            self.d.ctrl[3] = 0.0
            if self._pushes:
                self.d.xfrc_applied[:] = 0
                for (pt0, pdur, pfx, pfz) in self._pushes:
                    if pt0 <= t_now < pt0 + pdur:
                        self.d.xfrc_applied[head_bid] = [pfx, 0.0, pfz, 0, 0, 0]
            mujoco.mj_step(self.m, self.d)
            if self._pushes:
                self.d.xfrc_applied[:] = 0
            comz = self.d.subtree_com[1][2]
            in_air = self.d.qpos[2] > 0.0135
            if task in ("travel", "gated") and t_now > 0.5:
                sp = JumpControllerV2.STAND_POSE
                pose_dev_sum += abs(q[3]-sp[0]) + abs(q[4]-sp[1]) + abs(q[5]-sp[2])
                pose_dev_n += 1
            if in_air and t_now > 0.5:
                if air_streak == 0:
                    pitch_at_lift = base_pitch(self.d)
                air_streak += 1
                if air_streak * dt > 0.02:
                    registered = True
                    air_t += dt
                    com_apex = max(com_apex, comz)
                    flip_rot = max(flip_rot, abs(base_pitch(self.d) - pitch_at_lift))
            else:
                air_streak = 0
            if record and i % 8 == 0:
                rec["t"].append(t_now)
                rec["q"].append(self.q_like().tolist())
                rec["com"].append([self.d.subtree_com[1][0], comz])
                rec["contact"].append(not in_air)
                rec["phase"].append(ctrl_.phase)
        apex_at = max(0.0, com_apex - 0.150) if registered else 0.0
        pose_dev = (pose_dev_sum / max(1, pose_dev_n)) if pose_dev_n else 0.0
        disp = np.array([self.d.qpos[0] - self.x0, self.d.qpos[1] - self.y0])
        yaw = self.d.qpos[7]
        heading = np.array([np.cos(yaw), np.sin(yaw)])
        qe = self.q_like()
        sp1, sp2, _ = JumpControllerV2.STAND_POSE
        pitch_e = base_pitch(self.d)
        lamp_pose = bool(abs(pitch_e) < 0.25 and not in_air
                         and abs(qe[3] - sp1) < 0.30 and abs(qe[4] - sp2) < 0.45
                         and np.abs(self.d.qvel).max() < 0.8)
        deform = (abs(qe[3] - sp1) + abs(qe[4] - sp2) + abs(qe[5] - JumpControllerV2.STAND_POSE[2]))
        info = dict(x_end=float(disp @ heading), apex_at=apex_at, air_t=air_t, flip_rot=flip_rot,
                    pose_dev=pose_dev,
                    deform=deform, lamp_pose=lamp_pose, x_cmd=x_cmd,
                    hold_err=(hold_err_sum / max(1, hold_n)) if hold_n else 0.0,
                    n_push=len(self._pushes),
                    upright=bool(abs(pitch_e) < 0.30 and not in_air),
                    fell=bool(abs(pitch_e) > 1.2), pitch_end=float(pitch_e),
                    cycles=int(ctrl_.cycles))
        if record:
            info["rec"] = rec
        return info


# ---------------- 奖励 ----------------
def reward_leap(info, ctrl=None):
    x = max(0.0, info["x_end"])
    r = 600.0 * max(0.0, 1.0 - abs(x - 0.10) / 0.08) \
        + (120.0 if info["upright"] else 0.0) - (80.0 if info["fell"] else 0.0) \
        - 30.0 * abs(info["pitch_end"]) + 8.0 * min(info["apex_at"], 0.05) \
        + (80.0 if info["air_t"] > 0.06 else 0.0) \
        - (40.0 if info["air_t"] < 0.03 and x > 0.02 else 0.0)
    r -= 400.0 * max(0.0, info["flip_rot"] - 0.35)     # 空中翻转: 0.35rad内正常晃, 超过重罚(咚!)
    r -= 120.0 * min(info["deform"], 1.0)              # 跳完变形(不回冻结姿态)
    r -= 400.0 * max(0.0, info["flip_rot"] - 0.35)     # 空中翻转: 0.35rad内正常晃, 超过重罚(咚!)
    r -= 120.0 * min(info["deform"], 1.0)              # 跳完变形(不回冻结姿态)
    r -= 400.0 * max(0.0, info["flip_rot"] - 0.35)     # 空中翻转: 0.35rad内正常晃, 超过重罚(咚!)
    r -= 120.0 * min(info["deform"], 1.0)              # 跳完变形(不回冻结姿态)
    if info["apex_at"] > 1.0 or abs(info["x_end"]) > 3.0:
        return -500.0
    return r


_STAGE = os.environ.get("MJ_STAGE", "2")


def reward_travel(info, ctrl=None):
    x = max(0.0, info["x_end"])
    n_hops = max(1, info.get("cycles", 1))
    per_hop = min(x / n_hops / 0.10, 1.0)
    r = (400.0 * min(x, 0.60) + (150.0 if info.get("lamp_pose") else -120.0)
         - (100.0 if info["fell"] else 0.0) - 30.0 * abs(info["pitch_end"])
         + 60.0 * min(info["air_t"], 0.30) / 0.30 + 20.0 * per_hop
         - (250.0 if _STAGE == "2" and info["air_t"] < 0.12 and x > 0.05 else 0.0)
         - (150.0 if _STAGE == "2" else 0.0) * max(0.0, info["apex_at"] - 0.10))
    if _STAGE == "2":
        r -= 400.0 * max(0.0, info["flip_rot"] - 0.35)
        r -= 120.0 * min(info["deform"], 1.0)
        r -= 500.0 * max(0.0, info.get("pose_dev", 0.0) - 0.15)   # 跳跃全程姿态贴近冻结姿态
    if info["apex_at"] > 1.0 or x > 3.0:
        return -500.0
    return r


def reward_gated(info, ctrl=None):
    x = max(0.0, info["x_cmd"])
    r = (400.0 * min(x, 0.40)
         + (150.0 if info.get("lamp_pose") else -120.0)
         - (150.0 if info["fell"] else 0.0)
         - 40.0 * abs(info["pitch_end"])
         + (40.0 if info["air_t"] > 0.05 else 0.0)
         - 300.0 * min(info["hold_err"], 0.6) / 0.6)
    r -= 400.0 * max(0.0, info["flip_rot"] - 0.35)     # 空中翻转: 0.35rad内正常晃, 超过重罚(咚!)
    r -= 120.0 * min(info["deform"], 1.0)              # 跳完变形(不回冻结姿态))
    if info["apex_at"] > 1.0 or abs(info["x_end"]) > 3.0:
        return -500.0
    return r


REWARDS = dict(leap=reward_leap, travel=reward_travel, gated=reward_gated)
INIT_FILES = dict(leap=("mj_travel.json",), travel=("mj_travel.json", "mj_leap.json"),
                  gated=("mj_travel.json",))

_G = {}
_TASK = "leap"


def _worker_init():
    np.seterr(all="ignore")
    _G["env"] = Env()


def _worker_eval(args):
    p, seed = args
    try:
        info = _G["env"].run(p, task=_TASK)
        r = REWARDS[_TASK](info, _G["env"]._last_ctrl)
        return (r if np.isfinite(r) else -500.0), info
    except Exception:
        return -500.0, None


def cem(iters=45, pop=64, elites=12, seeds=3, workers=6, out=None, task="leap"):
    global _TASK
    _TASK = task
    lo, hi = BOUNDS[:, 0], BOUNDS[:, 1]
    p0 = np.array([0.0, 1.9, -8.0, -8.0, 0.02, 0.08, 30.0, 0.3,
                   1.2, 1.8, 0.8, 0.70, 0.30, 0.35, 200.0, 20.0, -0.005])
    mu = p0.copy()
    for fn in INIT_FILES[task]:
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
    from multiprocessing import get_context
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
            mu = np.clip(cand[order].mean(0), lo, hi)
            sig = np.clip(cand[order].std(0) + 0.02 * (hi - lo), 0.02 * (hi - lo), 0.5 * (hi - lo))
            bi = int(order[0]) if cand_sc.max() >= mu_sc else -1
            bp = cand[bi] if bi >= 0 else mu.copy()
            if max(cand_sc.max(), mu_sc) > best[0]:
                best = (max(cand_sc.max(), mu_sc), bp.copy())
            binfo = _G.setdefault("env", Env()).run(bp, task=task)
            hist.append(dict(iter=it, best=float(max(cand_sc.max(), mu_sc)), mu=float(mu_sc),
                             info={k: binfo[k] for k in ("x_end", "apex_at", "lamp_pose", "air_t")}))
            print(f"[mj-{task}] it{it:02d} best={max(cand_sc.max(), mu_sc):7.2f} mu={mu_sc:7.2f} "
                  f"x={binfo['x_end']:+.3f} apex={binfo['apex_at']*100:5.1f}cm lamp={binfo['lamp_pose']}",
                  flush=True)
    env = Env()
    rw = REWARDS[task]

    def _r(pp):
        return rw(env.run(pp, task=task), env._last_ctrl)

    r_mu, r_best = _r(mu), _r(best[1])
    final_p = best[1] if r_best > r_mu else mu
    info = env.run(final_p, record=True, task=task)
    data = dict(params=final_p.tolist(), reward=max(r_mu, r_best),
                info={k: v for k, v in info.items() if k != "rec"},
                rec=info.get("rec"), history=hist, wall_s=time.time() - t0,
                note=f"MuJoCo 3D {task}; final={'best' if r_best > r_mu else 'mu'}")
    out = out or os.path.join(RESULTS, f"mj_{task}.json")
    with open(out, "w") as f:
        json.dump(data, f)
    print(f"saved -> {out} | x={info['x_end']:+.3f} apex={info['apex_at']*100:.1f}cm "
          f"lamp={info['lamp_pose']} fell={info['fell']}")


if __name__ == "__main__":
    iters = int(sys.argv[1]) if len(sys.argv) > 1 else 45
    task = sys.argv[2] if len(sys.argv) > 2 else "leap"
    assert task in ("leap", "travel", "gated"), f"未知任务 {task}"
    cem(iters=iters, task=task)
