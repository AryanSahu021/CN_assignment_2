import subprocess
import datetime
import matplotlib.pyplot as plt

PCAP_FILE = "attack_mitigate.pcap"  # Replace with the actual PCAP file

# Run tshark to extract TCP packets with timestamps, flags, and connection details
tshark_cmd = [
    "tshark", "-r", PCAP_FILE, "-T", "fields",
    "-e", "frame.time_epoch", "-e", "ip.src", "-e", "ip.dst",
    "-e", "tcp.srcport", "-e", "tcp.dstport", "-e", "tcp.flags"
]

try:
    output = subprocess.run(tshark_cmd, capture_output=True, text=True, check=True)
    lines = output.stdout.strip().split("\n")
except subprocess.CalledProcessError as e:
    print("Error running tshark:", e)
    exit(1)

# Store connection start and end times
connections = {}

for line in lines:
    fields = line.split("\t")
    if len(fields) < 6:
        continue

    timestamp, ip_src, ip_dst, sport, dport, flags = fields
    timestamp = float(timestamp)  # Convert to float
    conn_key = (ip_src, ip_dst, sport, dport)

    flags = int(flags, 16)  # Convert TCP flag hex to integer

    if flags & 0x02:  # SYN packet
        if conn_key not in connections:
            connections[conn_key] = {'start': timestamp, 'end': None, 'fin': None}
    elif flags & 0x04:  # RST packet (immediate termination)
        if conn_key in connections:
            connections[conn_key]['end'] = timestamp
    elif flags & 0x01:  # FIN packet
        if conn_key in connections:
            connections[conn_key]['fin'] = timestamp
    elif flags & 0x10:  # ACK packet
        if conn_key in connections and connections[conn_key]['fin'] is not None:
            connections[conn_key]['end'] = timestamp

# Assign default duration if no ACK after FIN-ACK
start_times = []
durations = []

for conn, times in connections.items():
    start_time = times['start']
    end_time = times.get('end')

    if end_time is None:  # If no proper termination found, assign 100s duration
        end_time = start_time + 100

    duration = end_time - start_time
    start_times.append(datetime.datetime.fromtimestamp(start_time))
    durations.append(duration)

# Detect attack period (Example: Based on highest duration or manual threshold)
attack_start = min(start_times) + datetime.timedelta(seconds=30)
attack_end = attack_start + datetime.timedelta(seconds=60)

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(start_times, durations, color='blue', label="TCP Connections", alpha=0.6)
plt.axvline(attack_start, color='red', linestyle='dashed', linewidth=2, label="Attack Start")
plt.axvline(attack_end, color='green', linestyle='dashed', linewidth=2, label="Attack End")

plt.xlabel("Connection Start Time")
plt.ylabel("Connection Duration (seconds)")
plt.title("TCP Connection Duration vs. Start Time")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
