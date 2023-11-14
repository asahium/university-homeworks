#!/bin/bash

# Function to send ICMP timestamp requests
send_icmp_timestamp_requests() {
    hping3 -c 3 -t 5 --icmp-ts "$1"
}

# Function to connect to OpenVPN
connect_to_openvpn() {
    # Replace the placeholders with your OpenVPN configuration file, username, and password
    openvpn --config /path/to/your/openvpn.conf --auth-user-pass <(echo -e "your_username\nyour_password")
}

# Send ICMP timestamp requests
send_icmp_timestamp_requests "51.89.166.139"

# Sleep for 30 seconds (adjust as needed)
sleep 30

# Connect to OpenVPN
connect_to_openvpn
