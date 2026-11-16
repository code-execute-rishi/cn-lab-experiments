import socket
import threading

HOST = "127.0.0.1"
PORT = 5050

clients = {}          # conn -> name
lock = threading.Lock()


def broadcast(message, sender=None):
    with lock:
        for conn in list(clients):
            if conn is not sender:
                try:
                    conn.sendall(message.encode())
                except OSError:
                    pass


def handle_client(conn, addr):
    name = conn.recv(1024).decode().strip()
    with lock:
        clients[conn] = name
    print(f"[SERVER] {name} joined from {addr}")
    broadcast(f"*** {name} joined the chat ***", sender=conn)

    while True:
        data = conn.recv(1024)
        if not data or data.decode().strip() == "/quit":
            break
        text = data.decode().strip()
        print(f"[{name}] {text}")
        broadcast(f"[{name}] {text}", sender=conn)

    with lock:
        del clients[conn]
    conn.close()
    print(f"[SERVER] {name} left the chat")
    broadcast(f"*** {name} left the chat ***")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen()
        print(f"[SERVER] Chat server started on {HOST}:{PORT}")

        while True:
            conn, addr = server_sock.accept()
            threading.Thread(target=handle_client, args=(conn, addr),
                             daemon=True).start()


if __name__ == "__main__":
    main()
