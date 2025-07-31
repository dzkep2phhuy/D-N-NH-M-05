import socket
import threading
import queue

HOST = "0.0.0.0"
PORT = 9999

match_queue = queue.Queue()


def determine_winner(p1, p2):
    if p1 == p2:
        return "draw"
    elif (
        (p1 == "rock" and p2 == "scissors")
        or (p1 == "scissors" and p2 == "paper")
        or (p1 == "paper" and p2 == "rock")
    ):
        return "win"
    else:
        return "lose"


def handle_client(conn, addr):
    try:
        name = conn.recv(1024).decode().strip()
        conn.sendall(b"Waiting for opponent...\n")
        match_queue.put((conn, name))

        while True:
            if match_queue.qsize() >= 2:
                player1 = match_queue.get()
                player2 = match_queue.get()

                c1, name1 = player1
                c2, name2 = player2

                c1.sendall(
                    f"Matched with {name2}! Enter your move (rock/paper/scissors): ".encode()
                )
                c2.sendall(
                    f"Matched with {name1}! Enter your move (rock/paper/scissors): ".encode()
                )

                m1 = c1.recv(1024).decode().strip().lower()
                m2 = c2.recv(1024).decode().strip().lower()

                r1 = determine_winner(m1, m2)
                r2 = determine_winner(m2, m1)

                c1.sendall(
                    f"You chose {m1}, opponent chose {m2}. Result: {r1.upper()}\n".encode()
                )
                c2.sendall(
                    f"You chose {m2}, opponent chose {m1}. Result: {r2.upper()}\n".encode()
                )

                match_queue.put((c1, name1))
                match_queue.put((c2, name2))
    except:
        conn.close()


def start_server():
    print(f"Server is starting on port {PORT}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        print(f"New connection from {addr}")
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_server()
