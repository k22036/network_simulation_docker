#!/bin/bash

# --- ヘルプメッセージとエラー終了のための関数 ---
# この関数を最初に定義しておくと便利です
usage() {
  echo "Error: Capture directory not specified." >&2
  echo "Usage: $0 <CAPTURE_DIRECTORY>" >&2
  exit 1
}

# --- メイン処理 ---

# 引数が提供されていない（-z "$1" は文字列が空かをチェック）場合、
# usage関数を呼び出してエラー終了する
if [ -z "$1" ]; then
  usage
fi

# 引数チェックを通過した場合、第1引数をCAPTURE_DIRとして設定
CAPTURE_DIR="$1"

# 指定されたディレクトリが存在しない場合もエラーメッセージを出して終了
if [ ! -d "$CAPTURE_DIR" ]; then
  echo "Error: The specified directory '${CAPTURE_DIR}' does not exist." >&2
  exit 1
fi

# 合計バイト数を初期化
total_bytes=0

echo "Calculating total bytes from pcap files in ${CAPTURE_DIR}..."

# 指定されたディレクトリ内の全ての.pcapファイルをループ処理
for pcap_file in ${CAPTURE_DIR}/*.pcap
do
  # ワイルドカードにマッチするファイルが一つもなかった場合を考慮
  if [ -f "$pcap_file" ]; then
    echo "Processing file: $pcap_file"
    
    # tsharkでファイル内の全パケットのフレーム長を抽出し、awkで合計する
    bytes_in_file=$(tshark -r "$pcap_file" -T fields -e frame.len | awk '{s+=$1} END {print s}')
    
    # ファイルが空でなかった場合のみ加算
    if [ -n "$bytes_in_file" ]; then
      total_bytes=$((total_bytes + bytes_in_file))
    fi
  else
    echo "Warning: No .pcap files found in the directory."
    # .pcapファイルが一つも見つからなかった場合はループを抜ける
    break
  fi
done

echo "----------------------------------------"
echo "Total Bytes Across All Files: ${total_bytes} bytes"