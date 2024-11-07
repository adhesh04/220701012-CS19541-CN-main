import os
import socket
import struct
import time
import select

# ICMP header fields
ICMP_ECHO_REQUEST = 8  # ICMP type for Echo Request
ICMP_ECHO_REPLY = 0    # ICMP type for Echo Reply

# Calculate the checksum of the packet
def checksum(data):
    sum = 0
    count = 0
    # Loop over the data two bytes at a time
    while count < len(data):
        val = data[count] + (data[count + 1] << 8)
        sum += val
        sum = sum & 0xffffffff  # Keep sum within 32 bits
        count += 2
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    return ~sum & 0xffff

# Create the ICMP packet
def create_packet(id):
    header = struct.pack('bbHHH', ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = struct.pack('d', time.time())
    checksum_val = checksum(header + data)
    header = struct.pack('bbHHH', ICMP_ECHO_REQUEST, 0, checksum_val, id, 1)
    return header + data

# Ping function to send the ICMP request and measure the round-trip time
def ping(host):
    # Get the destination IP address
    dest_ip = socket.gethostbyname(host)
    print(f"Pinging {host} [{dest_ip}] with 32 bytes of data:")

    # Open a raw socket
    try:
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError:
        print("You need to run this script as administrator/root!")
        return

    # Get the current process ID for the ICMP packet
    pid = os.getpid() & 0xFFFF
    packet = create_packet(pid)

    # Send the packet and wait for a reply
    raw_socket.settimeout(2)
    try:
        start_time = time.time()
        raw_socket.sendto(packet, (dest_ip, 1))  # Send the packet to the destination IP
        reply = raw_socket.recv(1024)  # Wait for reply
        end_time = time.time()

        # Parse the ICMP reply
        icmp_header = reply[20:28]
        rtt = (end_time - start_time) * 1000  # Round-trip time in milliseconds

        # Extract the type of the received message (Echo Reply should be type 0)
        type = struct.unpack('bbHHH', icmp_header)[0]
        if type == ICMP_ECHO_REPLY:
            print(f"Reply from {host} ({dest_ip}): bytes=32 time={rtt:.2f}ms")
        else:
            print("Received unexpected ICMP message.")
    except socket.timeout:
        print("Request timed out.")
    finally:
        raw_socket.close()

if __name__ == "__main__":
    host = input("Enter the host to ping: ")
    ping(host)
