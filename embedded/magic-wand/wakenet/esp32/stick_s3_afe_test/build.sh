#!/bin/zsh
# 组装并编译/烧录 AFE 集成实测固件（StickS3 N8R8：8MB Flash + OPI PSRAM）。
# 用法: ./build.sh            # 只编译
#       ./build.sh /dev/cu.usbmodemXXX   # 编译+烧录+监视
set -e
cd "$(dirname "$0")"
cp ../wakenet.c ../wakenet.h ../mel_fbank.c ../mel_fbank.h ../wakenet_model.h .
FQBN="esp32:esp32:esp32s3:FlashSize=8M,PSRAM=opi"
echo "==> compile $FQBN"
arduino-cli compile --fqbn "$FQBN" .
if [ -n "$1" ]; then
    echo "==> upload $1"
    arduino-cli upload -p "$1" --fqbn "$FQBN" .
    echo "==> monitor (ctrl+] 退出)"
    arduino-cli monitor -p "$1" -c baudrate=115200
fi
