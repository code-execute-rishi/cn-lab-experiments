# Lab 5: Flow Control Protocols (Stop-and-Wait & Sliding Window)

## Question
**Aim:** Implement flow control protocols, Stop-and-Wait and Sliding Window (Go-Back-N), and prove both recover correctly under frame loss and ACK loss, across more than one loss pattern.

## Files
- [`stop_and_wait.py`](stop_and_wait.py): sends 8 frames one at a time. A lost frame or lost ACK causes a timeout and a retransmission; the receiver discards duplicates.
- [`sliding_window.py`](sliding_window.py): Go-Back-N with 12 frames. On a loss, the sender resends from the lost frame.

## How to Run
```bash
python3 stop_and_wait.py 1     # Scenario A: F2 lost once, ACK4 lost once
python3 stop_and_wait.py 2     # Scenario B: F1, F5 lost once; ACK3, ACK6 lost once
python3 sliding_window.py 1    # Scenario A: window 4, loss at F3
python3 sliding_window.py 2    # Scenario B: window 3, losses at F2 and F8
```

## Output

### Stop-and-Wait, Scenario A
```
=== Scenario A: clean-ish channel, frame F2 lost once, ACK4 lost once ===

[SENDER] sending F0 (attempt 1), starting timer 0.3s
[RECEIVER] F0 received correctly, buffered
[SENDER] ACK0 received, window slides to next frame

[SENDER] sending F1 (attempt 1), starting timer 0.3s
[RECEIVER] F1 received correctly, buffered
[SENDER] ACK1 received, window slides to next frame

[SENDER] sending F2 (attempt 1), starting timer 0.3s
  [CHANNEL] frame F2 LOST in transit
[SENDER] timeout waiting for ACK2 -> retransmit
[SENDER] sending F2 (attempt 2), starting timer 0.3s
[RECEIVER] F2 received correctly, buffered
[SENDER] ACK2 received, window slides to next frame

[SENDER] sending F3 (attempt 1), starting timer 0.3s
[RECEIVER] F3 received correctly, buffered
[SENDER] ACK3 received, window slides to next frame

[SENDER] sending F4 (attempt 1), starting timer 0.3s
[RECEIVER] F4 received correctly, buffered
  [CHANNEL] ACK4 LOST in transit
[SENDER] timeout waiting for ACK4 -> retransmit
[SENDER] sending F4 (attempt 2), starting timer 0.3s
[RECEIVER] duplicate F4 discarded, resending ACK4
[SENDER] ACK4 received, window slides to next frame

[SENDER] sending F5 (attempt 1), starting timer 0.3s
[RECEIVER] F5 received correctly, buffered
[SENDER] ACK5 received, window slides to next frame

[SENDER] sending F6 (attempt 1), starting timer 0.3s
[RECEIVER] F6 received correctly, buffered
[SENDER] ACK6 received, window slides to next frame

[SENDER] sending F7 (attempt 1), starting timer 0.3s
[RECEIVER] F7 received correctly, buffered
[SENDER] ACK7 received, window slides to next frame

[STATS] frames to deliver: 8 | total transmissions: 10 | retransmits: 2
[RESULT] all frames delivered exactly once, in order: True
```

### Stop-and-Wait, Scenario B
```
=== Scenario B: noisy channel, frames F1,F5 lost once, ACK3,ACK6 lost once ===

[SENDER] sending F0 (attempt 1), starting timer 0.3s
[RECEIVER] F0 received correctly, buffered
[SENDER] ACK0 received, window slides to next frame

[SENDER] sending F1 (attempt 1), starting timer 0.3s
  [CHANNEL] frame F1 LOST in transit
[SENDER] timeout waiting for ACK1 -> retransmit
[SENDER] sending F1 (attempt 2), starting timer 0.3s
[RECEIVER] F1 received correctly, buffered
[SENDER] ACK1 received, window slides to next frame

[SENDER] sending F2 (attempt 1), starting timer 0.3s
[RECEIVER] F2 received correctly, buffered
[SENDER] ACK2 received, window slides to next frame

[SENDER] sending F3 (attempt 1), starting timer 0.3s
[RECEIVER] F3 received correctly, buffered
  [CHANNEL] ACK3 LOST in transit
[SENDER] timeout waiting for ACK3 -> retransmit
[SENDER] sending F3 (attempt 2), starting timer 0.3s
[RECEIVER] duplicate F3 discarded, resending ACK3
[SENDER] ACK3 received, window slides to next frame

[SENDER] sending F4 (attempt 1), starting timer 0.3s
[RECEIVER] F4 received correctly, buffered
[SENDER] ACK4 received, window slides to next frame

[SENDER] sending F5 (attempt 1), starting timer 0.3s
  [CHANNEL] frame F5 LOST in transit
[SENDER] timeout waiting for ACK5 -> retransmit
[SENDER] sending F5 (attempt 2), starting timer 0.3s
[RECEIVER] F5 received correctly, buffered
[SENDER] ACK5 received, window slides to next frame

[SENDER] sending F6 (attempt 1), starting timer 0.3s
[RECEIVER] F6 received correctly, buffered
  [CHANNEL] ACK6 LOST in transit
[SENDER] timeout waiting for ACK6 -> retransmit
[SENDER] sending F6 (attempt 2), starting timer 0.3s
[RECEIVER] duplicate F6 discarded, resending ACK6
[SENDER] ACK6 received, window slides to next frame

[SENDER] sending F7 (attempt 1), starting timer 0.3s
[RECEIVER] F7 received correctly, buffered
[SENDER] ACK7 received, window slides to next frame

[STATS] frames to deliver: 8 | total transmissions: 12 | retransmits: 4
[RESULT] all frames delivered exactly once, in order: True
```

