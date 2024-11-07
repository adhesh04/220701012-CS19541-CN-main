from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.config import conf

# Change the socket layer to Layer 3 (IP layer)
conf.L3socket = conf.L3socket6  # You can also use conf.L3socket depending on your IP version (IPv4 or IPv6)

# Callback function to process each captured packet
def packet_callback(packet):
    if IP in packet:
        ip_layer = packet[IP]
        protocol = ip_layer.proto
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst

        # Determine the protocol
        if protocol == 1:
            protocol_name = "ICMP"
        elif protocol == 6:
            protocol_name = "TCP"
        elif protocol == 17:
            protocol_name = "UDP"
        else:
            protocol_name = "Unknown Protocol"

        # Print packet details
        print(f"Protocol: {protocol_name}")
        print(f"Source IP: {src_ip}")
        print(f"Destination IP: {dst_ip}")
        print("-" * 50)

# Main function to start sniffing
def main():
    # Capture packets on the default network interface
    sniff(prn=packet_callback, filter="ip", store=0)

# Start the packet sniffer when the script is run
if __name__ == "__main__":
    main()
