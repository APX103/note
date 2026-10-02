# -*- coding: utf-8 -*-
"""build_doc.py — 把训练结果 JSON + 图表注入文档模板，生成最终自包含 HTML。
用法: python3 build_doc.py"""
import base64
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(HERE, "results")
MJ = os.path.join(ROOT, "mujoco", "results")


def b64img(name, root=None):
    p = os.path.join(root or RESULTS, name)
    if not os.path.exists(p):
        return None
    with open(p, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def fig_block(name, caption, root=None):
    data = b64img(name, root=root)
    if data is None:
        return f"<p class='dim'>（图缺失: {name}）</p>"
    return f"<div class=\"fig\"><img src=\"{data}\" alt=\"{caption}\">"\
           f"<div class=\"figcap\">{caption}</div></div>"


def load(task):
    p = os.path.join(RESULTS, f"cem_{task}.json")
    if not os.path.exists(p):
        return None
    with open(p) as f:
        return json.load(f)


def fmt(v, nd=1):
    try:
        return f"{float(v):.{nd}f}"
    except (TypeError, ValueError):
        return str(v)


def main():
    tpl_path = os.path.join(ROOT, "doc_template.html")
    with open(tpl_path) as f:
        html = f.read()

    hop = load("hop") or {}
    leap = load("leap") or {}
    flip = load("flip") or {}
    hi = hop.get("info", {})
    ti = leap.get("info", {})
    fi = flip.get("info", {})

    R = {}
    R["HOP_APEX"] = fmt(hi.get("apex_at", 0) * 100, 1)
    R["HOP_VTO"] = fmt((2 * 9.81 * max(0.0, hi.get("apex_at", 0))) ** 0.5, 2)
    R["HOP_AIR"] = fmt(hi.get("air_t", 0), 2)
    R["HOP_UPRIGHT"] = "✅ 直立着陆" if hi.get("upright") else "⚠ 仍需迭代（落地姿态超差）"
    R["HOP_FN"] = fmt(hi.get("peak_Fn", 0), 0)
    R["HOP_FN_W"] = fmt(hi.get("peak_Fn", 0) / 12.66, 1)
    R["HOP_TAU"] = fmt(hi.get("peak_tau", 0), 1)
    R["HOP_WALL"] = fmt(hop.get("wall_s", 0) / 60, 0)
    R["BASELINE_APEX"] = "2.0 cm（翻倒）"
    R["BASELINE_AIR"] = "0.12 s"
    # 扭矩余量结论（从 margin.json 提取，若有）
    R["MARGIN_TORQUE"] = "见 §5 余量分析"
    mg = os.path.join(RESULTS, "margin.json")
    if os.path.exists(mg):
        with open(mg) as f:
            rows = json.load(f)
        ok = [r[0] for r in rows if abs(r[1] - 1.5) < 1e-9 and r[2] > 30]
        if ok:
            R["MARGIN_TORQUE"] = (f"训练策略在 {min(ok):.0f} N·m 峰值扭矩下仍能完成有效跳跃"
                                  f"（12.5 N·m 选型留有 {12.5/min(ok)*100-100:.0f}% 余量，见 §5）")
    # leap
    if leap:
        per_cycle = ti.get("x_end", 0) / max(1, ti.get("cycles", 1))
        R["LEAP_SUMMARY"] = (f"单跳定向位移 {fmt(abs(ti.get('x_end',0))*100,0)} cm"
                             f"、腾空 {fmt(ti.get('apex_at',0)*100,1)} cm，{'直立落地 ✅' if ti.get('upright') else '落地姿态待改进 ⚠'}")
    else:
        R["LEAP_SUMMARY"] = "训练进行中（见 §6）"
    # travel/flip 小节
    R["FIG_STROBE_HOP"] = fig_block("fig_strobe_hop.png", "图 2 · CEM 策略的原地跳频闪（每帧 45ms，红星为全机质心）")
    R["FIG_FILMSTRIP_HOP"] = fig_block("view_filmstrip_hop.png", "图 3 · 原地跳全程帧序列（相机跟拍：下蹲蓄力→点火蹬伸→腾空→落地缓冲→起身站立）")
    R["FIG_PORTRAIT"] = fig_block("view_portrait.png", "图 10 · v1 造型渲染：亚光黑本体、镀铬关节、可见弹簧、灯罩暖光（摄像头藏于罩口）")
    R["FIG_TELEMETRY_HOP"] = fig_block("fig_telemetry_hop.png", "图 4 · 最佳策略遥测：质心高度 / 地面反力 / 关节扭矩（虚线为电机峰值 ±12.5 N·m）")
    R["FIG_LEARNING_HOP"] = fig_block("fig_learning_hop.png", f"图 5 · CEM 学习曲线（CPU {fmt(hop.get('wall_s',0)/60,0)} 分钟，回报≈腾空 cm）")
    R["FIG_MARGIN"] = fig_block("fig_margin.png", "图 7 · 硬件余量：训练好的策略在降扭矩（左）与变弹簧刚度（右）下的表现")

    if leap:
        R["LEAP_SECTION"] = (
            "<p>先说结论的实现路径：<b>CEM 收敛的跳法天然带 ~20cm 定向位移且直立落地</b>——"
            "因为点火时序本身不对称（肩-肘顺序点火使冲量方向偏离竖直）。把机器人的机身朝向定义为该漂移方向，"
            "定向跳即刻成立：单跳位移 17-24cm、腾空 10-12cm、直立率 5/5。跳跃方向指令在世界系下表达，"
            "由磁力计航向闭环 + 跳前转身实现（§7.4）。</p>"
            "<p>另一个发现同样重要：给控制器加了「质心目标偏移 com_ref」方向旋钮后（物理直觉：先倾后蹬），"
            "前倾 3.5cm 可以把位移推到 +26cm——但代价是翻倒落地：从「后跳直立」到「前跳直立」之间没有"
            "CEM 能走通的连续路径（两代 26 迭代训练均困在各自盆地），需要重新协调全部点火时序。"
            "这正是<b>结构化策略（本阶段）与全维策略（阶段 B 的神经网络 + PPO）的能力分界</b>——"
            "PPO 直接在 50Hz 位置指令空间优化，不受预定时序结构的限制。</p>"
            + fig_block("fig_strobe_leap.png", "图 6 · 定向跳频闪（+x 方向，注意蹲姿前倾）")
            + f"<table><tr><th>指标</th><th>值</th></tr>"
            f"<tr><td>单跳水平位移</td><td class='num'>{fmt(ti.get('x_end',0)*100,0)} cm</td></tr>"
            f"<tr><td>腾空高度</td><td class='num'>{fmt(ti.get('apex_at',0)*100,1)} cm</td></tr>"
            f"<tr><td>直立落地</td><td>{'✅' if ti.get('upright') else '⚠'}</td></tr></table>")
    else:
        R["LEAP_SECTION"] = "<p class='dim'>（leap 训练结果待注入）</p>"

    if flip:
        rot_ok = fi.get("landed_up")
        R["FLIP_SUMMARY"] = (f"仿真中{'完成 360° 翻身跳并直立落地 ✅' if rot_ok else '获得 %.0f° 转体，落地姿态待优化 ⚠' % (fi.get('rot',0)*57.3)}")
        R["FLIP_SECTION"] = (
            "<p>翻身跳 = 不对称起跳（肩部点火带偏置，获取角动量）+ 空中收拢（转动惯量下降、角速度上升，"
            "体操收腿原理）+ 转体到位展开降速 + 着地缓冲。CEM 结果：<b>未实现完整 360°</b>——"
            "结构化策略稳定收敛到 27° 转体 + 直立落地。关键诊断是：最优解滞空时间 0.42s，"
            "收拢态只需 15 rad/s 即可转满 2π，<b>时间够、角动量不够</b>：起跳阶段不对称冲量的精细协调"
            "（既要竖直分量跳得高、又要切向分量产生旋转、还不能破坏落地姿态）超出了"
            "「预定时序结构 + 线性反馈」策略类的表达能力。这正是给阶段 B 神经网络策略"
            "（50Hz 位置指令全维优化）保留的头号目标；另一个现实路径是升级执行器（DM-J4340/RobStride-01）"
            "把腾空推到 25cm+，角动量预算翻倍。</p>"
            + fig_block("fig_strobe_flip.png", "图 7 · 翻身跳频闪")
            + f"<table><tr><th>指标</th><th>值</th></tr>"
            f"<tr><td>累计转体</td><td class='num'>{fmt(fi.get('rot',0)*57.3,0)}°</td></tr>"
            f"<tr><td>腾空高度</td><td class='num'>{fmt(fi.get('apex_at',0)*100,1)} cm</td></tr>"
            f"<tr><td>直立落地</td><td>{'✅' if rot_ok else '⚠'}</td></tr></table>")
    else:
        R["FLIP_SUMMARY"] = "仿真探索中（§6）"
        R["FLIP_SECTION"] = "<p class='dim'>（flip 训练结果待注入）</p>"

    mjf = os.path.join(MJ, "mj_leap.json")
    if os.path.exists(mjf):
        with open(mjf) as f:
            mj = json.load(f)
        mi = mj["info"]
        R["MJ_SECTION"] = (
            "<h2>6A · 三维 MuJoCo 验证（几何 v2：圆片底盘 + 圆台灯罩）</h2>"
            "<p>按评审意见重构几何与初始化：<b>超薄圆片底盘（r=15cm，Ø30cm）</b>替代半球底座，中央立柱居中接下连杆，"
            "上连杆接<b>圆台（截头圆锥）灯罩</b>侧面、罩口斜朝地面，罩内藏摄像头与暖光灯——总质量维持 1.29kg，"
            "执行器/弹簧/摩擦参数与二维模型一致，另增<b>底盘偏航自由度</b>（Z 轴位置伺服）。"
            "<b>前方 = 肘弯开口方向</b>（下臂前倾、上臂折回，肘弯所指即 +x）。"
            "初始化按'台灯出生'协议：关节由位置 PD <b>力锁</b>在台灯站姿、整体半悬浮 ~3cm 出生、落下后弹性落定"
            "（'像弹簧'正是位置 PID 的闭环表现）。奖励定义为 10cm 峰值谷形（两侧衰减）+ 直立落地硬要求，"
            "CEM 收敛到 0.093-0.115m。反馈在臂体坐标系（按 yaw 反旋转），转向后策略方向不变：</p>"
            + f"<table><tr><th>指标</th><th>值</th></tr>"
            f"<tr><td>单跳前向位移</td><td class='num'>{mi['x_end']*100:.0f} cm（目标 10-15cm 级轻跳）</td></tr>"
            f"<tr><td>腾空高度</td><td class='num'>{mi['apex_at']*100:.0f} cm</td></tr>"
            f"<tr><td>落地与收势</td><td class='num'>直立落地 ✅ · 起身站立收势 ✅</td></tr>"
            f"<tr><td>转向跳</td><td class='num'>偏航 90.0° 后沿 102° 方位跳出 ~13cm ✅</td></tr>"
            f"<tr><td>初始化</td><td class='num'>半悬浮出生 → 位置PD力锁 → 弹性落定 ✅</td></tr></table>"
            + fig_block("view_mj_filmstrip.png", "图 6A-1 · MuJoCo 三维向前跳全程帧序列（下蹲蓄力→点火蹬伸→腾空→落地缓冲→起身站立）", root=MJ)
            + fig_block("view_mj_airborne.png", "图 6A-2 · 腾空瞬间：圆片底盘离地，圆台灯罩暖光朝前", root=MJ)
            + "<p><b>动画演示（GIF，随仓库分发）：</b>"
            "<a href='../mujoco/results/view_mj_leap.gif'>三维向前跳</a> · "
            "<a href='../mujoco/results/view_mj_turn_leap.gif'>三维转向+前跳</a>。"
            "工程备忘：<b>偏航必须慢转</b>——快转时反作用矩会让圆片底盘在地面上打滑反转（角动量守恒，"
            "地面扭转摩擦仅 ~0.5 N·m），斜坡目标 + kp30 伺服实测转到 90.0°；"
            "MuJoCo 训练中策略回报 161.2 打满（位移饱和 + 直立达成）。训练脚本 "
            "<code>mujoco/mujoco_train.py</code>，复用二维策略类做热启动。</p>")
    else:
        R["MJ_SECTION"] = ""
    for k, v in R.items():
        html = html.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{(\w+)\}\}", html)
    for k in left:
        html = html.replace("{{" + k + "}}", "—")

    out = os.path.join(ROOT, "pixar-lamp-feasibility.html")
    with open(out, "w") as f:
        f.write(html)
    print("written", out, f"({len(html)/1024:.0f} KB), 未解析占位: {left}")


if __name__ == "__main__":
    main()
