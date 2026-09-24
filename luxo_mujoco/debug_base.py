import mujoco
import imageio

model = mujoco.MjModel.from_xml_path("luxo_lamp.xml")
data = mujoco.MjData(model)

mujoco.mj_resetData(model, data)
key_id = model.key("home").id
mujoco.mj_resetDataKeyframe(model, data, key_id)

# No control, just let gravity do its thing.
for _ in range(200):
    mujoco.mj_step(model, data)
    print(f"t={data.time:.3f} base_z={data.qpos[2]:.3f} base_quat={data.qpos[3:7]}")

renderer = mujoco.Renderer(model, height=480, width=640)
renderer.update_scene(data)
imageio.imwrite("debug_base.png", renderer.render())
renderer.close()
