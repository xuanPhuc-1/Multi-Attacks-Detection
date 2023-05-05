import numpy as np
import csv
# from scipy.stats import entropy
from detection import Entropy


time_interval = 3
# Standard deviation of packets (SDFP)
# i.e., number of packets in the T period.
# SDFP = sqrt((1/n) * sum((packets_i - mean_packets,2) ** 2))
# packets_i = number of packets of flow ith in T period
# mean_packets: mean of total packets of all flows in T period
packets_csv = np.genfromtxt('data/packets.csv', delimiter=",")
dt_packets = packets_csv[:,0]
sdfp = np.std(dt_packets) 

# Standard deviation of bytes (SDFB)
# i.e., number of bytes in the T period
# SDFB = sqrt((1/n) * sum((bytes_i - mean_bytes,2) ** 2))
# bytes_i: number of total bytes of flow ith in T period
# mean_bytes: mean of total bytes of all flows in T period
bytes_csv = np.genfromtxt('data/bytes.csv', delimiter=",")
dt_bytes = bytes_csv[:,0]
sdfb = np.std(dt_bytes)

# Number of source IPs
# Speed of source IP (SSIP), number of source IPs per unit of time
# SSIP = Number of different IP sources / T period
with open('data/ipsrc.csv', newline='') as f:
    reader = csv.reader(f)
    ipsrc_csv = list(reader)
n_ip = len(np.unique(ipsrc_csv))      # Get number of different source IPs
# print(n_ip)
ssip = n_ip // time_interval               # Get number of IPs for every second by multiple interval - 4s
f.close()

entropy = Entropy()
entropy.start()

# print(entropy.value)


# Number of Flow entries
# Speed of Flow entries (SFE), number of flow entries to the switch per unit of time
# SFE = Number of flow entries / T period
sfe = n_ip // 3

# Number of interactive flow entries
# Ratio of Pair-Flow Entries (RFIP)
# RFIP = Interactive flow entries / total number of flows in T period
fileone = None
filetwo = None

with open('data/ipsrc.csv', 'r') as t1, open('data/ipdst.csv', 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

# Check if the src_ip exists in the dst_ip,
# which indicates that source IP has two-way interaction with the destination IP. 
# If not, append that one-way interaction IP into interactive flow file (intflow.csv)
with open('data/intflow.csv','w') as f:
    for line in fileone:
        if line not in filetwo:
            f.write(line)

# Count number of 
with open('data/intflow.csv') as f:
    reader = csv.reader(f, delimiter=",")
    dt = list(reader)
    row_count_nonint = len(dt)


rfip = abs(float(n_ip - row_count_nonint) / n_ip)
headers = ["SSIP", "SDFP", "SDFB", "SFE", "RFIP", "ENTROPY"]

features = [ssip, sdfp, sdfb, sfe, rfip, entropy.value]

# print(dict(zip(headers, features)))
# print(features)

with open('features-file.csv', 'a') as f:
    cursor = csv.writer(f, delimiter=",")
    #cursor.writerow(headers)
    cursor.writerow(features)


with open('realtime.csv', 'w') as f:
    cursor = csv.writer(f, delimiter=",")
    cursor.writerow(headers)
    cursor.writerow(features)
    
    f.close()
