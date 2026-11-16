# Computer Network Lab - Experiment 7
# Student Name: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
# Cyclic Redundancy Check (CRC): Modulo-2 Polynomial Division Engine

def xor(a: str, b: str) -> str:
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))

def mod2div(dividend: str, divisor: str) -> str:
    """Performs modulo-2 polynomial division using bitwise XOR without borrows."""
    k = len(divisor)
    cur = dividend[:k]
    for i in range(k, len(dividend)):
        if cur[0] == '1':
            cur = xor(cur, divisor)[1:] + dividend[i]
        else:
            cur = cur[1:] + dividend[i]
    if cur[0] == '1':
        rem = xor(cur, divisor)[1:]
    else:
        rem = cur[1:]
    return rem

def encode_crc(data_bits: str, generator_poly: str):
    """Appends r zeros, computes remainder R(x), and returns transmitted codeword."""
    r = len(generator_poly) - 1
    appended_data = data_bits + ('0' * r)
    remainder = mod2div(appended_data, generator_poly)
    codeword = data_bits + remainder
    return codeword, remainder

def verify_crc(received_codeword: str, generator_poly: str) -> bool:
    """Checks if remainder on received codeword is strictly all zeros."""
    rem = mod2div(received_codeword, generator_poly)
    return set(rem) == {'0'} or rem == ''

if __name__ == "__main__":
    data = "1101011011"
    key = "10011"  # CRC-4 generator: x^4 + x + 1
    codeword, rem = encode_crc(data, key)

    print(f"Data Bitstream D(x): {data}  |  Generator G(x): {key} (CRC-4: x^4 + x + 1)")
    print(f"Appended Dividend:   {data + '0'*(len(key)-1)}")
    print(f"Modulo-2 Long Division Remainder R(x): {rem}")
    print(f"Transmitted Codeword T(x): {codeword}\n")

    print("[TEST 1: RECEIVER CHECK ON UNCORRUPTED CODEWORD]")
    check1 = verify_crc(codeword, key)
    rem1 = mod2div(codeword, key)
    print(f"Received: {codeword}  ->  Remainder: {rem1}  ->  {'ACCEPTED (No Error Detected)' if check1 else 'REJECTED'}\n")

    print("[TEST 2: SINGLE-BIT ERROR AT BIT POSITION 3]")
    corrupted_single = list(codeword)
    corrupted_single[3] = '0' if corrupted_single[3] == '1' else '1'
    corrupted_single = ''.join(corrupted_single)
    rem2 = mod2div(corrupted_single, key)
    print(f"Received: {corrupted_single}  ->  Remainder: {rem2}  ->  {'ACCEPTED' if verify_crc(corrupted_single, key) else 'ERROR DETECTED! (Frame Rejected)'}\n")

    print("[TEST 3: 4-BIT BURST ERROR INJECTED (Bits 6 to 9)]")
    burst = list(codeword)
    for idx in range(6, 10):
        burst[idx] = '0' if burst[idx] == '1' else '1'
    burst = ''.join(burst)
    rem3 = mod2div(burst, key)
    print(f"Received: {burst}  ->  Remainder: {rem3}  ->  {'ACCEPTED' if verify_crc(burst, key) else 'BURST ERROR DETECTED! (Frame Rejected)'}")
