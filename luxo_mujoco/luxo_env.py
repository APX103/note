import numpy as np
import gymnasium as gym
import mujoco


class LuxoJumpEnv(gym.Env):
    """
    A MuJoCo-Gymnasium environment for a Pixar-style Luxo lamp that learns
    to jump in a commanded horizontal direction.
    """

    metadata = {"render_modes": ["rgb_array"], "render_fps": 50}

    def __init__(
        self,
        xml_path: str = "luxo_lamp.xml",
        frame_skip: int = 1,
        max_episode_steps: int = 2500,
        cmd_scale: float = 2.0,
        height_scale: float = 1.0,
        takeoff_scale: float = 5.0,
        up_vel_scale: float = 0.5,
        alive_bonus: float = 0.05,
        energy_weight: float = 0.02,
        smooth_weight: float = 0.05,
        upright_weight: float = 0.2,
        render_mode: str | None = None,
    ):
        super().__init__()
        self.xml_path = xml_path
        self.frame_skip = frame_skip
        self.max_episode_steps = max_episode_steps

        self.cmd_scale = cmd_scale
        self.height_scale = height_scale
        self.takeoff_scale = takeoff_scale
        self.up_vel_scale = up_vel_scale
        self.alive_bonus = alive_bonus
        self.energy_weight = energy_weight
        self.smooth_weight = smooth_weight
        self.upright_weight = upright_weight
        self.render_mode = render_mode

        self.model = mujoco.MjModel.from_xml_path(self.xml_path)
        self.data = mujoco.MjData(self.model)

        # Number of actuated joints (5 hinge joints after the base freejoint)
        self.nu = self.model.nu
        self.n_actuated = self.nu

        # Actuator ranges for mapping [-1, 1] actions to joint setpoints
        self.ctrl_low = self.model.actuator_ctrlrange[:, 0].copy()
        self.ctrl_high = self.model.actuator_ctrlrange[:, 1].copy()
        self.ctrl_mid = (self.ctrl_low + self.ctrl_high) / 2.0
        self.ctrl_rng = (self.ctrl_high - self.ctrl_low) / 2.0

        # Freejoint (7 qpos, 6 qvel) + 5 hinge joints
        self.nq = self.model.nq
        self.nv = self.model.nv
        self.base_qpos_offset = 7
        self.base_qvel_offset = 6

        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(self.nu,), dtype=np.float32)

        obs_dim = (
            3                        # base position
            + 4                      # base quaternion
            + 3                      # base linear velocity
            + 3                      # base angular velocity
            + self.n_actuated        # joint positions
            + self.n_actuated        # joint velocities
            + self.nu                # previous action
            + 2                      # command direction
            + 1                      # base contact flag
        )
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(obs_dim,), dtype=np.float32
        )

        self.command = np.array([1.0, 0.0], dtype=np.float32)
        self.last_action = np.zeros(self.nu, dtype=np.float32)
        self.last_pos = np.zeros(2, dtype=np.float32)
        self.steps = 0

        if self.render_mode == "rgb_array":
            self.renderer = mujoco.Renderer(self.model, height=480, width=640)
        else:
            self.renderer = None

    def _get_obs(self) -> np.ndarray:
        q = self.data.qpos
        v = self.data.qvel

        base_pos = q[:3].astype(np.float32)
        base_quat = q[3:7].astype(np.float32)  # w, x, y, z
        base_lin = v[:3].astype(np.float32)
        base_ang = v[3:6].astype(np.float32)

        jnt_pos = q[self.base_qpos_offset : self.base_qpos_offset + self.n_actuated].astype(np.float32)
        jnt_vel = v[self.base_qvel_offset : self.base_qvel_offset + self.n_actuated].astype(np.float32)

        # Simple contact flag: is the base touching the ground?
        contact_flag = 0.0
        for i in range(self.data.ncon):
            c = self.data.contact[i]
            if (c.geom1 == self.model.geom("floor").id and c.geom2 == self.model.geom("base_geom").id) or \
               (c.geom2 == self.model.geom("floor").id and c.geom1 == self.model.geom("base_geom").id):
                contact_flag = 1.0
                break

        obs = np.concatenate(
            [
                base_pos,
                base_quat,
                base_lin,
                base_ang,
                jnt_pos,
                jnt_vel,
                self.last_action,
                self.command,
                [contact_flag],
            ]
        )
        return obs

    def _set_ctrl(self, action: np.ndarray):
        """Map normalized action [-1, 1] to actuator ctrl range."""
        self.data.ctrl[:] = self.ctrl_mid + action * self.ctrl_rng

    def reset(self, seed: int | None = None, options: dict | None = None):
        super().reset(seed=seed)
        if seed is not None:
            np.random.seed(seed)

        mujoco.mj_resetData(self.model, self.data)
        key_id = self.model.key("home").id
        mujoco.mj_resetDataKeyframe(self.model, self.data, key_id)

        # Sample a random horizontal jump direction
        theta = self.np_random.uniform(0.0, 2.0 * np.pi)
        self.command = np.array([np.cos(theta), np.sin(theta)], dtype=np.float32)

        # Hold home pose briefly so the robot does not collapse before first action
        home_ctrl = self.data.qpos[self.base_qpos_offset : self.base_qpos_offset + self.n_actuated].copy()
        self.data.ctrl[:] = home_ctrl
        for _ in range(20):
            mujoco.mj_step(self.model, self.data)

        self.last_action = np.zeros(self.nu, dtype=np.float32)
        self.last_pos = self.data.qpos[:2].copy()
        self.steps = 0

        return self._get_obs(), {}

    def step(self, action: np.ndarray):
        action = np.clip(action, -1.0, 1.0).astype(np.float32)
        self._set_ctrl(action)

        for _ in range(self.frame_skip):
            mujoco.mj_step(self.model, self.data)

        self.steps += 1

        # Reward: getting airborne / pushing off
        base_z = self.data.qpos[2]
        base_lin = self.data.qvel[:3]
        flight_factor = max(0.0, min(1.0, (base_z - 0.10) / 0.05))

        r_takeoff = max(0.0, base_z - 0.08) * self.takeoff_scale
        r_up_vel = max(0.0, base_lin[2]) * self.up_vel_scale
        r_height = max(0.0, base_z - 0.12) * self.height_scale

        # Reward: horizontal movement, but only while the base is off the ground
        pos = self.data.qpos[:2]
        delta = pos - self.last_pos
        self.last_pos = pos.copy()
        r_cmd = np.dot(delta, self.command) * self.cmd_scale * flight_factor

        # Penalty: energy / actuator effort
        r_energy = -np.sum(np.square(action)) * self.energy_weight

        # Penalty: action rate (smooth control)
        r_smooth = -np.sum(np.square(action - self.last_action)) * self.smooth_weight
        self.last_action = action.copy()

        # Penalty: base tilt (keep base z-axis close to world z-axis)
        xmat = self.data.body("base").xmat.reshape(3, 3)
        base_z_axis = xmat[:, 2]
        r_upright = (base_z_axis[2] - 1.0) * self.upright_weight

        reward = float(r_cmd + r_takeoff + r_up_vel + r_height + self.alive_bonus + r_energy + r_smooth + r_upright)

        # Termination conditions
        terminated = False
        if base_z < 0.03 or base_z > 1.5 or not np.isfinite(base_z):
            terminated = True
        # If the base tilts too far, the lamp has fallen over
        if base_z_axis[2] < 0.5:
            terminated = True

        truncated = self.steps >= self.max_episode_steps

        info = {
            "r_cmd": r_cmd,
            "r_takeoff": r_takeoff,
            "r_up_vel": r_up_vel,
            "r_height": r_height,
            "r_energy": r_energy,
            "r_smooth": r_smooth,
            "r_upright": r_upright,
            "base_z": base_z,
        }

        return self._get_obs(), reward, terminated, truncated, info

    def render(self):
        if self.renderer is None:
            return None
        self.renderer.update_scene(self.data)
        return self.renderer.render()

    def close(self):
        if self.renderer is not None:
            self.renderer.close()


if __name__ == "__main__":
    env = LuxoJumpEnv()
    obs, _ = env.reset()
    print("obs shape:", obs.shape, "action shape:", env.action_space.shape)
    for _ in range(100):
        obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
        if terminated or truncated:
            obs, _ = env.reset()
    env.close()
    print("Env smoke test passed.")
