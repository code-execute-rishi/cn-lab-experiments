import socket

HOST = "127.0.0.1"
PORT = 65432

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.connect((HOST, PORT))
        print(f"[CLIENT] Connected to {HOST}:{PORT}")

        while True:
            msg = input("[CLIENT] > ")
            client_sock.sendall(msg.encode())
            if msg == "/quit":
                break

            data = client_sock.recv(1024)
            if not data or data.decode() == "/quit":
                print("[CLIENT] Server disconnected")
                break
            print(f"[SERVER] {data.decode()}")

if __name__ == "__main__":
    main()
