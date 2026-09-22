#!/usr/bin/env python3
"""按键录音采集器：空格开始/停止，一条录音一个文件，自动编号落盘。

专门为采训练数据设计：实时电平条帮你控制距离/音量，音量分桶统计提醒
"花样"够不够（远/正常/近 各来一些，比堆量重要）。

用法:
  .venv/bin/python scripts/record.py                              # 采正样本 → data/raw/mylumos/
  .venv/bin/python scripts/record.py --goal 50                    # 目标 50 条，显示进度
  .venv/bin/python scripts/record.py --dir data/raw/unknown \
      --tag chat --chunk 2                                        # 采负样本(聊天)，长录自动切 2s 一条
  .venv/bin/python scripts/record.py --test                       # 自检：录 1 秒并回放
  .venv/bin/python scripts/record.py --list                       # 列音频设备

按键: [空格]开始/停止并存盘  [ESC]放弃当前  [p]回放上一条  [d]删除上一条  [q]退出
输出: 16kHz 单声道 int16 wav，make_dataset.py 可直接吸收。
注意: 录到 unknown/ 时文件名首段会被当作"说话人"，别用 Daniel/Tessa 开头的 tag。
"""
import argparse, sys, time, wave, pathlib, select, termios, tty
import numpy as np
import sounddevice as sd

SR = 16000
MIN_DUR = 0.3          # 短于这个时长的按误触丢弃
BAR_CELLS, BAR_DB = 22, 60.0   # 电平条：22 格覆盖 -60..0 dB


def dbfs(x: np.ndarray) -> float:
    return 20.0 * np.log10(np.sqrt(np.mean(x.astype(np.float32) ** 2)) + 1e-12)


def bucket(db: float) -> str:
    if db < -33.0:
        return "远/轻"
    if db < -16.0:
        return "正常"
    return "近/响"


def next_seq(directory: pathlib.Path, tag: str) -> int:
    n = 0
    for p in directory.glob(f"{tag}_*.wav"):
        try:
            n = max(n, int(p.stem.rsplit("_", 1)[1]))
        except (ValueError, IndexError):
            pass
    return n + 1


def scan_existing(directory: pathlib.Path, tag: str):
    """统计此前会话已录的条数和音量分桶（只认 {tag}_ 前缀，不混入 TTS 文件）。"""
    files = sorted(directory.glob(f"{tag}_*.wav"))[:500]
    stat = {"远/轻": 0, "正常": 0, "近/响": 0}
    for p in files:
        try:
            with wave.open(str(p)) as w:
                x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
            stat[bucket(dbfs(x))] += 1
        except Exception:
            pass
    return len(files), stat


def save_wav(path: pathlib.Path, pcm: np.ndarray):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def meter(db: float) -> str:
    n = int(np.clip((db + BAR_DB) / BAR_DB, 0, 1) * BAR_CELLS)
    return "█" * n + "░" * (BAR_CELLS - n)


class Rec:
    """一个打开的输入流：callback 攒数据 + 维护实时电平。"""

    def __init__(self, device):
        self.chunks, self.peak, self.rms_db = [], 0.0, -90.0
        self.stream = sd.InputStream(samplerate=SR, channels=1, dtype="int16",
                                     blocksize=1024, device=device, callback=self._cb)
        self.stream.start()

    def _cb(self, indata, frames, t, status):
        x = np.frombuffer(indata, dtype=np.int16)
        self.chunks.append(x.copy())
        f = x.astype(np.float32) / 32768.0
        self.peak = max(self.peak, float(np.abs(f).max()))
        self.rms_db = dbfs(f)

    def stop(self) -> np.ndarray:
        self.stream.stop()
        self.stream.close()
        return np.concatenate(self.chunks) if self.chunks else np.array([], dtype=np.int16)


def erase_line():
    sys.stdout.write("\r\x1b[K")


def read_key(timeout):
    r, _, _ = select.select([sys.stdin], [], [], timeout)
    if not r:
        return None
    ch = sys.stdin.read(1)
    if ch == "\x1b":  # 真按 ESC 只发 1 字节；方向键会跟后续字节，排掉
        r2, _, _ = select.select([sys.stdin], [], [], 0.02)
        while r2:
            sys.stdin.read(1)
            r2, _, _ = select.select([sys.stdin], [], [], 0.02)
        return "ESC"
    return ch


