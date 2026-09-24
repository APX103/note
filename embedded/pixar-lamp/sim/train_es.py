# -*- coding: utf-8 -*-
"""
CEM(交叉熵方法)策略搜索：台灯跳跃控制器的 CPU 训练。
阶段A：在自研平面仿真上做直接策略搜索（开环时序 + 线性姿态反馈），
验证"可学性"并产出第一版跳跃参数。GPU/PPO 属于阶段B（见方案文档）。

任务:
  hop    最大化腾空高度(离地后 COM 上升量)，要求落地基本直立
  travel 连续跳跃向 +x 移动，最大化位移并保持直立
  flip   翻身跳：起跳带角动量 + 空中收拢旋转 + 展开落地

用法: python3 train_es.py <task> [iters]
"""
import json
import os
import sys
import time
import numpy as np

from lamp_sim import Sim, JumpControllerV2, FlipController, NQ

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

# ---------------- 参数空间 ----------------
SPACE = {}

SPACE["hop"] = SPACE["travel"] = SPACE["leap"] = dict(
    names=["th1c", "th2c", "tau1", "tau2", "d1", "d2", "kphi", "kdphi",
           "th1l", "th2l", "kp_land", "t_wait", "stop2", "t_fire_max", "kx", "kdx", "com_ref"],
    bounds=np.array([
        [0.15, 1.00], [-3.00, -1.40], [-12.5, -2.0], [2.0, 12.5],
        [0.0, 0.25], [0.0, 0.25], [0.0, 80.0], [0.0, 1.0],
        [0.2, 1.2], [-2.6, -1.2], [0.4, 1.6], [0.45, 0.90],
        [-0.60, -0.05], [0.20, 0.50], [0.0, 400.0], [0.0, 60.0], [-0.045, 0.045]]),
    p0=np.array([0.5, -2.2, -7.0, 9.0, 0.02, 0.08, 30.0, 0.3,
                 0.6, -1.8, 0.8, 0.70, -0.30, 0.35, 200.0, 20.0, 0.0]))

SPACE["flip"] = dict(
    names=["th1c", "th2c", "tau1", "tau2", "bias", "kphi",
           "th1t", "th2t", "t_tuck", "rot_ext", "th1l", "th2l", "kp_land", "t_wait"],
    bounds=np.array([
        [0.15, 1.00], [-3.00, -1.40], [-12.5, -2.0], [2.0, 12.5],
        [-6.0, 6.0], [0.0, 60.0],
        [0.8, 2.2], [-3.0, -1.4], [0.0, 0.18], [2.0, 5.5],
        [0.2, 1.0], [-2.2, -1.0], [0.4, 1.6], [0.45, 0.90]]),
    p0=np.array([0.5, -2.2, -7.0, 9.0, 2.0, 20.0,
                 1.6, -2.6, 0.06, 5.0, 0.5, -1.8, 1.0, 0.70]))


def make_sim(k_spring=1.5):
    return Sim(k_spring=(k_spring, k_spring, 0.0))


