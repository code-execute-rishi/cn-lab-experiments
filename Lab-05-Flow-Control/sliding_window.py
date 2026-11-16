# Lab 5: Flow control - Sliding Window (Go-Back-N)
# Run: python3 sliding_window.py 1   (Scenario A)
#      python3 sliding_window.py 2   (Scenario B)
import sys

N_FRAMES = 12

# scenario: (title, window size, frames lost the first time they are sent)
SCENARIOS = {
    "1": ("Scenario A: window=4, single loss at F3", 4, {3}),
    "2": ("Scenario B: window=3, two losses at F2 and F8", 3, {2, 8}),
}
title, WINDOW, LOSSES = SCENARIOS[sys.argv[1] if len(sys.argv) > 1 else "1"]

sends = 0
rounds = 0
delivered = []


def lost(i):
    return i in LOSSES


def send(i, base):
    global sends
    sends += 1
    last = min(base + WINDOW, N_FRAMES) - 1
    note = " (will be lost)" if lost(i) else ""
    print(f"[SENDER] send F{i}, window=[{base}..{last}]{note}")


def accept(i):
    delivered.append(i)
    print(f"[RECEIVER] F{i} accepted in order, ACK{i} sent")


print(f"=== {title} ===")
base = next_seq = 0
while base < N_FRAMES:
    print()
    while next_seq < base + WINDOW and next_seq < N_FRAMES:
        send(next_seq, base); next_seq += 1          # send whole window
    i = base
    while i < next_seq:
        if lost(i):
            print(f"  [CHANNEL] F{i} LOST -> receiver discards F{i} and everything after it this round")
            print(f"[SENDER] timeout on ACK{i} -> Go-Back-N: resending from F{i}")
            LOSSES.discard(i)                         # lost only once
            rounds += 1
            next_seq = base = i                       # discard rest of window
            break
        accept(i); i += 1
    else:
        base = i                                      # window slides forward
        print(f"[SENDER] window slides, base is now {base}")

print()
print(f"[STATS] window={WINDOW} | frames to deliver: {N_FRAMES} | total frame-sends: {sends} | Go-Back-N rounds: {rounds}")
print(f"[RESULT] frames delivered in order: {delivered}")
print(f"[RESULT] correct and complete: {delivered == list(range(N_FRAMES))}")
