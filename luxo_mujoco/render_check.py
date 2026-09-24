import mujoco
import numpy as np

model = mujoco.MjModel.from_xml_path('luxo_lamp.xml')
data = mujoco.MjData(model)

mujoco.mj_resetDataKeyframe(model, data, model.key('home').id)

# Hold the home pose with the position actuators
if model.nu > 0:
    data.ctrl[:model.nu] = data.qpos[7:7+model.nu]

# Step a bit to let it settle
for _ in range(200):
    mujoco.mj_step(model, data)

print("Model compiled and stepped successfully.")
print(f"  Base position: {data.qpos[:3]}")
print(f"  Joint angles: {data.qpos[7:]}")

# Try to render an image (useful even if no interactive display)
try:
    from PIL import Image
    renderer = mujoco.Renderer(model, height=480, width=640)
    renderer.update_scene(data)
    img = renderer.render()
    Image.fromarray(img).save('luxo_check.png')
    print("Rendered preview saved to luxo_check.png")
except Exception as e:
    print(f"Offscreen rendering skipped: {e}")
