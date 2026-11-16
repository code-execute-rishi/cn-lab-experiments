# Lab 1: Linux Commands & Star Topology in Cisco Packet Tracer

## Question
**Objective (lab handout):** Configuring a simple network topology using a switch.

**Aim:** To get hands-on with basic Linux/Unix commands and then design a working star topology network in Cisco Packet Tracer, assign IPs to the hosts and check that they can actually talk to each other.

This lab has no program. Part A is Linux commands; Part B is done in Cisco Packet Tracer.

## Part A: Basic Linux Commands

| Command | What it does | Example |
|---------|--------------|---------|
| `pwd` | Shows the current directory | `pwd` |
| `ls` | Lists files (`-la` shows hidden files and details) | `ls -la` |
| `cd` | Changes directory | `cd Documents` |
| `cat` | Prints a file | `cat notes.txt` |
| `echo` | Prints text or a variable | `echo "Hello from Aradhya"` |
| `cp` | Copies a file or folder | `cp notes.txt backup.txt` |
| `mv` | Moves or renames a file | `mv old.txt new.txt` |
| `rm` | Deletes a file | `rm junk.txt` |
| `mkdir` | Creates a directory | `mkdir lab_files` |
| `rmdir` | Removes an empty directory | `rmdir lab_files` |
| `date` | Shows the date and time | `date` |
| `df` | Shows free disk space | `df -h` |
| `ps` | Lists running processes | `ps aux` |
| `wc` | Counts lines, words and characters | `wc -l notes.txt` |
| `bc` | Calculator | `echo "12*4" \| bc` |

## Part B: Star Topology in Cisco Packet Tracer

**Equipment:** Cisco Packet Tracer, 1 × Cisco 2960 switch, 4 × PCs, copper straight-through cables.

| Device | Interface | IP Address | Subnet Mask | Connected To |
|--------|-----------|------------|-------------|--------------|
| SW_Central | Fa0/1 – Fa0/4 | – | – | All PCs |
| PC0 | FastEthernet0 | 192.168.1.1 | 255.255.255.0 | Switch Fa0/1 |
| PC1 | FastEthernet0 | 192.168.1.3 | 255.255.255.0 | Switch Fa0/2 |
| PC2 | FastEthernet0 | 192.168.1.2 | 255.255.255.0 | Switch Fa0/3 |
| PC3 | FastEthernet0 | 192.168.1.4 | 255.255.255.0 | Switch Fa0/4 |

**Steps**
1. Place a 2960 switch in the centre and four PCs around it.
2. Connect each PC's FastEthernet0 to its own switch port with a copper straight-through cable. Wait until the link lights turn green.
3. On each PC: **Desktop → IP Configuration → Static**, and enter the IP address and subnet mask from the table.
4. On one PC: **Desktop → Command Prompt**, then `ping` another PC's IP.

**Result:** The ping got 4 replies with 0% packet loss. Only a switch is needed (no router) because all PCs are on the same 192.168.1.0/24 subnet.

## Viva Questions

1. **What is a star topology?**
   Every device connects to one central device (a switch or hub). If one cable or PC fails, the rest keep working; if the central device fails, the whole network goes down.
2. **Why is no router needed here?**
   All PCs are on the same subnet (192.168.1.0/24). A router is needed only to send traffic between different networks.
3. **Switch vs hub?**
   A hub sends every frame to all ports. A switch learns MAC addresses and sends each frame only to the port where the destination is connected.
4. **How does a switch learn MAC addresses?**
   It reads the source MAC of every incoming frame and stores it with the port number in its MAC (CAM) table.
5. **What does ping use?**
   ICMP Echo Request and Echo Reply messages. Before the first ping, ARP finds the MAC address for the destination IP.
6. **Which cable connects a PC to a switch?**
   A straight-through cable. A crossover cable is used between similar devices, such as PC to PC or switch to switch.
7. **What does the subnet mask 255.255.255.0 mean?**
   The first 24 bits are the network part, so hosts 192.168.1.1–192.168.1.254 are on the same network.
8. **Kernel vs shell?**
   The kernel controls the hardware, memory and processes. The shell (e.g. Bash) reads your commands and asks the kernel to run them.
