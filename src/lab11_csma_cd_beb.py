# Computer Network Lab - Experiment 11
# Student Name: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
# Implementation of 1-Persistent and p-Persistent CSMA/CD with Truncated Binary Exponential Backoff

import random
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Frame:
    frame_id: int
    station_id: int
    arrival_slot: int
    size_bytes: int = 64  # Min Ethernet frame size (512 bits)
    collisions: int = 0
    backoff_slots_remaining: int = 0
    state: str = "WAITING"  # WAITING, SENSING, TRANSMITTING, COLLIDED, DELIVERED, DROPPED

class CSMACDNetwork:
    """
    Simulates IEEE 802.3 CSMA/CD (Carrier Sense Multiple Access with Collision Detection).
    Features:
      - 1-Persistent: Transmit with probability 1.0 when channel is idle.
      - p-Persistent: Transmit with probability p when idle; defer 1 slot with (1-p).
      - Collision Detection: Senses channel while transmitting. Upon collision,
        aborts immediately and transmits 32-bit Jamming Signal.
      - Truncated Binary Exponential Backoff (BEB):
          k = min(n_collisions, 10)
          r in Uniform(0, 2^k - 1)
          Max retries = 16 (frame dropped thereafter).
    """
    def __init__(self, num_stations: int = 8, persistence_mode: str = "1-PERSISTENT",
                 p_prob: float = 0.5, slot_time_us: float = 51.2, max_retries: int = 16, seed: int = 42):
        self.num_stations = num_stations
        self.persistence_mode = persistence_mode
        self.p_prob = p_prob
        self.slot_time_us = slot_time_us  # 51.2 us for 10 Mbps Ethernet (512 bits)
        self.max_retries = max_retries
        self.rng = random.Random(seed)

    def simulate(self, total_slots: int = 500, arrival_prob_per_station: float = 0.05) -> Dict:
        """
        Executes slotted CSMA/CD channel simulation.
        """
        station_queues: Dict[int, List[Frame]] = {i: [] for i in range(self.num_stations)}
        frame_counter = 0

        # Metrics
        frames_generated = 0
        frames_delivered = 0
        frames_dropped = 0
        collision_events = 0
        jam_slots_spent = 0
        idle_slots = 0
        busy_slots = 0
        total_delay_slots = 0

        # Channel state: (busy_until_slot, status, active_transmitters)
        channel_busy_until = 0
        transmitting_frames: List[Frame] = []
        frame_duration_slots = 2  # Frame takes 2 slots; collision detected in slot 1

        for slot in range(total_slots):
            # 1. Packet arrivals at stations
            for s in range(self.num_stations):
                if self.rng.random() < arrival_prob_per_station:
                    frame_counter += 1
                    frames_generated += 1
                    f = Frame(frame_id=frame_counter, station_id=s, arrival_slot=slot)
                    station_queues[s].append(f)

            # 2. Check channel sensing
            channel_is_busy = (slot < channel_busy_until)
            
            # Decrement backoffs for waiting stations
            for s in range(self.num_stations):
                if station_queues[s]:
                    head = station_queues[s][0]
                    if head.backoff_slots_remaining > 0:
                        head.backoff_slots_remaining -= 1

            if channel_is_busy:
                busy_slots += 1
                continue

            # Channel is IDLE in this slot
            ready_to_transmit: List[Tuple[int, Frame]] = []
            for s in range(self.num_stations):
                if station_queues[s]:
                    head = station_queues[s][0]
                    if head.backoff_slots_remaining == 0:
                        # Apply persistence rule
                        if self.persistence_mode == "1-PERSISTENT":
                            ready_to_transmit.append((s, head))
                        else:  # p-PERSISTENT
                            if self.rng.random() <= self.p_prob:
                                ready_to_transmit.append((s, head))
                            else:
                                # Defer for 1 slot
                                head.backoff_slots_remaining = 1

            # 3. Transmission & Collision Handling
            if len(ready_to_transmit) == 0:
                idle_slots += 1
            elif len(ready_to_transmit) == 1:
                # Uncontested successful transmission
                s, f = ready_to_transmit[0]
                channel_busy_until = slot + frame_duration_slots
                station_queues[s].pop(0)
                frames_delivered += 1
                total_delay_slots += (slot + frame_duration_slots - f.arrival_slot)
            else:
                # Collision detected! CSMA/CD aborts immediately
                collision_events += 1
                # Channel is held only for collision detection + jamming signal (1 slot)
                channel_busy_until = slot + 1
                jam_slots_spent += 1
                for s, f in ready_to_transmit:
                    f.collisions += 1
                    if f.collisions >= self.max_retries:
                        station_queues[s].pop(0)
                        frames_dropped += 1
                    else:
                        # Binary Exponential Backoff: r in [0, 2^k - 1]
                        k = min(f.collisions, 10)
                        max_backoff = (2 ** k) - 1
                        f.backoff_slots_remaining = self.rng.randint(0, max_backoff)

        avg_delay = (total_delay_slots / frames_delivered) if frames_delivered > 0 else 0.0
        throughput = (frames_delivered * frame_duration_slots) / total_slots

        return {
            "mode": self.persistence_mode,
            "p": self.p_prob if self.persistence_mode == "p-PERSISTENT" else 1.0,
            "total_slots": total_slots,
            "generated": frames_generated,
            "delivered": frames_delivered,
            "dropped": frames_dropped,
            "collisions": collision_events,
            "jam_slots": jam_slots_spent,
            "idle_slots": idle_slots,
            "busy_slots": total_slots - idle_slots,
            "throughput": throughput,
            "avg_delay_slots": round(avg_delay, 2)
        }

