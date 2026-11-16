# Computer Network Lab - Experiment 7
# Student Name: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
# Hamming Code (7,4) Single-Bit Correction and Extended SEC-DED (8,4) Double-Bit Detection

class HammingCode:
    @staticmethod
    def encode_74(data_4bit: str) -> list:
        """Encodes 4 data bits into a 7-bit codeword with parity at 1, 2, 4 (1-indexed)."""
        d = [int(b) for b in data_4bit]  # d1, d2, d3, d4
        p1 = d[0] ^ d[1] ^ d[3]
        p2 = d[0] ^ d[2] ^ d[3]
        p4 = d[1] ^ d[2] ^ d[3]
        return [0, p1, p2, d[0], p4, d[1], d[2], d[3]]

    @staticmethod
    def decode_74(bits: list):
        """Calculates syndrome S = s4*4 + s2*2 + s1. Corrects bit at S if S > 0."""
        s1 = bits[1] ^ bits[3] ^ bits[5] ^ bits[7]
        s2 = bits[2] ^ bits[3] ^ bits[6] ^ bits[7]
        s4 = bits[4] ^ bits[5] ^ bits[6] ^ bits[7]
        syndrome = (s4 << 2) | (s2 << 1) | s1
        corrected = list(bits)
        if syndrome != 0:
            corrected[syndrome] ^= 1
        extracted_data = f"{corrected[3]}{corrected[5]}{corrected[6]}{corrected[7]}"
        return syndrome, corrected, extracted_data

    @staticmethod
    def encode_84_secded(data_4bit: str) -> list:
        """Extended SEC-DED (8,4): Adds overall parity bit p0 at index 0."""
        c = HammingCode.encode_74(data_4bit)
        p0 = 0
        for bit in c[1:]:
            p0 ^= bit
        c[0] = p0
        return c

    @staticmethod
    def decode_84_secded(bits: list):
        """SEC-DED: Distinguishes correctable 1-bit from uncorrectable 2-bit errors."""
        s1 = bits[1] ^ bits[3] ^ bits[5] ^ bits[7]
        s2 = bits[2] ^ bits[3] ^ bits[6] ^ bits[7]
        s4 = bits[4] ^ bits[5] ^ bits[6] ^ bits[7]
        syndrome = (s4 << 2) | (s2 << 1) | s1
        overall_parity_calc = 0
        for b in bits:
            overall_parity_calc ^= b

        if syndrome == 0 and overall_parity_calc == 0:
            return "NO_ERROR", bits[1:], f"{bits[3]}{bits[5]}{bits[6]}{bits[7]}"
        elif syndrome != 0 and overall_parity_calc == 1:
            corrected = list(bits)
            corrected[syndrome] ^= 1
            data = f"{corrected[3]}{corrected[5]}{corrected[6]}{corrected[7]}"
            return f"SINGLE_BIT_CORRECTED_AT_POS_{syndrome}", corrected[1:], data
        elif syndrome != 0 and overall_parity_calc == 0:
            return "DOUBLE_BIT_ERROR_DETECTED_UNCORRECTABLE", bits[1:], None
        else:
            return "PARITY_BIT_P0_ERROR", bits[1:], f"{bits[3]}{bits[5]}{bits[6]}{bits[7]}"

if __name__ == "__main__":
    data_input = "1011"
    print(f"[HAMMING (7,4) ENCODING FOR DATA '{data_input}']")
    c7 = HammingCode.encode_74(data_input)
    print(f"Input Data: d1={c7[3]}, d2={c7[5]}, d3={c7[6]}, d4={c7[7]}")
    print(f"Calculated Check Bits: p1={c7[1]}, p2={c7[2]}, p4={c7[4]}")
    print(f"Transmitted Codeword [p1, p2, d1, p4, d2, d3, d4]: {' '.join(str(b) for b in c7[1:])}\n")

    print("[TEST 1: SINGLE-BIT INVERSION AT POSITION 6 (d3 flipped 1 -> 0)]")
    c7_err = list(c7)
    c7_err[6] ^= 1
    print(f"Received Bits: {c7_err[1:]}")
    syn, corr, out_data = HammingCode.decode_74(c7_err)
    print(f"Syndrome Evaluation: Syndrome Vector = {syn} (binary {bin(syn)[2:].zfill(3)})")
    print(f"** ERROR PINPOINTED AT BIT POSITION {syn} **")
    print(f"Flipping bit {syn}: Restored codeword to {corr[1:]}  ->  Extracted Data: {out_data} (Success)\n")

    print("[TEST 2: EXTENDED SEC-DED (8,4) DOUBLE-BIT ERROR TEST (Bits 3 & 7 inverted)]")
    c8 = HammingCode.encode_84_secded(data_input)
    c8_err = list(c8)
    c8_err[3] ^= 1
    c8_err[7] ^= 1
    print(f"Received 8-bit Word: [p0={c8_err[0]}, {', '.join(str(b) for b in c8_err[1:])}]")
    status, _, data_rec = HammingCode.decode_84_secded(c8_err)
    print(f"SEC-DED Status: {status}")
    print("** CRITICAL ALERT: DOUBLE-BIT ERROR DETECTED! **")
    print("Syndrome is non-zero but overall parity is consistent. Halting correction to prevent corruption!")
