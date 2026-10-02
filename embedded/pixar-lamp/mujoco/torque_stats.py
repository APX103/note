# -*- coding: utf-8 -*-
"""
torque_stats.py — 采集训练策略的各关节电机负载: 峰值力矩/持续时间/转速/功率。
运行: luxo_mujoco/.venv/bin/python torque_stats.py
输出: results/torque_stats.json + fig_torque.png (相对路径)
"""
import sys
import os
import json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mujoco  # noqa: E402
from mujoco_train import Env, JumpControllerV2  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")

JOINTS = ["th1_肩(竖臂)", "th2_肘(弯钩)", "th3_颈(灯罩)", "yaw_偏航"]


def run_collect(env, p, task, cmd_schedule=None, T=None):
    """跑一集, 逐ms记录各关节电机指令力矩/角速度/功率(不含弹簧等被动项)。"""
    if task == "travel":
        ctrl_ = JumpControllerV2(np.asarray(p, float), repeat=True, stop_t=4.2)
        T = T or 6.5
    elif task == "gated":
        ctrl_ = JumpControllerV2(np.asarray(p, float), repeat=True, stop_t=99.0)
        T = T or 7.0
    else:
        ctrl_ = JumpControllerV2(np.asarray(p, float))
        T = T or 4.6
    env.reset()
    dt = env.dt
    n = int(T / dt)
    head_bid = mujoco.mj_name2id(env.m, mujoco.mjtObj.mjOBJ_BODY, "head")
    pushes = []
    if task == "gated":
        if cmd_schedule is None:
            t_off = float(env.rng.uniform(1.5, 4.0)) if env.rng.random() < 0.5 else 0.0
            cmd_schedule = (0.0, t_off)
        for _ in range(int(env.rng.integers(1, 4))):
            t0p = float(env.rng.uniform(max(cmd_schedule[1], 0.9) + 0.15, T - 0.8))
            dur = float(env.rng.uniform(0.10, 0.25))
            fx = float(env.rng.uniform(2.0, 5.0)) * (-1 if env.rng.random() < 0.5 else 1)
            pushes.append((t0p, dur, fx))
    tau_log, vel_log = [], []
    for i in range(n):
        t_now = i * dt
        q, qd = env.q_like(), env.qd_like()
        contact = env.d.ncon > 0
        if task == "gated":
            c = 1 if (cmd_schedule[0] <= t_now < cmd_schedule[1]) else 0
            ctrl_.set_cmd(c, q, t_now)
        tau, kd = ctrl_(t_now, q, qd, contact, env)
        ctrl3 = 0.0
        env.d.ctrl[0] = np.clip(tau[0] - kd[0] * qd[3], -12.5, 12.5)
        env.d.ctrl[1] = np.clip(tau[1] - kd[1] * qd[4], -12.5, 12.5)
        env.d.ctrl[2] = np.clip(tau[2] - kd[2] * qd[5], -1.2, 1.2)
        # yaw: 记录转向伺服所需的力矩(PD 跟踪 90° 目标)
        if task == "turn":
            ctrl3 = np.clip(30.0 * (np.pi / 2 - q[0] * 0) - 6.0 * env.d.qvel[6], -12.5, 12.5)
        env.d.ctrl[3] = ctrl3
        if pushes:
            env.d.xfrc_applied[:] = 0
            for (pt0, pdur, pfx) in pushes:
                if pt0 <= t_now < pt0 + pdur:
                    env.d.xfrc_applied[head_bid] = [pfx, 0, 0, 0, 0, 0]
        mujoco.mj_step(env.m, env.d)
        if pushes:
            env.d.xfrc_applied[:] = 0
        tau_log.append([env.d.ctrl[0], env.d.ctrl[1], env.d.ctrl[2], env.d.ctrl[3]])
        vel_log.append([qd[3], qd[4], qd[5], env.d.qvel[6]])
    w, x, y, z = env.d.qpos[3:7]
    pitch_end = abs(np.arctan2(2 * (w * y + z * x), 1 - 2 * (y * y + x * x)))
    return np.array(tau_log), np.array(vel_log), (pitch_end < 1.2)


