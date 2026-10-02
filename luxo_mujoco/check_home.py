import mujoco
import imageio
import numpy as np

model = mujoco.MjModel.from_xml_path("luxo_lamp.xml")
data = mujoco.MjData(model)

mujoco.mj_resetData(model, data)
key_id = model.key("home").id
mujoco.mj_resetDataKeyframe(model, data, key_id)

# Let the PID joints settle into contact with the floor.
home_ctrl = data.qpos[7:7+model.nu].copy()
data.ctrl[:] = home_ctrl
for _ in range(80):
    mujoco.mj_step(model, data)

renderer = mujoco.Renderer(model, height=600, width=800)

# Default view (side).
renderer.update_scene(data)
frame = renderer.render()
imageio.imwrite("home_side.png", frame)

# Elevated front-quarter view.
cam = mujoco.MjvCamera()
cam.type = mujoco.mjtCamera.mjCAMERA_TRACKING
cam.trackbodyid = model.body("base").id
cam.distance = 0.7
cam.azimuth = 45.0
cam.elevation = -25.0
renderer.update_scene(data, camera=cam)
frame = renderer.render()
imageio.imwrite("home_iso.png", frame)

print(f"Base z = {data.qpos[2]:.3f}, base xy = {data.qpos[:2]}")
print("Saved home_side.png and home_iso.png")

renderer.close()
