#!/bin/sh

# --- 設定 ---
IP=$(hostname -I | awk '{print $1}')
# パケットキャプチャの出力先ファイル
OUTPUT_FILE="/app/output/tcp_dump/${IP}.pcap"
# 監視対象のポート
CAPTURE_PORT=1883

# --- スクリプト本体 ---
echo "Starting packet capture to ${OUTPUT_FILE}..."

# tcpdumpをバックグラウンドで実行 (&)
tcpdump -i eth0 -w ${OUTPUT_FILE} port ${CAPTURE_PORT} &

# バックグラウンドで実行したtcpdumpのプロセスIDを取得
TCPDUMP_PID=$!

# Ctrl+Cなどでスクリプトが中断されたときに、tcpdumpを停止するための処理
trap 'echo "Stopping tcpdump (PID: ${TCPDUMP_PID})..."; kill ${TCPDUMP_PID}' SIGINT SIGTERM

echo "Starting subscriber.py..."
# Pythonスクリプトを実行。これが終了するまでシェルは待機する
python -u subscriber.py

# Pythonスクリプトが正常に終了した場合もtcpdumpを停止する
echo "Stopping tcpdump (PID: ${TCPDUMP_PID})..."
kill ${TCPDUMP_PID}

echo "Subscriber script finished."