# Computer Networks Laboratory (CS-504 / CS-501) — Experiments 1 to 14

[![Language: C++17](https://img.shields.io/badge/language-C%2B%2B17%20%2F%20POSIX-00599C.svg?logo=c%2B%2B)](https://en.wikipedia.org/wiki/C%2B%2B17)
[![POSIX Sockets](https://img.shields.io/badge/sockets-POSIX%20BSD%20API-red.svg)]()
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Build: Passing](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> Complete, modular, and mathematically verified implementations for **Computer Networks Laboratory (CS-504 / CS-501)** Experiments 1 through 14 (13 source files). Labs 1–9 are written in modern **C++17 with native POSIX Berkeley Sockets and POSIX Threads (`std::thread`, `std::mutex`)**; Labs 10–14 (CSMA, CSMA/CD, RIP, OSPF, TCP Echo) are written in **Python 3** using only the standard library. Build tooling (`Makefile`) included, with **zero external dependencies**.

---

## 👨‍🎓 Student & Academic Details

* **Student Name:** Aradhya Jain
* **Scholar Number:** `24112011111`
* **Department & Section:** Department of Computer Science & Engineering, `CSE-1`
* **Institution:** Maulana Azad National Institute of Technology (MANIT), Bhopal
* **Course:** Computer Networks Laboratory (`CS-504` / `CS-501`)
* **Semester:** V Semester, B.Tech CSE

---

## 📋 Comprehensive Table of Experiments

| Experiment | Title & Protocol Focus | Source File / Class | CLI Target |
| :---: | :--- | :--- | :---: |
| **Lab 1** | **Star Topology LAN & Linux Diagnostics Simulator**<br>• Cisco Catalyst Switch 2960 emulation with dynamic CAM MAC learning table<br>• Address Resolution Protocol (ARP) broadcast and unicast resolution cache<br>• ICMP Echo Request / Reply `ping` with min/avg/max RTT and packet loss<br>• Linux diagnostics emulation: `ifconfig`, `netstat`, and `arp -a` | [`src/lab1_star_topology.cpp`](src/lab1_star_topology.cpp)<br>`Lab1_StarTopology` | `--lab 1` |
| **Lab 2** | **TCP Socket Programming (Client-Server Architecture)**<br>• Stream socket lifecycle: `socket()`, `setsockopt(SO_REUSEADDR)`, `bind()`<br>• Passive listen & 3-way handshake: `listen()`, `accept()`, `connect()`<br>• Bidirectional conversational streaming with `send()` and `recv()`<br>• Graceful connection termination on `/quit` / `EXIT` | [`src/lab2_tcp_sockets.cpp`](src/lab2_tcp_sockets.cpp)<br>`Lab2_TCPSocket` | `--lab 2` |
| **Lab 3** | **Concurrent Multi-Client Threaded Chat Hub**<br>• Concurrency via worker threads (`std::thread`) per incoming connection<br>• Thread-safe shared client registry guarded by `std::mutex`<br>• Centralized broadcast routing filtering out the message origin<br>• Dynamic user presence tracking (Join & Leave notifications) | [`src/lab3_multiclient_chat.cpp`](src/lab3_multiclient_chat.cpp)<br>`Lab3_MultiClientChat` | `--lab 3` |
| **Lab 4** | **Serial / Point-to-Point Socket File Transfer Protocol**<br>• Custom stream framing header: `<FILENAME>|<FILESIZE_BYTES>\n`<br>• Flow-controlled chunked binary transmission (64-byte streaming windows)<br>• End-to-end cryptographic integrity audit via IEEE 802.3 CRC-32 & FNV-1a 64-bit | [`src/lab4_file_transfer.cpp`](src/lab4_file_transfer.cpp)<br>`Lab4_FileTransfer` | `--lab 4` |
| **Lab 5** | **Flow Control Protocols (ARQ Simulations)**<br>• **Stop-and-Wait ARQ:** Window size $W=1$, timer expiration, retransmissions<br>• **Go-Back-N ARQ:** Window sliding ($W=4$), cumulative ACKs, rollback<br>• **Selective Repeat ARQ:** Independent receiver buffers, selective NAKs | [`src/lab5_flow_control.cpp`](src/lab5_flow_control.cpp)<br>`Lab5_FlowControl` | `--lab 5` |
| **Lab 6 & 7** | **Error Control Protocols & Alternating Bit Protocol**<br>• Alternating Bit Protocol (Stop-and-Wait with 1-bit sequence tags: 0 and 1)<br>• Data frame loss recovery via retransmission timeout (RTO)<br>• ACK loss recovery with duplicate frame filtering at the receiver<br>• Channel efficiency derivations: $\eta_{\text{SAW}} = \frac{1}{1 + 2a}$ vs $\eta_{\text{Sliding}} = \frac{W}{1 + 2a}$ | [`src/lab6_7_error_control.cpp`](src/lab6_7_error_control.cpp)<br>`Lab6_7_ErrorControl` | `--lab 6`<br>`--lab 7` |
| **Lab 8** | **Data Link Error Detection Methods**<br>• **VRC (1D Parity):** Even and Odd parity generator and parity bit verifier<br>• **LRC (Block Parity):** Columnar Block Check Character (BCC) calculation<br>• **2D Parity Matrix:** Autonomous single-bit error localization & correction at $(r, c)$ intersection; 4-bit corner failure demonstration<br>• **Cyclic Redundancy Check (CRC):** Modulo-2 binary polynomial division (GF(2)) for CRC-4, CRC-8, CRC-16, and CRC-32 (Ethernet) | [`src/lab8_crc_lrc_vrc.cpp`](src/lab8_crc_lrc_vrc.cpp)<br>`Lab8_ErrorDetection` | `--lab 8` |
| **Lab 9** | **Error Correction Codes (Hamming SEC & Extended SEC-DED)**<br>• **Hamming (7,4) Code:** Single Error Correction (SEC), syndrome decoding $S = (S_4 S_2 S_1)_2$, Hamming redundancy bound $(m+r+1) \le 2^r$<br>• **Extended SEC-DED (8,4) Architecture:** Overall parity bit $P_0$ distinguishing correctable 1-bit from uncorrectable 2-bit errors<br>• **Stream Forward Error Correction (FEC):** Continuous ASCII text transmission over noisy channels with on-the-fly bit inversion correction | [`src/lab9_hamming_code.cpp`](src/lab9_hamming_code.cpp)<br>`Lab9_HammingCode` | `--lab 9` |
| **Lab 10** | **Non-Persistent CSMA Protocol**<br>• Carrier sensing on a shared bus; transmit immediately if the channel is idle<br>• Random backoff (no continuous sensing) when the channel is busy<br>• Collision tracking inside the propagation window $\tau$<br>• Simulated vs theoretical throughput $S$ across offered loads $G$ | [`src/lab10_csma_non_persistent.py`](src/lab10_csma_non_persistent.py) | `make lab10` |
| **Lab 11** | **1-Persistent & p-Persistent CSMA/CD with Binary Exponential Backoff**<br>• Collision detection with immediate abort and 32-bit jam signal<br>• IEEE 802.3 truncated Binary Exponential Backoff (BEB)<br>• Delivered frames, collisions, throughput and delay under light, medium and heavy load | [`src/lab11_csma_cd_beb.py`](src/lab11_csma_cd_beb.py) | `make lab11` |
| **Lab 12** | **Distance Vector Routing (RIP)**<br>• Distributed Bellman-Ford: $D_x(y) = \min_v \{ c(x,v) + D_v(y) \}$<br>• 5-router mesh convergence and per-router routing tables<br>• Count-to-Infinity hazard after link failure<br>• Split Horizon with Poisoned Reverse | [`src/lab12_rip_distance_vector.py`](src/lab12_rip_distance_vector.py) | `make lab12` |
| **Lab 13** | **OSPF Link-State Routing (Dijkstra SPF)**<br>• LSA flooding and synchronized Link-State Database (LSDB)<br>• Dijkstra shortest-path tree and forwarding tables<br>• Dynamic rerouting after a link metric change | [`src/lab13_ospf_link_state.py`](src/lab13_ospf_link_state.py) | `make lab13` |
| **Lab 14** | **TCP/IP Echo Client-Server**<br>• Multi-threaded TCP echo server (`AF_INET`, `SOCK_STREAM`, `SO_REUSEADDR`, port 65432)<br>• Client stream I/O with echo verification<br>• Round-Trip Time (RTT) measurement | [`src/lab14_tcp_echo_socket.py`](src/lab14_tcp_echo_socket.py) | `make lab14` |

---

## 🏛️ Theoretical Foundations & Protocol Mathematics

### 1. TCP Stream Socket Lifecycle & POSIX State Machine (Labs 2, 3, 4)

```
        SERVER LIFECYCLE                               CLIENT LIFECYCLE
      ┌──────────────────┐                           ┌──────────────────┐
      │     socket()     │                           │     socket()     │
      └────────┬─────────┘                           └────────┬─────────┘
               │                                              │
      ┌────────▼─────────┐                                    │
      │   bind(PORT)     │                                    │
      └────────┬─────────┘                                    │
               │                                              │
      ┌────────▼─────────┐                                    │
      │     listen()     │                                    │
      └────────┬─────────┘                                    │
               │                                              │
      ┌────────▼─────────┐        Three-Way Handshake         │
      │     accept()     │ ◄───────────────────────────────► │    connect()     │
      └────────┬─────────┘    [SYN -> SYN-ACK -> ACK]        └────────┬─────────┘
               │                                              │
               │            ESTABLISHED CONNECTION            │
      ┌────────▼─────────┐                               ┌────▼─────────────┐
      │  recv() / send() │ ◄───────────────────────────► │  send() / recv() │
      └────────┬─────────┘                               └────┬─────────────┘
               │                                              │
      ┌────────▼─────────┐                               ┌────▼─────────────┐
      │     close()      │                               │     close()      │
      └──────────────────┘                               └──────────────────┘
```

### 2. Protocol Efficiency & Normalized Propagation Ratio (Labs 5, 6, 7)

The normalized propagation delay ratio $a$ is defined as:
$$a = \frac{T_{\text{prop}}}{T_{\text{trans}}} = \frac{d / v}{L / B}$$
Where:
* $d$ = link distance (meters), $v$ = propagation velocity ($\approx 2 \times 10^8\text{ m/s}$)
* $L$ = frame length in bits, $B$ = channel bandwidth in bps.

The channel efficiency $\eta$ is given by:
* **Stop-and-Wait ARQ ($W=1$):**
  $$\eta_{\text{Stop-and-Wait}} = \frac{1}{1 + 2a}$$
* **Sliding Window (Go-Back-N / Selective Repeat with window $W$):**
  $$\eta_{\text{Sliding Window}} = \min\left(1.0, \frac{W}{1 + 2a}\right)$$

### 3. Error Detection & 2D Parity Matrix Intersection (Lab 8)

In a 2D Parity Matrix, each 7-bit character receives an even parity bit (VRC), and each bit column across the frame receives a Block Check Character bit (LRC):

```
       Bit 1  Bit 2  Bit 3  Bit 4  Bit 5  Bit 6  Bit 7 │ VRC (Row Parity)
Row 0:   1      0      1      0      1      0      1   │     0
Row 1:   1      1      0      0    [ 1 ]*   1      0   │     0   <-- Parity Failure! (Row 1)
Row 2:   0      1      1      1      0      0      1   │     0
Row 3:   1      0      0      1      0      1      1   │     0
───────────────────────────────────────────────────────┼───────
LRC  :   1      0      0      0    [ 0 ]    0      1   │     0
                                       ▲
                         Parity Failure! (Col 4)
```
* **Syndrome Intersection:** Bad Row $= 1$, Bad Column $= 4$.
* The corrupted bit is localized at coordinate $(1, 4)$. By flipping this single bit: $1 \to 0$, the receiver achieves **Autonomous Forward Error Correction**!

### 4. Cyclic Redundancy Check (CRC) Polynomial Division (Lab 8)

Given data polynomial $M(x)$ of degree $k$ and generator polynomial $G(x)$ of degree $r$:
1. Multiply data by $x^r$ (append $r$ zeros): $M(x) \cdot x^r$.
2. Divide by $G(x)$ using **Modulo-2 division (XOR arithmetic)**:
   $$\frac{M(x) \cdot x^r}{G(x)} = Q(x) + \frac{R(x)}{G(x)}$$
3. Transmitted Codeword: $T(x) = M(x) \cdot x^r + R(x)$.
4. At receiver: Divide received codeword $T'(x)$ by $G(x)$. If remainder $R'(x) \equiv 0$, the frame is accepted with high cryptographic confidence.

Standard generator polynomials implemented:
* **CRC-4:** $G(x) = x^4 + x + 1$ (`10011`)
* **CRC-8-ATM:** $G(x) = x^8 + x^2 + x + 1$ (`100000111`)
* **CRC-16-ANSI:** $G(x) = x^{16} + x^{15} + x^2 + 1$
* **CRC-32 (IEEE 802.3 Ethernet):** `0xEDB88320`

### 5. Hamming Code (7,4) & Extended SEC-DED (8,4) (Lab 9)

According to the **Hamming Bound**, $r$ parity bits can protect $m$ message bits if:
$$2^r \ge m + r + 1$$
For $m = 4$ data bits $\implies r = 3$ parity bits ($2^3 = 8 \ge 4 + 3 + 1 = 8$).

Bit positions are assigned so that check bits occupy powers of two:
* Bit 1: $P_1$ (Checks bits with LSB $= 1$: 1, 3, 5, 7) $\implies P_1 = D_1 \oplus D_2 \oplus D_4$
* Bit 2: $P_2$ (Checks bits with 2nd bit $= 1$: 2, 3, 6, 7) $\implies P_2 = D_1 \oplus D_3 \oplus D_4$
* Bit 3: $D_1$
* Bit 4: $P_4$ (Checks bits with 3rd bit $= 1$: 4, 5, 6, 7) $\implies P_4 = D_2 \oplus D_3 \oplus D_4$
* Bit 5: $D_2$
* Bit 6: $D_3$
* Bit 7: $D_4$

#### Extended SEC-DED (8,4) Decision Matrix:
By adding bit $P_0$ as the overall parity covering all 7 bits:
* **Syndrome $S = 0$, Overall Parity Valid:** No error detected.
* **Syndrome $S \ne 0$, Overall Parity Invalid:** **Single-bit error at position $S$** $\implies$ Corrected.
* **Syndrome $S \ne 0$, Overall Parity Valid:** **Double-bit error detected!** $\implies$ Uncorrectable, frame discarded.
* **Syndrome $S = 0$, Overall Parity Invalid:** The overall parity bit $P_0$ itself is corrupted.

---

## ⚡ Quick Start & Compilation Guide

### Prerequisites
* **C++ Compiler:** `clang++` (macOS/LLVM) or `g++` (Linux/GCC) with C++17 support.
* **Python:** Python 3.7+ for Labs 10–14 (standard library only).
* **Make:** Standard GNU Make.
* **Operating System:** macOS, Linux, Ubuntu, Debian, CentOS, WSL.

### Clone the Repository
```bash
git clone https://github.com/code-execute-rishi/cn-lab-experiments.git
cd cn-lab-experiments
```

### 1. Build and Run All Experiments via Make
```bash
# Build the master binary
make all

# Run complete automated test suite (Labs 1 through 9, C++)
make run

# Run Labs 10 through 14 (Python)
make run_python
```

### 2. Run a Specific Lab Experiment
```bash
# Individual Make targets
make lab1    # Star Topology & Linux Diagnostics
make lab2    # TCP Client-Server Stream Sockets
make lab3    # Concurrent Multi-Client Chat Hub
make lab4    # Socket File Transfer with CRC-32 & FNV
make lab5    # Flow Control (Stop & Wait / Go-Back-N / Selective Repeat)
make lab6    # Error Control & Alternating Bit Protocol
make lab8    # Error Detection (VRC, LRC, 2D Parity, CRC Modulo-2)
make lab9    # Error Correction (Hamming 7,4 & Extended SEC-DED 8,4)
make lab10   # Non-Persistent CSMA
make lab11   # 1-Persistent & p-Persistent CSMA/CD with BEB
make lab12   # Distance Vector Routing (RIP)
make lab13   # OSPF Link-State Routing (Dijkstra)
make lab14   # TCP/IP Echo Client-Server
```

### 3. Direct Compiler Invocations
```bash
# Compile master all-in-one suite
clang++ -std=c++17 -Wall -Wextra -O2 cn_labs_1_to_9.cpp -o bin/cn_labs_all -lpthread
./bin/cn_labs_all --all

# Or compile individual modular lab files directly from src/
clang++ -std=c++17 src/lab8_crc_lrc_vrc.cpp -o bin/lab8
./bin/lab8

clang++ -std=c++17 src/lab9_hamming_code.cpp -o bin/lab9
./bin/lab9

# Labs 10-14 are Python scripts
python3 src/lab10_csma_non_persistent.py
python3 src/lab14_tcp_echo_socket.py
```

### 4. Interactive Menu Mode
Run without command-line arguments to launch the interactive selector (C++ binary, Labs 1–9):
```bash
./bin/cn_labs_all
```
```text
============================================================================
  COMPUTER NETWORKS LABORATORY - EXPERIMENTS 1 TO 9 (CS-504 / CS-501)
  Student: Aradhya Jain  |  Scholar No: 24112011111  |  Section: CSE-1
  Institution: Maulana Azad National Institute of Technology (MANIT) Bhopal
============================================================================

Select an experiment to execute:
  1. Lab 1  : Star Topology Network & Diagnostics (ping, ifconfig, netstat, arp)
  2. Lab 2  : TCP Socket Client-Server Communication (Stream Sockets)
  3. Lab 3  : Multi-Client Threaded Chat Hub & Broadcast Routing
  4. Lab 4  : Reliable Socket File Transfer Protocol with CRC-32 & FNV Checksums
  5. Lab 5  : Flow Control Protocols (Stop-and-Wait, Go-Back-N, Selective Repeat)
  6. Lab 6-7: Error Control Protocols (Alternating Bit Protocol & Loss Recovery)
  8. Lab 8  : Error Detection Techniques (VRC, LRC, 2D Parity Matrix, Modulo-2 CRC)
  9. Lab 9  : Error Correction Codes (Hamming 7,4 SEC & Extended SEC-DED 8,4)
  A. Run ALL Experiments (Labs 1 to 9)
  0. Exit

Enter your choice [1-9, A, 0]:
```

---

## 🔬 Sample Execution Output Traces

<details>
<summary><b>Click to expand verified terminal outputs (Labs 1 through 9)</b></summary>

```text
============================================================================
  EXPERIMENT 1: STAR TOPOLOGY SIMULATION & NETWORK DIAGNOSTICS
  Student: Aradhya Jain  |  Scholar No: 24112011111  |  Section: CSE-1
============================================================================

1. Executing ping from PC0 (192.168.1.1) to PC2 (192.168.1.3)...
[DIAGNOSTIC] PC0 (192.168.1.1) initiating ICMP ping to 192.168.1.3
  [ARP REQUEST] PC0 broadcasts: Who has 192.168.1.3? Tell 192.168.1.1
  [SWITCH 2960] Incoming frame on Port 1 (Src: 00:0A:95:9D:68:01 -> Dst: FF:FF:FF:FF:FF:FF)
  --> Broadcast destination detected! Flooding frame to all active ports except Port 1
  [ARP REPLY] PC2 replies unicast: 192.168.1.3 is at 00:0A:95:9D:68:03
  [SWITCH 2960] Incoming frame on Port 3 (Src: 00:0A:95:9D:68:03 -> Dst: 00:0A:95:9D:68:01)
  --> CAM Cache HIT! Forwarding frame directly out unicast Port 1 (PC0)
  --> Dynamic ARP resolution cached: 192.168.1.3 -> 00:0A:95:9D:68:03

PING 192.168.1.3 (192.168.1.3) 56(84) bytes of data.
  [SWITCH 2960] Incoming frame on Port 1 (Src: 00:0A:95:9D:68:01 -> Dst: 00:0A:95:9D:68:03)
  --> CAM Cache HIT! Forwarding frame directly out unicast Port 3 (PC2)
  64 bytes from 192.168.1.3: icmp_seq=1 ttl=64 time=0.98 ms
  64 bytes from 192.168.1.3: icmp_seq=2 ttl=64 time=0.69 ms
  64 bytes from 192.168.1.3: icmp_seq=3 ttl=64 time=0.92 ms
  64 bytes from 192.168.1.3: icmp_seq=4 ttl=64 time=1.31 ms

--- 192.168.1.3 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss
rtt min/avg/max = 0.69/0.97/1.31 ms

=== Switch 2960 Central CAM MAC Address Table ===
  VLAN    MAC Address           Type        Port      
  ----------------------------------------------------
  1       00:0A:95:9D:68:01     DYNAMIC     Fa0/1     
  1       00:0A:95:9D:68:03     DYNAMIC     Fa0/3     
  ----------------------------------------------------

============================================================================
  EXPERIMENT 8: ERROR DETECTION METHODS (VRC, LRC, 2D PARITY, CRC)
  Student: Aradhya Jain  |  Scholar No: 24112011111  |  Section: CSE-1
============================================================================

--- TWO-DIMENSIONAL (2D) PARITY MATRIX WITH AUTONOMOUS CORRECTION ---
Input 7-bit Data Words (4 rows):
  Row 0: 1010101
  Row 1: 1100110
  Row 2: 0111001
  Row 3: 1001011

Encoded 2D Parity Matrix (with VRC column and LRC row):
  Row 0: 1010101 | VRC: 0
  Row 1: 1100110 | VRC: 0
  Row 2: 0111001 | VRC: 0
  Row 3: 1001011 | VRC: 0
  --------------------------
  LRC:   1000001 | 0

[CHANNEL FAULT] Inverting bit at Row 1, Column 4 (1 -> 0)
  Syndrome Results: Bad Rows = {1} | Bad Columns = {4}
  --> ** EXACT SINGLE-BIT ERROR PINPOINTED AT INTERSECTION (1, 4) **
  --> Autonomously flipped corrupted bit back. 2D Parity restored with 100% data recovery!

--- CYCLIC REDUNDANCY CHECK (CRC) MODULO-2 DIVISION ---
Data Bitstream D(x): 1101011011
Generator Poly G(x): 10011 (CRC-4: x^4 + x + 1, degree r=4)
Appended Dividend  : 11010110110000
Modulo-2 Remainder : 1110
Transmitted Codeword: 11010110111110

[TEST 1: UNCORRUPTED CODEWORD]
  Received Codeword: 11010110111110 -> Remainder: 0000 -> ACCEPTED (No Error Detected)

[TEST 2: SINGLE-BIT ERROR AT BIT 3]
  Received Codeword: 11000110111110 -> Remainder: 0111 -> ERROR DETECTED! Frame Rejected.

[TEST 3: 4-BIT BURST ERROR ACROSS BITS 5 TO 8]
  Received Codeword: 11010001011110 -> Remainder: 0100 -> BURST ERROR DETECTED! Frame Rejected.

============================================================================
  EXPERIMENT 9: ERROR CORRECTION CODES (HAMMING 7,4 & EXTENDED SEC-DED 8,4)
  Student: Aradhya Jain  |  Scholar No: 24112011111  |  Section: CSE-1
============================================================================

--- 1. HAMMING (7,4) SINGLE ERROR CORRECTION (SEC) ---
Input 4-bit Data Vector: 1011 (d1=1, d2=0, d3=1, d4=1)
Generated Check Parity Bits: P1=0, P2=1, P4=0
Transmitted 7-bit Codeword [P1 P2 D1 P4 D2 D3 D4]: 0 1 1 0 0 1 1 

[TEST 1: UNCORRUPTED CODEWORD]
  Syndrome = 0 -> Status: NO ERROR -> Extracted: 1011

[TEST 2: CHANNEL BIT-INVERSION AT POSITION 6]
  Received Codeword with error: 0 1 1 0 0 0 1 
  Calculated Syndrome Vector S = (S4 S2 S1) = 6
  --> ** EXACT BIT CORRUPTION LOCALIZED AT POSITION 6 **
  --> Receiver inverted bit 6 back to original state.
  --> Recovered Data: 1011 (SUCCESSFUL 100% CORRECTION)

--- 2. EXTENDED SEC-DED (8,4) HAMMING CODE ARCHITECTURE ---
Input 4-bit Data: 1101
Encoded 8-bit Word [P0 | P1 P2 D1 P4 D2 D3 D4]: 0 | 1 0 1 0 1 0 1 

[SEC-DED TEST 1: SINGLE-BIT ERROR AT BIT 5]
  Status        : SINGLE_BIT_ERROR_CORRECTED
  Extracted Data: 1101 (Accurately corrected!)

[SEC-DED TEST 2: TWO SIMULTANEOUS BIT ERRORS AT BITS 3 AND 7]
  Status        : DOUBLE_BIT_ERROR_DETECTED_UNCORRECTABLE
  --> ** CRITICAL ALERT: DOUBLE-BIT ERROR DETECTED! **
  --> Syndrome is non-zero, but overall parity is valid.
  --> Receiver prevents erroneous bit correction, raising uncorrectable error alarm.

--- 3. CONTINUOUS TEXT STREAM FORWARD ERROR CORRECTION (FEC) ---
Transmitting string: "MANIT" with Forward Error Correction
  Char 'M' (0x4D) -> Injected Bit Error -> Auto-Corrected Char: 'M'
  Char 'A' (0x41) -> Injected Bit Error -> Auto-Corrected Char: 'A'
  Char 'N' (0x4E) -> Injected Bit Error -> Auto-Corrected Char: 'N'
  Char 'I' (0x49) -> Injected Bit Error -> Auto-Corrected Char: 'I'
  Char 'T' (0x54) -> Injected Bit Error -> Auto-Corrected Char: 'T'
```
</details>

<details>
<summary><b>Click to expand verified terminal outputs (Labs 10 through 14)</b></summary>

**Lab 10:** `python3 src/lab10_csma_non_persistent.py`

```text
==============================================================================
COMPUTER NETWORKS LAB - EXPERIMENT 10: NON-PERSISTENT CSMA SIMULATOR
Student: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
==============================================================================
Topology: 10 Stations | Bandwidth: 1.0 Mbps | Frame: 1000 bits (1.0 ms)
Propagation Delay (tau): 10.0 us | Parameter a = tau / T_fr = 0.010
------------------------------------------------------------------------------
Arrival (fps) Offered (G)   Sim Throughput (S)  Theory (S)    Collisions  Avg Delay
------------------------------------------------------------------------------
100           0.115         0.1150              0.1029        0           1.06 ms
300           0.310         0.3100              0.2354        0           1.28 ms
500           0.475         0.4750              0.3195        1           1.79 ms
800           0.710         0.7050              0.4106        9           2.82 ms
1000          1.012         0.7700              0.4955        73          28.81 ms
1500          1.555         0.7675              0.5956        81          88.53 ms
2500          2.502         0.7125              0.6918        106         129.63 ms
4000          3.882         0.7400              0.7588        95          156.81 ms
------------------------------------------------------------------------------
[STATUS] Non-Persistent CSMA channel contention protocol verified successfully.
```

**Lab 11:** `python3 src/lab11_csma_cd_beb.py`

```text
================================================================================
COMPUTER NETWORKS LAB - EXPERIMENT 11: CSMA/CD PERSISTENCE & BEB TESTBENCH
Student: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
================================================================================
Parameters: 8 Stations | Slot Time: 51.2 us | Max Retries: 16 | Slots: 1000
--------------------------------------------------------------------------------
Protocol Mode     Arrival Rate   Delivered   Collisions  Dropped   Throughput  Avg Delay
--------------------------------------------------------------------------------
1-Persistent      Light (2%)     168         57          0         0.336       4.92 slots
p-Persistent(0.5) Light (2%)     162         29          0         0.324       6.5 slots
p-Persistent(0.2) Light (2%)     153         25          0         0.306       10.18 slots
--------------------------------------------------------------------------------
1-Persistent      Medium (6%)    303         144         0         0.606       106.77 slots
p-Persistent(0.5) Medium (6%)    285         199         0         0.570       84.55 slots
p-Persistent(0.2) Medium (6%)    295         203         0         0.590       184.86 slots
--------------------------------------------------------------------------------
1-Persistent      Heavy (12%)    330         156         0         0.660       116.47 slots
p-Persistent(0.5) Heavy (12%)    308         162         0         0.616       247.83 slots
p-Persistent(0.2) Heavy (12%)    290         196         0         0.580       312.25 slots
--------------------------------------------------------------------------------
```

**Lab 12:** `python3 src/lab12_rip_distance_vector.py`

```text
==============================================================================
COMPUTER NETWORKS LAB - EXPERIMENT 12: DISTANCE VECTOR ROUTING (RIP)
Student: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
==============================================================================
[PHASE 1: 5-ROUTER MESH CONVERGENCE TESTBENCH]
>> Initial network converged successfully in 4 rounds.
Router A Routing Table:
  Destination    Cost (Hops)    Next Hop
  ----------------------------------------
  A              0              A
  B              1              B
  C              2              B
  D              3              B
  E              4              B

Router B Routing Table:
  Destination    Cost (Hops)    Next Hop
  ----------------------------------------
  A              1              A
  B              0              B
  C              1              C
  D              2              C
  E              3              C

Router C Routing Table:
  Destination    Cost (Hops)    Next Hop
  ----------------------------------------
  A              2              B
  B              1              B
  C              0              C
  D              1              D
  E              2              D

Router D Routing Table:
  Destination    Cost (Hops)    Next Hop
  ----------------------------------------
  A              3              C
  B              2              C
  C              1              C
  D              0              D
  E              1              E

Router E Routing Table:
  Destination    Cost (Hops)    Next Hop
  ----------------------------------------
  A              4              D
  B              3              D
  C              2              D
  D              1              D
  E              0              E

------------------------------------------------------------------------------
[PHASE 2: LINK FAILURE & COUNT-TO-INFINITY HAZARD EVALUATION]
Scenario: Severing link A <---> B. Destination B unreachable from A directly.

Simulating failure without Split Horizon (Count-to-Infinity):
>> Bounced routing vectors. Convergence took 15 rounds to count to 16.

Simulating failure WITH Split Horizon & Poisoned Reverse:
>> Immediate loop suppression! Converged cleanly in 2 rounds.
==============================================================================
```

**Lab 13:** `python3 src/lab13_ospf_link_state.py`

```text
==============================================================================
COMPUTER NETWORKS LAB - EXPERIMENT 13: OSPF LINK-STATE ROUTING (DIJKSTRA)
Student: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
==============================================================================
[PHASE 1: LSDB FLOODING & DIJKSTRA SPF COMPUTATION]
OSPF Forwarding Table for Router [R1] (Area: 0.0.0.0):
  Destination    Metric (Cost)  Next Hop          Shortest Path
  -----------------------------------------------------------------
  R1             0              DIRECT (Self)     R1
  R2             10             R2                R1 -> R2
  R3             20             R2                R1 -> R2 -> R3
  R4             45             R2                R1 -> R2 -> R3 -> R5 -> R4
  R5             35             R2                R1 -> R2 -> R3 -> R5
  R6             65             R2                R1 -> R2 -> R3 -> R5 -> R4 -> R6

OSPF Forwarding Table for Router [R3] (Area: 0.0.0.0):
  Destination    Metric (Cost)  Next Hop          Shortest Path
  -----------------------------------------------------------------
  R1             20             R2                R3 -> R2 -> R1
  R2             10             R2                R3 -> R2
  R3             0              DIRECT (Self)     R3
  R4             25             R5                R3 -> R5 -> R4
  R5             15             R5                R3 -> R5
  R6             45             R5                R3 -> R5 -> R4 -> R6

------------------------------------------------------------------------------
[PHASE 2: DYNAMIC METRIC RECONFIGURATION & PATH ADAPTATION]
Action: Increasing R1-R2 link metric from 10 to 70 (Simulating trunk congestion)
>> Recomputed Shortest Path Tree for Router R1:
OSPF Forwarding Table for Router [R1] (Area: 0.0.0.0):
  Destination    Metric (Cost)  Next Hop          Shortest Path
  -----------------------------------------------------------------
  R1             0              DIRECT (Self)     R1
  R2             40             R3                R1 -> R3 -> R2
  R3             30             R3                R1 -> R3
  R4             55             R3                R1 -> R3 -> R5 -> R4
  R5             45             R3                R1 -> R3 -> R5
  R6             75             R3                R1 -> R3 -> R5 -> R4 -> R6

[STATUS] OSPF Link-State Database and Dijkstra SPF verified successfully.
==============================================================================
```

**Lab 14:** `python3 src/lab14_tcp_echo_socket.py` (RTT values change on every run)

```text
==============================================================================
COMPUTER NETWORKS LAB - EXPERIMENT 14: TCP/IP ECHO SOCKET ARCHITECTURE
Student: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
==============================================================================
[SERVER STARTED] Listening on 127.0.0.1:65432

[PHASE 1: CLIENT-SERVER STREAM I/O & RTT MEASUREMENT]
>> Sent   : "SYN -> SYN-ACK -> ACK: Handshake Verified"
   Echoed : "SYN -> SYN-ACK -> ACK: Handshake Verified" | RTT: 0.139 ms | Status: MATCH [PASS]

>> Sent   : "Computer Networks Lab (CS-501) - MANIT Bhopal"
   Echoed : "Computer Networks Lab (CS-501) - MANIT Bhopal" | RTT: 0.062 ms | Status: MATCH [PASS]

>> Sent   : "Scholar Number: 24112011111 | Aradhya Jain"
   Echoed : "Scholar Number: 24112011111 | Aradhya Jain" | RTT: 0.058 ms | Status: MATCH [PASS]

>> Sent   : "Packet Stream Frame 04: Hello Berkeley Sockets"
   Echoed : "Packet Stream Frame 04: Hello Berkeley Sockets" | RTT: 0.056 ms | Status: MATCH [PASS]

>> Sent   : "Stream Boundary Test: Full-Duplex Byte Transport"
   Echoed : "Stream Boundary Test: Full-Duplex Byte Transport" | RTT: 0.057 ms | Status: MATCH [PASS]

------------------------------------------------------------------------------
[PHASE 2: CONCURRENT MULTI-CLIENT THREAD POOL STRESS TEST]
Thread Client-0: Transmitted 3 frames concurrently | Avg RTT: 0.163 ms | Verified: 100%
Thread Client-1: Transmitted 3 frames concurrently | Avg RTT: 0.144 ms | Verified: 100%
Thread Client-2: Transmitted 3 frames concurrently | Avg RTT: 0.162 ms | Verified: 100%
Thread Client-3: Transmitted 3 frames concurrently | Avg RTT: 0.155 ms | Verified: 100%
------------------------------------------------------------------------------
>> Total bytes echoed by server: 407 bytes across sessions.
[SERVER SHUTDOWN] Port 65432 closed cleanly.
[STATUS] TCP/IP Socket Stream and 3-Way Handshake echo model verified.
==============================================================================
```

</details>

---

## 📂 Repository File Structure

```
cn-lab-experiments/
├── Makefile                                # Automated build system (all, run, run_python, lab1..lab14)
├── README.md                               # Comprehensive documentation & theory guide
├── LICENSE                                 # MIT Open Source License
├── .gitignore                              # Git exclusion rules (bin, objects, debug symbols)
├── cn_labs_1_to_9.cpp                      # Master all-in-one C++17 implementation (Labs 1-9)
├── cn_labs_1_to_5.py                       # Companion Python test suite (Labs 1-5)
└── src/                                    # Modular standalone C++ source files
    ├── lab1_star_topology.cpp              # Lab 1: Star Topology & Diagnostics
    ├── lab2_tcp_sockets.cpp                # Lab 2: TCP Client-Server Stream Sockets
    ├── lab3_multiclient_chat.cpp           # Lab 3: Concurrent Multi-Client Threaded Chat
    ├── lab4_file_transfer.cpp              # Lab 4: Socket File Transfer with CRC-32 & FNV
    ├── lab5_flow_control.cpp               # Lab 5: Stop-and-Wait, Go-Back-N, Selective Repeat
    ├── lab6_7_error_control.cpp            # Lab 6-7: Alternating Bit Protocol & Loss Recovery
    ├── lab8_crc_lrc_vrc.cpp                # Lab 8: VRC, LRC, 2D Parity Matrix & CRC Modulo-2
    ├── lab9_hamming_code.cpp               # Lab 9: Hamming (7,4) SEC & Extended SEC-DED (8,4)
    ├── lab10_csma_non_persistent.py        # Lab 10: Non-Persistent CSMA
    ├── lab11_csma_cd_beb.py                # Lab 11: 1-Persistent & p-Persistent CSMA/CD with BEB
    ├── lab12_rip_distance_vector.py        # Lab 12: Distance Vector Routing (RIP)
    ├── lab13_ospf_link_state.py            # Lab 13: OSPF Link-State Routing (Dijkstra SPF)
    └── lab14_tcp_echo_socket.py            # Lab 14: TCP/IP Echo Client-Server
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
