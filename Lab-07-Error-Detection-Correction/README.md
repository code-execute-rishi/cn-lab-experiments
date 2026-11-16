# Lab 7: Error Detection & Correction Methods

## Question
**Aim:** To implement, test, and comparatively evaluate Linear Error Detection and Forward Error Correction algorithms at the Data Link Layer in Python: Vertical Redundancy Check (VRC), Longitudinal Redundancy Check (LRC), 2D Parity Matrix, and Hamming (7,4) Code.

## Files
- [`vrc_lrc.py`](vrc_lrc.py): VRC (row parity), LRC (column parity) and the 2D parity matrix with single-bit correction.
- [`hamming_code.py`](hamming_code.py): Hamming (7,4) single error correction and Extended (8,4) SEC-DED.

## How to Run
No input is needed; the test data is built into each program.
```bash
python3 vrc_lrc.py
python3 hamming_code.py
```

## Output

### `vrc_lrc.py`

```
[TRANSMITTER: ENCODING 4 BYTES INTO 2D PARITY GRID]
Data Words: ['1010101', '1100110', '0111001', '1001011']
Generated 2D Grid (with VRC column and LRC row):
  Row 0: 1 0 1 0 1 0 1 | VRC: 0
  Row 1: 1 1 0 0 1 1 0 | VRC: 0
  Row 2: 0 1 1 1 0 0 1 | VRC: 0
  Row 3: 1 0 0 1 0 1 1 | VRC: 0
  ---------------------------------
  LRC:   1 0 0 0 0 0 1 | 0

[CHANNEL: INJECTING 1-BIT ERROR AT ROW 1, COL 4 (Bit 1 -> 0)]
Corrupted Row 1 received as: 1 1 0 0 0 1 0 | VRC: 0
** SINGLE-BIT ERROR LOCALIZED AT INTERSECTION (Row 1, Column 4) **
Autonomously inverting bit at (1, 4): Restored original bit. Data completely corrected!
```

### `hamming_code.py`

```
[HAMMING (7,4) ENCODING FOR DATA '1011']
Input Data: d1=1, d2=0, d3=1, d4=1
Calculated Check Bits: p1=0, p2=1, p4=0
Transmitted Codeword [p1, p2, d1, p4, d2, d3, d4]: 0 1 1 0 0 1 1

[TEST 1: SINGLE-BIT INVERSION AT POSITION 6 (d3 flipped 1 -> 0)]
Received Bits: [0, 1, 1, 0, 0, 0, 1]
Syndrome Evaluation: Syndrome Vector = 6 (binary 110)
** ERROR PINPOINTED AT BIT POSITION 6 **
Flipping bit 6: Restored codeword to [0, 1, 1, 0, 0, 1, 1]  ->  Extracted Data: 1011 (Success)

[TEST 2: EXTENDED SEC-DED (8,4) DOUBLE-BIT ERROR TEST (Bits 3 & 7 inverted)]
Received 8-bit Word: [p0=0, 0, 1, 0, 0, 0, 1, 0]
SEC-DED Status: DOUBLE_BIT_ERROR_DETECTED_UNCORRECTABLE
** CRITICAL ALERT: DOUBLE-BIT ERROR DETECTED! **
Syndrome is non-zero but overall parity is consistent. Halting correction to prevent corruption!
```


## Viva Questions

1. **Error detection vs error correction?**
   Detection only finds that an error happened (then the frame is resent). Correction (FEC) also finds where it is and fixes it at the receiver.
2. **What is VRC?**
   Vertical Redundancy Check: one parity bit per character. It detects odd numbers of bit errors.
3. **What is LRC?**
   Longitudinal Redundancy Check: a parity bit for each bit position across a block of characters, forming a Block Check Character.
4. **How does a 2D parity matrix correct a single bit?**
   The bad row (from VRC) and the bad column (from LRC) cross at the flipped bit, so the receiver flips it back.
5. **When does 2D parity fail?**
   When 4 errors form a rectangle: every row and column still has correct parity, so the error is not detected.
6. **What is the Hamming bound?**
   With r parity bits for m data bits: 2^r ≥ m + r + 1. For m = 4, r = 3.
7. **Where are the Hamming parity bits placed?**
   At positions that are powers of 2: 1, 2 and 4. Data bits go in positions 3, 5, 6 and 7.
8. **What does the syndrome tell you?**
   0 means no error. Otherwise, its decimal value is the position of the wrong bit.
