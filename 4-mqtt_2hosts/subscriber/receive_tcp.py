import socket

s = socket.socket()
s.bind(("0.0.0.0", 5000))
s.listen(1)
print("Server waiting...")
conn, addr = s.accept()
print("Connected from", addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Received:", data.decode())

conn.close()
