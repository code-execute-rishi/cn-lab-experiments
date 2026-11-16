# Computer Network Lab - Experiment 12
# Student Name: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
# Implementation of Distance Vector Routing (RIP) using Bellman-Ford Algorithm
# Features: Distributed Convergence, Count-to-Infinity Simulation, Split Horizon with Poison Reverse

from typing import Dict, List, Tuple
import copy

INFINITY = 16  # RFC 1058 standard maximum metric (16 = unreachable)

class Router:
    def __init__(self, name: str):
        self.name = name
        # Routing table: dest -> {"metric": int, "next_hop": str}
        self.table: Dict[str, Dict] = {name: {"metric": 0, "next_hop": name}}
        # Physical links to immediate neighbors: neighbor_name -> cost
        self.neighbors: Dict[str, int] = {}

    def add_link(self, neighbor: str, cost: int):
        self.neighbors[neighbor] = cost
        self.table[neighbor] = {"metric": cost, "next_hop": neighbor}

    def update_link_cost(self, neighbor: str, new_cost: int):
        self.neighbors[neighbor] = new_cost
        if self.table.get(neighbor, {}).get("next_hop") == neighbor:
            self.table[neighbor]["metric"] = min(new_cost, INFINITY)

    def sever_link(self, neighbor: str):
        if neighbor in self.neighbors:
            self.neighbors[neighbor] = INFINITY
            # Poison all routes passing through this neighbor
            for dest, entry in self.table.items():
                if entry["next_hop"] == neighbor:
                    entry["metric"] = INFINITY

    def generate_advertisement(self, neighbor: str, split_horizon: bool = True, poison_reverse: bool = True) -> Dict[str, int]:
        """
        Builds the distance vector to advertise to a specific neighbor.
        - Split Horizon: Omit destinations where next_hop == neighbor.
        - Poison Reverse: Advertise metric 16 for destinations where next_hop == neighbor.
        """
        ad = {}
        for dest, entry in self.table.items():
            metric = entry["metric"]
            if entry["next_hop"] == neighbor and dest != self.name:
                if poison_reverse:
                    ad[dest] = INFINITY
                elif split_horizon:
                    continue  # suppress route entirely
                else:
                    ad[dest] = metric
            else:
                ad[dest] = metric
        return ad

    def receive_advertisement(self, from_neighbor: str, vector: Dict[str, int]) -> bool:
        """
        Applies Bellman-Ford update:
        D_x(y) = min_v { c(x,v) + D_v(y) }
        Returns True if any table entry was updated.
        """
        link_cost = self.neighbors.get(from_neighbor, INFINITY)
        table_changed = False

        for dest, adv_metric in vector.items():
            if dest == self.name:
                continue

            new_metric = min(link_cost + adv_metric, INFINITY)
            current_entry = self.table.get(dest)

            if current_entry is None:
                if new_metric < INFINITY:
                    self.table[dest] = {"metric": new_metric, "next_hop": from_neighbor}
                    table_changed = True
            else:
                # If advertisement comes from current next-hop, accept it unconditionally (even if it increased)
                if current_entry["next_hop"] == from_neighbor:
                    if current_entry["metric"] != new_metric:
                        current_entry["metric"] = new_metric
                        table_changed = True
                # If advertisement offers a strictly better path through an alternative neighbor
                elif new_metric < current_entry["metric"]:
                    current_entry["metric"] = new_metric
                    current_entry["next_hop"] = from_neighbor
                    table_changed = True

        return table_changed


