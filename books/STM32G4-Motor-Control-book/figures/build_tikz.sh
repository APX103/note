#!/bin/bash
# 编译全部 TikZ 图为 PDF，输出到 ../images/
set -e
cd "$(dirname "$0")"
mkdir -p ../images
for f in fig_*.tex; do
  name="${f%.tex}"
  echo "=== $name ==="
  tectonic -X compile --outdir ../images "$f" 2>&1 | grep -E 'error|warning: font' || true
done
ls -la ../images/*.pdf
