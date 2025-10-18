import paho.mqtt.client as mqtt
import time
import os
import json

# 環境変数から接続情報を取得
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "broker")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "test/topic")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Brokerへの接続に成功しました")
    else:
        print(f"Brokerへの接続に失敗しました (コード: {rc})")


client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

client.loop_start()

try:
    for message_count in range(1, 101):
        payload = {
            "message_id": message_count,
            "timestamp": time.time()
        }
        # JSON形式でメッセージを送信
        client.publish(MQTT_TOPIC, json.dumps(payload))
        print(f"送信: {payload}")
        time.sleep(1)  # 1秒ごとに送信
except KeyboardInterrupt:
    print("送信を終了します。")
finally:
    client.loop_stop()
    client.disconnect()
