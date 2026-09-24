# -*- coding: utf-8 -*-
"""生成圆台(截头圆锥)灯罩 mesh: 局部 +x = 罩口朝向(前方), x=0 背面 r=0.026, x=L 罩口 r=0.052。"""
import numpy as np

L, R0, R1, SEG = 0.105, 0.026, 0.052, 24
verts, faces = [], []
for i in range(SEG):
    a = 2 * np.pi * i / SEG
    ca, sa = np.cos(a), np.sin(a)
    verts.append((0.0, R0 * ca, R0 * sa))       # 背面环
    verts.append((L, R1 * ca, R1 * sa))         # 罩口环
for i in range(SEG):
    b0, t0 = 2 * i, 2 * i + 1
    b1, t1 = 2 * ((i + 1) % SEG), 2 * ((i + 1) % SEG) + 1
    faces.append((b0, b1, t1, t0))              # 侧面
c_back, c_front = len(verts), len(verts) + 1
verts.append((0.0, 0, 0)); verts.append((L, 0, 0))
for i in range(SEG):
    b1 = 2 * ((i + 1) % SEG)
    faces.append((c_back, 2 * i, b1))           # 背面盖
    t1 = 2 * ((i + 1) % SEG) + 1
    faces.append((c_front, t1, 2 * i + 1))      # 罩口盖(发光面板)
with open("frustum.obj", "w") as f:
    for v in verts:
        f.write(f"v {v[0]:.5f} {v[1]:.5f} {v[2]:.5f}\n")
    for fc in faces:
        f.write("f " + " ".join(str(k + 1) for k in fc) + "\n")
print("frustum.obj:", len(verts), "verts")
