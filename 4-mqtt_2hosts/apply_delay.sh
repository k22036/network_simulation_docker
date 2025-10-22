#!/bin/bash

# --- 設定項目 ---
DELAY="20ms"

# --- スクリプト本体 ---

# root権限で実行されているかチェック
if [ "$(id -u)" -ne 0 ]; then
  echo "このスクリプトは管理者権限（sudo）で実行する必要があります。" >&2
  exit 1
fi

echo "すべてのvethインターフェースに ${DELAY} の遅延を追加します..."
echo ""

for VETH in $(ip -o link | awk -F': ' '/veth/ {print $2}' | cut -d'@' -f1); do
  echo "-> ${VETH} の遅延を ${DELAY} に設定/置換中..."
  tc qdisc replace dev "${VETH}" root netem delay "${DELAY}"
  echo "   完了: ${VETH} の遅延を ${DELAY} に設定しました。"
done

echo ""
echo "すべてのvethインターフェースへの遅延設定が完了しました。"