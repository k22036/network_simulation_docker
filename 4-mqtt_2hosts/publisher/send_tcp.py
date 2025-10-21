import socket
import time

# ---- settings ----
number_of_messages = 5
# ------------------

# Client側
time.sleep(1)  # サーバ起動待ち
print("Client connecting to server...")
s = socket.socket()
s.connect(("172.28.1.2", 5000))
for i in range(number_of_messages):
    s.sendall(f"Hello from client! Message {i+1}".encode())
    time.sleep(1)
s.close()
