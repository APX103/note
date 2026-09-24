#!/bin/bash
# download_pdfs.sh —— 从 ADI 官网批量下载原书 PDF（整本 + 11 章 + 4 附录）
# 用法: bash tools/download_pdfs.sh   （在书目录下执行，产物落 pdf/）
# 注意: 整本书 SDR4Engineers.pdf 约 17.3MB，CDN 对单连接有 1MiB 截断，
#       必须用 Range 分块下载后拼接（本脚本已内置）。

set -e
cd "$(dirname "$0")/.."
mkdir -p pdf
cd pdf

BASE="https://www.analog.com/media/en/training-seminars/design-handbooks/Software-Defined-Radio-for-Engineers-2018"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
REF="https://www.analog.com/en/resources/technical-books/software-defined-radio-for-engineers.html"
FILES="SDR4Engineers_CH01.pdf SDR4Engineers_CH02.pdf SDR4Engineers_CH03.pdf SDR4Engineers_CH04.pdf SDR4Engineers_CH05.pdf SDR4Engineers_CH06.pdf SDR4Engineers_CH07.pdf SDR4Engineers_CH08.pdf SDR4Engineers_CH09.pdf SDR4Engineers_CH10.pdf SDR4Engineers_CH11.pdf SDR4Engineers_Appendix-A.pdf SDR4Engineers_Appendix-B.pdf SDR4Engineers_Appendix-C.pdf SDR4Engineers_Appendix-D.pdf"

for f in $FILES; do
  [ -s "$f" ] && { echo "跳过(已存在): $f"; continue; }
  echo "下载: $f"
  curl -sL --retry 3 -H "User-Agent: $UA" -H "Accept: application/pdf,*/*" -H "Referer: $REF" "$BASE/$f" -o "$f"
  sleep 1
done

# 整本书：Range 分块下载
if [ ! -s SDR4Engineers.pdf ] || [ "$(wc -c < SDR4Engineers.pdf | tr -d ' ')" -ne 18147267 ]; then
  echo "分块下载整本书 SDR4Engineers.pdf ..."
  TOTAL=18147267; CHUNK=1048576; START=0; N=0
  rm -f SDR4Engineers.pdf /tmp/sdr_full_part_???
  while [ $START -lt $TOTAL ]; do
    END=$((START + CHUNK - 1)); [ $END -ge $TOTAL ] && END=$((TOTAL - 1))
    curl -sL --retry 3 -H "User-Agent: $UA" -H "Accept: application/pdf,*/*" \
      -H "Range: bytes=$START-$END" "$BASE/SDR4Engineers.pdf" -o /tmp/sdr_full_part_$(printf %03d $N)
    START=$((END + 1)); N=$((N + 1))
  done
  cat /tmp/sdr_full_part_??? > SDR4Engineers.pdf
  rm -f /tmp/sdr_full_part_???
fi

echo; echo "== 结果 =="
for f in *.pdf; do printf "%-30s %10s bytes\n" "$f" "$(wc -c < "$f" | tr -d ' ')"; done
