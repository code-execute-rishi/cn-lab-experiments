# Lab 13: OSPF Link-State Routing

## Question
**Aim:** To design, simulate, and verify a Link-State Routing Protocol based on OSPF (RFC 2328) in Python, simulating LSA flooding, synchronized Link-State Database (LSDB) construction, Dijkstra SPF computation, and dynamic path rerouting.

## Files
- [`ospf_link_state.py`](ospf_link_state.py): LSA flooding, the LSDB, Dijkstra shortest paths and rerouting after a link cost change.

## Logic (How the Program Works)

```text
ospf_link_state.py
1. Each router knows only its own links (neighbour -> cost).
2. originate_lsa(): the router makes a Link-State Advertisement with a new sequence number listing its links.
3. synchronize_lsdb() (flooding): every router's LSA is installed in every router (newer sequence numbers replace older ones), so all routers have the same Link-State Database, i.e. the same map.
4. run_dijkstra_spf(): Dijkstra from this router.
   - distance to itself 0, all others infinity; use a min-heap;
   - take the closest unvisited router, and for each of its links: if going through it is shorter, update the distance and remember the parent.
5. For each destination, follow the parents back to get the full path; the first router after the source is the next hop.
6. Phase 1: 6 routers (R1-R6); print the forwarding tables of R1 and R3.
7. Phase 2: the R1-R2 cost changes from 10 to 70. New LSAs are flooded and Dijkstra runs again, so R1 now routes through R3.
```

## How to Run
No input is needed; the test data is built into each program.
```bash
python3 ospf_link_state.py
```

## Output

```
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


## Viva Questions

1. **What is link-state routing?**
   Every router floods information about its own links (LSAs) to all routers. Each router builds the same map of the network and computes shortest paths itself.
2. **What is an LSA?**
   A Link-State Advertisement: a message listing a router's neighbours and the cost of each link.
3. **What is the LSDB?**
   The Link-State Database: the collection of all LSAs. It is the same on every router in an area.
4. **Which algorithm does OSPF use?**
   Dijkstra's Shortest Path First (SPF) algorithm.
5. **OSPF cost metric?**
   Cost = reference bandwidth / interface bandwidth (by default 10^8 / bandwidth in bps).
6. **What is an OSPF area?**
   A group of routers that share the same LSDB. Area 0 is the backbone; areas reduce flooding in large networks.
7. **Why does OSPF converge faster than RIP?**
   Changes are flooded immediately and every router recomputes its routes itself, instead of waiting for periodic updates from neighbours.
8. **Does OSPF suffer from count-to-infinity?**
   No. Each router has the full map, so it computes loop-free shortest paths directly.
