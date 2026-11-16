# Computer Network Lab - Experiment 6
# Student Name: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
# Parity Check: Even and Odd Parity Generator, Inverter, and Verifier

def generate_parity(data_bits: str, mode: str = 'even') -> str:
    """Generates parity bit for a binary string under even or odd scheme."""
    ones_count = data_bits.count('1')
    if mode.lower() == 'even':
        return '0' if (ones_count % 2 == 0) else '1'
    elif mode.lower() == 'odd':
        return '1' if (ones_count % 2 == 0) else '0'
    raise ValueError("Mode must be 'even' or 'odd'")

def verify_parity(codeword: str, mode: str = 'even') -> bool:
    """Verifies received codeword. Codeword = data_bits + parity_bit."""
    return codeword[-1] == generate_parity(codeword[:-1], mode)

def inject_bit_errors(codeword: str, bit_indices: list) -> str:
    """Inverts bits at specified zero-indexed positions to simulate physical noise."""
    bits = list(codeword)
    for idx in bit_indices:
        if 0 <= idx < len(bits):
            bits[idx] = '0' if bits[idx] == '1' else '1'
    return ''.join(bits)

if __name__ == "__main__":
    print("=" * 60)
    print("TEST 1: PARITY GENERATION & VERIFICATION")
    print("=" * 60)
    data = "1011001"
    even_p = generate_parity(data, 'even')
    odd_p = generate_parity(data, 'odd')
    cw_even = data + even_p
    cw_odd = data + odd_p
    print(f"Data Word: {data} (Count of 1s: {data.count('1')})")
    print(f"  Even Parity Bit: {even_p} -> Transmitted Codeword: {cw_even}  |  Receiver: {'VALID' if verify_parity(cw_even, 'even') else 'ERROR'}")
    print(f"  Odd Parity Bit:  {odd_p} -> Transmitted Codeword: {cw_odd}  |  Receiver: {'VALID' if verify_parity(cw_odd, 'odd') else 'ERROR'}")

    print("\n" + "=" * 60)
    print("TEST 2: SINGLE-BIT ERROR INJECTION (Bit 3 inverted)")
    print("=" * 60)
    err_cw_1 = inject_bit_errors(cw_even, [3])
    print(f"Original Codeword:  {cw_even}  ->  Injected Codeword: {err_cw_1} (Bit 3 flipped)")
    print(f"Receiver Check (Even Scheme): {'ERROR DETECTED!' if not verify_parity(err_cw_1, 'even') else 'VALID'}")

    print("\n" + "=" * 60)
    print("TEST 3: DOUBLE-BIT ERROR INJECTION (Bits 1 and 4 inverted)")
    print("=" * 60)
    err_cw_2 = inject_bit_errors(cw_even, [1, 4])
    print(f"Original Codeword:  {cw_even}  ->  Injected Codeword: {err_cw_2} (Bits 1 & 4 flipped)")
    print(f"Receiver Check (Even Scheme): {'ERROR DETECTED!' if not verify_parity(err_cw_2, 'even') else 'VALID (FALSE ACCEPTANCE - CRITICAL FLAW)'}")
    print("Observation: Parity count remained even (6 ones). Double-bit error completely missed!")
