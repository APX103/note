import math
import os

r1 = 0.08   # bottom (wide opening) radius, at z=0
r2 = 0.04   # top (narrow back) radius, at z=h
h = 0.12    # height
n = 32      # segments

verts = []
# bottom circle at z=0
for i in range(n):
    theta = 2 * math.pi * i / n
    verts.append((r1 * math.cos(theta), r1 * math.sin(theta), 0.0))
# top circle at z=h
for i in range(n):
    theta = 2 * math.pi * i / n
    verts.append((r2 * math.cos(theta), r2 * math.sin(theta), h))

faces = []
# side faces (two triangles per quad)
for i in range(n):
    j = (i + 1) % n
    b0 = i
    b1 = j
    t0 = i + n
    t1 = j + n
    faces.append((b0, t0, b1))
    faces.append((b1, t0, t1))

# bottom cap (fan from center)
center_bottom = len(verts)
verts.append((0.0, 0.0, 0.0))
for i in range(n):
    j = (i + 1) % n
    faces.append((center_bottom, j, i))

# top cap (fan from center)
center_top = len(verts)
verts.append((0.0, 0.0, h))
for i in range(n):
    j = (i + 1) % n
    faces.append((center_top, i + n, j + n))

with open(os.path.join(os.path.dirname(__file__), 'shade.obj'), 'w') as f:
    for v in verts:
        f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
    for fa in faces:
        f.write(f"f {fa[0]+1} {fa[1]+1} {fa[2]+1}\n")

print(f"shade.obj written with {len(verts)} vertices and {len(faces)} faces")
