import socket

host_input = input("Nhập IP server (mặc định localhost): ").strip()
HOST = host_input if host_input else "127.0.0.1"
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

name = input("Nhập tên của bạn: ")
s.sendall(name.encode())

while True:
    msg = s.recv(1024).decode()
    print(msg)
    if "Enter your move" in msg:
        move = input("Lựa chọn (rock/paper/scissors): ")
        s.sendall(move.encode())
