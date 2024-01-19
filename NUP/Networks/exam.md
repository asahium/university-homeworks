## Task 1 
- You're given a [pcap file](task01.pcap) with large ( > 100000 ) amount of packets
- Your goal is to find the flag into **multicast** UDP **packet** with **broken** IP checksum.
- This the only packet contains flag


### Solution
`udp && ip.checksum_bad.expert && (eth.dst[0] & 1)`

EX_M{7c44db4290107db8d9a5f9041533fb2a}

win


## Task 2 
- You're given a binary
  for [Linux](task02.linux)/[OSX M1/M2](task02.armmac)/[OSX Intel](task02.x64mac)/[Windows](task02.exe) that works as a
  DNS server.
- It listens UDP and TCP port 6053 on 127.0.0.1 and answers to some type of queries, like A, CNAME and so on.
- Try to get all the data from the server to find the flag.

You may also need to use HEX2ASCII decoder, like

```python
bytes.fromhex("557365206469672C204C756B6521")
```

**P.S. Do chmod 755 for Linux/OSX and [disable Gatekeeper](https://disable-gatekeeper.github.io/) for OSX.**

### Solution
запускаем как всегда сервер

`./dns_server`

и начинаем биться головой о клаву

`dig @127.0.0.1 -p 6053 -t AXFR wsglrlskdqnbawp.nup23.local`

```
; <<>> DiG 9.18.20 <<>> @127.0.0.1 -p 6053 -t AXFR wsglrlskdqnbawp.nup23.local
; (1 server found)
;; global options: +cmd
wsglrlskdqnbawp.nup23.local. 60	IN	SOA	wsglrlskdqnbawp.nup23.local. wsglrlskdqnbawp.nup23.local. 1299731653 3600 300 7200 60
wsglrlskdqnbawp.nup23.local. 60	IN	A	1.2.3.4
wsglrlskdqnbawp.nup23.local. 60	IN	CNAME	google.com.
wsglrlskdqnbawp.nup23.local. 60	IN	TXT	"SRV is the key"
wsglrlskdqnbawp.nup23.local. 60	IN	SRV	0 0 6053 _tcp._axfr.wsglrlskdqnbawp.nup23.local.
wsglrlskdqnbawp.nup23.local. 60	IN	TYPE31337 \# 38 4558414D7B3830333332356535613338616464613861313363326534 3535633135366264617D
wsglrlskdqnbawp.nup23.local. 60	IN	SOA	wsglrlskdqnbawp.nup23.local. wsglrlskdqnbawp.nup23.local. 1299731653 3600 300 7200 60
;; Query time: 0 msec
;; SERVER: 127.0.0.1#6053(127.0.0.1) (TCP)
;; WHEN: Thu Jan 18 12:22:58 EET 2024
;; XFR size: 7 records (messages 1, bytes 292)
```

using next python script

```python
hex_string = "38 4558414D7B3830333332356535613338616464613861313363326534 3535633135366264617D"

hex_bytes = bytes.fromhex(hex_string)
ascii_string = hex_bytes.decode("utf-8")

print(ascii_string)
```

we get flag `EXAM{803325e5a38adda8a13c2e455c156bda}`


## Task 3 
- You're given a binary
  for [Linux](task03.linux)/[OSX M1/M2](task03.armmac)/[OSX Intel](task03.x64mac)/[Windows](task03.exe) that works as an HTTP server.
- This HTTP server uses H/1.1337 HTTP version that is unsupported in most browsers. 
- Start from / and follow the instructions to get your flag.

**P.S. Do chmod 755 for Linux/OSX and [disable Gatekeeper](https://disable-gatekeeper.github.io/) for OSX.**

### Solution
запустить сервер: `./http_server.linux`
    
`nc 127.0.0.1 60592`

``` 
GET / H/1.1337

H/1.1337 302 Found
location: /get_my_flag
content-length: 0
date: Thu, 18 Jan 2024 10:27:46 GMT
```

next 

```
GET /get_my_flag H/1.1337

H/1.1337 200 OK
content-length: 25
date: Thu, 18 Jan 2024 10:28:09 GMT

Now POST to the same URI!
```

next

```
POST /get_my_flag H/1.1337

H/1.1337 200 OK
content-length: 36
date: Thu, 18 Jan 2024 10:28:38 GMT

Now POST body "give_me_flag_please!"
```

and finally

```
POST /get_my_flag H/1.1337
Host: 127.0.0.1:60592
Content-Type:text/plain
Content-Length:20

give_me_flag_please!
H/1.1337 200 OK
content-length: 38
date: Thu, 18 Jan 2024 10:28:55 GMT

EXAM{051e3aae826ecbc955354d847e594b90}
```

## Task 4
- You're given a binary for Linux/OSX Arm/OSX Intel/Windows that works as TCP server. Your goal is to connect to the TCP port the program listens, so find the port first. Your source port must be the same as the destination port.

- After the connection is established - send the "getflag" command. No more, no less. No quotes, no CRLF.

- Look into console output to get the idea why it's not working. Trial and error are expected.

    **P.S. Do chmod 755 for Linux/OSX and disable Gatekeeper for OSX.**

### Solution
запускаем сервер

`./tcp_server.linux`

ищем порт

`lsof -i -P -n | grep LISTEN`

```
code       19816 wyrm   47u  IPv4  48908      0t0  TCP 127.0.0.1:41637 (LISTEN)
tcp_porto 167399 wyrm    3u  IPv6 357516      0t0  TCP [::1]:64231 (LISTEN)
```

`echo -n "getflag" | nc -6 -s ::2 -p 64231 ::1 64231`

```
EXAM{adf6a79bb57a6c314047e47b77205d4d}
```


## Task 5

- Do you remember the chat lab? :) Will all these fake flags and poems being sent?

- You have a traffic dump here, so your goal is to find the flag into all this chat.. And the traffic was collected via WIFI monitor mode.

- Router IP is 192.168.0.1

    Enjoy.

### Solution

using crunch to generate all possible keys

`crunch 5 5 -t 0123456789 -o 5keys.txt`

`aircrack-ng -n 64 -w 5keys.txt file.pcap`

got 

```
 KEY FOUND! [ 31:36:30:36:33 ] (ASCII: 16063 )
	Decrypted correctly: 100%

```

`airdecap-ng -w 31:36:30:36:33 -o output.pcap file.pcap`

using wireshark to find flag

```
EXAM{293359e14306567e8a18f37f5761c022}
```
## Task 6
- You're given a binary
  for [Linux](task06.linux)/[OSX M1/M2](task06.armmac)/[OSX Intel](task06.x64mac)/[Windows](task06.exe) that listens TCP
  port 4888 with SNI-enabled SSL/TLS.
- Your goal is to connect to the server with correct parameters and send "getflag" command.
- Look into console output to get the idea why it's not working. Trial and error are expected.
    
    **P.S. Do chmod 755 for Linux/OSX and [disable Gatekeeper](https://disable-gatekeeper.github.io/) for OSX.**

### Solutiongetflag
подключаемся к серверу

`./tlss.linux`

надо получать имена серверов без выпендрежа через nmap:

`nmap -p 4888 --script ssl-cert 127.0.0.1`

```
Starting Nmap 7.93 ( https://nmap.org ) at 2024-01-18 12:34 EET
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00014s latency).

PORT     STATE SERVICE
4888/tcp open  xcap-portal
| ssl-cert: Subject: commonName=rcgen self signed cert
| Subject Alternative Name: DNS:gmsobneezkoosuy.nup23.local, DNS:ovnyxsgixfkrhca.nup23.local, DNS:ggpimoukletgafy.nup23.local, DNS:gimjqgiedrcpbag.nup23.local, DNS:eekltjmfpkavoxj.nup23.local
| Issuer: commonName=rcgen self signed cert
| Public Key type: ec
| Public Key bits: 256
| Signature Algorithm: ecdsa-with-SHA256
| Not valid before: 1975-01-01T00:00:00
| Not valid after:  4096-01-01T00:00:00
| MD5:   61cd951c1bb61232702acbc2e140c825
|_SHA-1: da3a5bdba78b1545ed484a6c3d701a25ca6e64b4

Nmap done: 1 IP address (1 host up) scanned in 0.33 seconds
```

подключаемся к серверу с указанием нужного нам сервера (конечно это последний)

`openssl s_client -connect 127.0.0.1:4888 -servername eekltjmfpkavoxj.nup23.local`

и здесь надо ввести `getflag`

```
CONNECTED(00000003)
depth=0 CN = rcgen self signed cert
verify error:num=18:self-signed certificate
verify return:1
depth=0 CN = rcgen self signed cert
verify return:1
---
бла-бла-бла
---
read R BLOCK
Fine, now send me the command
getflagEXAM{205eb791f0fe0b5b4288009cf468254b}closed
```

отправлять нужно через ctrl+d а не Enter

EXAM{205eb791f0fe0b5b4288009cf468254b}

## Task 7

- You're given a pcap file with captured traffic of unknown protocol. Also, you're given the protocol details in writings. Your goal is to reverse engineer the protocol, collect the data and find the flag.

### Solution

EXAM{e5c2f2b2f2b2f2b2f2b2f2b2f2b2f2b2}