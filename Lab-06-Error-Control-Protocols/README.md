# Lab 6: Error Control Protocols

## Question
**Aim:** To implement, test, and comparatively evaluate Data Link Layer Error Control Protocols in Python: Stop-and-Wait ARQ with 1-bit sequence alternation, Go-Back-N Sliding Window ARQ, and Selective-Repeat ARQ with individual packet buffering under simulated transmission loss. (The lab manual also lists Even and Odd Parity Check.)

## Files
- [`parity_check.py`](parity_check.py): Even and odd parity: generating the parity bit and detecting errors.
- [`stop_and_wait_arq.py`](stop_and_wait_arq.py): Stop-and-Wait ARQ with 1-bit sequence numbers, frame corruption and ACK loss.
- [`sliding_window_arq.py`](sliding_window_arq.py): Go-Back-N and Selective Repeat ARQ.

## Logic (How the Program Works)

```text
parity_check.py
1. generate_parity(data, mode): count the 1s. Even parity adds '1' if the count is odd (to make it even), else '0'. Odd parity does the opposite.
2. The codeword is data + parity bit. verify_parity() recomputes the parity of the data part and compares it with the last bit.
3. inject_bit_errors() flips chosen bits to simulate noise.
4. Tests: 1011001 with even and odd parity; 1 flipped bit is detected; 2 flipped bits are NOT detected (the count of 1s is still even).

stop_and_wait_arq.py
1. Sender, Channel and Receiver are classes. The sender uses a 1-bit sequence number (0, 1, 0, ...).
2. The sender sends the frame and waits for ACK = 1 - seq. If the ACK is correct, it flips seq; if not (timeout), it resends.
3. The channel can corrupt the frame on the first try (the receiver sees a bad checksum, discards it and sends no ACK) or drop the ACK on the first try.
4. The receiver accepts a frame only if seq equals the expected value, then flips expected and sends ACK(expected). A repeated seq is a duplicate: discard it and resend the ACK.
5. 3 packets in 3 scenarios: normal, corrupted frame, lost ACK -> 5 transmissions, 2 retransmissions.

sliding_window_arq.py
Go-Back-N (W = 4, 8 frames, F2 lost once)
1. Send every frame in the window.
2. The receiver accepts frames only in order and sends a cumulative ACK.
3. When F2 is lost, the sender times out and resends the whole window starting from F2.
Selective Repeat (W = 4, 8 frames, F2 lost once)
1. Send every frame in the window that is not ACKed yet; each frame is ACKed on its own.
2. Frames after the lost one are kept in the receiver's buffer instead of being thrown away.
3. When the timer for F2 expires, only F2 is resent. Then the buffered frames are delivered in order and the window slides.
Result: Selective Repeat needs fewer retransmissions than Go-Back-N.
```

## How to Run
No input is needed; the test data is built into each program.
```bash
python3 parity_check.py
python3 stop_and_wait_arq.py
python3 sliding_window_arq.py
```

## Output

### `parity_check.py`

```
============================================================
TEST 1: PARITY GENERATION & VERIFICATION
============================================================
Data Word: 1011001 (Count of 1s: 4)
  Even Parity Bit: 0 -> Transmitted Codeword: 10110010  |  Receiver: VALID
  Odd Parity Bit:  1 -> Transmitted Codeword: 10110011  |  Receiver: VALID

============================================================
TEST 2: SINGLE-BIT ERROR INJECTION (Bit 3 inverted)
============================================================
Original Codeword:  10110010  ->  Injected Codeword: 10100010 (Bit 3 flipped)
Receiver Check (Even Scheme): ERROR DETECTED!

============================================================
TEST 3: DOUBLE-BIT ERROR INJECTION (Bits 1 and 4 inverted)
============================================================
Original Codeword:  10110010  ->  Injected Codeword: 11111010 (Bits 1 & 4 flipped)
Receiver Check (Even Scheme): VALID (FALSE ACCEPTANCE - CRITICAL FLAW)
Observation: Parity count remained even (6 ones). Double-bit error completely missed!
```

### `stop_and_wait_arq.py`

```
[SCENARIO 1: NORMAL ERROR-FREE TRANSMISSION]
[SENDER] Transmitting Frame(seq=0, data='DATA_PKT_0', attempt=1)
  [RECEIVER] In-order Frame(seq=0, data='DATA_PKT_0') accepted.
  [RECEIVER] Sending ACK(1)
[SENDER] Received valid ACK(1). Sliding sequence bit to 1.

[SCENARIO 2: FRAME 1 CORRUPTED IN TRANSIT]
[SENDER] Transmitting Frame(seq=1, data='DATA_PKT_1', attempt=1)
  [CHANNEL] Noise burst injected on channel! Checksum inverted.
  [RECEIVER] Checksum mismatch! Corrupted Frame(seq=1) discarded.
[SENDER] !! Timeout (No ACK / ACK lost). Retransmitting Frame(seq=1)...
[SENDER] Transmitting Frame(seq=1, data='DATA_PKT_1', attempt=2)
  [RECEIVER] In-order Frame(seq=1, data='DATA_PKT_1') accepted.
  [RECEIVER] Sending ACK(0)
[SENDER] Received valid ACK(0). Sliding sequence bit to 0.

[SCENARIO 3: ACK 1 LOST IN TRANSIT -> DUPLICATE DETECTION]
[SENDER] Transmitting Frame(seq=0, data='DATA_PKT_2', attempt=1)
  [RECEIVER] In-order Frame(seq=0, data='DATA_PKT_2') accepted.
  [RECEIVER] Sending ACK(1)
  [CHANNEL] *** ACK dropped by physical interface! ***
[SENDER] !! Timeout (No ACK / ACK lost). Retransmitting Frame(seq=0)...
[SENDER] Transmitting Frame(seq=0, data='DATA_PKT_2', attempt=2)
  [RECEIVER] Duplicate Frame(seq=0) detected! Discarding payload.
  [RECEIVER] Resending ACK(1)
[SENDER] Received valid ACK(1). Sliding sequence bit to 1.

Delivered all 3 packets without duplication. Total Transmissions: 5, Retransmissions: 2.
```

