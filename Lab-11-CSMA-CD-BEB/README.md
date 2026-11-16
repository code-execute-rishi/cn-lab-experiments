# Lab 11: 1-Persistent & p-Persistent CSMA/CD with Binary Exponential Backoff

## Question
**Aim:** To design, simulate, and comparatively evaluate 1-Persistent and p-Persistent CSMA/CD incorporating real-time collision sensing, 32-bit jamming signal abortion, and the IEEE 802.3 Truncated Binary Exponential Backoff (BEB) algorithm in Python.

## Files
- [`csma_cd_protocols.py`](csma_cd_protocols.py): 1-persistent and p-persistent CSMA/CD with truncated BEB under light, medium and heavy load.

## How to Run
No input is needed; the test data is built into each program.
```bash
python3 csma_cd_protocols.py
```

## Output

```
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


## Viva Questions

1. **What is CSMA/CD?**
   CSMA with Collision Detection: a station keeps listening while it transmits and stops immediately if it detects a collision. Used by classic Ethernet.
2. **Why send a jam signal?**
   The 32-bit jam signal makes sure every station notices the collision.
3. **What is Binary Exponential Backoff?**
   After the k-th collision, wait a random number of slots between 0 and 2^k − 1. k stops growing at 10, and the frame is dropped after 16 attempts.
4. **Why is there a minimum Ethernet frame size (64 bytes)?**
   The sender must still be transmitting when a collision from the far end comes back: frame time ≥ 2 × propagation delay.
5. **1-persistent vs p-persistent?**
   1-persistent sends as soon as the channel is idle (many collisions under load). p-persistent sends with probability p, reducing collisions but adding delay.
6. **Why is CSMA/CD not used in Wi-Fi?**
   A wireless station cannot hear collisions while it transmits. Wi-Fi uses CSMA/CA (collision avoidance) instead.
7. **What is the slot time in 10 Mbps Ethernet?**
   51.2 µs, the time to send 512 bits.
8. **CSMA/CD vs CSMA/CA?**
   CD detects collisions and stops (wired Ethernet). CA tries to avoid them with random waits and RTS/CTS (wireless).
