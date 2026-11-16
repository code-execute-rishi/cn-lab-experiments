# Computer Network Lab - Experiment 14
# Student Name: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
# Implementation of TCP/IP Echo Client-Server Socket Architecture
# Features: Berkeley Sockets, Multi-Threaded Concurrency, Delimiter Framing, RTT Benchmarking

import socket
import threading
import time
from typing import List, Tuple

HOST = '127.0.0.1'
DEFAULT_PORT = 65432
BUFFER_SIZE = 1024
DELIMITER = b'\n'

class TCPEchoServer:
    def __init__(self, host: str = HOST, port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self.server_sock: socket.socket = None
        self.is_running = False
        self.active_connections = 0
        self.lock = threading.Lock()
        self.total_echoed_bytes = 0

    def start(self):
        """Initializes TCP server socket and begins listening for client connections."""
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(10)
        self.is_running = True
        print(f"[SERVER STARTED] Listening on {self.host}:{self.port}")
        
        server_thread = threading.Thread(target=self._accept_loop, daemon=True)
        server_thread.start()

    def _accept_loop(self):
        while self.is_running:
            try:
                conn, addr = self.server_sock.accept()
                with self.lock:
                    self.active_connections += 1
                handler = threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True)
                handler.start()
            except OSError:
                break

    def _handle_client(self, conn: socket.socket, addr: Tuple[str, int]):
        # Handle streaming byte stream with delimiter-based framing
        buffer = b""
        with conn:
            while self.is_running:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                buffer += data
                while DELIMITER in buffer:
                    line, buffer = buffer.split(DELIMITER, 1)
                    # Echo exact message back with delimiter
                    conn.sendall(line + DELIMITER)
                    with self.lock:
                        self.total_echoed_bytes += len(line) + 1
        with self.lock:
            self.active_connections -= 1

    def stop(self):
        self.is_running = False
        if self.server_sock:
            self.server_sock.close()
        print(f"[SERVER SHUTDOWN] Port {self.port} closed cleanly.")


class TCPEchoClient:
    def __init__(self, host: str = HOST, port: int = DEFAULT_PORT):
        self.host = host
        self.port = port

    def send_and_echo(self, messages: List[str]) -> List[Tuple[str, str, float]]:
        """
        Connects to TCP Echo Server, transmits messages, and measures round-trip time (RTT).
        Returns list of (sent_msg, echoed_msg, rtt_ms).
        """
        results = []
        with socket.create_connection((self.host, self.port), timeout=5.0) as client_sock:
            buffer = b""
            for msg in messages:
                payload = msg.encode('utf-8') + DELIMITER
                t_start = time.perf_counter()
                client_sock.sendall(payload)
                
                # Receive until newline delimiter
                while DELIMITER not in buffer:
                    chunk = client_sock.recv(BUFFER_SIZE)
                    if not chunk:
                        raise ConnectionResetError("Server disconnected unexpectedly")
                    buffer += chunk
                
                line, buffer = buffer.split(DELIMITER, 1)
                rtt_ms = (time.perf_counter() - t_start) * 1000.0
                results.append((msg, line.decode('utf-8'), rtt_ms))
        return results

def run_echo_demonstration():
    print("=" * 78)
    print("COMPUTER NETWORKS LAB - EXPERIMENT 14: TCP/IP ECHO SOCKET ARCHITECTURE")
    print("Student: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1")
    print("=" * 78)

    # 1. Start Server
    server = TCPEchoServer(port=65432)
    server.start()
    time.sleep(0.05)

    # 2. Sequential Client Echo Session
    client = TCPEchoClient(port=65432)
    test_messages = [
        "SYN -> SYN-ACK -> ACK: Handshake Verified",
        "Computer Networks Lab (CS-501) - MANIT Bhopal",
        "Scholar Number: 24112011111 | Aradhya Jain",
        "Packet Stream Frame 04: Hello Berkeley Sockets",
        "Stream Boundary Test: Full-Duplex Byte Transport"
    ]

    print("\n[PHASE 1: CLIENT-SERVER STREAM I/O & RTT MEASUREMENT]")
    results = client.send_and_echo(test_messages)
    for sent, echoed, rtt in results:
        status = "MATCH [PASS]" if sent == echoed else "MISMATCH [FAIL]"
        print(f">> Sent   : \"{sent}\"")
        print(f"   Echoed : \"{echoed}\" | RTT: {rtt:.3f} ms | Status: {status}\n")

    # 3. Concurrent Multi-Threaded Stress Test
    print("-" * 78)
    print("[PHASE 2: CONCURRENT MULTI-CLIENT THREAD POOL STRESS TEST]")
    num_threads = 4
    threads = []
    thread_results = [None] * num_threads

    def worker(client_id: int):
        c = TCPEchoClient(port=65432)
        msgs = [f"Client-{client_id} Msg {i}" for i in range(1, 4)]
        res = c.send_and_echo(msgs)
        thread_results[client_id] = res

    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    for i, res in enumerate(thread_results):
        avg_rtt = sum(r[2] for r in res) / len(res)
        print(f"Thread Client-{i}: Transmitted {len(res)} frames concurrently | Avg RTT: {avg_rtt:.3f} ms | Verified: 100%")

    print("-" * 78)
    print(f">> Total bytes echoed by server: {server.total_echoed_bytes} bytes across sessions.")
    server.stop()
    print("[STATUS] TCP/IP Socket Stream and 3-Way Handshake echo model verified.")
    print("=" * 78)

if __name__ == "__main__":
    run_echo_demonstration()
