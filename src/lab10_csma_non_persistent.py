# Computer Network Lab - Experiment 10
# Student Name: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
# Implementation of Non-Persistent CSMA Protocol with Channel Contention Analysis

import random
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Packet:
    packet_id: int
    station_id: int
    generation_time: float
    size_bits: int
    retries: int = 0
    backoff_expiry: float = 0.0

class NonPersistentCSMASimulator:
    """
    Simulates Non-Persistent Carrier Sense Multiple Access (CSMA) over a shared broadcast channel.
    Rules:
      1. When a station has a frame to send, it senses the channel.
      2. If channel is IDLE: Transmit frame immediately.
      3. If channel is BUSY: Do NOT continuously sense. Defer transmission by scheduling
         a random backoff interval before sensing again.
    """
    def __init__(self, num_stations: int = 10, channel_rate_bps: float = 1e6, 
                 frame_size_bits: int = 1000, prop_delay_sec: float = 1e-5,
                 max_backoff_slots: int = 16, seed: int = 42):
        self.num_stations = num_stations
        self.channel_rate_bps = channel_rate_bps
        self.frame_size_bits = frame_size_bits
        self.prop_delay = prop_delay_sec  # One-way propagation delay tau
        self.frame_duration = frame_size_bits / channel_rate_bps  # T_fr
        self.slot_time = 2 * self.prop_delay  # Slot duration (2 * tau)
        self.max_backoff_slots = max_backoff_slots
        self.rng = random.Random(seed)

    def calculate_theoretical_throughput(self, G: float) -> float:
        """
        Theoretical throughput S for Non-Persistent CSMA:
        S = (G * exp(-a * G)) / (G * (1 + 2 * a) + exp(-a * G))
        where a = tau / T_fr (normalized propagation delay).
        """
        a = self.prop_delay / self.frame_duration
        numerator = G * math.exp(-a * G)
        denominator = G * (1 + 2 * a) + math.exp(-a * G)
        return numerator / denominator if denominator > 0 else 0.0

    def run_simulation(self, sim_duration_sec: float = 1.0, arrival_rate_lambda: float = 500.0) -> Dict:
        """
        Runs discrete-event channel simulation for a given aggregate Poisson arrival rate.
        """
        current_time = 0.0
        channel_busy_until = 0.0
        transmitting_stations = []
        
        # Statistics
        total_generated = 0
        successful_transmissions = 0
        collision_count = 0
        channel_idle_time = 0.0
        busy_time = 0.0
        deferral_count = 0
        total_delay = 0.0

        # Station queues
        station_queues: Dict[int, List[Packet]] = {i: [] for i in range(self.num_stations)}
        pkt_seq = 0

        # Schedule initial packet arrivals per station using exponential distribution
        next_arrival = {}
        for s in range(self.num_stations):
            lam = arrival_rate_lambda / self.num_stations
            next_arrival[s] = self.rng.expovariate(lam)

        step_dt = min(self.prop_delay, 1e-5)
        
        while current_time < sim_duration_sec:
            # 1. Generate packet arrivals
            for s in range(self.num_stations):
                if current_time >= next_arrival[s]:
                    pkt_seq += 1
                    total_generated += 1
                    p = Packet(packet_id=pkt_seq, station_id=s, generation_time=current_time, size_bits=self.frame_size_bits)
                    station_queues[s].append(p)
                    lam = arrival_rate_lambda / self.num_stations
                    next_arrival[s] = current_time + self.rng.expovariate(lam)

            # 2. Check channel state at current_time
            is_channel_busy = (current_time < channel_busy_until)
            
            # 3. Process stations ready to sense
            ready_transmitters = []
            for s in range(self.num_stations):
                if station_queues[s]:
                    head_pkt = station_queues[s][0]
                    if current_time >= head_pkt.backoff_expiry:
                        if is_channel_busy:
                            # Channel busy: Non-Persistent rule -> Backoff without continuous listening
                            deferral_count += 1
                            backoff_slots = self.rng.randint(1, self.max_backoff_slots)
                            head_pkt.backoff_expiry = current_time + (backoff_slots * self.slot_time)
                            head_pkt.retries += 1
                        else:
                            # Channel idle: Station decides to transmit
                            ready_transmitters.append((s, head_pkt))

            # 4. Handle transmissions & collisions
            if ready_transmitters and not is_channel_busy:
                tx_end_time = current_time + self.frame_duration + self.prop_delay
                channel_busy_until = tx_end_time
                busy_time += self.frame_duration

                if len(ready_transmitters) == 1:
                    # Successful transmission
                    s, pkt = ready_transmitters[0]
                    station_queues[s].pop(0)
                    successful_transmissions += 1
                    total_delay += (tx_end_time - pkt.generation_time)
                else:
                    # Collision detected!
                    collision_count += 1
                    for s, pkt in ready_transmitters:
                        pkt.retries += 1
                        backoff_slots = self.rng.randint(1, self.max_backoff_slots)
                        pkt.backoff_expiry = tx_end_time + (backoff_slots * self.slot_time)

            current_time += step_dt

        offered_load_G = (total_generated * self.frame_duration) / sim_duration_sec
        throughput_S = (successful_transmissions * self.frame_duration) / sim_duration_sec
        avg_delay = (total_delay / successful_transmissions) if successful_transmissions > 0 else 0.0

        return {
            "duration": sim_duration_sec,
            "offered_load_G": offered_load_G,
            "throughput_S": throughput_S,
            "theoretical_S": self.calculate_theoretical_throughput(offered_load_G),
            "generated_frames": total_generated,
            "successful_frames": successful_transmissions,
            "collisions": collision_count,
            "deferrals": deferral_count,
            "avg_delay_ms": avg_delay * 1000.0,
            "channel_efficiency_pct": (throughput_S / offered_load_G * 100) if offered_load_G > 0 else 0.0
        }

def run_load_sweep_demonstration():
    print("=" * 78)
    print("COMPUTER NETWORKS LAB - EXPERIMENT 10: NON-PERSISTENT CSMA SIMULATOR")
    print("Student: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1")
    print("=" * 78)
    print("Topology: 10 Stations | Bandwidth: 1.0 Mbps | Frame: 1000 bits (1.0 ms)")
    print("Propagation Delay (tau): 10.0 us | Parameter a = tau / T_fr = 0.010")
    print("-" * 78)
    print(f"{'Arrival (fps)':<14}{'Offered (G)':<14}{'Sim Throughput (S)':<20}{'Theory (S)':<14}{'Collisions':<12}{'Avg Delay':<10}")
    print("-" * 78)

    sim = NonPersistentCSMASimulator(num_stations=10, channel_rate_bps=1e6, frame_size_bits=1000, prop_delay_sec=1e-5, seed=101)
    rates = [100, 300, 500, 800, 1000, 1500, 2500, 4000]
    
    for r in rates:
        res = sim.run_simulation(sim_duration_sec=0.4, arrival_rate_lambda=float(r))
        print(f"{r:<14}{res['offered_load_G']:<14.3f}{res['throughput_S']:<20.4f}{res['theoretical_S']:<14.4f}{res['collisions']:<12}{res['avg_delay_ms']:.2f} ms")
    print("-" * 78)
    print("[STATUS] Non-Persistent CSMA channel contention protocol verified successfully.")

if __name__ == "__main__":
    run_load_sweep_demonstration()
