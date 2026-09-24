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
        max_episode_steps: int = 400,
        target_distance: float = 0.05,
        jump_deadline_steps: int = 120,
        render_mode: str | None = None,
    ):
        super().__init__()
        self.xml_path = xml_path
        self.frame_skip = frame_skip
        self.max_episode_steps = max_episode_steps
        self.target_distance = target_distance
        self.jump_deadline_steps = jump_deadline_steps
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
        """
        Return 1.0 if the base is near the ground.
        The base is now a flat cylinder of half-height 0.025; when settled
        the base body z is about 0.075.  Use a threshold a few cm above that.
        """
        return 1.0 if self.data.qpos[2] < 0.12 else 0.0

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

        # With torque motors, use a PD controller to hold the home pose while
        # the lamp drops and settles elastically on the floor.
        home_q = self.data.qpos[self.base_qpos_offset : self.base_qpos_offset + self.n_actuated].copy()
        kp_hold = 120.0
        kv_hold = 12.0
        for _ in range(80):
            current_q = self.data.qpos[self.base_qpos_offset : self.base_qpos_offset + self.n_actuated]
            current_v = self.data.qvel[self.base_qvel_offset : self.base_qvel_offset + self.n_actuated]
            self.data.ctrl[:] = kp_hold * (home_q - current_q) - kv_hold * current_v
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
        self.ground_z = self.last_z
        self.low_upright_steps = 0
        self.jumped_this_episode = False

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

        # Update flight bookkeeping.
        if contact == 0.0:
            self.air_steps += 1
            self.max_air_z = max(self.max_air_z, base_z)

        # ------------------------------------------------------------------
        # Reward design (v6): fixes two bugs from v5 that made "never jump"
        # the optimal policy:
        #   (a) r_peak used to penalize every single step for the rest of the
        #       episode based on the *historical* max_air_z, so one jump over
        #       8cm poisoned hundreds of subsequent steps.
        #   (b) landing_stable used to truncate the episode early, which cut
        #       off future per-step alive/upright reward -- so standing still
        #       for the full 800-step episode out-earned jumping once.
        # v6: height penalty is only applied once, at landing, based on the
        # flight's own peak; episodes are no longer truncated early on a
        # successful landing (the agent keeps earning standing reward
        # afterwards, on top of the landing bonus).
        # ------------------------------------------------------------------

        # 1) Time pressure: do not dither forever.
        r_alive = -0.01
        r_upright = upright * 0.15

        # 1b) Escalating "please jump" pressure: standing still forever must
        # not out-earn attempting a jump. This grows the longer the agent
        # has gone without ever leaving the ground, which breaks the
        # "safe zero-variance standing" local optimum PPO tends to collapse
        # into once its action std shrinks.
        r_urgency = 0.0
        if not self.jumped_this_episode:
            r_urgency = -0.01 * (self.steps / 50.0)

        # 2) Tiny upward-velocity reward only while airborne (no ground bounce-hack).
        r_upward = 0.0
        if contact == 0.0:
            r_upward += max(0.0, base_lin[2]) * 0.2

        # 3) Height regulation while airborne only (based on current z, not a
        #    permanently-elevated running max) -- soft, not punitive.
        r_peak = 0.0
        if contact == 0.0:
            r_peak -= max(0.0, base_z - 0.28) * 5.0

        # 4) Forward guidance while airborne: reward velocity toward target,
        #    penalize overshooting past it.
        r_forward = 0.0
        if self.target_distance > 0.01:
            if contact == 0.0:
                forward_vel = float(np.dot(base_lin[:2], self.command))
                along = float(np.dot(base_pos - self.target_pos, self.command))
                if along > 0.0:
                    # Still approaching target.
                    r_forward += max(0.0, forward_vel) * 2.0
                else:
                    # Overshot: penalize any additional forward velocity.
                    r_forward -= max(0.0, forward_vel) * 5.0
        else:
            # Jump-in-place phase: mild drift penalty only (do not dominate
            # the jump incentive).
            drift = float(np.linalg.norm(base_pos - self.start_pos))
            r_forward -= drift * 0.3

        # 5) Small airtime bonus, but flight should be short.
        r_air = 0.0
        if contact == 0.0:
            r_air += 0.1
            r_air -= max(0.0, (1.0 - upright)) * 1.0
            r_air -= float(np.linalg.norm(base_ang)) * 0.1

        # 6) Takeoff event: reward leaving the ground with real upward push,
        #    so the agent has an immediate incentive to attempt a jump.
        r_takeoff = 0.0
        if just_took_off:
            self.jumped_this_episode = True
            self.takeoff_vel = base_lin.copy()
            forward_vel = float(np.dot(base_lin[:2], self.command))
            upward_vel = float(base_lin[2])
            r_takeoff = max(0.0, upward_vel) * 3.0 + max(0.0, forward_vel) * 3.0

        # 7) Landing event: the dominant reward. One-time height penalty for
        #    excessive jumps is charged here too (not every subsequent step).
        r_landing = 0.0
        landed_stable = False
        real_jump = self.air_steps >= 3 and self.max_air_z >= self.ground_z + 0.03
        if just_landed:
            self.landed_once = True
            landing_error = float(np.linalg.norm(base_pos - self.target_pos))
            if real_jump:
                # +80 at target, zero at ~5.3 cm error.
                r_landing = 80.0 - landing_error * 1500.0
                if landing_error < 0.03:
                    r_landing += 40.0
                elif landing_error < 0.05:
                    r_landing += 15.0
                r_landing += upright * 8.0
                r_landing -= float(np.linalg.norm(base_ang)) * 1.0
                r_landing -= float(abs(base_lin[2])) * 5.0
                # One-time penalty for jumping much higher than needed
                # (>10cm above ground); charged once, not per-step.
                r_landing -= max(0.0, self.max_air_z - self.ground_z - 0.10) * 30.0
                # Success: landed close, upright, and nearly still.
                if landing_error < 0.06 and upright > 0.75 and np.linalg.norm(base_lin) < 2.0:
                    landed_stable = True
            else:
                r_landing = -2.0

        # 8) Post-landing stability.
        r_stable = 0.0
        if self.landed_once and real_jump and contact == 1.0:
            landing_error = float(np.linalg.norm(base_pos - self.target_pos))
            r_stable += upright * 0.5
            r_stable -= landing_error * 1.0
            r_stable -= float(np.linalg.norm(base_ang)) * 0.1

        # 9) Keep head joints near neutral.
        r_yaw = -abs(jnt_pos[0]) * 0.1 - abs(jnt_pos[4]) * 0.1

        # 10) Regularization.
        r_energy = -np.sum(np.square(action)) * 0.005
        r_smooth = -np.sum(np.square(action - self.last_action)) * 0.03

        self.last_action = action.copy()
        self.last_pos = base_pos.copy()
        self.last_z = base_z
        self.prev_contact = contact

        # Track consecutive low-upright steps for termination.
        if upright < 0.15:
            self.low_upright_steps += 1
        else:
            self.low_upright_steps = 0

        reward = float(
            r_alive + r_upright + r_urgency + r_upward + r_peak + r_forward + r_air + r_takeoff
            + r_landing + r_stable + r_yaw + r_energy + r_smooth
        )

        # ---- Termination conditions ------------------------------------------
        terminated = False
        truncated = False
        # Flat base settles around z=0.024; allow a little penetration.
        if base_z < 0.015 or base_z > 1.5 or not np.isfinite(base_z):
            terminated = True
        # Only terminate if the lamp has been clearly fallen for a while.
        if self.low_upright_steps >= 15:
            terminated = True
        # v7 fix: standing still forever must not be a viable strategy at
        # all. If the agent has never even left the ground by the deadline,
        # end the episode with a penalty -- this closes off the "never jump"
        # optimum instead of just discouraging it.
        if not self.jumped_this_episode and self.steps >= self.jump_deadline_steps:
            terminated = True
            reward -= 20.0
        # NOTE (v6 fix): do NOT truncate early on a successful landing.
        # Ending the episode here used to forfeit hundreds of steps of
        # future alive/upright reward, which made "never jump" earn more
        # expected return than "jump once and land well". Let the agent
        # keep collecting standing reward after a good landing instead.
        if landed_stable:
            pass

        if self.steps >= self.max_episode_steps:
            truncated = True

        info = {
            "r_alive": r_alive,
            "r_upright": r_upright,
            "r_urgency": r_urgency,
            "r_upward": r_upward,
            "r_peak": r_peak,
            "r_forward": r_forward,
            "r_air": r_air,
            "r_takeoff": r_takeoff,
            "r_landing": r_landing,
            "r_stable": r_stable,
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
