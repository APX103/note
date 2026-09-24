# -*- coding: utf-8 -*-
"""
MuJoCo 渲染: 向前跳 GIF / 转向+前跳 GIF / 帧序列 PNG。
运行: 用 luxo_mujoco/.venv 的 python（mujoco + PIL）。
"""
import json
import os
import numpy as np
import mujoco
from PIL import Image, ImageDraw

from mujoco_train import Env, JumpControllerV2  # noqa: F401 (sys.path 已带 sim)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
FRAMES = os.path.join(RESULTS, "frames")
os.makedirs(FRAMES, exist_ok=True)

W, H = 960, 720


def render_episode(p, mode="side", turn_first=False, every=40, T=None,
                   gif_name="view_mj_leap.gif", frame_prefix=None):
    """跑一集并离屏渲染; every=每多少仿真步出一帧(0.04s) -> GIF 30fps ≈ 4.4x 慢放。"""
    env = Env()
    m, d = env.m, env.d
    T = T or (5.8 if turn_first else 4.6)
    ctrl_ = JumpControllerV2(np.asarray(p, float))
    env.reset()
    renderer = mujoco.Renderer(m, height=H, width=W)
    cam = mujoco.MjvCamera()
    frames = []
    phases = []
    zs = []
    n = int(T / m.opt.timestep)
    for i in range(n):
        q, qd = env.q_like(), env.qd_like()
        contact = d.ncon > 0
        t_ctrl = max(0.0, i * env.dt - 1.2) if turn_first else i * env.dt  # 转向预留1.2s
        tau, kd = ctrl_(t_ctrl, q, qd, contact, env)
        d.ctrl[0] = np.clip(tau[0] - kd[0] * qd[3], -12.5, 12.5)
        d.ctrl[1] = np.clip(tau[1] - kd[1] * qd[4], -12.5, 12.5)
        d.ctrl[2] = np.clip(tau[2] - kd[2] * qd[5], -1.2, 1.2)
        # 转向演示: 0.9s 斜坡转到 90°(慢转, 让地面摩擦抓住底盘)
        yaw_tgt = float(np.clip(i * env.dt / 0.9, 0.0, 1.0)) * (np.pi / 2) if turn_first else 0.0
        d.ctrl[3] = yaw_tgt
        mujoco.mj_step(m, d)
        if i % every == 0:
            # 相机跟拍 (lookat + 方位/仰角/距离)
            cam.lookat[:] = [d.qpos[0], d.qpos[1], 0.20]
            if mode == "side":
                cam.distance, cam.azimuth, cam.elevation = 1.30, -90, 8
            else:  # 3/4 视角
                cam.distance, cam.azimuth, cam.elevation = 1.45, -100, 22
            renderer.update_scene(d, camera=cam)
            img = renderer.render()
            frames.append(Image.fromarray(img).copy())
            phases.append(int(ctrl_.phase))
            zs.append(float(d.qpos[2]))
    renderer.close()
    # 信息条
    info = dict(x=float(d.qpos[0]), y=float(d.qpos[1]), yaw=float(d.qpos[7]),
                pitch=float(np.arctan2(2 * (d.qpos[3] * d.qpos[5] + d.qpos[6] * d.qpos[4]),
                                       1 - 2 * (d.qpos[5] ** 2 + d.qpos[4] ** 2))))
    out_gif = os.path.join(RESULTS, gif_name)
    frames[0].save(out_gif, save_all=True, append_images=frames[1:], duration=33, loop=0)
    if frame_prefix:
        for k, f in enumerate(frames):
            f.save(os.path.join(FRAMES, f"{frame_prefix}_{k:03d}.png"))
    with open(os.path.join(FRAMES, f"{frame_prefix or 'x'}_meta.json"), "w") as f:
        json.dump(dict(phases=phases, zs=zs, info=info, n=len(frames)), f)
    print(f"saved {out_gif} ({len(frames)} 帧) x={info['x']:+.3f} yaw={info['yaw']:+.2f}")
    return frames, phases


if __name__ == "__main__":
    with open(os.path.join(RESULTS, "mj_leap.json")) as f:
        p = np.array(json.load(f)["params"])
    render_episode(p, mode="side", gif_name="view_mj_leap.gif", frame_prefix="mj_leap")
    render_episode(p, mode="quarter", turn_first=True, gif_name="view_mj_turn_leap.gif",
                   frame_prefix="mj_turn")
