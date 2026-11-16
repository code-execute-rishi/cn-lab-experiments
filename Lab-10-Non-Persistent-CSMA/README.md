# Lab 10: Non-Persistent CSMA Protocol

## Question
**Aim:** To implement, simulate, and verify the Non-Persistent CSMA protocol in Python, modeling carrier sensing, random backoff upon busy detection, collision tracking within propagation window tau, and throughput across varying offered loads.

## Files
- [`csma_non_persistent.py`](csma_non_persistent.py): Non-Persistent CSMA simulation: throughput, collisions and delay across offered loads.

## How to Run
No input is needed; the test data is built into each program.
```bash
python3 csma_non_persistent.py
```

## Output

```
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


## Viva Questions

1. **What is CSMA?**
   Carrier Sense Multiple Access: a station listens to the channel and transmits only when it is idle.
2. **What does non-persistent mean?**
   If the channel is busy, the station does not keep listening; it waits a random time and senses again.
3. **1-persistent vs non-persistent vs p-persistent?**
   1-persistent sends as soon as the channel becomes idle. Non-persistent waits a random time when busy. p-persistent sends with probability p when idle.
4. **Why can collisions still happen in CSMA?**
   Because of propagation delay: two stations can sense the channel as idle at almost the same time and both transmit.
5. **What is the vulnerable period?**
   The propagation delay τ: a station that starts within τ of another one will not yet hear it.
6. **What is parameter a?**
   a = τ / T_frame (propagation delay / transmission time). The smaller a is, the better CSMA works.
7. **Offered load G vs throughput S?**
   G is the number of transmission attempts per frame time. S is the fraction of time spent carrying successful frames.
8. **Why does non-persistent CSMA keep throughput high under heavy load?**
   The random waiting spreads stations out, so fewer of them jump in together when the channel frees up.
