import os
import mujoco
from PIL import Image

model = mujoco.MjModel.from_xml_path('luxo_lamp.xml')
data = mujoco.MjData(model)

mujoco.mj_resetDataKeyframe(model, data, model.key('home').id)
if model.nu > 0:
    data.ctrl[:model.nu] = data.qpos[7:7+model.nu]

# Let it settle with actuators holding the pose
for _ in range(500):
    mujoco.mj_step(model, data)

renderer = mujoco.Renderer(model, height=600, width=800)

cam = mujoco.MjvCamera()
cam.type = mujoco.mjtCamera.mjCAMERA_FREE
cam.lookat[:] = [0.0, 0.0, 0.35]

views = [
    ('view_iso.png',    0.9,  135, -25),
    ('view_side.png',   0.75,  90, -15),
    ('view_front.png',  0.75,   0, -15),
    ('view_top.png',    0.85,   0, -90),
    ('view_head.png',   0.28,  60, -20),
]

for filename, distance, azimuth, elevation in views:
    cam.distance = distance
    cam.azimuth = azimuth
    cam.elevation = elevation
    if filename == 'view_head.png':
        # Close-up on the head connection
        cam.lookat[:] = [0.02, 0.0, 0.37]
    else:
        cam.lookat[:] = [0.0, 0.0, 0.35]

    renderer.update_scene(data, camera=cam)
    img = renderer.render()
    Image.fromarray(img).save(filename)
    print(f"Saved {filename}")
