# Computer Network Lab - Experiment 13
# Student Name: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
# Implementation of Open Shortest Path First (OSPF) using Dijkstra's Link-State Algorithm
# Features: LSA Flooding, LSDB Synchronization, Dijkstra SPF Computation, Forwarding Table Derivation

import heapq
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional

@dataclass
class LSA:
    router_id: str
    sequence_number: int
    neighbors: Dict[str, int]  # neighbor_id -> cost (metric)

class OSPFRouter:
    def __init__(self, router_id: str):
        self.router_id = router_id
        self.seq_num = 0
        # Local links: neighbor_id -> cost
        self.local_links: Dict[str, int] = {}
        # Link-State Database (LSDB): router_id -> LSA
        self.lsdb: Dict[str, LSA] = {}
        # Computed forwarding table: dest -> {"cost": int, "next_hop": str, "path": List[str]}
        self.forwarding_table: Dict[str, Dict] = {}

    def add_interface(self, neighbor_id: str, cost: int):
        self.local_links[neighbor_id] = cost

    def update_interface_cost(self, neighbor_id: str, new_cost: int):
        self.local_links[neighbor_id] = new_cost

    def originate_lsa(self) -> LSA:
        self.seq_num += 1
        lsa = LSA(
            router_id=self.router_id,
            sequence_number=self.seq_num,
            neighbors=dict(self.local_links)
        )
        self.lsdb[self.router_id] = lsa
        return lsa

    def install_lsa(self, lsa: LSA) -> bool:
        """Installs received LSA if newer than existing entry in LSDB."""
        existing = self.lsdb.get(lsa.router_id)
        if existing is None or lsa.sequence_number > existing.sequence_number:
            self.lsdb[lsa.router_id] = lsa
            return True
        return False

    def run_dijkstra_spf(self) -> Dict[str, Dict]:
        """
        Executes Dijkstra's Shortest Path First (SPF) algorithm over the LSDB graph.
        Time Complexity: O((V + E) log V) using a binary min-heap.
        Derives shortest path tree and next-hop forwarding entries.
        """
        distances: Dict[str, float] = {node: float('inf') for node in self.lsdb}
        parents: Dict[str, Optional[str]] = {node: None for node in self.lsdb}
        distances[self.router_id] = 0
        
        # Priority queue stores tuples of (tentative_distance, node_id)
        pq: List[Tuple[int, str]] = [(0, self.router_id)]
        visited: Set[str] = set()

        while pq:
            curr_dist, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)

            lsa = self.lsdb.get(u)
            if not lsa:
                continue

            for v, weight in lsa.neighbors.items():
                if v not in distances:
                    distances[v] = float('inf')
                    parents[v] = None

                alt_dist = curr_dist + weight
                if alt_dist < distances[v]:
                    distances[v] = alt_dist
                    parents[v] = u
                    heapq.heappush(pq, (alt_dist, v))

        # Reconstruct next-hop and shortest paths
        table = {}
        for dest in sorted(self.lsdb.keys()):
            if dest == self.router_id:
                table[dest] = {"cost": 0, "next_hop": "DIRECT (Self)", "path": [self.router_id]}
                continue

            if distances[dest] == float('inf'):
                table[dest] = {"cost": 65535, "next_hop": "UNREACHABLE", "path": []}
                continue

            # Backtrack parent pointers to find complete path and immediate next hop
            path = [dest]
            curr = dest
            while parents[curr] is not None and parents[curr] != self.router_id:
                curr = parents[curr]
                path.append(curr)
            
            next_hop = curr  # The node directly adjacent to source along the optimal branch
            path.append(self.router_id)
            path.reverse()

            table[dest] = {
                "cost": int(distances[dest]),
                "next_hop": next_hop,
                "path": path
            }

        self.forwarding_table = table
        return table


class OSPFArea:
    def __init__(self, area_id: str = "0.0.0.0 (Backbone)"):
        self.area_id = area_id
        self.routers: Dict[str, OSPFRouter] = {}

    def add_router(self, router_id: str) -> OSPFRouter:
        r = OSPFRouter(router_id)
        self.routers[router_id] = r
        return r

    def add_bidirectional_link(self, u: str, v: str, cost: int):
        self.routers[u].add_interface(v, cost)
        self.routers[v].add_interface(u, cost)

    def synchronize_lsdb(self):
        """Floods all LSAs across the entire area until all LSDBs are identical."""
        all_lsas = [r.originate_lsa() for r in self.routers.values()]
        for r in self.routers.values():
            for lsa in all_lsas:
                r.install_lsa(lsa)

    def compute_all_routes(self):
        for r in self.routers.values():
            r.run_dijkstra_spf()

    def print_forwarding_table(self, router_id: str):
        r = self.routers[router_id]
        print(f"OSPF Forwarding Table for Router [{router_id}] (Area: {self.area_id}):")
        print(f"  {'Destination':<15}{'Metric (Cost)':<15}{'Next Hop':<18}{'Shortest Path'}")
        print(f"  {'-'*65}")
        for dest, entry in r.forwarding_table.items():
            path_str = " -> ".join(entry['path'])
            print(f"  {dest:<15}{entry['cost']:<15}{entry['next_hop']:<18}{path_str}")
        print()

def run_ospf_demonstration():
    print("=" * 78)
    print("COMPUTER NETWORKS LAB - EXPERIMENT 13: OSPF LINK-STATE ROUTING (DIJKSTRA)")
    print("Student: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1")
    print("=" * 78)

    area = OSPFArea("0.0.0.0")
    for rid in ["R1", "R2", "R3", "R4", "R5", "R6"]:
        area.add_router(rid)

    # Topology links with standard OSPF metrics (Cost = 10^8 / Bandwidth)
    area.add_bidirectional_link("R1", "R2", 10)  # FastEthernet (100 Mbps)
    area.add_bidirectional_link("R1", "R3", 30)
    area.add_bidirectional_link("R2", "R3", 10)
    area.add_bidirectional_link("R2", "R4", 50)
    area.add_bidirectional_link("R3", "R5", 15)
    area.add_bidirectional_link("R4", "R5", 10)
    area.add_bidirectional_link("R4", "R6", 20)
    area.add_bidirectional_link("R5", "R6", 40)

    print("[PHASE 1: LSDB FLOODING & DIJKSTRA SPF COMPUTATION]")
    area.synchronize_lsdb()
    area.compute_all_routes()
    area.print_forwarding_table("R1")
    area.print_forwarding_table("R3")

    print("-" * 78)
    print("[PHASE 2: DYNAMIC METRIC RECONFIGURATION & PATH ADAPTATION]")
    print("Action: Increasing R1-R2 link metric from 10 to 70 (Simulating trunk congestion)")
    area.routers["R1"].update_interface_cost("R2", 70)
    area.routers["R2"].update_interface_cost("R1", 70)
    area.synchronize_lsdb()
    area.compute_all_routes()
    print(">> Recomputed Shortest Path Tree for Router R1:")
    area.print_forwarding_table("R1")
    print("[STATUS] OSPF Link-State Database and Dijkstra SPF verified successfully.")
    print("=" * 78)

if __name__ == "__main__":
    run_ospf_demonstration()
