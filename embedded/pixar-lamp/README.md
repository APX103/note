# Pixar 台灯机器人（Luxo）— 跳跃可行性项目

复刻 Pixar 片头 Luxo Jr.：一盏**真的能跳**的台灯机器人。底盘 + 双连杆 + 灯头（灯罩内摄像头），
QDD 关节电机驱动，多 IMU 感知，强化学习控制。

## 目录

- `pixar-lamp-feasibility.html` — **主方案文档**（单文件自包含：动力学、仿真、训练结果、硬件拍板、RL 方案）
- `mujoco/` — **三维 MuJoCo 验证**（几何 v2：Ø30cm 圆片底盘 + 双连杆 + 圆台灯罩 + 偏航自由度；
  `mujoco_train.py` CEM 训练向前跳 17.4cm 直立落地；`mujoco_render.py` 出 GIF/帧序列）
- `sim/lamp_sim.py` — 自研平面多体动力学内核（仅 numpy）+ 跳跃控制器
- `sim/train_es.py` — CEM 策略搜索（CPU 训练）
- `sim/experiments.py` — 图表生成（频闪/遥测/学习曲线/余量）
- `sim/build_doc.py` — 把训练结果注入文档模板
- `sim/results/` — 训练 JSON 与图

## 快速复现

```bash
# 三维 MuJoCo(用 luxo_mujoco/.venv 的 python, 需 mujoco+PIL):
cd mujoco
python3 make_frustum.py                        # 生成圆台网格
python3 mujoco_train.py 55                     # 训练向前跳 (~2 分钟)
python3 mujoco_render.py                       # 渲染 GIF + 帧序列

# 二维自研仿真:
cd sim
python3 lamp_sim.py            # 动力学验证（能量守恒/静立/动量）
python3 train_es.py hop 55     # CEM 原地跳训练（~25 分钟, 8 核）
python3 train_es.py leap 30   # 定向跳（从 hop 解热启动）
python3 train_es.py flip 55    # 翻身跳
python3 experiments.py all     # 生成全部图
python3 build_doc.py           # 重建方案文档 HTML
```

## 结论速览（v1，2026-09-23）

1.29 kg / DM-J4310-V2 ×2（峰值 12.5 N·m）+ 1.5 N·m/rad 弹簧：原地跳（腾空 10.8cm 直立落地）、定向跳仿真可行；
翻身跳处于能力边缘。瓶颈是**协调时序**而非电机扭矩 → RL 方案见文档 §8。

阶段 B（GPU/Isaac Lab/PPO）等训练机到位后启动。
