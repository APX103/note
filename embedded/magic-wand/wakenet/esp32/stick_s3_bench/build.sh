#!/bin/zsh
# 一键组装并烧录 StickS3 性能基准（15 分钟内把算力估算变成实测）。
# 用法: cd wakenet/esp32/stick_s3_bench && ./build.sh [串口设备名]
#   串口默认 /dev/cu.usbmodem*（StickS3 原生 USB；刷机细节见仓库 m5sticks3-demo-flashing-setup.html）
set -e
cd "$(dirname "$0")"
cp ../wakenet.c ../wakenet.h ../mel_fbank.c ../mel_fbank.h ../wakenet_model.h .
PORT="${1:-/dev/cu.usbmodem*}"
echo "==> compile esp32:esp32:esp32s3"
arduino-cli compile --fqbn esp32:esp32:esp32s3 .
echo "==> upload to $PORT"
arduino-cli upload -p "$PORT" --fqbn esp32:esp32:esp32s3 .
echo "==> monitor (ctrl+] 退出)"
arduino-cli monitor -p "$PORT" -c baudrate=115200
