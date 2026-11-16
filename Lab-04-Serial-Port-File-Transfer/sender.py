import serial, sys, os, time

PORT = "/tmp/ttyV0"
BAUD = 9600

def main():
    infile = sys.argv[1]
    size = os.path.getsize(infile)
    ser = serial.Serial(PORT, BAUD, timeout=2)
    time.sleep(1)
    header = f"{os.path.basename(infile)}|{size}\n".encode()
    ser.write(header)
    print(f"[SENDER] sent header: {header.decode().strip()}")
    with open(infile, "rb") as f:
        sent = 0
        while True:
            chunk = f.read(64)
            if not chunk:
                break
            ser.write(chunk)
            sent += len(chunk)
    print(f"[SENDER] sent {sent} bytes of file data")
    ser.close()

if __name__ == "__main__":
    main()
