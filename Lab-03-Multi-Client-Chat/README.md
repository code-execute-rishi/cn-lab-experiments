# Lab 3: Multi-Client Chat Application

## Question
**Aim:** To make a client–server application for chat, that is, a program in which many clients join one server and exchange messages with each other.

## Files
- [`chat_server.py`](chat_server.py): binds 127.0.0.1:5050, starts one thread per client and broadcasts every message to the other clients.
- [`chat_client.py`](chat_client.py): sends your name first, then one thread receives messages while the main thread sends what you type.

## How to Run
Open three terminals in this folder:
```bash
python3 chat_server.py     # Terminal 1
python3 chat_client.py     # Terminal 2 (name: alice)
python3 chat_client.py     # Terminal 3 (name: bob)
```
Type `/quit` in a client to leave. The server keeps running.

## Output (from the lab run)

**Terminal 1: Server**
```
$ python3 chat_server.py
[SERVER] Chat server started on 127.0.0.1:5050
[SERVER] alice joined from ('127.0.0.1', 63625)
[SERVER] bob joined from ('127.0.0.1', 63626)
[alice] hi everyone
[bob] hello alice
[alice] how is the lab going
[bob] all good, my code is working
[SERVER] bob left the chat
[SERVER] alice left the chat
```

**Terminal 2: Client 1 (alice)**
```
$ python3 chat_client.py
Enter your name: alice
[CLIENT] Connected to chat server 127.0.0.1:5050 as alice
you> *** bob joined the chat ***
you> hi everyone
[bob] hello alice
you> how is the lab going
[bob] all good, my code is working
*** bob left the chat ***
you> /quit
[CLIENT] You left the chat
```

**Terminal 3: Client 2 (bob)**
```
$ python3 chat_client.py
Enter your name: bob
[CLIENT] Connected to chat server 127.0.0.1:5050 as bob
you> [alice] hi everyone
you> hello alice
[alice] how is the lab going
you> all good, my code is working
you> /quit
[CLIENT] You left the chat
```


## Viva Questions

1. **How does the server handle many clients at once?**
   After accept(), it starts a new thread for each client and goes straight back to accept(), so it is always ready for the next client.
2. **What is broadcasting here?**
   When one client sends a message, the server sends it to every other connected client.
3. **Why is a lock (threading.Lock) used?**
   The clients dictionary is shared by all threads. The lock stops two threads from changing it at the same time (a race condition).
4. **Why does the client use two threads?**
   One thread only receives and prints; the main thread only reads input and sends. So it can send and receive at the same time (full duplex).
5. **Thread vs process?**
   Threads of one process share memory, so they are lighter and can share the client list. Processes have separate memory.
6. **What happens when a client types /quit?**
   Its server thread removes it from the list, closes the socket and tells the others it left; the other clients continue.
7. **What is a daemon thread?**
   A background thread that does not stop the program from exiting (daemon=True).
8. **How could clients on other PCs join?**
   Bind the server to the machine's LAN IP (or 0.0.0.0) and have the clients connect to that IP.
