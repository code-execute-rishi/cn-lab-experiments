# Computer Network Lab - Experiment 6
# Student Name: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
# Stop-and-Wait ARQ Simulation with Frame/ACK Loss and Duplicate Handling

class SimulatedChannel:
    def __init__(self):
        self.scenario = "NORMAL"
        self.receiver = None

    def transmit_frame(self, seq_num, data, attempt):
        if self.scenario == "CORRUPT_FRAME" and attempt == 1:
            print("  [CHANNEL] Noise burst injected on channel! Checksum inverted.")
            return self.receiver.receive_frame(seq_num, data, is_corrupted=True)
        elif self.scenario == "LOST_ACK" and attempt == 1:
            self.receiver.receive_frame(seq_num, data, is_corrupted=False)
            print("  [CHANNEL] *** ACK dropped by physical interface! ***")
            return None  # ACK lost
        return self.receiver.receive_frame(seq_num, data, is_corrupted=False)

class StopAndWaitSender:
    def __init__(self, channel):
        self.channel = channel
        self.seq_num = 0
        self.total_tx = 0
        self.retransmissions = 0

    def send_frame(self, msg, scenario="NORMAL"):
        self.channel.scenario = scenario
        attempt = 1
        while True:
            self.total_tx += 1
            if attempt > 1:
                self.retransmissions += 1
            print(f"[SENDER] Transmitting Frame(seq={self.seq_num}, data='{msg}', attempt={attempt})")
            ack = self.channel.transmit_frame(self.seq_num, msg, attempt)
            if ack is not None and ack == (1 - self.seq_num):
                print(f"[SENDER] Received valid ACK({ack}). Sliding sequence bit to {ack}.\n")
                self.seq_num = ack
                break
            else:
                reason = "Timeout (No ACK / ACK lost)" if ack is None else f"Unexpected ACK({ack})"
                print(f"[SENDER] !! {reason}. Retransmitting Frame(seq={self.seq_num})...")
                attempt += 1

class StopAndWaitReceiver:
    def __init__(self):
        self.expected_seq = 0
        self.received_data = []

    def receive_frame(self, seq_num, data, is_corrupted=False):
        if is_corrupted:
            print(f"  [RECEIVER] Checksum mismatch! Corrupted Frame(seq={seq_num}) discarded.")
            return None
        if seq_num == self.expected_seq:
            print(f"  [RECEIVER] In-order Frame(seq={seq_num}, data='{data}') accepted.")
            self.received_data.append(data)
            self.expected_seq = 1 - self.expected_seq
            print(f"  [RECEIVER] Sending ACK({self.expected_seq})")
            return self.expected_seq
        else:
            print(f"  [RECEIVER] Duplicate Frame(seq={seq_num}) detected! Discarding payload.")
            print(f"  [RECEIVER] Resending ACK({self.expected_seq})")
            return self.expected_seq

if __name__ == "__main__":
    channel = SimulatedChannel()
    receiver = StopAndWaitReceiver()
    channel.receiver = receiver
    sender = StopAndWaitSender(channel)

    print("[SCENARIO 1: NORMAL ERROR-FREE TRANSMISSION]")
    sender.send_frame("DATA_PKT_0", "NORMAL")

    print("[SCENARIO 2: FRAME 1 CORRUPTED IN TRANSIT]")
    sender.send_frame("DATA_PKT_1", "CORRUPT_FRAME")

    print("[SCENARIO 3: ACK 1 LOST IN TRANSIT -> DUPLICATE DETECTION]")
    sender.send_frame("DATA_PKT_2", "LOST_ACK")

    print(f"Delivered all {len(receiver.received_data)} packets without duplication. Total Transmissions: {sender.total_tx}, Retransmissions: {sender.retransmissions}.")
