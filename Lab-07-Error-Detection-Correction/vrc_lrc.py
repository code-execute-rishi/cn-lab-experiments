# Computer Network Lab - Experiment 7
# Student Name: Aradhya Jain | Scholar No: 24112011111 | Section: CSE-1
# VRC, LRC, and 2D Parity Matrix with Autonomous Single-Bit Correction

def calculate_vrc(byte_str: str, mode: str = 'even') -> str:
    """Calculates row parity bit (VRC) for a single character bitstring."""
    ones = byte_str.count('1')
    return '0' if (ones % 2 == 0) else '1' if mode == 'even' else '1' if (ones % 2 == 0) else '0'

def calculate_lrc(matrix: list, mode: str = 'even') -> str:
    """Calculates Block Check Character (LRC) across columns of data matrix."""
    cols = len(matrix[0])
    bcc = []
    for c in range(cols):
        col_ones = sum(1 for row in matrix if row[c] == '1')
        bcc.append('0' if (col_ones % 2 == 0) else '1' if mode == 'even' else '1' if (col_ones % 2 == 0) else '0')
    return ''.join(bcc)

def construct_2d_parity(data_bytes: list):
    """Builds 2D grid: adds VRC to each row and appends LRC as final row."""
    grid = []
    for b in data_bytes:
        vrc = calculate_vrc(b)
        grid.append(list(b + vrc))
    cols = len(grid[0])
    bcc = []
    for c in range(cols):
        col_ones = sum(1 for r in range(len(grid)) if grid[r][c] == '1')
        bcc.append('0' if col_ones % 2 == 0 else '1')
    grid.append(bcc)
    return grid

def verify_and_correct_2d(grid: list):
    """Detects row and col parity failures; auto-corrects single bit at intersection."""
    rows = len(grid) - 1
    cols = len(grid[0])
    bad_rows = []
    for r in range(rows):
        data_part = ''.join(grid[r][:-1])
        if calculate_vrc(data_part) != grid[r][-1]:
            bad_rows.append(r)
    bad_cols = []
    for c in range(cols):
        col_ones = sum(1 for r in range(rows) if grid[r][c] == '1')
        expected_bcc = '0' if col_ones % 2 == 0 else '1'
        if expected_bcc != grid[-1][c]:
            bad_cols.append(c)
    if len(bad_rows) == 1 and len(bad_cols) == 1:
        r, c = bad_rows[0], bad_cols[0]
        grid[r][c] = '0' if grid[r][c] == '1' else '1'
        return True, (r, c)
    return False, (bad_rows, bad_cols)

if __name__ == "__main__":
    data_words = ['1010101', '1100110', '0111001', '1001011']
    print("[TRANSMITTER: ENCODING 4 BYTES INTO 2D PARITY GRID]")
    print(f"Data Words: {data_words}")
    grid = construct_2d_parity(data_words)
    print("Generated 2D Grid (with VRC column and LRC row):")
    for r in range(len(grid) - 1):
        print(f"  Row {r}: {' '.join(grid[r][:-1])} | VRC: {grid[r][-1]}")
    print("  " + "-" * 33)
    print(f"  LRC:   {' '.join(grid[-1][:-1])} | {grid[-1][-1]}\n")

    print("[CHANNEL: INJECTING 1-BIT ERROR AT ROW 1, COL 4 (Bit 1 -> 0)]")
    grid[1][4] = '0' if grid[1][4] == '1' else '1'
    print(f"Corrupted Row 1 received as: {' '.join(grid[1][:-1])} | VRC: {grid[1][-1]}")
    corrected, coords = verify_and_correct_2d(grid)
    if corrected:
        print(f"** SINGLE-BIT ERROR LOCALIZED AT INTERSECTION (Row {coords[0]}, Column {coords[1]}) **")
        print(f"Autonomously inverting bit at {coords}: Restored original bit. Data completely corrected!")
    else:
        print(f"Correction failed: {coords}")
