# Lab 8: LRC, VRC and CRC Error Detection Methods

## Question
**Aim:** To design, implement, and benchmark Vertical Redundancy Check (VRC), Longitudinal Redundancy Check (LRC), 2D Parity, and Cyclic Redundancy Check (CRC) using Galois Field GF(2) polynomial division in Python.

## Files
- [`vrc_lrc.py`](vrc_lrc.py): VRC, LRC and 2D parity.
- [`crc.py`](crc.py): CRC: modulo-2 division, building the codeword and checking it at the receiver.

## How to Run
No input is needed; the test data is built into each program.
```bash
python3 vrc_lrc.py
python3 crc.py
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

### `crc.py`

```
Data Bitstream D(x): 1101011011  |  Generator G(x): 10011 (CRC-4: x^4 + x + 1)
Appended Dividend:   11010110110000
Modulo-2 Long Division Remainder R(x): 1110
Transmitted Codeword T(x): 11010110111110

[TEST 1: RECEIVER CHECK ON UNCORRUPTED CODEWORD]
Received: 11010110111110  ->  Remainder: 0000  ->  ACCEPTED (No Error Detected)

[TEST 2: SINGLE-BIT ERROR AT BIT POSITION 3]
Received: 11000110111110  ->  Remainder: 0111  ->  ERROR DETECTED! (Frame Rejected)

[TEST 3: 4-BIT BURST ERROR INJECTED (Bits 6 to 9)]
Received: 11010101001110  ->  Remainder: 0010  ->  BURST ERROR DETECTED! (Frame Rejected)
```


## Viva Questions

1. **What is CRC?**
   Cyclic Redundancy Check: the data is divided by a generator polynomial using modulo-2 (XOR) division, and the remainder is sent with the data.
2. **How is the CRC codeword made?**
   Append r zeros to the data (r = degree of the generator), divide by the generator, and replace the zeros with the remainder.
3. **How does the receiver check it?**
   It divides the received codeword by the same generator. A remainder of 0 means no error was detected.
4. **Why modulo-2 arithmetic?**
   Addition and subtraction are both XOR with no carries, which is simple and fast in hardware.
5. **Which errors does CRC detect?**
   All single-bit errors, all odd numbers of errors (when x+1 is a factor of G(x)), and all burst errors no longer than the degree r.
6. **CRC vs parity?**
   Parity misses even numbers of errors. CRC is much stronger, especially against burst errors, which is why Ethernet uses CRC-32.
7. **Give a standard generator polynomial.**
   CRC-4: x^4 + x + 1 (10011). Ethernet uses CRC-32.
8. **What is a burst error?**
   Two or more bits in a row (or close together) are wrong, often caused by noise on the line.
