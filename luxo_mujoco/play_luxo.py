import os
import sys
import numpy as np
import imageio
import mujoco
import torch

torch.set_num_threads(4)

from stable_baselines3 import PPO
from luxo_env import LuxoJumpEnv


def render_with_camera(env, cam):
    env.renderer.update_scene(env.data, camera=cam)
    return env.renderer.render()


def main(model_path: str = "models/luxo_ppo_final.zip"):
    if not os.path.exists(model_path):
        print(f"Model not found: {model_path}")
        sys.exit(1)

    env = LuxoJumpEnv(render_mode="rgb_array")
    model = PPO.load(model_path, env=env, device="cpu")

    obs, _ = env.reset(seed=42)
    env.command = np.array([1.0, 0.0], dtype=np.float32)

    # Side-view camera: follow the base, looking from the side (y-axis).
    side_cam = mujoco.MjvCamera()
    side_cam.type = mujoco.mjtCamera.mjCAMERA_TRACKING
    side_cam.trackbodyid = env.model.body("base").id
    side_cam.distance = 0.7
    side_cam.azimuth = 90.0
    side_cam.elevation = -5.0

    # Iso camera.
    iso_cam = mujoco.MjvCamera()
    iso_cam.type = mujoco.mjtCamera.mjCAMERA_TRACKING
    iso_cam.trackbodyid = env.model.body("base").id
    iso_cam.distance = 0.7
    iso_cam.azimuth = 45.0
    iso_cam.elevation = -20.0

    side_frames = []
    iso_frames = []
    episode_reward = 0.0
    max_steps = 500
    infos = []

    for t in range(max_steps):
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        episode_reward += reward
        infos.append(info)

        if t % 3 == 0:
            side_frames.append(render_with_camera(env, side_cam))
            iso_frames.append(render_with_camera(env, iso_cam))

        if terminated or truncated:
            break

    env.close()

    if side_frames:
        imageio.mimsave("rollout_side.gif", side_frames, fps=20)
        imageio.mimsave("rollout_iso.gif", iso_frames, fps=20)
        print(f"Saved rollout_side.gif / rollout_iso.gif ({len(side_frames)} frames), reward={episode_reward:.2f}")

        last_info = infos[-1]
        start_x = 0.0  # approx, since we reset seed=42
        final_x = last_info.get("base_x", 0.0)
        print(f"Final base x = {final_x:.3f} m (target ~0.10 m)")
        print(f"Max air z    = {last_info.get('max_air_z', 0.0):.3f} m")
        print(f"Takeoff vz   = {last_info.get('takeoff_vz', 0.0):.3f} m/s")
        print(f"Takeoff vx   = {last_info.get('takeoff_vx', 0.0):.3f} m/s")
    else:
        print("No frames captured.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "models/luxo_ppo_final.zip")
