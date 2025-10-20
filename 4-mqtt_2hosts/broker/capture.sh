#!/bin/sh
set -e

# --- 設定 ---
OUTPUT_FILE=/mosquitto/log/capture.pcap
CAPTURE_PORT=1883
Docker_EXEC="docker exec -it mqtt_broker"

# --- スクリプト本体 ---
${Docker_EXEC} apk add tcpdump
${Docker_EXEC} tcpdump -i eth0 -w ${OUTPUT_FILE} port ${CAPTURE_PORT}