def evaluate(p, task, seed=0, k_spring=1.5, T=None, det=False, tau_cap=None):
    """返回 (reward, info)。"""
    sim = make_sim(k_spring)
    if tau_cap is not None:
        sim.tau_peak = np.array([tau_cap, tau_cap, 1.2])
    rng = np.random.default_rng(seed)
    p2 = p.copy()
    if not det:
        p2[0] += rng.normal(0, 0.03)
        p2[1] += rng.normal(0, 0.05)
    if task == "flip":
        ctrl = FlipController(p2)
        T = T or 2.6
    else:
        ctrl = JumpControllerV2(p2, repeat=(task == "travel"))
        T = T or (3.5 if task == "travel" else (2.6 if task == "leap" else 2.2))
    q0 = np.zeros(NQ); q0[1] = 0.0005
    h = sim.run(ctrl, T, q0, np.zeros(NQ))
    b = h["best"]
    qe = h["q_end"]
    upright = bool(abs(qe[2]) < 0.30 and h["contact"][-1])
    fell = bool(abs(qe[2]) > 1.2)
    info = dict(apex_at=b["apex_at"], apex=b["apex"], v_takeoff=b["v_takeoff"],
                air_t=b["air_t"], peak_Fn=b["peak_Fn"],
                peak_tau=float(b["peak_tau"][:2].max()), x_end=float(qe[0]),
                upright=upright, fell=fell, cycles=h.get("cycles", 0))
    over_tau = max(0.0, b["peak_tau"][:2].max() - 12.5)
    # 物理合理性门限: 能量预算内 v<=6m/s, 腾空<=1m, 峰值Fn<=600N
    if h.get("diverged") or b["apex_at"] > 1.2 or abs(b["v_takeoff"]) > 6.0 or b["peak_Fn"] > 600.0:
        return -500.0, info
    if task == "hop":
        r = 100.0 * b["apex_at"] + (40.0 if upright else 0.0) - (20.0 if fell else 0.0) - 3.0 * over_tau
    elif task == "travel":
        phi_n = qe[2] % (2 * np.pi)
        if phi_n > np.pi:
            phi_n -= 2 * np.pi
        fell = bool(abs(phi_n) > 1.2)
        r = 100.0 * (qe[0] - q0[0]) + (60.0 if upright else 0.0) - (60.0 if fell else 0.0) \
            + 10.0 * min(b["apex_at"], 0.08) - 3.0 * over_tau
    elif task == "leap":
        phi_n = qe[2] % (2 * np.pi)
        if phi_n > np.pi:
            phi_n -= 2 * np.pi
        fell = bool(abs(phi_n) > 1.2)
        r = 100.0 * (qe[0] - q0[0]) + (60.0 if upright else 0.0) - (60.0 if fell else 0.0) \
            + 25.0 * min(b["apex_at"], 0.12) - 3.0 * over_tau
    else:  # flip
        rot = abs(getattr(ctrl, "rot_unwrap", 0.0))
        phi_end = qe[2] % (2 * np.pi)
        if phi_end > np.pi:
            phi_end -= 2 * np.pi
        landed_up = bool(abs(phi_end) < 0.5 and h["contact"][-1] and abs(qe[2]) < 4.0)
        info.update(rot=rot, phi_end=float(phi_end), landed_up=landed_up)
        r = (18.0 * min(rot, 2 * np.pi)) + (60.0 if landed_up else 0.0) \
            + 20.0 * min(b["apex_at"], 0.20) - (15.0 if fell and not landed_up else 0.0) - 3.0 * over_tau
    if not np.isfinite(r):
        return -500.0, info
    return r, info


def _worker_init():
    import warnings
    warnings.filterwarnings("ignore")
    np.seterr(all="ignore")


def _worker_eval(args):
    p, task, seed = args
    try:
        r, info = evaluate(p, task, seed=seed)
        if not np.isfinite(r):
            return -500.0, None
    except Exception:
        return -500.0, None
    return r, info


