# Lab 14: TCP/IP Echo Client–Server

## Question
**Aim:** To implement, test, and benchmark a concurrent multi-threaded TCP/IP Echo Client and Server application using Python's Berkeley Sockets API, evaluating full-duplex stream I/O, delimiter-based framing, and Round-Trip Time (RTT).

## Files
- [`tcp_echo_socket.py`](tcp_echo_socket.py): Multi-threaded TCP echo server and client in one program, with echo checks and RTT measurement.

## How to Run
No input is needed; the test data is built into each program.
```bash
python3 tcp_echo_socket.py
```

## Output

The RTT values are different on every run.

```
==============================================================================
COMPUTER NETWORKS LAB - EXPERIMENT 14: TCP/IP ECHO SOCKET ARCHITECTURE
Student: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
==============================================================================
[SERVER STARTED] Listening on 127.0.0.1:65432

[PHASE 1: CLIENT-SERVER STREAM I/O & RTT MEASUREMENT]
>> Sent   : "SYN -> SYN-ACK -> ACK: Handshake Verified"
   Echoed : "SYN -> SYN-ACK -> ACK: Handshake Verified" | RTT: 0.186 ms | Status: MATCH [PASS]

>> Sent   : "Computer Networks Lab (CS-501) - MANIT Bhopal"
   Echoed : "Computer Networks Lab (CS-501) - MANIT Bhopal" | RTT: 0.093 ms | Status: MATCH [PASS]

>> Sent   : "Scholar Number: 24112011111 | Aradhya Jain"
   Echoed : "Scholar Number: 24112011111 | Aradhya Jain" | RTT: 0.121 ms | Status: MATCH [PASS]

>> Sent   : "Packet Stream Frame 04: Hello Berkeley Sockets"
   Echoed : "Packet Stream Frame 04: Hello Berkeley Sockets" | RTT: 0.076 ms | Status: MATCH [PASS]

>> Sent   : "Stream Boundary Test: Full-Duplex Byte Transport"
   Echoed : "Stream Boundary Test: Full-Duplex Byte Transport" | RTT: 0.074 ms | Status: MATCH [PASS]

------------------------------------------------------------------------------
[PHASE 2: CONCURRENT MULTI-CLIENT THREAD POOL STRESS TEST]
Thread Client-0: Transmitted 3 frames concurrently | Avg RTT: 0.174 ms | Verified: 100%
Thread Client-1: Transmitted 3 frames concurrently | Avg RTT: 0.206 ms | Verified: 100%
Thread Client-2: Transmitted 3 frames concurrently | Avg RTT: 0.197 ms | Verified: 100%
Thread Client-3: Transmitted 3 frames concurrently | Avg RTT: 0.240 ms | Verified: 100%
------------------------------------------------------------------------------
>> Total bytes echoed by server: 407 bytes across sessions.
[SERVER SHUTDOWN] Port 65432 closed cleanly.
[STATUS] TCP/IP Socket Stream and 3-Way Handshake echo model verified.
==============================================================================
```


## Viva Questions

1. **What does an echo server do?**
   It sends back exactly what it receives. It is used to test connections and measure round-trip time.
2. **What is RTT?**
   Round-Trip Time: the time from sending a message until its reply comes back.
3. **Why does the server use threads?**
   So several clients can be served at the same time; each connection gets its own thread.
4. **What is message framing, and why does TCP need it?**
   TCP is a byte stream with no message boundaries, so a delimiter (such as a newline) marks where each message ends.
5. **What is SO_REUSEADDR?**
   A socket option that lets the server bind the same port again right after it restarts.
6. **What does listen(10) mean?**
   Up to 10 incoming connections can wait in the queue before accept() takes them.
7. **What is full duplex?**
   Data can flow in both directions at the same time on one TCP connection.
8. **Which address and port does the server use here?**
   127.0.0.1 (loopback), port 65432.
