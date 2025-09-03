# server.py
import socket
import threading
import sys
from typing import Dict

HOST = "0.0.0.0"
DEFAULT_PORT = 55555
ENC = "utf-8"

clients_lock = threading.Lock()
# socket -> username
socket_to_name: Dict[socket.socket, str] = {}
# username -> socket
name_to_socket: Dict[str, socket.socket] = {}

WELCOME = (
    "Chào mừng đến với Chat!\n"
    "Lệnh: /nick <ten>, /list, /pm <ten> <msg>, /quit, /help\n"
)

def send_line(conn: socket.socket, line: str):
    try:
        conn.sendall((line + "\n").encode(ENC))
    except OSError:
        pass

def broadcast(line: str, skip_conn: socket.socket | None = None):
    with clients_lock:
        dead = []
        for conn in socket_to_name.keys():
            if conn is skip_conn:
                continue
            try:
                conn.sendall((line + "\n").encode(ENC))
            except OSError:
                dead.append(conn)
        for d in dead:
            cleanup_client(d)

def list_users() -> str:
    with clients_lock:
        names = sorted(name_to_socket.keys())
    return ", ".join(names) if names else "(trống)"

def set_nick(conn: socket.socket, new_name: str) -> str:
    new_name = new_name.strip()
    if not new_name:
        return "Tên không được rỗng."
    if any(ch.isspace() for ch in new_name):
        return "Tên không chứa khoảng trắng."
    with clients_lock:
        if new_name in name_to_socket:
            return "Tên đã được dùng, hãy chọn tên khác."
        old = socket_to_name.get(conn)
        if old:
            name_to_socket.pop(old, None)
        socket_to_name[conn] = new_name
        name_to_socket[new_name] = conn
    if old and old != new_name:
        broadcast(f"* {old} đổi tên thành {new_name}")
    return f"Đã đặt tên: {new_name}"

def pm(sender_conn: socket.socket, target: str, msg: str) -> str:
    with clients_lock:
        target_conn = name_to_socket.get(target)
        sender = socket_to_name.get(sender_conn, "?")
    if not target_conn:
        return f"Không tìm thấy người dùng: {target}"
    if not msg.strip():
        return "Tin nhắn trống."
    send_line(target_conn, f"[PM từ {sender}] {msg}")
    return f"[PM đến {target}] {msg}"

def cleanup_client(conn: socket.socket):
    with clients_lock:
        name = socket_to_name.pop(conn, None)
        if name:
            name_to_socket.pop(name, None)
    try:
        conn.close()
    except OSError:
        pass
    if name:
        broadcast(f"* {name} đã thoát.")

def handle_client(conn: socket.socket, addr):
    send_line(conn, WELCOME)
    send_line(conn, "Hãy đặt tên bằng lệnh: /nick <ten>")
    try:
        with conn:
            buf = b""
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                buf += data
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    text = line.decode(ENC, errors="ignore").strip()
                    if not text:
                        continue
                    if text.startswith("/"):
                        parts = text.split(maxsplit=2)
                        cmd = parts[0].lower()
                        if cmd == "/help":
                            send_line(conn, WELCOME.strip())
                        elif cmd == "/nick":
                            if len(parts) < 2:
                                send_line(conn, "Dùng: /nick <ten>")
                            else:
                                msg = set_nick(conn, parts[1])
                                send_line(conn, msg)
                        elif cmd == "/list":
                            send_line(conn, "Online: " + list_users())
                        elif cmd == "/pm":
                            if len(parts) < 3:
                                send_line(conn, "Dùng: /pm <ten> <noi dung>")
                            else:
                                target, body = parts[1], parts[2]
                                msg = pm(conn, target, body)
                                send_line(conn, msg)
                        elif cmd == "/quit":
                            send_line(conn, "Tạm biệt!")
                            raise ConnectionAbortedError
                        else:
                            send_line(conn, "Lệnh không hợp lệ. Gõ /help")
                        continue
                    with clients_lock:
                        name = socket_to_name.get(conn)
                    if not name:
                        send_line(conn, "Bạn chưa đặt tên. Dùng: /nick <ten>")
                        continue
                    broadcast(f"[{name}] {text}")
    except (ConnectionResetError, ConnectionAbortedError, OSError):
        pass
    finally:
        cleanup_client(conn)

def main():
    port = int(sys.argv[1]) if len(sys.argv) >= 2 else 60000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))
        s.listen()
        print(f"Server lắng nghe tại {HOST}:{port}")
        while True:
            conn, addr = s.accept()
            print(f"Kết nối từ {addr}")
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

if __name__ == "__main__":
    main()
