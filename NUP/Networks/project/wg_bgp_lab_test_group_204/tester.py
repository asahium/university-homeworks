#!/usr/bin/env python3
try:
    import requests
except ImportError:
    print("Please install requests via pip install requests")
    exit(0)
from socket import *

# 1. create UDP socket to get IP address
try:
    s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    s.connect(('10.200.200.200', 3000))
    host,port = s.getsockname()
    s.close()
except:
    print("Connection failed - check your BGP connectivity")
    exit(0)

if host.startswith('10.10.10.'):
    print("You shall connect from your USERS or CLIENTS networks, not from your BGP network")
    exit(0)

print(f"DEBUG: we have HOST {host}, let's connect to the target")
# now let's send request
r = requests.get('http://10.200.200.200').json()

if r['ip_address'] == host:
    print("We're in NO NAT network")
else:
    print("We're in NAT network")