def run_csma_cd_comparison():
    print("=" * 80)
    print("COMPUTER NETWORKS LAB - EXPERIMENT 11: CSMA/CD PERSISTENCE & BEB TESTBENCH")
    print("Student: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1")
    print("=" * 80)
    print("Parameters: 8 Stations | Slot Time: 51.2 us | Max Retries: 16 | Slots: 1000")
    print("-" * 80)
    print(f"{'Protocol Mode':<18}{'Arrival Rate':<15}{'Delivered':<12}{'Collisions':<12}{'Dropped':<10}{'Throughput':<12}{'Avg Delay'}")
    print("-" * 80)

    for rate, label in [(0.02, "Light (2%)"), (0.06, "Medium (6%)"), (0.12, "Heavy (12%)")]:
        # 1-Persistent
        net_1p = CSMACDNetwork(num_stations=8, persistence_mode="1-PERSISTENT", seed=77)
        res_1p = net_1p.simulate(total_slots=1000, arrival_prob_per_station=rate)
        print(f"{'1-Persistent':<18}{label:<15}{res_1p['delivered']:<12}{res_1p['collisions']:<12}{res_1p['dropped']:<10}{res_1p['throughput']:<12.3f}{res_1p['avg_delay_slots']} slots")

        # p-Persistent (p = 0.5)
        net_pp5 = CSMACDNetwork(num_stations=8, persistence_mode="p-PERSISTENT", p_prob=0.5, seed=77)
        res_pp5 = net_pp5.simulate(total_slots=1000, arrival_prob_per_station=rate)
        print(f"{'p-Persistent(0.5)':<18}{label:<15}{res_pp5['delivered']:<12}{res_pp5['collisions']:<12}{res_pp5['dropped']:<10}{res_pp5['throughput']:<12.3f}{res_pp5['avg_delay_slots']} slots")

        # p-Persistent (p = 0.2)
        net_pp2 = CSMACDNetwork(num_stations=8, persistence_mode="p-PERSISTENT", p_prob=0.2, seed=77)
        res_pp2 = net_pp2.simulate(total_slots=1000, arrival_prob_per_station=rate)
        print(f"{'p-Persistent(0.2)':<18}{label:<15}{res_pp2['delivered']:<12}{res_pp2['collisions']:<12}{res_pp2['dropped']:<10}{res_pp2['throughput']:<12.3f}{res_pp2['avg_delay_slots']} slots")
        print("-" * 80)

if __name__ == "__main__":
    run_csma_cd_comparison()