### Go-Back-N, Scenario A
```
=== Scenario A: window=4, single loss at F3 ===

[SENDER] send F0, window=[0..3]
[SENDER] send F1, window=[0..3]
[SENDER] send F2, window=[0..3]
[SENDER] send F3, window=[0..3] (will be lost)
[RECEIVER] F0 accepted in order, ACK0 sent
[RECEIVER] F1 accepted in order, ACK1 sent
[RECEIVER] F2 accepted in order, ACK2 sent
  [CHANNEL] F3 LOST -> receiver discards F3 and everything after it this round
[SENDER] timeout on ACK3 -> Go-Back-N: resending from F3

[SENDER] send F3, window=[3..6]
[SENDER] send F4, window=[3..6]
[SENDER] send F5, window=[3..6]
[SENDER] send F6, window=[3..6]
[RECEIVER] F3 accepted in order, ACK3 sent
[RECEIVER] F4 accepted in order, ACK4 sent
[RECEIVER] F5 accepted in order, ACK5 sent
[RECEIVER] F6 accepted in order, ACK6 sent
[SENDER] window slides, base is now 7

[SENDER] send F7, window=[7..10]
[SENDER] send F8, window=[7..10]
[SENDER] send F9, window=[7..10]
[SENDER] send F10, window=[7..10]
[RECEIVER] F7 accepted in order, ACK7 sent
[RECEIVER] F8 accepted in order, ACK8 sent
[RECEIVER] F9 accepted in order, ACK9 sent
[RECEIVER] F10 accepted in order, ACK10 sent
[SENDER] window slides, base is now 11

[SENDER] send F11, window=[11..11]
[RECEIVER] F11 accepted in order, ACK11 sent
[SENDER] window slides, base is now 12

[STATS] window=4 | frames to deliver: 12 | total frame-sends: 13 | Go-Back-N rounds: 1
[RESULT] frames delivered in order: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
[RESULT] correct and complete: True
```

### Go-Back-N, Scenario B
```
=== Scenario B: window=3, two losses at F2 and F8 ===

[SENDER] send F0, window=[0..2]
[SENDER] send F1, window=[0..2]
[SENDER] send F2, window=[0..2] (will be lost)
[RECEIVER] F0 accepted in order, ACK0 sent
[RECEIVER] F1 accepted in order, ACK1 sent
  [CHANNEL] F2 LOST -> receiver discards F2 and everything after it this round
[SENDER] timeout on ACK2 -> Go-Back-N: resending from F2

[SENDER] send F2, window=[2..4]
[SENDER] send F3, window=[2..4]
[SENDER] send F4, window=[2..4]
[RECEIVER] F2 accepted in order, ACK2 sent
[RECEIVER] F3 accepted in order, ACK3 sent
[RECEIVER] F4 accepted in order, ACK4 sent
[SENDER] window slides, base is now 5

[SENDER] send F5, window=[5..7]
[SENDER] send F6, window=[5..7]
[SENDER] send F7, window=[5..7]
[RECEIVER] F5 accepted in order, ACK5 sent
[RECEIVER] F6 accepted in order, ACK6 sent
[RECEIVER] F7 accepted in order, ACK7 sent
[SENDER] window slides, base is now 8

[SENDER] send F8, window=[8..10] (will be lost)
[SENDER] send F9, window=[8..10]
[SENDER] send F10, window=[8..10]
  [CHANNEL] F8 LOST -> receiver discards F8 and everything after it this round
[SENDER] timeout on ACK8 -> Go-Back-N: resending from F8

[SENDER] send F8, window=[8..10]
[SENDER] send F9, window=[8..10]
[SENDER] send F10, window=[8..10]
[RECEIVER] F8 accepted in order, ACK8 sent
[RECEIVER] F9 accepted in order, ACK9 sent
[RECEIVER] F10 accepted in order, ACK10 sent
[SENDER] window slides, base is now 11

[SENDER] send F11, window=[11..11]
[RECEIVER] F11 accepted in order, ACK11 sent
[SENDER] window slides, base is now 12

[STATS] window=3 | frames to deliver: 12 | total frame-sends: 16 | Go-Back-N rounds: 2
[RESULT] frames delivered in order: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
[RESULT] correct and complete: True
```


## Viva Questions

1. **What is flow control?**
   It stops a fast sender from overwhelming a slow receiver, by making the sender wait for permission (ACKs) before sending more.
2. **How does Stop-and-Wait work?**
   Send one frame, start a timer, wait for its ACK. If the timer expires, send the same frame again.
3. **How does the receiver detect a duplicate frame?**
   By its sequence number. If an ACK was lost, the sender resends a frame the receiver already has; the receiver discards it and resends the ACK.
4. **Efficiency of Stop-and-Wait?**
   η = 1 / (1 + 2a), where a = propagation time / transmission time. It is poor on long or fast links.
5. **How does Go-Back-N work?**
   The sender can have up to W unacknowledged frames. If frame i is lost, the receiver discards everything after it and the sender resends from frame i.
6. **Go-Back-N vs Selective Repeat?**
   Go-Back-N resends the lost frame and all frames after it (receiver window 1). Selective Repeat resends only the lost frame; the receiver buffers out-of-order frames.
7. **Maximum window size with m-bit sequence numbers?**
   Go-Back-N: 2^m − 1. Selective Repeat: 2^(m−1).
8. **Why did Go-Back-N Scenario B need more frame-sends?**
   Two losses mean two Go-Back-N rounds, and each round resends the frames after the lost one: 16 sends for 12 frames, against 13 with one loss.
