#!/usr/bin/env python3
"""训练迷你唤醒词模型（自研 WakeNet 复刻版）。

配方照 WakeNet 文档：MFCC/log-mel 特征(30ms窗/10ms步) + 小型量化友好 CNN + 平滑触发。
模型: Conv1d → [深度可分离卷积×2 (膨胀卷积)] → 时间平均池化 → 全连接 3 类
      (lumos / unknown / noise)，约 12k 参数。
"""
import json, pathlib, time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

ROOT = pathlib.Path(__file__).resolve().parents[1]
SR, WIN, HOP, N_MEL, N_FFT = 16000, 480, 160, 40, 512
CLIP, N_FRAMES = 16000, 97
CLASSES = ["lumos", "unknown", "noise"]


# ---------------------------------------------------------------- 特征前端
def hz2mel(f):
    return 2595.0 * np.log10(1.0 + f / 700.0)


def mel2hz(m):
    return 700.0 * (10.0 ** (m / 2595.0) - 1.0)


def mel_filterbank():
    fmin, fmax = 40.0, SR / 2
    mel_pts = np.linspace(hz2mel(fmin), hz2mel(fmax), N_MEL + 2)
    bins = np.floor((N_FFT + 1) * mel2hz(mel_pts) / SR).astype(int)
    fb = np.zeros((N_MEL, N_FFT // 2 + 1), dtype=np.float32)
    for m in range(1, N_MEL + 1):
        l, c, r = bins[m - 1], bins[m], bins[m + 1]
        for k in range(l, c):
            fb[m - 1, k] = (k - l) / max(1, c - l)
        for k in range(c, r):
            fb[m - 1, k] = (r - k) / max(1, r - c)
    return fb


FB = mel_filterbank()
WINDOW = np.hanning(WIN).astype(np.float32)


def logmel(x: np.ndarray) -> np.ndarray:
    """x: (16000,) float32 [-1,1] → (97, 40) log-mel（未归一化）。
    mel 投影与 log 用 float64（与 esp32/mel_fbank.c 的 double 累加对齐）。"""
    frames = np.lib.stride_tricks.sliding_window_view(x, WIN)[::HOP][:N_FRAMES]
    spec = np.abs(np.fft.rfft(frames * WINDOW, n=N_FFT, axis=1)) ** 2
    mel = np.log10(spec.astype(np.float64) @ FB.T.astype(np.float64) + 1e-8)
    return mel.astype(np.float32)


def compute_stats(X):
    feats = np.stack([logmel(x) for x in X])
    return float(feats.mean()), float(feats.std())


# ---------------------------------------------------------------- 模型
class DSConv(nn.Module):
    """深度可分离一维卷积：depthwise(带膨胀) + pointwise，WakeNet9s 的基本积木。"""

    def __init__(self, cin, cout, k, dilation):
        super().__init__()
        pad = dilation * (k - 1) // 2
        self.dw = nn.Conv1d(cin, cin, k, padding=pad, dilation=dilation, groups=cin)
        self.pw = nn.Conv1d(cin, cout, 1)

    def forward(self, x):
        return self.pw(self.dw(x))


class MiniWakeNet(nn.Module):
    """3 个深度可分离块（膨胀率 1,2,4,8），感受野 ~600ms 覆盖整个唤醒词。"""

    def __init__(self, n_in=40, ch=(48, 64, 96, 128), n_cls=3):
        super().__init__()
        self.ch = ch
        self.stem = nn.Conv1d(n_in, ch[0], 5, padding=2)
        self.b1 = DSConv(ch[0], ch[1], 5, 2)
        self.b2 = DSConv(ch[1], ch[2], 5, 4)
        self.b3 = DSConv(ch[2], ch[3], 5, 8)
        self.fc = nn.Linear(ch[3], n_cls)

    def forward(self, x):                    # x: (B, 40, 97)
        h = torch.relu(self.stem(x))
        h = torch.relu(self.b1(h))
        h = torch.relu(self.b2(h))
        h = torch.relu(self.b3(h))           # (B, 128, 97)
        h = h.mean(dim=2)                    # 时间 GAP
        return self.fc(h)

    def _fwd_qat(self, x, sc):
        """量化感知前向：伪量化路径与 export_c.py 的 int8 前向同构。"""
        x = fq_act(x, 4.0, relu=False)       # 输入特征 clamp±4 后量化
        h = F.relu(F.conv1d(x, wfq(self.stem.weight), self.stem.bias, padding=2))
        h = fq_act(h, sc["stem"])
        h = F.relu(F.conv1d(h, wfq(self.b1.dw.weight), self.b1.dw.bias,
                            padding=4, dilation=2, groups=self.ch[0]))
        h = fq_act(h, sc["b1.dw"])
        h = F.relu(F.conv1d(h, wfq(self.b1.pw.weight), self.b1.pw.bias))
        h = fq_act(h, sc["b1.pw"])
        h = F.relu(F.conv1d(h, wfq(self.b2.dw.weight), self.b2.dw.bias,
                            padding=8, dilation=4, groups=self.ch[1]))
        h = fq_act(h, sc["b2.dw"])
        h = F.relu(F.conv1d(h, wfq(self.b2.pw.weight), self.b2.pw.bias))
        h = fq_act(h, sc["b2.pw"])
        h = F.relu(F.conv1d(h, wfq(self.b3.dw.weight), self.b3.dw.bias,
                            padding=16, dilation=8, groups=self.ch[2]))
        h = fq_act(h, sc["b3.dw"])
        h = F.relu(F.conv1d(h, wfq(self.b3.pw.weight), self.b3.pw.bias))
        h = fq_act(h, sc["b3.pw"])
        h = h.mean(dim=2)
        h = fq_act(h, sc["b3.pw"])           # GAP 后取整（scale 不变）
        return F.linear(h, wfq(self.fc.weight), self.fc.bias)


def wfq(w: torch.Tensor) -> torch.Tensor:
    """权重伪量化：逐输出通道对称 int8，直通估计器（STE）。"""
    s = w.detach().abs().amax(dim=tuple(range(1, w.ndim)), keepdim=True) / 127.0
    s = s.clamp(min=1e-8)
    q = torch.round(w / s).clamp(-127, 127) * s
    return w + (q - w).detach()


def fq_act(x: torch.Tensor, scale: float, relu: bool = True) -> torch.Tensor:
    """激活伪量化：对称 int8（ReLU 层下限 0），STE。"""
    s = max(scale, 1e-8) / 127.0
    lo = 0.0 if relu else -127.0
    q = torch.round(x / s).clamp(lo, 127.0) * s
    return x + (q - x).detach()


class QATWrap(nn.Module):
    """把 _fwd_qat 包成普通 module，复用 evaluate / fa_stream_eval。"""

    def __init__(self, m, sc):
        super().__init__()
        self.m, self.sc = m, sc

    def forward(self, x):
        return self.m._fwd_qat(x, self.sc)


def calibrate_scales(model, X, mean, std, n_batches=40):
    """确定性激活标定：未增广数据 + 固定种子，训练与导出共用同一结果。"""
    ds = DS(X, np.zeros(len(X), dtype=np.int64), mean, std, train=False)
    g = torch.Generator().manual_seed(0)
    dl = torch.utils.data.DataLoader(ds, batch_size=64, shuffle=True, generator=g)
    acts, hooks = {}, []
    for name, mod in [("stem", model.stem), ("b1.dw", model.b1.dw), ("b1.pw", model.b1.pw),
                      ("b2.dw", model.b2.dw), ("b2.pw", model.b2.pw),
                      ("b3.dw", model.b3.dw), ("b3.pw", model.b3.pw), ("fc", model.fc)]:
        acts[name] = []
        hooks.append(mod.register_forward_hook(
            lambda m, i, o, n=name: acts[n].append(float(o.abs().max()))))
    model.eval()
    with torch.no_grad():
        for bi, (xb, _) in enumerate(dl):
            model(xb)
            if bi >= n_batches:
                break
    for h in hooks:
        h.remove()
    return {n: max(v) for n, v in acts.items()}


# ---------------------------------------------------------------- 数据
class DS(torch.utils.data.Dataset):
    def __init__(self, X, y, mean, std, train=True):
        self.X, self.y = X, y
        self.mean, self.std, self.train = mean, std, train

    def __len__(self):
        return len(self.y)

    def augment(self, x):
        rng = np.random.default_rng()
        x = x * rng.uniform(0.25, 1.0)                        # 随机增益
        snr = rng.uniform(12, 40)
        noise = rng.standard_normal(len(x)).astype(np.float32)
        x = x + noise * (np.sqrt(np.mean(x ** 2)) + 1e-4) / (10 ** (snr / 20))
        shift = rng.integers(-2400, 2400)                     # ±150ms 环移
        x = np.roll(x, shift)
        return x.astype(np.float32)

    def __getitem__(self, i):
        x = self.X[i].copy()
        if self.train:
            x = self.augment(x)
        f = (logmel(x) - self.mean) / self.std
        if self.train:                                        # SpecAugment
            rng = np.random.default_rng()
            if rng.random() < 0.5:
                b = rng.integers(0, N_MEL - 6)
                f[:, b:b + 6] = 0.0
            if rng.random() < 0.5:
                b = rng.integers(0, N_FRAMES - 12)
                f[b:b + 12, :] = 0.0
        f = np.clip(f, -4.0, 4.0)
        return torch.from_numpy(f.T.copy()), int(self.y[i])


# ---------------------------------------------------------------- 训练与评估
def evaluate(model, loader):
    model.eval()
    cm = np.zeros((3, 3), int)
    probs = []
    with torch.no_grad():
        for xb, yb in loader:
            p = torch.softmax(model(xb), 1)
            for pi, yi in zip(p.numpy(), yb.numpy()):
                cm[yi, pi.argmax()] += 1
                probs.append((pi[0], yi))
    acc = cm.diagonal().sum() / cm.sum()
    return acc, cm, probs


def fa_stream_eval(model, X_val_unknown, X_val_noise, mean, std):
    """把验证集负样本+噪声拼成连续流，1s 窗、0.32s 步进，统计误触发。"""
    rng = np.random.default_rng(3)
    parts, dur = [], 0.0
    pool = list(X_val_unknown) + list(X_val_noise)
    rng.shuffle(pool)
    for i, x in enumerate(pool[:80]):
        parts.append(x)
        parts.append(rng.standard_normal(16000).astype(np.float32) * 0.003)
        dur += 2.0
    stream = np.concatenate(parts)
    model.eval()
    n_win, hits = 0, 0
    with torch.no_grad():
        for s in range(0, len(stream) - CLIP + 1, int(0.32 * SR)):
            f = torch.from_numpy(np.clip((logmel(stream[s:s + CLIP]) - mean) / std, -4, 4).T.copy()).unsqueeze(0)
            p = torch.softmax(model(f), 1)[0, 0].item()
            n_win += 1
            hits += p > 0.9
    fa_per_hour = hits / (dur / 3600) if dur else 0
    return n_win, hits, dur, fa_per_hour


def main():
    t0 = time.time()
    d = np.load(ROOT / "data" / "dataset.npz", allow_pickle=True)
    X, y, val = d["X"], d["y"], d["val"]
    tr, va = val == 0, val == 1
    mean, std = compute_stats(X[tr][::4])
    print(f"统计: mean={mean:.4f} std={std:.4f}  train={tr.sum()} val={va.sum()}")

    g = torch.Generator().manual_seed(0)
    cls_n = np.bincount(y[tr])                                 # 类平衡采样：正样本被过采样
    w = (1.0 / cls_n[y[tr]]).astype(np.double)
    sampler = torch.utils.data.WeightedRandomSampler(torch.as_tensor(w), num_samples=len(y[tr]),
                                                     replacement=True, generator=g)
    dl_tr = torch.utils.data.DataLoader(DS(X[tr], y[tr], mean, std, True), batch_size=64,
                                        sampler=sampler, num_workers=0)
    dl_va = torch.utils.data.DataLoader(DS(X[va], y[va], mean, std, False), batch_size=64)

    model = MiniWakeNet()
    torch.manual_seed(0)
    n_par = sum(p.numel() for p in model.parameters())
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    lossf = nn.CrossEntropyLoss()

    def quick_score(m):
        """返回 (score, 召回, unknown误报率)：score = 召回 - 2×误报，用于挑最优 checkpoint"""
        _, _, probs = evaluate(m, dl_va)
        pos = [p for p, yi in probs if yi == 0]
        unk = [p for p, yi in probs if yi == 1]
        rec = float(np.mean([p > 0.5 for p in pos])) if pos else 0
        fa = float(np.mean([p > 0.5 for p in unk])) if unk else 0
        return rec - 2 * fa, rec, fa

    best_score, best_state = -1.0, None
    for ep in range(50):
        for pg in opt.param_groups:
            pg["lr"] = 1.5e-3 if ep < 25 else (7e-4 if ep < 40 else 3e-4)
        model.train()
        tot, corr, losses = 0, 0, []
        for xb, yb in dl_tr:
            opt.zero_grad()
            out = model(xb)
            loss = lossf(out, yb)
            loss.backward()
            opt.step()
            losses.append(loss.item())
            corr += (out.argmax(1) == yb).sum().item()
            tot += len(yb)
        sc, rec, fa = quick_score(model)
        if sc > best_score:
            best_score = sc
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        if ep % 5 == 4 or ep == 49:
            print(f"epoch {ep}: loss={np.mean(losses):.4f} train_acc={corr/tot:.3f} "
                  f"val召回={rec:.3f} val误报={fa:.3f} best_score={best_score:.3f}")
    model.load_state_dict(best_state)   # 回滚验证集表现最好的 checkpoint

    # ---- 阶段 2：量化感知微调（QAT）——伪量化前向训练，保住 int8 部署后的边距
    scales = calibrate_scales(model, X[tr], mean, std)
    print("激活标定:", {k: round(v, 2) for k, v in scales.items()})
    qmodel = QATWrap(model, scales)
    opt = torch.optim.Adam(model.parameters(), lr=3e-4)
    best2, best2_state = quick_score(qmodel)[0], {k: v.detach().clone() for k, v in model.state_dict().items()}
    for ep in range(20):
        model.train()
        losses = []
        for xb, yb in dl_tr:
            opt.zero_grad()
            out = model._fwd_qat(xb, scales)
            loss = lossf(out, yb)
            loss.backward()
            opt.step()
            losses.append(loss.item())
        sc, rec, fa = quick_score(qmodel)
        if sc > best2:
            best2, best2_state = sc, {k: v.detach().clone() for k, v in model.state_dict().items()}
        if ep % 5 == 4 or ep == 19:
            print(f"QAT {ep}: loss={np.mean(losses):.4f} val召回={rec:.3f} val误报={fa:.3f} best={best2:.3f}")
    model.load_state_dict(best2_state)

    # 最终指标用 QAT 前向评估（≈ 部署后的 int8 行为）
    acc, cm, probs = evaluate(qmodel, dl_va)
    print("\n[QAT/int8 等效] 验证集混淆矩阵 (行=真实 lumos/unknown/noise):")
    print(cm)
    pos = [p for p, yi in probs if yi == 0]
    r50 = np.mean([p > 0.5 for p in pos])
    r90 = np.mean([p > 0.9 for p in pos])
    print(f"正样本召回: thr=0.5 → {r50:.3f}   thr=0.9 → {r90:.3f}")

    unk_idx = np.where(va & (y == 1))[0]
    noi_idx = np.where(va & (y == 2))[0]
    n_win, hits, dur, fah = fa_stream_eval(qmodel, X[unk_idx], X[noi_idx], mean, std)
    print(f"误报流测试: {dur:.0f}s / {n_win} 窗 → p>0.9 命中 {hits} 次 ≈ {fah:.1f} 次/小时")

    torch.save(model.state_dict(), ROOT / "models" / "model.pt")
    (ROOT / "models" / "stats.json").write_text(json.dumps({
        "mean": mean, "std": std, "val_acc": acc, "confusion": cm.tolist(),
        "recall@0.5": float(r50), "recall@0.9": float(r90),
        "fa_hits": int(hits), "fa_seconds": dur, "fa_per_hour": float(fah),
        "act_max": scales, "params": n_par,
    }, indent=2))
    print(f"\n参数量 {n_par}  总耗时 {time.time()-t0:.0f}s  已保存 models/model.pt")


if __name__ == "__main__":
    main()
