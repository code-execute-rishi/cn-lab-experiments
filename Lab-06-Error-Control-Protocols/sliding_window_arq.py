# Computer Network Lab - Experiment 6
# Student Name: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
# Sliding Window ARQ: Go-Back-N vs. Selective-Repeat Comparison

class GoBackN:
    def __init__(self, window_size=4, total_frames=8):
        self.W = window_size
        self.total_frames = total_frames
        self.base = 0
        self.next_seq = 0
        self.tx_count = 0

    def run_simulation(self, drop_frame_once=2):
        print(f"=== RUNNING GO-BACK-N (W = {self.W}, Total = {self.total_frames} Frames, Drop F{drop_frame_once}) ===")
        dropped = False
        receiver_expected = 0

        while self.base < self.total_frames:
            while self.next_seq < self.base + self.W and self.next_seq < self.total_frames:
                self.tx_count += 1
                print(f"[SENDER] Sent Frame F{self.next_seq}")
                self.next_seq += 1

            i = self.base
            timeout_seq = None
            while i < self.next_seq:
                if i == drop_frame_once and not dropped:
                    print(f"  [CHANNEL] *** Frame F{i} LOST IN TRANSIT! ***")
                    dropped = True
                    timeout_seq = i
                    break
                elif i == receiver_expected:
                    print(f"  [RECEIVER] In-order Frame F{i} accepted -> Sending cumulative ACK{i + 1}")
                    receiver_expected += 1
                    i += 1
                else:
                    print(f"  [RECEIVER] Out-of-order Frame F{i} discarded! Resending ACK{receiver_expected}")
                    i += 1

            if timeout_seq is not None:
                print(f"[SENDER] !! TIMEOUT for Frame F{timeout_seq}! Go-Back-N triggered.")
                print(f"[SENDER] Resending entire window from base F{timeout_seq} (F{timeout_seq} to F{self.next_seq - 1})")
                self.base = timeout_seq
                self.next_seq = timeout_seq
            else:
                self.base = receiver_expected
        print(f"GBN Result: Delivered {self.total_frames} frames in {self.tx_count} total transmissions ({self.tx_count - self.total_frames} retransmissions).\n")

class SelectiveRepeat:
    def __init__(self, window_size=4, total_frames=8):
        self.W = window_size
        self.total_frames = total_frames
        self.sender_base = 0
        self.receiver_base = 0
        self.tx_count = 0
        self.acked = [False] * total_frames
        self.recv_buffer = {}

    def run_simulation(self, drop_frame_once=2):
        print(f"=== RUNNING SELECTIVE-REPEAT (W_S = {self.W}, W_R = {self.W}, Total = {self.total_frames} Frames, Drop F{drop_frame_once}) ===")
        dropped = False

        while self.sender_base < self.total_frames:
            for seq in range(self.sender_base, min(self.sender_base + self.W, self.total_frames)):
                if not self.acked[seq]:
                    self.tx_count += 1
                    print(f"[SENDER] Transmitted Frame F{seq}")
                    if seq == drop_frame_once and not dropped:
                        print(f"  [CHANNEL] *** Frame F{seq} LOST IN TRANSIT! ***")
                        dropped = True
                    else:
                        if self.receiver_base <= seq < self.receiver_base + self.W:
                            print(f"  [RECEIVER] Frame F{seq} received and cached in receive buffer. Sent ACK({seq})")
                            self.recv_buffer[seq] = f"DATA_{seq}"
                            self.acked[seq] = True

            if not self.acked[self.sender_base]:
                print(f"[SENDER] !! Timer expired for missing base frame F{self.sender_base}!")
                print(f"[SENDER] Selective Retransmit: Resending ONLY Frame F{self.sender_base}")
                self.tx_count += 1
                self.recv_buffer[self.sender_base] = f"DATA_{self.sender_base}"
                self.acked[self.sender_base] = True
                print(f"  [RECEIVER] Retransmitted F{self.sender_base} received! Merged buffer: delivering F{self.sender_base} and buffered frames!")

            while self.receiver_base in self.recv_buffer:
                print(f"  [RECEIVER] Delivered F{self.receiver_base} to Network Layer.")
                self.receiver_base += 1
            self.sender_base = self.receiver_base
        print(f"SR Result: Delivered {self.total_frames} frames in {self.tx_count} total transmissions (Only {self.tx_count - self.total_frames} retransmission)!\n")

if __name__ == "__main__":
    gbn = GoBackN(window_size=4, total_frames=8)
    gbn.run_simulation(drop_frame_once=2)

    sr = SelectiveRepeat(window_size=4, total_frames=8)
    sr.run_simulation(drop_frame_once=2)
