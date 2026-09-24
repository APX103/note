import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path('luxo_lamp.xml')
data = mujoco.MjData(model)

# Start from the "home" keyframe (a slight crouch pose)
key_id = model.key('home').id
mujoco.mj_resetDataKeyframe(model, data, key_id)

# Initialize actuator targets so the lamp holds the home pose
if model.nu > 0:
    data.ctrl[:model.nu] = data.qpos[7:7+model.nu]

print("MuJoCo model loaded.")
print(f"  Bodies: {model.nbody}")
print(f"  Joints: {model.njnt}")
print(f"  Actuators: {model.nu}")
print("Launching interactive viewer...")
print("Tip: use the on-screen actuator sliders to move the lamp joints.")

mujoco.viewer.launch(model, data)
