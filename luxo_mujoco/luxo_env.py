import numpy as np
import gymnasium as gym
import mujoco


class LuxoJumpEnv(gym.Env):
    """
    MuJoCo-Gymnasium environment for a Pixar-style Luxo lamp.
    Current task: learn to jump once, forward (+x), and land roughly 10 cm ahead.
    """

    metadata = {"render_modes": ["rgb_array"], "render_fps": 50}

    def __init__(
        self,
        xml_path: str = "luxo_lamp.xml",
        frame_skip: int = 5,
        max_episode_steps: int = 800,
        target_distance: float = 0.10,
        render_mode: str | None = None,
    ):
        super().__init__()
        self.xml_path = xml_path
        self.frame_skip = frame_skip
        self.max_episode_steps = max_episode_steps
        self.target_distance = target_distance
        self.render_mode = render_mode

        self.model = mujoco.MjModel.from_xml_path(self.xml_path)
        self.data = mujoco.MjData(self.model)

        self.nu = self.model.nu
        self.n_actuated = self.nu

        self.ctrl_low = self.model.actuator_ctrlrange[:, 0].copy()
        self.ctrl_high = self.model.actuator_ctrlrange[:, 1].copy()
        self.ctrl_mid = (self.ctrl_low + self.ctrl_high) / 2.0
        self.ctrl_rng = (self.ctrl_high - self.ctrl_low) / 2.0

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
        self.last_z = 0.0
        self.steps = 0

        self.start_pos = np.zeros(2, dtype=np.float32)
        self.target_pos = np.zeros(2, dtype=np.float32)
        self.prev_contact = 1.0
        self.takeoff_vel = np.zeros(3, dtype=np.float32)
        self.max_air_z = 0.0
        self.landed_once = False

        if self.render_mode == "rgb_array":
            self.renderer = mujoco.Renderer(self.model, height=480, width=640)
        else:
            self.renderer = None

    def _base_contact(self) -> float:
        """Return 1.0 if the base geom is touching the floor, else 0.0."""
        floor_id = self.model.geom("floor").id
        base_id = self.model.geom("base_geom").id
        for i in range(self.data.ncon):
            c = self.data.contact[i]
            if (c.geom1 == floor_id and c.geom2 == base_id) or \
               (c.geom2 == floor_id and c.geom1 == base_id):
                return 1.0
        return 0.0

    def _get_obs(self) -> np.ndarray:
        q = self.data.qpos
        v = self.data.qvel

        base_pos = q[:3].astype(np.float32)
        base_quat = q[3:7].astype(np.float32)
        base_lin = v[:3].astype(np.float32)
        base_ang = v[3:6].astype(np.float32)

        jnt_pos = q[self.base_qpos_offset : self.base_qpos_offset + self.n_actuated].astype(np.float32)
        jnt_vel = v[self.base_qvel_offset : self.base_qvel_offset + self.n_actuated].astype(np.float32)

        contact_flag = self._base_contact()

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

        # Fixed forward-jump command for this training phase.
        self.command = np.array([1.0, 0.0], dtype=np.float32)

        # Hold the home pose with the actuators so the lamp drops and settles
        # elastically, like a position-controlled joint "locking" into place.
        home_ctrl = self.data.qpos[self.base_qpos_offset : self.base_qpos_offset + self.n_actuated].copy()
        self.data.ctrl[:] = home_ctrl
        for _ in range(40):
            mujoco.mj_step(self.model, self.data)

        # Record the actual starting position after settling.
        self.start_pos = self.data.qpos[:2].copy()
        self.target_pos = self.start_pos + self.command * self.target_distance

        self.last_action = np.zeros(self.nu, dtype=np.float32)
        self.last_pos = self.data.qpos[:2].copy()
        self.last_z = float(self.data.qpos[2])
        self.steps = 0

        self.prev_contact = self._base_contact()
        self.takeoff_vel = np.zeros(3, dtype=np.float32)
        self.max_air_z = self.last_z
        self.air_steps = 0
        self.landed_once = False

        return self._get_obs(), {}

    def step(self, action: np.ndarray):
        action = np.clip(action, -1.0, 1.0).astype(np.float32)
        self._set_ctrl(action)

        for _ in range(self.frame_skip):
            mujoco.mj_step(self.model, self.data)

        self.steps += 1

        base_pos = self.data.qpos[:2].copy()
        base_z = float(self.data.qpos[2])
        base_lin = self.data.qvel[:3].copy()
        base_ang = self.data.qvel[3:6].copy()
        xmat = self.data.body("base").xmat.reshape(3, 3)
        base_z_axis = xmat[:, 2]
        upright = float(base_z_axis[2])

        jnt_pos = self.data.qpos[self.base_qpos_offset : self.base_qpos_offset + self.n_actuated].copy()

        contact = self._base_contact()
        just_took_off = (self.prev_contact == 1.0 and contact == 0.0)
        just_landed = (self.prev_contact == 0.0 and contact == 1.0)

        # ---- Potential-based target-approach reward -------------------------
        # Dense signal that pulls the base toward the 10 cm landing target.
        prev_dist = float(np.linalg.norm(self.last_pos - self.target_pos))
        curr_dist = float(np.linalg.norm(base_pos - self.target_pos))
        r_approach = (prev_dist - curr_dist) * 8.0

        # ---- Small forward-progress reward (do not let it dominate) -----------
        delta = base_pos - self.last_pos
        r_forward = float(np.dot(delta, self.command)) * 3.0

        # ---- Lift reward only while on the ground and capped ------------------
        dz = base_z - self.last_z
        r_lift = max(0.0, dz) * 5.0 if contact == 1.0 else 0.0

        # ---- Takeoff event: modest bonus; too much makes it overshoot ---------
        r_takeoff = 0.0
        if just_took_off:
            self.takeoff_vel = base_lin.copy()
            self.air_steps = 0
            self.max_air_z = base_z
            forward_vel = float(np.dot(base_lin[:2], self.command))
            r_takeoff = (
                max(0.0, base_lin[2]) * 0.5          # upward velocity
                + max(0.0, forward_vel) * 1.5        # forward velocity
            )

        # ---- Flight reward: stay low-ish, upright, and keep approaching target
        r_flight = 0.0
        if contact == 0.0:
            self.air_steps += 1
            self.max_air_z = max(self.max_air_z, base_z)
            r_flight += 0.05                                    # tiny airborne bonus
            r_flight += max(0.0, np.dot(base_lin[:2], self.command)) * 0.5
            # Strongly discourage wasting energy on excessive height.
            r_flight -= max(0.0, (base_z - 0.12)) * 8.0
            # Penalize overshooting the target while still in the air.
            along_target = float(np.dot(base_pos - self.target_pos, self.command))
            r_flight -= max(0.0, along_target - 0.03) * 5.0
            r_flight -= max(0.0, (1.0 - upright)) * 2.0         # tilt penalty
            r_flight -= float(np.linalg.norm(base_ang)) * 0.2   # spin penalty

        # ---- Landing event: the dominant reward. -----------------------------
        # Only count a landing if the lamp has genuinely been airborne
        # (>= 4 env steps and peak z >= 8 cm above settled base).
        r_landing = 0.0
        landed_stable = False
        real_jump = self.air_steps >= 4 and (self.max_air_z - self.last_z) >= 0.06
        if just_landed:
            self.landed_once = True
            landing_error = float(np.linalg.norm(base_pos - self.target_pos))
            if real_jump:
                r_landing = 15.0 - landing_error * 120.0        # +15 at target, 0 at 12.5 cm
                if landing_error < 0.03:
                    r_landing += 8.0                            # bullseye bonus
                elif landing_error < 0.05:
                    r_landing += 3.0
                r_landing += max(0.0, self.max_air_z - 0.10) * 2.0  # reward a genuine leap
                r_landing += upright * 3.0                      # upright bonus
                r_landing -= float(np.linalg.norm(base_ang)) * 0.5
                r_landing -= float(abs(base_lin[2])) * 3.0      # soft touchdown
                # End the episode successfully if it lands close and stable.
                if landing_error < 0.05 and upright > 0.92 and np.linalg.norm(base_lin) < 1.0:
                    landed_stable = True
            else:
                # Tiny shuffle-jump: small penalty to force a real leap.
                r_landing = -2.0

        # ---- Post-landing stability reward -----------------------------------
        # After a real jump, reward staying upright and close to the target.
        r_stable = 0.0
        if self.landed_once and real_jump and contact == 1.0:
            r_stable += upright * 1.0
            landing_error = float(np.linalg.norm(base_pos - self.target_pos))
            r_stable -= landing_error * 2.0
            r_stable -= float(np.linalg.norm(base_ang)) * 0.2

        # ---- Upright bonus/penalty throughout the episode ---------------------
        r_upright = (upright - 1.0) * 1.5

        # ---- Keep unused yaw joints quiet ------------------------------------
        r_yaw = -abs(jnt_pos[0]) * 0.4 - abs(jnt_pos[4]) * 0.4

        # ---- Regularization --------------------------------------------------
        r_energy = -np.sum(np.square(action)) * 0.005
        r_smooth = -np.sum(np.square(action - self.last_action)) * 0.03

        self.last_action = action.copy()
        self.last_pos = base_pos.copy()
        self.last_z = base_z
        self.prev_contact = contact

        reward = float(
            r_approach + r_forward + r_lift + r_takeoff + r_flight + r_landing
            + r_stable + r_upright + r_yaw + r_energy + r_smooth
        )

        # ---- Termination conditions ------------------------------------------
        terminated = False
        truncated = False
        if base_z < 0.01 or base_z > 1.2 or not np.isfinite(base_z):
            terminated = True
        # Fallen over: base z-axis nearly horizontal or pointing down.
        if upright < 0.25:
            terminated = True
        # Successful landing: within 5 cm, upright, and staying still.
        if landed_stable:
            truncated = True

        if self.steps >= self.max_episode_steps:
            truncated = True

        info = {
            "r_approach": r_approach,
            "r_forward": r_forward,
            "r_lift": r_lift,
            "r_takeoff": r_takeoff,
            "r_flight": r_flight,
            "r_landing": r_landing,
            "r_stable": r_stable,
            "r_upright": r_upright,
            "r_yaw": r_yaw,
            "r_energy": r_energy,
            "r_smooth": r_smooth,
            "base_x": base_pos[0],
            "base_y": base_pos[1],
            "base_z": base_z,
            "upright": upright,
            "contact": contact,
            "takeoff_vz": float(self.takeoff_vel[2]),
            "takeoff_vx": float(self.takeoff_vel[0]),
            "max_air_z": self.max_air_z,
            "landing_error": float(np.linalg.norm(base_pos - self.target_pos)) if self.landed_once else None,
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
