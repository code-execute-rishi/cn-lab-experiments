import socket

HOST = "127.0.0.1"
PORT = 65432

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen()
        print(f"[SERVER] Listening on {HOST}:{PORT}")

        conn, addr = server_sock.accept()
        with conn:
            print(f"[SERVER] Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data or data.decode() == "/quit":
                    print("[SERVER] Client disconnected")
                    break
                print(f"[CLIENT] {data.decode()}")

                reply = input("[SERVER] > ")
                conn.sendall(reply.encode())
                if reply == "/quit":
                    break

if __name__ == "__main__":
    main()
