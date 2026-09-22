#!/usr/bin/env python3
"""int8 量化 + 导出 C 运行时所需文件。

1. 用 numpy 复刻整条 int8 前向（与 C 实现逐位对齐：整数累加 + requant 取整）
2. 在验证集上对比 float / int8 精度损失
3. 生成 esp32/wakenet_model.h（权重、尺度、mel 滤波器组、归一化参数）
4. 生成对拍文件：test_features.txt / test_pcm.raw / test_mel_expected.txt
"""
import json, pathlib, sys
import numpy as np
import torch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from train import MiniWakeNet, logmel, CLIP, N_FRAMES, N_MEL, WINDOW, FB  # noqa: E402

ESP = ROOT / "esp32"
FEAT_CLAMP = 4.0


# ------------------------------------------------ numpy int8 前向（= C 语义）
def qclip(x):
    return np.clip(x, -127, 127)


def qconv(x_q, w_q, b_q, requant, relu, pad=0, dil=1, depthwise=False):
    """x_q:(C,T) int8 → y:(C_out,T) int8。整数累加 + float requant，与 wakenet.c 一致。
    requant: (C_out,) 逐输出通道 = s_in*s_w[o]/s_out。"""
    C_in, T = x_q.shape
    C_out, K = w_q.shape[0], w_q.shape[2]
    xp = np.zeros((C_in, T + 2 * pad), np.int32)
    xp[:, pad:pad + T] = x_q
    W = np.stack([xp[:, k * dil: k * dil + T] for k in range(K)], 0)   # (K,C,T)
    if depthwise:
        acc = np.einsum("mk,kmt->mt", w_q[:, 0, :].astype(np.int32), W)
    else:
        acc = np.einsum("oik,kit->ot", w_q.astype(np.int32), W)
    acc = acc + b_q[:, None]
    y = np.rint(acc.astype(np.float32) * np.float32(requant)[:, None])
    y = np.clip(y, 0 if relu else -127, 127)          # ReLU 层下限 0
    return y.astype(np.int8)


class QuantModel:
    def __init__(self, model: MiniWakeNet, act_max: dict):
        sd = model.state_dict()
        A = {k: v / 127 for k, v in act_max.items()}       # 各层输出激活 scale
        s_in0 = FEAT_CLAMP / 127.0
        spec = [
            # (名字, 权重键, s_in, s_out, relu, pad, dil, depthwise)
            ("stem",  ("stem.weight", "stem.bias"), s_in0,    A["stem"], True, 2, 1, False),
            ("b1.dw", ("b1.dw.weight", "b1.dw.bias"), A["stem"], A["b1.dw"], True, 4, 2, True),
            ("b1.pw", ("b1.pw.weight", "b1.pw.bias"), A["b1.dw"], A["b1.pw"], True, 0, 1, False),
            ("b2.dw", ("b2.dw.weight", "b2.dw.bias"), A["b1.pw"], A["b2.dw"], True, 8, 4, True),
            ("b2.pw", ("b2.pw.weight", "b2.pw.bias"), A["b2.dw"], A["b2.pw"], True, 0, 1, False),
            ("b3.dw", ("b3.dw.weight", "b3.dw.bias"), A["b2.pw"], A["b3.dw"], True, 16, 8, True),
            ("b3.pw", ("b3.pw.weight", "b3.pw.bias"), A["b3.dw"], A["b3.pw"], True, 0, 1, False),
        ]
        self.q = []
        for name, (wk, bk), s_in, s_out, relu, pad, dil, dw in spec:
            w = sd[wk].detach().numpy().astype(np.float32)
            b = sd[bk].detach().numpy().astype(np.float32)
            s_w = np.abs(w).max(axis=tuple(range(1, w.ndim))) / 127.0   # 逐输出通道
            w_q = np.rint(w / s_w.reshape(-1, *([1] * (w.ndim - 1)))).astype(np.int8)
            b_q = np.rint(b / (s_in * s_w)).astype(np.int32)
            requant = (s_in * s_w / s_out).astype(np.float32)
            self.q.append(dict(name=name, w_q=w_q, b_q=b_q, requant=requant,
                               relu=relu, pad=pad, dil=dil, dw=dw))
        # fc（输入 = b3.pw 输出时间 GAP，scale 不变）
        w = sd["fc.weight"].detach().numpy().astype(np.float32)
        b = sd["fc.bias"].detach().numpy().astype(np.float32)
        fc_s_in = A["b3.pw"]
        fc_s_w = np.abs(w).max(axis=1) / 127.0
        self.fc_in_ch = w.shape[1]
        self.fc = dict(w_q=np.rint(w / fc_s_w[:, None]).astype(np.int8),
                       b_q=np.rint(b / (fc_s_in * fc_s_w)).astype(np.int32),
                       logit_scale=(fc_s_in * fc_s_w).astype(np.float32))

    def forward(self, x_q: np.ndarray):
        """x_q:(40,97) int8（= clamp(±4) 后的输入量化）→ (3,) float softmax 前的 logits"""
        h = x_q
        for L in self.q:
            h = qconv(h, L["w_q"], L["b_q"], L["requant"], L["relu"], L["pad"], L["dil"], L["dw"])
        gap = np.rint(h.astype(np.float32).mean(axis=1))       # 时间 GAP，scale 不变
        gap = np.clip(gap, 0, 127).astype(np.int8)
        acc = self.fc["w_q"].astype(np.int32) @ gap.astype(np.int32) + self.fc["b_q"]
        return acc.astype(np.float32) * self.fc["logit_scale"]


