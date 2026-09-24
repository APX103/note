import os
import sys
import numpy as np
import imageio
import mujoco
import torch

torch.set_num_threads(4)

from stable_baselines3 import PPO
from luxo_env import LuxoJumpEnv


def main(model_path: str = "models/luxo_ppo_final.zip"):
    if not os.path.exists(model_path):
        print(f"Model not found: {model_path}")
        sys.exit(1)

    env = LuxoJumpEnv(render_mode="rgb_array")

    model = PPO.load(model_path, env=env, device="cpu")

    obs, _ = env.reset(seed=42)
    # Make it jump toward +x for the recording
    env.command = np.array([1.0, 0.0], dtype=np.float32)

    frames = []
    episode_reward = 0.0
    max_steps = 400

    for t in range(max_steps):
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        episode_reward += reward

        # Render every 5 simulation steps to keep GIF short
        if t % 5 == 0:
            frame = env.render()
            if frame is not None:
                frames.append(frame)

        if terminated or truncated:
            break

    env.close()

    if frames:
        gif_path = "rollout.gif"
        imageio.mimsave(gif_path, frames, fps=20)
        print(f"Saved rollout to {gif_path} ({len(frames)} frames), reward={episode_reward:.2f}")
    else:
        print("No frames captured.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "models/luxo_ppo_final.zip")