def run(args):
    out_dir: pathlib.Path = args.dir
    out_dir.mkdir(parents=True, exist_ok=True)
    seq = next_seq(out_dir, args.tag)
    n_exist, exist_stat = scan_existing(out_dir, args.tag)
    sess_stat = {"远/轻": 0, "正常": 0, "近/响": 0}
    sess_n, last_path = 0, None

    def goal_mark():
        return f"{n_exist + sess_n}/{args.goal}" if args.goal else f"{n_exist + sess_n}"

    print(f"设备: {sd.query_devices(args.device)['name']}")
    print(f"目录: {out_dir}  （已有 {args.tag}_* 文件 {n_exist} 条"
          f"：远/轻{exist_stat['远/轻']} 正常{exist_stat['正常']} 近/响{exist_stat['近/响']}）")
    print("[空格]开始/停止并存盘  [ESC]放弃  [p]回放上一条  [d]删上一条  [q]退出\n")

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    rec = None
    try:
        tty.setcbreak(fd)
        while True:
            key = read_key(0.05)
            if rec is None:
                if key == "q":
                    break
                elif key == " ":
                    rec = Rec(args.device)
                elif key == "p" and last_path and last_path.exists():
                    with wave.open(str(last_path)) as w:
                        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
                    print(f"♪ 回放 {last_path.name} …")
                    sd.play(x, SR)
                    sd.wait()
                elif key == "d" and last_path and last_path.exists():
                    last_path.unlink()
                    seq, sess_n = seq - 1, max(0, sess_n - 1)
                    print(f"✗ 已删除 {last_path.name}（{goal_mark()}）")
                    last_path = None
                if rec is None:
                    erase_line()
                    sys.stdout.write(f"● 待机 {goal_mark()} 条 — 按空格开始录"
                                     f"（提示：{args.hint}）")
                    sys.stdout.flush()
            else:
                dur = sum(len(c) for c in rec.chunks) / SR
                if key == " " or key == "ESC":
                    pcm = rec.stop()
                    rec = None
                    dur = len(pcm) / SR
                    if key == "ESC":
                        print(f"— 已放弃（{dur:.1f}s）")
                        continue
                    if dur < MIN_DUR:
                        print(f"— 太短({dur:.2f}s)未保存，按住说完一整句再停")
                        continue
                    f = pcm.astype(np.float32) / 32768.0
                    db, peak = dbfs(f), float(np.abs(f).max())
                    pk_db = 20.0 * np.log10(peak + 1e-12)
                    b = bucket(db)
                    if args.chunk and dur > 2 * args.chunk:   # 长录音切块（负样本聊天模式）
                        step, saved = int(args.chunk * SR), []
                        for i in range(0, len(pcm) - int(0.5 * SR), step):
                            p = out_dir / f"{args.tag}_{seq:03d}.wav"
                            save_wav(p, pcm[i:i + step])
                            saved.append(p.name)
                            seq, sess_n = sess_n + 1, sess_n + 1
                        print(f"✓ 切成 {len(saved)} 条: {' '.join(saved)}（各 {args.chunk}s）")
                    else:
                        p = out_dir / f"{args.tag}_{seq:03d}.wav"
                        save_wav(p, pcm)
                        last_path = p
                        seq, sess_n = sess_n + 1, sess_n + 1
                        clip = "  ⚠ 削波！离麦远点或小声点" if np.abs(f).max() >= 0.98 else ""
                        print(f"✓ {p.name}  {dur:.2f}s  rms {db:.1f}dB  peak {pk_db:.1f}dB"
                              f"  [{b}]{clip}")
                    sess_stat[b] += 1
                    print(f"  本会话累计 {goal_mark()} 条 — 远/轻{sess_stat['远/轻']}"
                          f" 正常{sess_stat['正常']} 近/响{sess_stat['近/响']}"
                          f"（三类都要有，别只录同一距离）")
                else:
                    erase_line()
                    sys.stdout.write(f"● 录音 {dur:.1f}s {meter(rec.rms_db)} {rec.rms_db:.1f}dB"
                                     f"  [空格]存 [ESC]弃")
                    sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        print(f"\n会话结束：本次录 {sess_n} 条，目录共 {n_exist + sess_n} 条"
              f"{f'（目标 {args.goal}）' if args.goal else ''}")
        print("下一步: .venv/bin/python scripts/make_dataset.py && "
              ".venv/bin/python scripts/train.py && .venv/bin/python scripts/export_c.py")


def self_test(args):
    print(f"设备: {sd.query_devices(args.device)['name']}，录 1 秒…")
    rec = Rec(args.device)
    time.sleep(1.0)
    pcm = rec.stop()
    f = pcm.astype(np.float32) / 32768.0
    db = dbfs(f)
    print(f"时长 {len(pcm)/SR:.2f}s  rms {db:.1f}dB（{bucket(db)}）"
          f"  peak {20*np.log10(np.abs(f).max()+1e-12):.1f}dB")
    print("回放中…听一下是不是自己的声音")
    sd.play(pcm, SR)
    sd.wait()
    print("自检通过。正式采集: .venv/bin/python scripts/record.py")


def main():
    ap = argparse.ArgumentParser(description="唤醒词训练数据按键采集器")
    here = pathlib.Path(__file__).resolve().parents[1]
    ap.add_argument("--dir", type=pathlib.Path, default=here / "data/raw/mylumos",
                    help="落盘目录（默认 data/raw/mylumos）")
    ap.add_argument("--tag", default="own", help="文件名前缀，兼作 unknown/ 里的说话人名")
    ap.add_argument("--goal", type=int, default=None, help="目标条数，显示进度")
    ap.add_argument("--chunk", type=float, default=None, metavar="SEC",
                    help="长录音按 SEC 秒切块各存一条（采负样本聊天用）")
    ap.add_argument("--device", type=int, default=None, help="输入设备号（--list 查看）")
    ap.add_argument("--hint", default="远中近各来几条", help="待机行里的采集提示")
    ap.add_argument("--list", action="store_true", help="列出音频设备后退出")
    ap.add_argument("--test", action="store_true", help="自检：录 1 秒并回放")
    args = ap.parse_args()
    try:
        if args.list:
            for i, d in enumerate(sd.query_devices()):
                if d["max_input_channels"] > 0:
                    print(f"[{i}] {d['name']}")
            return
        if args.test:
            self_test(args)
            return
        run(args)
    except sd.PortAudioError as e:
        sys.exit(f"打不开麦克风: {e}\n如果是权限问题：系统设置 → 隐私与安全性 → 麦克风 → "
                 "勾选你运行 Python 的终端 App，然后重开终端。")


if __name__ == "__main__":
    main()
