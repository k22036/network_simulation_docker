#!/bin/bash
set -euo pipefail

TARGET_DIR="subscriber/output/latency_log"

# ファイルが存在するか確認
files=( "$TARGET_DIR"/*.txt )
if [ ${#files[@]} -eq 0 ]; then
    # 黄色で強調表示
    printf '\e[33m%s\e[0m\n' "No data found."
    exit 1
fi

# 平均を計算（ミリ秒）
avg=$(awk '{ total += $1; count++ } END { if (count>0) printf "%.3f", total/count; else print "NaN" }' "${files[@]}")

# 結果を太字＋緑で強調表示
printf '\e[1;32mAverage Latency: %s ms\e[0m\n' "$avg"