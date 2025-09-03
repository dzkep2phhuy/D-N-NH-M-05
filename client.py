# client.py
import socket
import sys
import threading

ENC = "utf-8"

def recv_loop(sock: socket.socket):
    try:
        buf = b""
        while True:
            data = sock.recv(4096)
            if not data:
                print("\n[Mất kết nối tới server]")
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                print(line.decode(ENC, errors="ignore"))
    except OSError:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass

def main():
    if len(sys.argv) < 3:
        print("Dùng: python client.py <host> <port>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print(f"Đã kết nối tới {host}:{port}")
        threading.Thread(target=recv_loop, args=(sock,), daemon=True).start()

        try:
            while True:
                text = input()
                if not text:
                    continue
                sock.sendall((text + "\n").encode(ENC))
                if text.strip().lower() == "/quit":
                    break
        except (KeyboardInterrupt, EOFError):
            try:
                sock.sendall(b"/quit\n")
            except OSError:
                pass
        finally:
            try:
                sock.close()
            except OSError:
                pass

if __name__ == "__main__":
    main()
