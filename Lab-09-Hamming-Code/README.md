# Lab 9: Hamming Code for Error Detection and Correction

## Question
**Aim:** To design and implement Hamming (7,4) Single Error Correction (SEC) and Extended Hamming (8,4) SEC-DED (Single Error Correction, Double Error Detection) block codes with character-level ASCII streaming forward error correction in Python.

## Files
- [`hamming_code.py`](hamming_code.py): Hamming (7,4) encode and decode with the syndrome, and Extended (8,4) SEC-DED.

## Logic (How the Program Works)

```text
hamming_code.py
1. Hamming (7,4): 4 data bits need 3 parity bits (2^r >= m + r + 1 -> 8 >= 8).
2. encode_74(): parity bits at positions 1, 2, 4: p1 = d1^d2^d4, p2 = d1^d3^d4, p4 = d2^d3^d4. Codeword [p1 p2 d1 p4 d2 d3 d4].
3. decode_74(): recompute the checks s1 = b1^b3^b5^b7, s2 = b2^b3^b6^b7, s4 = b4^b5^b6^b7.
   Syndrome = 4*s4 + 2*s2 + s1. 0 = no error, otherwise flip the bit at that position. Data = bits 3, 5, 6, 7.
4. Extended SEC-DED (8,4): add p0 = XOR of all 7 bits.
5. decode_84_secded(): syndrome != 0 and overall parity wrong -> single error, corrected.
   syndrome != 0 and overall parity correct -> double error, detected, not corrected.
   syndrome 0 and overall parity wrong -> only p0 is wrong.
6. Demo: data 1011, bit 6 flipped -> syndrome = 6 -> corrected. Bits 3 and 7 flipped -> double-bit error detected.
```

## How to Run
No input is needed; the test data is built into each program.
```bash
python3 hamming_code.py
```

## Output

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

1. **What is a Hamming code?**
   A block code that adds parity bits so the receiver can find and correct a single-bit error.
2. **Parity equations for Hamming (7,4)?**
   p1 = d1 ⊕ d2 ⊕ d4, p2 = d1 ⊕ d3 ⊕ d4, p4 = d2 ⊕ d3 ⊕ d4.
3. **How is the syndrome formed?**
   S = (s4 s2 s1) in binary, where each s is a recomputed parity check. Its value is the error position (0 means no error).
4. **Minimum Hamming distance of (7,4)?**
   3. It can correct 1 error or detect 2 errors, but not both.
5. **What does SEC-DED add?**
   An overall parity bit P0 over all 7 bits, giving distance 4: it corrects 1 error and detects 2.
6. **How does SEC-DED tell 1 error from 2?**
   Syndrome ≠ 0 and overall parity wrong → 1 error (correct it). Syndrome ≠ 0 and overall parity correct → 2 errors (cannot correct).
7. **Code rate of Hamming (7,4)?**
   4/7: 4 data bits in every 7 bits sent.
8. **Where is Hamming code used?**
   ECC memory (RAM) and other places where resending is not possible, so errors must be fixed at the receiver.