class RIPNetwork:
    def __init__(self, split_horizon: bool = True, poison_reverse: bool = True):
        self.routers: Dict[str, Router] = {}
        self.split_horizon = split_horizon
        self.poison_reverse = poison_reverse

    def add_router(self, name: str) -> Router:
        r = Router(name)
        self.routers[name] = r
        return r

    def add_bidirectional_link(self, u: str, v: str, cost: int):
        self.routers[u].add_link(v, cost)
        self.routers[v].add_link(u, cost)

    def converge(self, max_rounds: int = 25) -> int:
        """Runs iterative rounds of distributed distance vector exchanges until stable."""
        for round_num in range(1, max_rounds + 1):
            any_change = False
            # Generate all advertisements in parallel
            pending_ads: List[Tuple[str, str, Dict[str, int]]] = []
            for src_name, router in self.routers.items():
                for nbr_name in router.neighbors:
                    ad = router.generate_advertisement(nbr_name, self.split_horizon, self.poison_reverse)
                    pending_ads.append((src_name, nbr_name, ad))

            # Deliver advertisements and trigger Bellman-Ford relaxation
            for src_name, dst_name, vector in pending_ads:
                changed = self.routers[dst_name].receive_advertisement(src_name, vector)
                if changed:
                    any_change = True

            if not any_change:
                return round_num
        return max_rounds

    def dump_routing_tables(self):
        for name in sorted(self.routers.keys()):
            r = self.routers[name]
            print(f"Router {name} Routing Table:")
            print(f"  {'Destination':<15}{'Cost (Hops)':<15}{'Next Hop':<15}")
            print(f"  {'-'*40}")
            for dest in sorted(r.table.keys()):
                entry = r.table[dest]
                metric_str = str(entry['metric']) if entry['metric'] < INFINITY else "16 (Unreachable)"
                print(f"  {dest:<15}{metric_str:<15}{entry['next_hop']:<15}")
            print()

def run_rip_demonstration():
    print("=" * 78)
    print("COMPUTER NETWORKS LAB - EXPERIMENT 12: DISTANCE VECTOR ROUTING (RIP)")
    print("Student: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1")
    print("=" * 78)

    # 1. Standard Topology Convergence
    print("[PHASE 1: 5-ROUTER MESH CONVERGENCE TESTBENCH]")
    net = RIPNetwork(split_horizon=True, poison_reverse=True)
    for node in ["A", "B", "C", "D", "E"]:
        net.add_router(node)
    
    # Links: A-B(1), B-C(1), C-D(1), D-E(1), A-C(3), B-D(4)
    net.add_bidirectional_link("A", "B", 1)
    net.add_bidirectional_link("B", "C", 1)
    net.add_bidirectional_link("C", "D", 1)
    net.add_bidirectional_link("D", "E", 1)
    net.add_bidirectional_link("A", "C", 3)
    net.add_bidirectional_link("B", "D", 4)

    rounds = net.converge()
    print(f">> Initial network converged successfully in {rounds} rounds.")
    net.dump_routing_tables()

    # 2. Count-to-Infinity vs Poison Reverse comparison
    print("-" * 78)
    print("[PHASE 2: LINK FAILURE & COUNT-TO-INFINITY HAZARD EVALUATION]")
    print("Scenario: Severing link A <---> B. Destination B unreachable from A directly.")
    
    # Test WITHOUT Split Horizon
    net_naive = RIPNetwork(split_horizon=False, poison_reverse=False)
    for node in ["A", "B", "C"]:
        net_naive.add_router(node)
    net_naive.add_bidirectional_link("A", "B", 1)
    net_naive.add_bidirectional_link("B", "C", 1)
    net_naive.converge()
    
    print("\nSimulating failure without Split Horizon (Count-to-Infinity):")
    net_naive.routers["A"].sever_link("B")
    net_naive.routers["B"].sever_link("A")
    rounds_inf = net_naive.converge(max_rounds=20)
    print(f">> Bounced routing vectors. Convergence took {rounds_inf} rounds to count to 16.")

    # Test WITH Split Horizon & Poison Reverse
    net_pr = RIPNetwork(split_horizon=True, poison_reverse=True)
    for node in ["A", "B", "C"]:
        net_pr.add_router(node)
    net_pr.add_bidirectional_link("A", "B", 1)
    net_pr.add_bidirectional_link("B", "C", 1)
    net_pr.converge()

    print("\nSimulating failure WITH Split Horizon & Poisoned Reverse:")
    net_pr.routers["A"].sever_link("B")
    net_pr.routers["B"].sever_link("A")
    rounds_pr = net_pr.converge(max_rounds=20)
    print(f">> Immediate loop suppression! Converged cleanly in {rounds_pr} rounds.")
    print("=" * 78)

if __name__ == "__main__":
    run_rip_demonstration()
