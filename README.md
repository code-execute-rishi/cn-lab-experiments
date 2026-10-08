# Computer Networks Laboratory (CS-504) — Experiments 1 to 5

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)]()

> Complete, modular, and self-contained implementations for **Computer Networks Laboratory (CS-504)** Experiments 1 through 5. Written in pure Python with **zero external dependencies** (`pip` not required).

---

## 👨‍🎓 Student & Academic Details

* **Student Name:** Aradhya Jain
* **Scholar Number:** `24112011111`
* **Department & Section:** Department of Computer Science & Engineering, `CSE-1`
* **Institution:** Maulana Azad National Institute of Technology (MANIT), Bhopal
* **Course:** Computer Networks Laboratory (`CS-504`)
* **Semester:** V Semester, B.Tech CSE

---

## 📋 Table of Experiments

| Experiment | Title & Focus | Implementing Class | CLI Flag |
| :---: | :--- | :--- | :---: |
| **Lab 1** | **Star Topology Network & Linux Commands Simulator**<br>• Switch 2960 emulation & dynamic MAC address learning table<br>• Address Resolution Protocol (ARP) broadcasting<br>• Subnet pinging with RTT latency and packet loss tracking<br>• Emulation of `ifconfig`, `netstat`, and `ping` | `Lab1_StarTopologyAndNetworkDiagnostics` | `--lab 1` |
| **Lab 2** | **TCP Socket Programming (Client-Server Binding)**<br>• Stream socket setup: `socket()`, `setsockopt(SO_REUSEADDR)`, `bind()`<br>• Connection handshake: `listen()`, `accept()`, `connect()`<br>• Two-way conversational messaging & graceful teardown on `/quit` | `Lab2_TCPSocketBasics` | `--lab 2` |
| **Lab 3** | **Multi-Client Threaded Chat Application**<br>• Concurrent multi-threading (`threading.Thread`) for simultaneous clients<br>• Thread-safe shared client registry using `threading.Lock()`<br>• Centralized message broadcast filtering out the sender<br>• Dynamic join announcements and clean disconnect notifications | `Lab3_MultiClientChatApplication` | `--lab 3` |
| **Lab 4** | **Serial / Point-to-Point File Transfer with SHA-256**<br>• Protocol framing (`<filename>|<filesize>\n`)<br>• Chunk-based binary streaming across 64-byte windows<br>• Cryptographic verification: SHA-256 hash comparison & byte diff | `Lab4_FileTransferProtocol` | `--lab 4` |
| **Lab 5** | **Flow Control Protocols (ARQ Simulations)**<br>• **Stop-and-Wait ARQ:** Timeout retransmissions & duplicate discarding<br>• **Go-Back-N ARQ:** Window sliding ($W=4$), cumulative ACKs, rollback<br>• **Selective Repeat ARQ:** Independent windows, selective retransmission | `Lab5_FlowControlProtocols` | `--lab 5` |

---

## ⚡ Quick Start & Installation

This project relies **exclusively on the Python standard library**. No third-party modules or virtual environments are needed.

### Clone the Repository
```bash
git clone https://github.com/code-execute-rishi/cn-lab-experiments.git
cd cn-lab-experiments
```

### Requirements
* Python 3.7 or newer.

---

## 💻 Usage Guide

### 1. Run All Experiments (Full Automated Test Suite)
Executes all 5 experiments sequentially and prints verified results:
```bash
python3 cn_labs_1_to_5.py --all
```

### 2. Run a Specific Experiment
Target an individual lab experiment by passing its number via `--lab`:
```bash
# Lab 1: Star Topology & Diagnostics
python3 cn_labs_1_to_5.py --lab 1

# Lab 2: TCP Client-Server Sockets
python3 cn_labs_1_to_5.py --lab 2

# Lab 3: Multi-Client Threaded Chat
python3 cn_labs_1_to_5.py --lab 3

# Lab 4: Serial Byte File Transfer & SHA-256
python3 cn_labs_1_to_5.py --lab 4

# Lab 5: Flow Control (Stop & Wait / Go-Back-N / Selective Repeat)
python3 cn_labs_1_to_5.py --lab 5
```