def stats_of(tau, vel, dt):
    """每关节: 峰值力矩/RMS/持续时间@阈值/峰值转速/峰值功率/平均功率"""
    out = []
    for j in range(4):
        t, w = tau[:, j], vel[:, j]
        a = np.abs(t)
        p = np.abs(t * w)
        out.append(dict(
            peak_tau=float(a.max()), rms_tau=float(np.sqrt((t ** 2).mean())),
            t_over_50pct=float((a > 0.5 * a.max()).sum() * dt),
            t_over_6Nm=float((a > 6.0).sum() * dt),
            t_over_9Nm=float((a > 9.0).sum() * dt),
            peak_vel=float(np.abs(w).max()),
            peak_power=float(p.max()), mean_power=float(p.mean()),
            total_work_J=float(np.sum(p) * dt)))
    return out


def main():
    tasks = {}
    for name in ("travel", "leap", "gated"):
        f = os.path.join(RESULTS, f"mj_{name}.json")
        if os.path.exists(f):
            with open(f) as fh:
                tasks[name] = np.array(json.load(fh)["params"])

    # 偏航转向工况: 慢斜坡转90°, 记录伺服力矩
    yaw_tau = []
    env = Env(seed=7)
    env.reset()
    for i in range(int(2.5 / env.dt)):
        t = i * env.dt
        tgt = float(np.clip(t / 1.5, 0, 1)) * np.pi / 2
        ctrl3 = np.clip(30.0 * (tgt - env.d.qpos[7]) - 6.0 * env.d.qvel[6], -12.5, 12.5)
        q, qd = env.q_like(), env.qd_like()
        contact = env.d.ncon > 0
        tau, kd = JumpControllerV2(tasks.get("travel", np.zeros(17)), repeat=True, stop_t=99)(t, q, qd, contact, env)
        env.d.ctrl[0] = np.clip(tau[0] - kd[0] * qd[3], -12.5, 12.5)
        env.d.ctrl[1] = np.clip(tau[1] - kd[1] * qd[4], -12.5, 12.5)
        env.d.ctrl[2] = np.clip(tau[2] - kd[2] * qd[5], -1.2, 1.2)
        env.d.ctrl[3] = ctrl3
        mujoco.mj_step(env.m, env.d)
        yaw_tau.append([0, 0, 0, ctrl3])
    report = {"per_task": {"yaw转向": [dict() for _ in range(4)]}, "worst_case": {}}
    series_for_fig = None
    for name, p in tasks.items():
        if name == "gated":
            runs = [("gated/1态", (0.0, 3.0)), ("gated/0态抗推", (0.0, 0.0))]
        else:
            runs = [(name, None)]
        for label, sched in runs:
            all_stats = []
            for seed in range(5):
                env = Env(seed=1000 + seed)
                tau, vel, ok = run_collect(env, p, "gated" if label.startswith("gated") else name,
                                           cmd_schedule=sched)
                if ok:
                    all_stats.append(stats_of(tau, vel, env.dt))
                if label == "travel" and seed == 0:
                    series_for_fig = (tau.copy(), vel.copy(), env.dt)
            if not all_stats:
                continue
            agg = []
            for j in range(4):
                agg.append(dict(
                    peak_tau=max(s[j]["peak_tau"] for s in all_stats),
                    rms_tau=float(np.mean([s[j]["rms_tau"] for s in all_stats])),
                    t_over_50pct=max(s[j]["t_over_50pct"] for s in all_stats),
                    t_over_6Nm=max(s[j]["t_over_6Nm"] for s in all_stats),
                    t_over_9Nm=max(s[j]["t_over_9Nm"] for s in all_stats),
                    peak_vel=max(s[j]["peak_vel"] for s in all_stats),
                    peak_power=max(s[j]["peak_power"] for s in all_stats),
                    total_work_J=float(np.mean([s[j]["total_work_J"] for s in all_stats]))))
            report["per_task"][label] = agg
        ys = stats_of(np.array(yaw_tau), np.zeros((len(yaw_tau), 4)), env.dt)
        report["per_task"]["yaw转向"] = ys
    # 最坏情况(跳跃类任务; yaw 单独用转向工况)
    for j in range(4):
        report["worst_case"][JOINTS[j]] = {
            k: max(report["per_task"][lab][j][k] for lab in report["per_task"])
            for k in ("peak_tau", "rms_tau", "t_over_50pct", "t_over_6Nm", "t_over_9Nm",
                      "peak_vel", "peak_power")}
    with open(os.path.join(RESULTS, "torque_stats.json"), "w") as f:
        json.dump(report, f, indent=1, ensure_ascii=False)
    print(json.dumps(report["worst_case"], indent=1, ensure_ascii=False))
    return series_for_fig


if __name__ == "__main__":
    main()
