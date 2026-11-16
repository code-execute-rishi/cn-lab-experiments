# Lab 4: PC to PC File Transfer Using Serial Port

## Question
**Aim:** PC to PC file transfer using serial port: send a file from one machine to another over a serial link, byte for byte, and prove the received file is identical (checksum + hexdump + diff).

## Files
- [`sender.py`](sender.py): opens `/tmp/ttyV0`, sends a header `filename|size`, then the file in 64-byte chunks.
- [`receiver.py`](receiver.py): opens `/tmp/ttyV1`, reads the header and then exactly `size` bytes, and saves the file.
- [`hello.txt`](hello.txt): the 256-byte test file.

## Setup
Real UART hardware was not available, so a virtual null-modem cable (two linked serial ports) is created with `socat`. The programs use pyserial's real serial API.
```bash
pip3 install pyserial
brew install socat             # macOS   (Linux: sudo apt install socat)
```

## How to Run
```bash
# Terminal 1: create the virtual serial cable
socat -d -d pty,raw,echo=0,link=/tmp/ttyV0 pty,raw,echo=0,link=/tmp/ttyV1

# Terminal 2: receiver (PC B)
mkdir -p recv
python3 receiver.py ./recv

# Terminal 3: sender (PC A)
python3 sender.py hello.txt
```

## Output
```
$ python3 receiver.py ./recv
[RECEIVER] header says filename=hello.txt size=256 bytes
[RECEIVER] received 256 bytes, wrote to ./recv/hello.txt
```

```
$ python3 sender.py hello.txt
[SENDER] sent header: hello.txt|256
[SENDER] sent 256 bytes of file data
```

**Verification**
```
$ diff hello.txt recv/hello.txt && echo "FILES MATCH"
FILES MATCH

$ shasum -a 256 hello.txt recv/hello.txt
1fd606be53a2a4f3ce86e601b419dc4c99f0b0dbd991b0fa4e87af302ffadf75  hello.txt
1fd606be53a2a4f3ce86e601b419dc4c99f0b0dbd991b0fa4e87af302ffadf75  recv/hello.txt
```


## Viva Questions

1. **What is serial communication?**
   Data is sent one bit at a time over a single line, as opposed to parallel, where many bits go together on several lines.
2. **What is baud rate?**
   The number of signal changes per second. Here it is 9600 baud; both sides must use the same rate.
3. **What is a null-modem cable?**
   A cable that crosses TX and RX so two computers can talk directly over serial ports. socat creates a virtual one here.
4. **Why send a header first?**
   So the receiver knows the file name and exactly how many bytes to read, and therefore when the file has ended.
5. **How do you prove the file arrived correctly?**
   diff shows no differences, the SHA-256 checksums match, and the hexdumps (xxd) are identical.
6. **What is a UART?**
   Universal Asynchronous Receiver/Transmitter: the hardware that converts bytes to serial bits, with start and stop bits around each byte.
7. **Synchronous vs asynchronous transmission?**
   Synchronous uses a shared clock signal. Asynchronous (like UART) has no shared clock; start and stop bits mark each byte.
8. **What is the timeout in serial.Serial for?**
   read() returns after that many seconds even if no data came, so the program does not hang forever.
