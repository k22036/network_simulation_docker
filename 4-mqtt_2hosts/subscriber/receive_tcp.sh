#!/bin/bash
set -e

# --- 設定 ---
IP=$(hostname -I | awk '{print $1}')
# パケットキャプチャの出力先ファイル
OUTPUT_FILE="/app/output/debug/${IP}.pcap"
# 監視対象のポート
CAPTURE_PORT=5000

# tcpdumpをバックグラウンドで実行 (&)
tcpdump -i eth0 -w ${OUTPUT_FILE} port ${CAPTURE_PORT} &

# バックグラウンドで実行したtcpdumpのプロセスIDを取得
TCPDUMP_PID=$!

# Ctrl+Cなどでスクリプトが中断されたときに、tcpdumpを停止するための処理
trap 'echo "Stopping tcpdump (PID: ${TCPDUMP_PID})..."; kill ${TCPDUMP_PID}' SIGINT SIGTERM

sleep 2
python receive_tcp.py
sleep 2
kill ${TCPDUMP_PID}
