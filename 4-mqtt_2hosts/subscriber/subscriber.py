import paho.mqtt.client as mqtt
import time
import os
import json
import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # ダミーの接続で自身のIPを取得
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = 'unknown'
    finally:
        s.close()
    return ip


cur_ip = get_ip()
print(cur_ip)

# 環境変数から接続情報を取得
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "broker")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "test/topic")
CUR_IP = get_ip()
OUTPUT_FILE_NAME = f"output/latency_log/{CUR_IP}.txt"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Brokerへの接続に成功しました")
        client.subscribe(MQTT_TOPIC)
        print(f"トピック '{MQTT_TOPIC}' の購読を開始しました")
    else:
        print(f"Brokerへの接続に失敗しました (コード: {rc})")


def on_message(client, userdata, msg):
    try:
        # 受信したJSONメッセージをパース
        payload = json.loads(msg.payload.decode())
        send_time = payload["timestamp"]
        receive_time = time.time()

        # 遅延を計算 (ミリ秒)
        latency = (receive_time - send_time) * 1000

        print(f"受信: {payload}, 遅延: {latency:.2f} ms")

        # 遅延をファイルに記録
        with open(OUTPUT_FILE_NAME, "a") as f:
            f.write(f"{latency}\n")

    except (json.JSONDecodeError, KeyError) as e:
        print(f"メッセージの処理中にエラーが発生しました: {e}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

# 無限ループでメッセージを待ち受ける
client.loop_forever()