def softmax(x):
    e = np.exp(x - x.max())
    return e / e.sum()


def feats_to_q(x_wav, mean, std):
    f = np.clip((logmel(x_wav) - mean) / std, -FEAT_CLAMP, FEAT_CLAMP)
    return np.rint(f * (127.0 / FEAT_CLAMP)).astype(np.int8).T          # (40,97)


# ------------------------------------------------ 生成 C 头文件
def carr(name, arr, typ):
    flat = np.asarray(arr).ravel()
    body = ",".join(f"{v:.8f}" if typ == "float" else str(int(v)) for v in flat)
    return f"static const {typ} {name}[{flat.size}] = {{{body}}};\n"


def main():
    stats = json.loads((ROOT / "models" / "stats.json").read_text())
    d = np.load(ROOT / "data" / "dataset.npz", allow_pickle=True)
    X, y, val = d["X"], d["y"], d["val"]
    va, tr = val == 1, val == 0
    mean, std = stats["mean"], stats["std"]

    model = MiniWakeNet()
    model.load_state_dict(torch.load(ROOT / "models" / "model.pt", weights_only=True))
    model.eval()
    qm = QuantModel(model, stats["act_max"])   # 与训练 QAT 阶段同一份激活标定

    # 验证集 float vs int8
    n_ok_f = n_ok_q = 0
    cmq = np.zeros((3, 3), int)
    with torch.no_grad():
        for i in np.where(va)[0]:
            xq = feats_to_q(X[i], mean, std)
            pf = torch.softmax(model(torch.from_numpy(xq.astype(np.float32) * (FEAT_CLAMP / 127.0)).unsqueeze(0)), 1)[0].numpy()
            pq = softmax(qm.forward(xq))
            n_ok_f += int(pf.argmax() == y[i])
            n_ok_q += int(pq.argmax() == y[i])
            cmq[y[i], pq.argmax()] += 1
    n = int(va.sum())
    print(f"验证集 {n} 条: float acc={n_ok_f/n:.4f}  int8 acc={n_ok_q/n:.4f}  (损失 {n_ok_f/n - n_ok_q/n:+.4f})")
    print("int8 混淆矩阵 (行=真实 lumos/unknown/noise):")
    print(cmq)

    # ---- 生成 wakenet_model.h
    dims = {"WN_C0": qm.q[0]["w_q"].shape[0], "WN_C1": qm.q[2]["w_q"].shape[0],
            "WN_C2": qm.q[4]["w_q"].shape[0], "WN_C3": qm.q[6]["w_q"].shape[0]}
    hdr = ["// 由 scripts/export_c.py 自动生成，勿手改",
           "#pragma once", "#include <stdint.h>", "",
           "#define WN_MEL 40", "#define WN_FRAMES 97", "#define WN_CLASSES 3",
           "#define WN_FEAT_CLAMP 4.0f", "#define WN_IN_SCALE (4.0f/127.0f)"]
    hdr += [f"#define {k} {v}" for k, v in dims.items()]
    hdr.append("")
    for L in qm.q:
        n = L["name"].replace(".", "_")
        hdr.append(carr(f"wn_{n}_w", L["w_q"], "int8_t"))
        hdr.append(carr(f"wn_{n}_b", L["b_q"], "int32_t"))
        hdr.append(carr(f"wn_{n}_requant", L["requant"], "float"))
    hdr.append(carr("wn_fc_w", qm.fc["w_q"], "int8_t"))
    hdr.append(carr("wn_fc_b", qm.fc["b_q"], "int32_t"))
    hdr.append(carr("wn_fc_logit_scale", qm.fc["logit_scale"], "float"))
    hdr.append(carr("wn_mel_fb", FB.T, "float"))          # (257,40) 供 C 直接 spec·FB
    hdr.append(carr("wn_window", WINDOW, "float"))
    hdr.append(carr("wn_feat_mean", [mean] * 1, "float"))
    hdr.append(carr("wn_feat_std", [std] * 1, "float"))
    (ESP / "wakenet_model.h").write_text("\n".join(hdr))
    print(f"已生成 {ESP/'wakenet_model.h'}")

    # ---- 对拍文件（期望值必须与 C 端同源：int16 PCM 往返后的波形）
    i = int(np.where(va & (y == 0))[0][0])
    xq = feats_to_q(X[i], mean, std)
    pcm16 = (np.clip(X[i], -1, 1) * 32767).astype("<i2")
    x_rt = pcm16.astype(np.float32) / 32768.0
    with open(ESP / "test_features.txt", "w") as f:
        f.write(f"{xq.shape[1]} {xq.shape[0]}\n")
        f.write("\n".join(" ".join(str(int(v)) for v in xq[:, t]) for t in range(xq.shape[1])))
        f.write("\n")
    pq = softmax(qm.forward(xq))
    (ESP / "test_expected.txt").write_text(" ".join(f"{p:.6f}" for p in pq) + "\n")
    (ESP / "test_pcm.raw").write_bytes(pcm16.tobytes())
    (ESP / "test_mel_expected.txt").write_text(
        "\n".join(" ".join(f"{v:.5f}" for v in np.clip((logmel(x_rt) - mean) / std, -4, 4)[t])
                  for t in range(N_FRAMES)) + "\n")
    print("已生成对拍文件 test_features/test_expected/test_pcm/test_mel_expected")
    print("int8 预期输出:", pq.round(4))


if __name__ == "__main__":
    main()
