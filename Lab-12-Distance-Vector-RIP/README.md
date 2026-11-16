# Lab 12: Distance Vector Routing Protocol (RIP)

## Question
**Aim:** To implement, simulate, and verify the distributed Bellman-Ford Distance Vector Routing Protocol (RIP - RFC 1058), analyze the Count-to-Infinity hazard during link failure, and implement Split Horizon with Poisoned Reverse.

## Files
- [`rip_distance_vector.py`](rip_distance_vector.py): Bellman-Ford distance vector routing on 5 routers, count-to-infinity, and split horizon with poisoned reverse.

## How to Run
No input is needed; the test data is built into each program.
```bash
python3 rip_distance_vector.py
```

## Output

```
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


## Viva Questions

1. **What is distance vector routing?**
   Each router sends its whole routing table (distances to every destination) to its neighbours, and updates its own using the Bellman-Ford equation.
2. **Bellman-Ford equation?**
   Dx(y) = min over neighbours v of { c(x,v) + Dv(y) }.
3. **What metric does RIP use?**
   Hop count. The maximum is 15; 16 means unreachable (infinity).
4. **What is the count-to-infinity problem?**
   After a link fails, routers keep learning wrong routes from each other and slowly raise the cost until it reaches 16.
5. **What is split horizon?**
   A router does not advertise a route back to the neighbour it learned that route from.
6. **What is poisoned reverse?**
   The router does advertise the route back to that neighbour, but with cost 16 (infinity), so the neighbour will not use it.
7. **How often does RIP send updates?**
   Every 30 seconds, over UDP port 520.
8. **Distance vector vs link state?**
   Distance vector shares routing tables with neighbours only (simple, slow to converge). Link state floods link information to all routers, and each runs Dijkstra (fast, uses more memory).
