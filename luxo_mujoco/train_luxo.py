import os
import sys

# Keep CPU usage reasonable on this machine (user cap ~50 %)
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"

import torch

torch.set_num_threads(4)

import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from luxo_env import LuxoJumpEnv


def make_env():
    def _init():
        return LuxoJumpEnv(frame_skip=5)
    return _init


def main():
    total_timesteps = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000

    env = DummyVecEnv([make_env()])

    # Slightly larger network and longer rollouts for this event-rich jump task.
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=128,
        n_epochs=5,
        gamma=0.99,
        gae_lambda=0.95,
        ent_coef=0.02,
        vf_coef=0.5,
        max_grad_norm=0.5,
        policy_kwargs=dict(net_arch=[256, 256]),
        device="cpu",
    )

    checkpoint_callback = CheckpointCallback(
        save_freq=50_000,
        save_path="./models/",
        name_prefix="luxo_ppo",
    )

    model.learn(total_timesteps=total_timesteps, callback=checkpoint_callback)
    model.save("models/luxo_ppo_final")
    print(f"Training finished. Final model saved to models/luxo_ppo_final.zip")


if __name__ == "__main__":
    main()
