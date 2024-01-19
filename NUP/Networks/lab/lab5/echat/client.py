# Read source code here - https://github.com/annmuor/nup2023networks/tree/main/echat
# Create client
# Listen for broadcast messages to get a message from server to find its mac address
# Send "getflag" private message to this mac address
# Listen for private message back to get flag
# we will know only mac address of server and need listen for ethernet frames to get flag

from scapy.all import *
import time

# get mac address of server
def get_mac_address():
    mac_address = None
    while mac_address is None:
        try:
            mac_address = sniff(filter="ether dst 00:00:00:00:00:00", count=1, timeout=5)[0].src
        except:
            pass
    return mac_address

# send private message to server
def send_private_message(mac_address):
    sendp(Ether(dst=mac_address)/IP(dst="1.1.1.1")/UDP(dport=1337)/Raw(load="getflag"))

# get flag from private message
def get_flag():
    flag = None
    while flag is None:
        try:
            flag = sniff(filter="ether dst 00:00:00:00:00:00 and udp port 1337", count=1, timeout=5)[0].load
        except:
            pass
    return flag

# main function
def main():
    mac_address = get_mac_address()
    send_private_message(mac_address)
    flag = get_flag()
    print(flag)