def cem(task, pop=40, elites=8, iters=60, seeds=2, workers=8, out=None,
        init_p=None, sig_scale=0.22):
    from multiprocessing import get_context
    sp = SPACE[task]
    lo, hi = sp["bounds"][:, 0], sp["bounds"][:, 1]
    mu = init_p.copy() if init_p is not None else sp["p0"].copy()
    sig = sig_scale * (hi - lo)
    rng = np.random.default_rng(7)
    hist = []
    best_overall = (-1e9, sp["p0"].copy())
    t_start = time.time()
    ctx = get_context("spawn")
    with ctx.Pool(workers, initializer=_worker_init) as pool:
        for it in range(iters):
            cand = np.clip(mu + sig * rng.standard_normal((pop - 1, len(mu))), lo, hi)
            batch = [(p, task, s) for p in cand for s in range(seeds)]
            batch += [(mu.copy(), task, s) for s in range(seeds)]
            results = pool.map(_worker_eval, batch)
            rs = np.array([r for r, _ in results])
            cand_scores = rs[:-seeds].reshape(pop - 1, seeds).mean(1)
            mu_score = rs[-seeds:].mean()
            order = np.argsort(-cand_scores)
            elite_idx = order[:elites]
            elites_p = cand[elite_idx]
            mu = np.clip(elites_p.mean(0), lo, hi)
            sig = np.clip(elites_p.std(0) + 0.02 * (hi - lo), 0.02 * (hi - lo), 0.5 * (hi - lo))
            best_r = float(max(cand_scores.max(), mu_score))
            best_p = cand[int(elite_idx[0])] if cand_scores.max() >= mu_score else mu.copy()
            r_det, best_info = evaluate(best_p, task, seed=0, det=True)
            if r_det > best_overall[0]:
                best_overall = (r_det, best_p.copy())
            hist.append(dict(iter=it, best=best_r, mu=float(mu_score),
                             elite_mean=float(cand_scores[elite_idx].mean()),
                             info=best_info))
            extra = f"rot={best_info.get('rot', 0):.2f}" if task == "flip" else f"x={best_info['x_end']:+.2f}"
            print(f"[{task}] it{it:02d} best={best_r:7.2f} mu={mu_score:7.2f} "
                  f"apex_at={best_info['apex_at']*100:5.1f}cm v_to={best_info['v_takeoff']:+.2f} "
                  f"{extra} upright={best_info['upright']}", flush=True)
    r_mu, info_mu = evaluate(mu, task, seed=0, det=True)
    if best_overall[0] > r_mu:
        mu = best_overall[1]
        r, info = evaluate(mu, task, seed=0, det=True)
        print(f"用历史最优替代均值策略: {r:.1f} > {r_mu:.1f}")
    else:
        r, info = r_mu, info_mu
    out_data = dict(task=task, params=dict(zip(sp["names"], mu.tolist())),
                    reward=r, info=info, history=hist,
                    wall_s=time.time() - t_start, pop=pop, iters=iters)
    if out:
        with open(out, "w") as f:
            json.dump(out_data, f, indent=1)
        print(f"saved -> {out}")
    return out_data


def hot_start(task, src_task="hop"):
    """用 src_task 的解作为 task 的初始均值(维度不足处用任务 p0 补齐)。"""
    f = os.path.join(RESULTS, f"cem_{src_task}.json")
    with open(f) as fh:
        sp0 = np.array(list(json.load(fh)["params"].values()))
    p0 = SPACE[task]["p0"].copy()
    n = min(len(sp0), len(p0))
    p0[:n] = sp0[:n]
    return p0


def polish(task, iters=12, out=None):
    """从已有结果出发的局部精修(小方差)。"""
    f = os.path.join(RESULTS, f"cem_{task}.json")
    with open(f) as fh:
        data = json.load(fh)
    p0 = np.array(list(data["params"].values()))
    sp = SPACE[task]
    if len(p0) < len(sp["p0"]):
        p0 = np.r_[p0, sp["p0"][len(p0):]]      # 补齐新增维度(如 com_ref)用默认值
    return cem(task, pop=24, elites=6, iters=iters, workers=8,
               out=out or f, init_p=p0, sig_scale=0.06)


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "hop"
    iters = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    os.makedirs(RESULTS, exist_ok=True)
    if task.endswith(":polish"):
        polish(task.split(":")[0], iters)
    elif task == "leap":
        p0 = hot_start("leap", "hop")
        p0[-1] = 0.03   # 前倾初始化: 直接进入"向前跳"盆地
        cem(task, iters=iters, out=os.path.join(RESULTS, f"cem_{task}.json"),
            init_p=p0, sig_scale=0.10)
    else:
        cem(task, iters=iters, out=os.path.join(RESULTS, f"cem_{task}.json"))
