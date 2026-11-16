import socket
import threading

HOST = "127.0.0.1"
PORT = 5050


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
        except OSError:         # socket closed when I leave the chat
            break
        if not data:
            print("[CLIENT] Server closed the connection")
            break
        print(data.decode())


def main():
    name = input("Enter your name: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(name.encode())
        print(f"[CLIENT] Connected to chat server {HOST}:{PORT} as {name}")

        threading.Thread(target=receive_messages, args=(sock,),
                         daemon=True).start()

        while True:
            msg = input("you> ")
            sock.sendall(msg.encode())
            if msg.strip() == "/quit":
                print("[CLIENT] You left the chat")
                break


if __name__ == "__main__":
    main()
