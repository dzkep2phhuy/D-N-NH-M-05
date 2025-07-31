import socket
import threading
import queue

HOST = "0.0.0.0"
PORT = 9999

match_queue = queue.Queue()


def determine_winner(p1, p2):
    if p1 == p2:
        return "hòa"
    elif (
        (p1 == "búa" and p2 == "kéo")
        or (p1 == "kéo" and p2 == "bao")
        or (p1 == "bao" and p2 == "búa")
    ):
        return "thắng"
    else:
        return "thua"


def handle_client(conn, addr):
    try:
        name = conn.recv(1024).decode().strip()
        conn.sendall("Đợi đối thủ...\n".encode('utf-8'))
        match_queue.put((conn, name))

        while True:
            if match_queue.qsize() >= 2:
                player1 = match_queue.get()
                player2 = match_queue.get()

                c1, name1 = player1
                c2, name2 = player2

                c1.sendall(f"Ghép trận cùng {name2}! Nhập lựa chọn (kéo/búa/bao): ".encode())
                c2.sendall(f"Ghép trận cùng {name1}! Nhập lựa chọn (kéo/búa/bao): ".encode())

                m1 = c1.recv(1024).decode().strip().lower()
                m2 = c2.recv(1024).decode().strip().lower()

                if not m1 or not m2:
                    c1.close()
                    c2.close()
                    break

                r1 = determine_winner(m1, m2)
                r2 = determine_winner(m2, m1)

                c1.sendall(f"Bạn chọn: {m1}, đối thủ chọn: {m2}. Kết quả: {r1.upper()}\n".encode())
                c2.sendall(f"Bạn chọn: {m2}, đối thủ chọn: {m1}. Kết quả: {r2.upper()}\n".encode())

                # Cho vào hàng đợi lại nếu vẫn còn chơi tiếp
                match_queue.put((c1, name1))
                match_queue.put((c2, name2))
    except:
        conn.close()


def start_server():
    print(f"🟢 Máy chủ đang chạy trên cổng {PORT}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        print(f"🔗 Kết nối mới từ {addr}")
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_server()
