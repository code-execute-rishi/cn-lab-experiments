import serial, sys

PORT = "/tmp/ttyV1"
BAUD = 9600

def main():
    outdir = sys.argv[1]
    ser = serial.Serial(PORT, BAUD, timeout=5)
    header = b""
    while not header.endswith(b"\n"):
        b = ser.read(1)
        if not b:
            break
        header += b
    name, size = header.decode().strip().split("|")
    size = int(size)
    print(f"[RECEIVER] header says filename={name} size={size} bytes")
    data = b""
    while len(data) < size:
        chunk = ser.read(64)
        if not chunk:
            break
        data += chunk
    outpath = f"{outdir}/{name}"
    with open(outpath, "wb") as f:
        f.write(data)
    print(f"[RECEIVER] received {len(data)} bytes, wrote to {outpath}")
    ser.close()

if __name__ == "__main__":
    main()