### 3. Interactive Menu Mode
Run without arguments in an interactive terminal to launch the selector:
```bash
python3 cn_labs_1_to_5.py
```
```text
======================================================================
  COMPUTER NETWORKS LABORATORY - EXPERIMENTS 1 TO 5 (CS-504)
  Student: Aradhya Jain  |  Scholar No: 24112011111  |  Section: CSE-1
======================================================================

Select an experiment to run:
  1. Lab 1: Star Topology Network & Linux Commands Simulator
  2. Lab 2: TCP Socket Client-Server Communication
  3. Lab 3: Multi-Client Threaded Chat Server & Broadcast
  4. Lab 4: Reliable Byte-by-Byte File Transfer & SHA-256 Checksum
  5. Lab 5: Flow Control Protocols (Stop-and-Wait, Go-Back-N, Selective Repeat)
  6. Run ALL Experiments (1 to 5)
  0. Exit
```

---

## 🔬 Sample Execution Traces

<details>
<summary><b>Click to expand sample execution output</b></summary>

```text
======================================================================
  EXPERIMENT 1: STAR TOPOLOGY NETWORK SIMULATION & DIAGNOSTICS
======================================================================
[TEST 1] PC0 (192.168.1.1) pings PC1 (192.168.1.3)

--- Ping from PC0 (192.168.1.1) to 192.168.1.3 ---
PING 192.168.1.3 (56 data bytes, 4 packets transmitted):
64 bytes from 192.168.1.3: icmp_seq=1 ttl=64 time=0.71 ms
64 bytes from 192.168.1.3: icmp_seq=2 ttl=64 time=0.85 ms
64 bytes from 192.168.1.3: icmp_seq=3 ttl=64 time=1.24 ms
64 bytes from 192.168.1.3: icmp_seq=4 ttl=64 time=0.53 ms
--- 192.168.1.3 ping statistics ---
4 packets transmitted, 4 received, 0.0% packet loss
rtt min/avg/max = 0.53/0.83/1.24 ms

=== Switch 2960 Central MAC Address Table ===
VLAN     MAC Address            Type       Port    
--------------------------------------------------
1        00:0A:95:9D:68:01      DYNAMIC    Fa0/1   
1        00:0A:95:9D:68:02      DYNAMIC    Fa0/2   
1        00:0A:95:9D:68:03      DYNAMIC    Fa0/3   
1        00:0A:95:9D:68:04      DYNAMIC    Fa0/4   
--------------------------------------------------
[VERIFIED] Star topology active, switch learned MACs dynamically, 0% loss.

======================================================================
  EXPERIMENT 4: SERIAL FILE TRANSFER & SHA-256 INTEGRITY CHECK
======================================================================
[SOURCE] Transmitting file: 'hello.txt' (256 bytes)
----------------------------------------------------------------------
Original File Size : 256 bytes
Received File Size : 256 bytes
Source SHA-256     : 42f9f36f67b677383caa48b4f179dcae5e0f4e3992c8855de0c51011ee0a8b41
Destination SHA-256: 42f9f36f67b677383caa48b4f179dcae5e0f4e3992c8855de0c51011ee0a8b41
Byte-for-Byte Match: True
----------------------------------------------------------------------
[VERIFIED] Complete byte integrity verified without single-bit corruption.

======================================================================
  EXPERIMENT 5: FLOW CONTROL PROTOCOLS (STOP-AND-WAIT & SLIDING WINDOW)
======================================================================
--- Sliding Window: Go-Back-N ARQ (Window Size = 4) ---
Total Frames: 12 | Injected Loss Sequence Numbers: [3]
[Round 01] Window [0..3] -> Sent frames: [0, 1, 2, 3]
  --> [TIMEOUT] Frame F3 LOST! Triggering Go-Back-N rollback to F3.
[Round 02] Window [3..6] -> Sent frames: [3, 4, 5, 6]
  --> [ACK BATCH] Frames [3, 4, 5, 6] cumulatively acknowledged. Window advances.
[Round 03] Window [7..10] -> Sent frames: [7, 8, 9, 10]
  --> [ACK BATCH] Frames [7, 8, 9, 10] cumulatively acknowledged. Window advances.
[Round 04] Window [11..11] -> Sent frames: [11]
  --> [ACK BATCH] Frames [11] cumulatively acknowledged. Window advances.
------------------------------------------------------------------------
Summary: All 12 frames delivered | Total Frame Transmissions: 13 | Overheads: 1
```

</details>

---

## 📄 License

This repository is distributed under the [MIT License](LICENSE).
