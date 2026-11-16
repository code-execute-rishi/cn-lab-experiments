# Lab 2: Socket Programming (Client–Server)

## Question
**Aim:** To learn the basics of socket programming and the binding of a client and server machine, and to write a program in which the client and the server send messages to each other.

## Files
- [`server.py`](server.py): binds 127.0.0.1:65432, accepts one client, prints its messages and sends replies typed on the server.
- [`client.py`](client.py): connects to the server and exchanges messages until `/quit`.

## Logic (How the Program Works)

```text
server.py
1. Create a TCP socket: socket(AF_INET, SOCK_STREAM). Set SO_REUSEADDR so the port can be reused right away.
2. bind() to 127.0.0.1:65432, then listen().
3. accept() blocks until a client connects, then returns a new socket (conn) and the client's address.
4. Loop: recv(1024). If nothing came or the text is "/quit", print "Client disconnected" and stop.
5. Otherwise print [CLIENT] <message>, read a reply with input(), and sendall() it. If the reply is "/quit", stop.

client.py
1. Create a TCP socket and connect() to 127.0.0.1:65432 (the OS picks the client's port).
2. Loop: read a message with input() and sendall() it. If it is "/quit", stop.
3. recv() the server's reply. If it is empty or "/quit", the server has left; otherwise print [SERVER] <reply>.

The two sides take turns: each one waits for the other's message before replying.
```

## How to Run
Open two terminals in this folder:
```bash
python3 server.py      # Terminal 1
python3 client.py      # Terminal 2
```
Type a message in the client, then a reply in the server. Type `/quit` in the client to end.

## Output (from the lab run)

**Terminal 1: Server**
```
$ python3 server.py
[SERVER] Listening on 127.0.0.1:65432
[SERVER] Connected by ('127.0.0.1', 62342)
[CLIENT] hello server
[SERVER] > hi client
[CLIENT] how are you
[SERVER] > fine thanks
[SERVER] Client disconnected
```

**Terminal 2: Client**
```
$ python3 client.py
[CLIENT] Connected to 127.0.0.1:65432
[CLIENT] > hello server
[SERVER] hi client
[CLIENT] > how are you
[SERVER] fine thanks
[CLIENT] > /quit
```

**Checking the bound port**
```
$ lsof -nP -iTCP:65432
COMMAND  PID    USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
Python 24394 aradhya   3u   IPv4  ...         0t0  TCP 127.0.0.1:65432 (LISTEN)
```

The client's port (62342 here) is chosen by the OS and is different every run.

## Viva Questions

1. **What is a socket?**
   One end of a two-way connection between two programs. It is identified by an IP address and a port number.
2. **Order of calls on the server and the client?**
   Server: socket() → bind() → listen() → accept() → recv()/send() → close(). Client: socket() → connect() → send()/recv() → close().
3. **Why does only the server call bind()?**
   The server needs a fixed, known address so clients can find it. The client gets a random free (ephemeral) port from the OS when it calls connect().
4. **What does accept() return?**
   A new socket for that client connection, plus the client's address (IP, port). The original socket keeps listening.
5. **TCP vs UDP?**
   TCP (SOCK_STREAM) is connection-oriented, reliable and in order, with a 3-way handshake. UDP (SOCK_DGRAM) is connectionless and faster, with no delivery guarantee.
6. **What is the 3-way handshake?**
   SYN → SYN-ACK → ACK. It happens before accept() returns on the server.
7. **Why encode() and decode()?**
   Sockets send bytes, not strings. encode() turns a string into bytes; decode() turns received bytes back into a string.
8. **What does SO_REUSEADDR do?**
   Lets the server reuse the port immediately after restarting, instead of waiting for the old connection's TIME_WAIT to end.
9. **What is 127.0.0.1?**
   The loopback address, meaning this same machine. Use the LAN IP instead to connect from another computer.
