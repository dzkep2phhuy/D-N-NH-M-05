import socket

host_input = input("Nhập IP server (mặc định localhost): ").strip()
HOST = host_input if host_input else "127.0.0.1"
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

name = input("Nhập tên của bạn: ")
s.sendall(name.encode("utf-8"))

while True:
    msg = s.recv(1024).decode("utf-8", errors="ignore")
    print(msg)
    # chỉ sửa điều kiện dưới đây để nhận cả tiếng Việt lẫn tiếng Anh
    if ("Enter your move" in msg) or ("Nhập lựa chọn" in msg) or ("(kéo/búa/bao)" in msg):
        move = input("Lựa chọn (kéo/búa/bao): ")
        s.sendall(move.encode("utf-8"))