### `sliding_window_arq.py`

```
=== RUNNING GO-BACK-N (W = 4, Total = 8 Frames, Drop F2) ===
[SENDER] Sent Frame F0
[SENDER] Sent Frame F1
[SENDER] Sent Frame F2
[SENDER] Sent Frame F3
  [RECEIVER] In-order Frame F0 accepted -> Sending cumulative ACK1
  [RECEIVER] In-order Frame F1 accepted -> Sending cumulative ACK2
  [CHANNEL] *** Frame F2 LOST IN TRANSIT! ***
[SENDER] !! TIMEOUT for Frame F2! Go-Back-N triggered.
[SENDER] Resending entire window from base F2 (F2 to F3)
[SENDER] Sent Frame F2
[SENDER] Sent Frame F3
[SENDER] Sent Frame F4
[SENDER] Sent Frame F5
  [RECEIVER] In-order Frame F2 accepted -> Sending cumulative ACK3
  [RECEIVER] In-order Frame F3 accepted -> Sending cumulative ACK4
  [RECEIVER] In-order Frame F4 accepted -> Sending cumulative ACK5
  [RECEIVER] In-order Frame F5 accepted -> Sending cumulative ACK6
[SENDER] Sent Frame F6
[SENDER] Sent Frame F7
  [RECEIVER] In-order Frame F6 accepted -> Sending cumulative ACK7
  [RECEIVER] In-order Frame F7 accepted -> Sending cumulative ACK8
GBN Result: Delivered 8 frames in 10 total transmissions (2 retransmissions).

=== RUNNING SELECTIVE-REPEAT (W_S = 4, W_R = 4, Total = 8 Frames, Drop F2) ===
[SENDER] Transmitted Frame F0
  [RECEIVER] Frame F0 received and cached in receive buffer. Sent ACK(0)
[SENDER] Transmitted Frame F1
  [RECEIVER] Frame F1 received and cached in receive buffer. Sent ACK(1)
[SENDER] Transmitted Frame F2
  [CHANNEL] *** Frame F2 LOST IN TRANSIT! ***
[SENDER] Transmitted Frame F3
  [RECEIVER] Frame F3 received and cached in receive buffer. Sent ACK(3)
  [RECEIVER] Delivered F0 to Network Layer.
  [RECEIVER] Delivered F1 to Network Layer.
[SENDER] Transmitted Frame F2
  [RECEIVER] Frame F2 received and cached in receive buffer. Sent ACK(2)
[SENDER] Transmitted Frame F4
  [RECEIVER] Frame F4 received and cached in receive buffer. Sent ACK(4)
[SENDER] Transmitted Frame F5
  [RECEIVER] Frame F5 received and cached in receive buffer. Sent ACK(5)
  [RECEIVER] Delivered F2 to Network Layer.
  [RECEIVER] Delivered F3 to Network Layer.
  [RECEIVER] Delivered F4 to Network Layer.
  [RECEIVER] Delivered F5 to Network Layer.
[SENDER] Transmitted Frame F6
  [RECEIVER] Frame F6 received and cached in receive buffer. Sent ACK(6)
[SENDER] Transmitted Frame F7
  [RECEIVER] Frame F7 received and cached in receive buffer. Sent ACK(7)
  [RECEIVER] Delivered F6 to Network Layer.
  [RECEIVER] Delivered F7 to Network Layer.
SR Result: Delivered 8 frames in 9 total transmissions (Only 1 retransmission)!
```


## Viva Questions

1. **What is error control?**
   Detecting damaged or lost frames and getting them resent, usually with ARQ (Automatic Repeat reQuest).
2. **What is a parity bit?**
   An extra bit that makes the number of 1s even (even parity) or odd (odd parity). It detects any odd number of bit errors, but not an even number.
3. **Why does Stop-and-Wait ARQ need only a 1-bit sequence number?**
   Only one frame is outstanding at a time, so alternating 0 and 1 is enough to tell a new frame from a duplicate.
4. **What happens when an ACK is lost?**
   The sender times out and resends the frame. The receiver sees the same sequence number, discards the duplicate and resends the ACK.
5. **Go-Back-N vs Selective Repeat?**
   Go-Back-N resends the lost frame and everything after it. Selective Repeat resends only the lost frame and buffers out-of-order frames at the receiver.
6. **What is a NAK?**
   A negative acknowledgement: the receiver asks for a specific frame to be resent without waiting for the timeout.
7. **Window size limits?**
   With m-bit sequence numbers: Go-Back-N up to 2^m − 1, Selective Repeat up to 2^(m−1).
8. **What is piggybacking?**
   Sending the ACK inside an outgoing data frame instead of as a separate frame, to save bandwidth.
