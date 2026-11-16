# Computer Networks Laboratory (CS-501) — Experiments 1 to 14

[![Python 3](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Python programs for the Computer Networks Laboratory at MANIT Bhopal. Each lab has its own folder with the **question (aim)**, the **code**, **how to run it**, the **output**, and **viva questions with answers**.

---

## 👨‍🎓 Student & Academic Details

* **Student Name:** Aradhya Jain
* **Scholar Number:** `24112011111`
* **Department & Section:** Department of Computer Science & Engineering, `CSE-1`
* **Institution:** Maulana Azad National Institute of Technology (MANIT), Bhopal
* **Course:** Computer Networks Laboratory (`CS-501`)
* **Semester:** V Semester, B.Tech CSE

---

## 📋 Experiments

| Lab | Topic | Code |
|:---:|-------|------|
| [1](Lab-01-Linux-Commands-Star-Topology) | Linux commands & star topology in Cisco Packet Tracer | no code (commands + Packet Tracer) |
| [2](Lab-02-Socket-Client-Server) | Socket programming: client–server messaging | `server.py`, `client.py` |
| [3](Lab-03-Multi-Client-Chat) | Multi-client chat application (threads, broadcast) | `chat_server.py`, `chat_client.py` |
| [4](Lab-04-Serial-Port-File-Transfer) | PC to PC file transfer over a serial port | `sender.py`, `receiver.py` |
| [5](Lab-05-Flow-Control) | Flow control: Stop-and-Wait & Go-Back-N | `stop_and_wait.py`, `sliding_window.py` |
| [6](Lab-06-Error-Control-Protocols) | Error control: parity, Stop-and-Wait ARQ, Go-Back-N, Selective Repeat | `parity_check.py`, `stop_and_wait_arq.py`, `sliding_window_arq.py` |
| [7](Lab-07-Error-Detection-Correction) | Error detection & correction: VRC, LRC, 2D parity, Hamming | `vrc_lrc.py`, `hamming_code.py` |
| [8](Lab-08-VRC-LRC-CRC) | VRC, LRC & CRC error detection | `vrc_lrc.py`, `crc.py` |
| [9](Lab-09-Hamming-Code) | Hamming (7,4) & Extended SEC-DED (8,4) | `hamming_code.py` |
| [10](Lab-10-Non-Persistent-CSMA) | Non-Persistent CSMA | `csma_non_persistent.py` |
| [11](Lab-11-CSMA-CD-BEB) | 1-Persistent & p-Persistent CSMA/CD with Binary Exponential Backoff | `csma_cd_protocols.py` |
| [12](Lab-12-Distance-Vector-RIP) | Distance Vector Routing (RIP) | `rip_distance_vector.py` |
| [13](Lab-13-OSPF-Link-State) | OSPF Link-State Routing (Dijkstra) | `ospf_link_state.py` |
| [14](Lab-14-TCP-Echo-Client-Server) | TCP/IP Echo Client–Server with RTT | `tcp_echo_socket.py` |

Labs 2–14 have code: 13 labs in total.

---

## ⚡ How to Run

**Requirements:** Python 3. Everything uses the standard library except Lab 4, which needs `pyserial` and `socat`:
```bash
pip3 install pyserial
brew install socat            # macOS   (Linux: sudo apt install socat)
```

**Run a lab:**
```bash
git clone https://github.com/code-execute-rishi/cn-lab-experiments.git
cd cn-lab-experiments/Lab-12-Distance-Vector-RIP
python3 rip_distance_vector.py
```
- Labs 2 and 3 need two or three terminals (server and clients); see their READMEs.
- Lab 4 needs `socat` running first to create the virtual serial cable.
- Lab 5 takes the scenario number: `python3 stop_and_wait.py 1` or `2`.
- Labs 6–14 need no input.

---

## 🏛️ Theory Summary

### 1. TCP Socket Lifecycle (Labs 2, 3, 14)

```
        SERVER                                         CLIENT
      ┌──────────────────┐                           ┌──────────────────┐
      │     socket()     │                           │     socket()     │
      └────────┬─────────┘                           └────────┬─────────┘
      ┌────────▼─────────┐                                    │
      │   bind(PORT)     │                                    │
      └────────┬─────────┘                                    │
      ┌────────▼─────────┐                                    │
      │     listen()     │                                    │
      └────────┬─────────┘                                    │
      ┌────────▼─────────┐     Three-Way Handshake       ┌────▼─────────────┐
      │     accept()     │ ◄───────────────────────────► │    connect()     │
      └────────┬─────────┘    [SYN -> SYN-ACK -> ACK]    └────────┬─────────┘
      ┌────────▼─────────┐                               ┌────▼─────────────┐
      │  recv() / send() │ ◄───────────────────────────► │  send() / recv() │
      └────────┬─────────┘                               └────┬─────────────┘
      ┌────────▼─────────┐                               ┌────▼─────────────┐
      │     close()      │                               │     close()      │
      └──────────────────┘                               └──────────────────┘
```

### 2. Protocol Efficiency (Labs 5, 6)

The normalized propagation delay ratio:
$$a = \frac{T_{\text{prop}}}{T_{\text{trans}}} = \frac{d / v}{L / B}$$
where $d$ = link distance, $v$ = propagation speed ($\approx 2 \times 10^8$ m/s), $L$ = frame length in bits, $B$ = bandwidth in bps.

* **Stop-and-Wait ARQ:** $\eta = \frac{1}{1 + 2a}$
* **Sliding Window (window $W$):** $\eta = \min\left(1, \frac{W}{1 + 2a}\right)$

### 3. 2D Parity (Labs 7, 8)

Each character gets a row parity bit (VRC), and each bit column gets a column parity bit (LRC). A single flipped bit makes exactly one row and one column fail; the bit where they cross is the error, and the receiver flips it back. Four errors in a rectangle are **not** detected.

### 4. Cyclic Redundancy Check (Lab 8)

For data $M(x)$ and generator $G(x)$ of degree $r$:
1. Append $r$ zeros: $M(x) \cdot x^r$.
2. Divide by $G(x)$ using modulo-2 (XOR) division to get the remainder $R(x)$.
3. Send $T(x) = M(x) \cdot x^r + R(x)$.
4. The receiver divides by $G(x)$; remainder 0 means no error detected.

Common generator: **CRC-4** $G(x) = x^4 + x + 1$ (`10011`). Ethernet uses **CRC-32**.

### 5. Hamming Code (Labs 7, 9)

Hamming bound: $2^r \ge m + r + 1$. For $m = 4$ data bits, $r = 3$ parity bits.

* Positions 1, 2, 4 are parity bits; 3, 5, 6, 7 are data bits.
* $P_1 = D_1 \oplus D_2 \oplus D_4$, $P_2 = D_1 \oplus D_3 \oplus D_4$, $P_4 = D_2 \oplus D_3 \oplus D_4$
* Syndrome $S = (S_4 S_2 S_1)_2$: 0 means no error, otherwise it is the position of the wrong bit.

**Extended SEC-DED (8,4)** adds an overall parity bit $P_0$:
* $S = 0$, overall parity OK → no error
* $S \ne 0$, overall parity wrong → single-bit error at position $S$, corrected
* $S \ne 0$, overall parity OK → double-bit error detected, cannot correct
* $S = 0$, overall parity wrong → $P_0$ itself is wrong

### 6. MAC Protocols (Labs 10, 11)

* **1-persistent CSMA:** send as soon as the channel is idle.
* **Non-persistent CSMA:** if busy, wait a random time before sensing again.
* **p-persistent CSMA:** if idle, send with probability $p$.
* **CSMA/CD:** stop as soon as a collision is detected, send a jam signal, then wait using Binary Exponential Backoff: after the $k$-th collision, wait a random $0$ to $2^k - 1$ slots ($k$ stops growing at 10).

### 7. Routing (Labs 12, 13)

* **Distance Vector (RIP):** Bellman-Ford $D_x(y) = \min_v \{ c(x,v) + D_v(y) \}$; hop count, 16 = infinity; count-to-infinity fixed with split horizon and poisoned reverse.
* **Link State (OSPF):** every router floods LSAs, builds the same link-state database, and runs Dijkstra's shortest path first.

---

## 📂 Repository Structure

```
cn-lab-experiments/
├── README.md
├── LICENSE
├── Lab-01-Linux-Commands-Star-Topology/   README only
├── Lab-02-Socket-Client-Server/           server.py, client.py
├── Lab-03-Multi-Client-Chat/              chat_server.py, chat_client.py
├── Lab-04-Serial-Port-File-Transfer/      sender.py, receiver.py, hello.txt
├── Lab-05-Flow-Control/                   stop_and_wait.py, sliding_window.py
├── Lab-06-Error-Control-Protocols/        parity_check.py, stop_and_wait_arq.py, sliding_window_arq.py
├── Lab-07-Error-Detection-Correction/     vrc_lrc.py, hamming_code.py
├── Lab-08-VRC-LRC-CRC/                    vrc_lrc.py, crc.py
├── Lab-09-Hamming-Code/                   hamming_code.py
├── Lab-10-Non-Persistent-CSMA/            csma_non_persistent.py
├── Lab-11-CSMA-CD-BEB/                    csma_cd_protocols.py
├── Lab-12-Distance-Vector-RIP/            rip_distance_vector.py
├── Lab-13-OSPF-Link-State/                ospf_link_state.py
├── Lab-14-TCP-Echo-Client-Server/         tcp_echo_socket.py
└── archive/cpp-version/                   earlier C++ version of Labs 1–9 (kept for reference)
```

Each lab folder has its own `README.md` with the question, code, how to run, output and viva questions.

---

## 📄 License

This project is licensed under the **MIT License**; see the [LICENSE](LICENSE) file for details.
