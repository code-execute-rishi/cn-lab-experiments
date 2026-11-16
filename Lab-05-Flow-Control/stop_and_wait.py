# Lab 5: Flow control - Stop-and-Wait ARQ
# Run: python3 stop_and_wait.py 1   (Scenario A)
#      python3 stop_and_wait.py 2   (Scenario B)
import sys

FRAMES = [f"F{i}" for i in range(8)]
TIMEOUT = 0.3

# scenario: (title, frames lost once, ACKs lost once)
SCENARIOS = {
    "1": ("Scenario A: clean-ish channel, frame F2 lost once, ACK4 lost once", {2}, {4}),
    "2": ("Scenario B: noisy channel, frames F1,F5 lost once, ACK3,ACK6 lost once", {1, 5}, {3, 6}),
}
title, LOST_FRAMES, LOST_ACKS = SCENARIOS[sys.argv[1] if len(sys.argv) > 1 else "1"]


def channel_send_frame(i, attempt):
    # the channel drops a frame only the first time it is sent
    if i in LOST_FRAMES and attempt == 1:
        print(f"  [CHANNEL] frame {FRAMES[i]} LOST in transit")
        print(f"[SENDER] timeout waiting for ACK{i} -> retransmit")
        return False
    return True


def receiver_get(i, seen):
    if i in seen:
        print(f"[RECEIVER] duplicate {FRAMES[i]} discarded, resending ACK{i}")
    else:
        seen.append(i)
        print(f"[RECEIVER] {FRAMES[i]} received correctly, buffered")


def channel_send_ack(i, attempt):
    if i in LOST_ACKS and attempt == 1:
        print(f"  [CHANNEL] ACK{i} LOST in transit")
        print(f"[SENDER] timeout waiting for ACK{i} -> retransmit")
        return False
    return True


print(f"=== {title} ===")
seen = []
transmissions = 0
for i in range(len(FRAMES)):
    print()
    attempt = 1
    while True:
        print(f"[SENDER] sending {FRAMES[i]} (attempt {attempt}), starting timer {TIMEOUT}s")
        transmissions += 1
        if not channel_send_frame(i, attempt):      # frame lost
            attempt += 1; continue                  # timeout -> resend
        receiver_get(i, seen)                       # receiver buffers / dedupes
        if not channel_send_ack(i, attempt):        # ack lost
            attempt += 1; continue                  # timeout -> resend
        break                                       # ACK received, slide to next frame
    print(f"[SENDER] ACK{i} received, window slides to next frame")

print()
print(f"[STATS] frames to deliver: {len(FRAMES)} | total transmissions: {transmissions} | retransmits: {transmissions - len(FRAMES)}")
print(f"[RESULT] all frames delivered exactly once, in order: {seen == list(range(len(FRAMES)))}")
