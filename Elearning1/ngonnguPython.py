import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
print("TCP_NODELAY và buffer đã được cấu hình.")
s.close()