"""HH-M03 烧录猎手 v3: 实时透传 hsflash 全部输出 + 端口监视自动抢窗。
用法: python hhm03_burn_hunter.py  → 拔插一次 HH-M03 的 USB 线(等2秒再插回)
"""
import subprocess, time, sys, threading, serial.tools.list_ports

HSFLASH = r"D:\hispark\tools\hsflash\hsflash.exe"
FW = r"D:\work\AirMouse-SLE\src\output\bs21e\fwpkg\standard-bs21e-1100e\bs21e_all_in_one.fwpkg"
PORT = "COM8"

def ts():
    return time.strftime("%H:%M:%S")

def com_present():
    return any(p.device == PORT for p in serial.tools.list_ports.comports())

def spawn():
    """启动hsflash, 返回(proc, lines列表, success标记容器)"""
    proc = subprocess.Popen([HSFLASH, "write", "-c", "bs21e", "-p", PORT,
                             "-b", "115200", "-f", FW],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, bufsize=1)
    state = {"lines": [], "success": False}

    def reader():
        try:
            for line in proc.stdout:
                line = line.rstrip()
                if not line:
                    continue
                state["lines"].append(line)
                state["lines"] = state["lines"][-20:]   # 留尾部20行
                # 进度条行会疯狂刷新, 压缩显示: 只在百分比整10%时透传
                s = line.strip()
                if "%" in s:
                    try:
                        pct = int(s.split("%")[0].strip(" [=-]").split("-")[-1].strip(" []=-"))
                        if pct % 10 == 0:
                            print(f"  [hsflash] ...{pct}%", flush=True)
                    except Exception:
                        pass
                else:
                    print(f"  [hsflash] {line}", flush=True)
                if "successfully" in line.lower() and "burn" in line.lower():
                    state["success"] = True
        except Exception:
            pass

    threading.Thread(target=reader, daemon=True).start()
    return proc, state

def main():
    print(f"[hunter v3] {ts()} 等待 {PORT} ...", flush=True)
    t0 = time.time()
    while not com_present():
        time.sleep(0.02)
        if time.time() - t0 > 120:
            print("[hunter] 2分钟没等到端口, 退出"); return 1
    print(f"[hunter] {ts()} 端口在位。", flush=True)
    print("[hunter] >>> 现在可以拔插 HH-M03 的 USB 线了(等2秒再插回), 可重复 <<<", flush=True)

    rounds = 0
    t_end = time.time() + 900   # 15分钟窗口, 只限制开新回合, 绝不打断进行中的烧录
    while True:
        if time.time() > t_end:
            print(f"[hunter] {ts()} 15分钟窗口结束, 停止开新回合", flush=True)
            return 1
        rounds += 1
        print(f"[hunter] {ts()} ---- 回合 {rounds}: 启动 hsflash ----", flush=True)
        proc, state = spawn()

        # 监视: hsflash自然退出 / 端口消失(=拔线或复位)
        while True:
            if proc.poll() is not None:
                print(f"[hunter] {ts()} hsflash 自行退出 (code={proc.returncode})", flush=True)
                break
            if not com_present():
                print(f"[hunter] {ts()} 端口消失(检测到拔线/复位) → 杀 hsflash", flush=True)
                proc.kill(); proc.wait()
                t1 = time.time()
                while not com_present():
                    time.sleep(0.01)
                    if time.time() - t1 > 15:
                        print(f"[hunter] {ts()} 端口15秒没回来", flush=True)
                        break
                back = time.time() - t1
                print(f"[hunter] {ts()} 端口 {back*1000:.0f}ms 后重现 → 立即重启 hsflash 抢窗口", flush=True)
                break
            if state["success"]:
                # 烧录成功, 等 hsflash 自然收尾(自动复位)
                proc.wait(timeout=30)
                break
            time.sleep(0.02)

        if state["success"]:
            print(f"[hunter] {ts()} *** BURN SUCCESS *** (回合{rounds})", flush=True)
            print("[hunter] 验证命令: python -c \"import serial,time;s=serial.Serial('COM8',115200,timeout=.5);t=time.time();b=b'';[b:=b+s.read(512) for _ in iter(lambda:time.time()-t<10,False)];print(b.decode(errors='replace'))\"", flush=True)
            return 0
        if proc.returncode == 0:
            # 没抓到握手, 正常失败, 继续下一回合
            time.sleep(0.05)
            continue
        # 非零退出也被杀过, 继续循环
        time.sleep(0.05)

if __name__ == "__main__":
    sys.exit(main())
