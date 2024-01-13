## Task 1 
- You're given a [pcap file](task01.pcap) with large ( > 100000 ) amount of packets
- Your goal is to find the flag into **multicast** UDP **packet** with **broken** IP checksum.
- This the only packet contains flag


### Solution
поебаться с настройками подсчета чексам для ipv4 и udp
    
`udp && ip.checksum_bad.expert && (eth.dst[0] & 1)`

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

`dig @127.0.0.1 -p 6053 -t AXFR wozyypjafnvolbg.nup23.local`

```
; <<>> DiG 9.18.20 <<>> @127.0.0.1 -p 6053 -t AXFR wozyypjafnvolbg.nup23.local
; (1 server found)
;; global options: +cmd
wozyypjafnvolbg.nup23.local. 60	IN	SOA	wozyypjafnvolbg.nup23.local. wozyypjafnvolbg.nup23.local. 1535818019 3600 300 7200 60
wozyypjafnvolbg.nup23.local. 60	IN	A	1.2.3.4
wozyypjafnvolbg.nup23.local. 60	IN	CNAME	google.com.
wozyypjafnvolbg.nup23.local. 60	IN	TXT	"SRV is the key"
wozyypjafnvolbg.nup23.local. 60	IN	SRV	0 0 6053 _tcp._axfr.wozyypjafnvolbg.nup23.local.
wozyypjafnvolbg.nup23.local. 60	IN	TYPE31337 \# 38 4558414D7B3966356662363331396162303665653961373965303435 3535346230373166667D
wozyypjafnvolbg.nup23.local. 60	IN	SOA	wozyypjafnvolbg.nup23.local. wozyypjafnvolbg.nup23.local. 1535818019 3600 300 7200 60
;; Query time: 0 msec
;; SERVER: 127.0.0.1#6053(127.0.0.1) (TCP)
;; WHEN: Fri Jan 12 22:07:34 EET 2024
;; XFR size: 7 records (messages 1, bytes 292)
```

using next python script

```python
hex_string = "4558414D7B3966356662363331396162303665653961373965303435 3535346230373166667D"

hex_bytes = bytes.fromhex(hex_string)
ascii_string = hex_bytes.decode("utf-8")

print(ascii_string)
```

we get flag `EXAM{9f5fb6319ab06ee9a79e045554b071ff}`


## Task 3 
- You're given a binary
  for [Linux](task03.linux)/[OSX M1/M2](task03.armmac)/[OSX Intel](task03.x64mac)/[Windows](task03.exe) that works as an HTTP server.
- This HTTP server uses H/1.1337 HTTP version that is unsupported in most browsers. 
- Start from / and follow the instructions to get your flag.

**P.S. Do chmod 755 for Linux/OSX and [disable Gatekeeper](https://disable-gatekeeper.github.io/) for OSX.**

### Solution
запустить сервер (маки лохи) : `./http_server`
    
`nc 127.0.0.1 60592`

``` 
GET / H/1.1337

H/1.1337 302 Found
location: /get_my_flag
content-length: 0
date: Fri, 12 Jan 2024 19:31:30 GMT
```

next 

```
GET /get_my_flag H/1.1337

H/1.1337 200 OK
content-length: 25
date: Fri, 12 Jan 2024 19:31:57 GMT

Now POST to the same URI!
```

next

```
POST /get_my_flag H/1.1337

H/1.1337 200 OK
content-length: 36
date: Fri, 12 Jan 2024 19:37:10 GMT

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
date: Fri, 12 Jan 2024 19:59:12 GMT

EXAM{160ddf9a878275fc0fa959ec12ea3082}
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

`./task06.linux`

делаем запрос для получения сертификата:

`openssl s_client -connect 127.0.0.1:4888`

```
CONNECTED(00000003)
Can't use SSL_get_servername
depth=0 CN = rcgen self signed cert
verify error:num=18:self-signed certificate
verify return:1
depth=0 CN = rcgen self signed cert
verify return:1
---
Certificate chain
 0 s:CN = rcgen self signed cert
   i:CN = rcgen self signed cert
   a:PKEY: id-ecPublicKey, 256 (bit); sigalg: ecdsa-with-SHA256
   v:NotBefore: Jan  1 00:00:00 1975 GMT; NotAfter: Jan  1 00:00:00 4096 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIB6jCCAZCgAwIBAgIVAP05fqVmLYW+krOtk+Jjdfpyl5X4MAoGCCqGSM49BAMC
MCExHzAdBgNVBAMMFnJjZ2VuIHNlbGYgc2lnbmVkIGNlcnQwIBcNNzUwMTAxMDAw
MDAwWhgPNDA5NjAxMDEwMDAwMDBaMCExHzAdBgNVBAMMFnJjZ2VuIHNlbGYgc2ln
bmVkIGNlcnQwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAAReFp5+T2YWPEfofw5M
33pCNM7ui2p0kz7Zd7QXzK/nKBzFPyKrTzF/vm1xAPbFJYb8w3krKt35/Apie0Pt
0CeOo4GiMIGfMIGcBgNVHREEgZQwgZGCG25scXN2dXlhcmN2c2lnbi5udXAyMy5s
b2NhbIIbd3Nkc21pbWJhZ2RhdXF6Lm51cDIzLmxvY2Fsghtyd29xcm9lcWN5cWll
YXcubnVwMjMubG9jYWyCG2ZjdGNoc2l2emphcm5tcC5udXAyMy5sb2NhbIIba2F4
anF5bHFkc2JyaHB2Lm51cDIzLmxvY2FsMAoGCCqGSM49BAMCA0gAMEUCIF5xP62Z
wBcC9hfWirM+ZrjtMuAGUC5y3Xv7psWe6pJJAiEA/HfuwxiNlPPpkcIG8HowiSf+
lZXNqAkQj6a+f1OBxr0=
-----END CERTIFICATE-----
subject=CN = rcgen self signed cert
issuer=CN = rcgen self signed cert
---
No client certificate CA names sent
Peer signing digest: SHA256
Peer signature type: ECDSA
Server Temp Key: X25519, 253 bits
---
SSL handshake has read 866 bytes and written 375 bytes
Verification error: self-signed certificate
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Server public key is 256 bit
This TLS version forbids renegotiation.
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 18 (self-signed certificate)
---
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 9928FBDC4EC320E15CD1F63578FB81C2C753BFCF02C02681C0F85D36D8FE714E
    Session-ID-ctx: 
    Resumption PSK: 2951CCCDCBDB6F4039532E57450E20AEE8CC69308BA96BF24A7F10592E8966035897E75596BF3B127A511CFD70A99A74
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 86400 (seconds)
    TLS session ticket:
    0000 - b3 d6 fb d0 03 73 ca 8c-03 14 27 aa c6 d5 9f dc   .....s....'.....
    0010 - fa 2f f9 6c 6d 4b bb 49-97 11 4e 5a f0 b0 55 e6   ./.lmK.I..NZ..U.

    Start Time: 1705159932
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 1A05D217DFE966FBBB4EC75BE7AD0C2D86A19C48BC38296B3F45BAF726DB39DA
    Session-ID-ctx: 
    Resumption PSK: 6DA2A3EDB2CC4E0B45CE93C0338A1204D18CA9A816E753F0E571C67BB68C9EDF405065A1FE4D19E1F8DCD143956BCB6B
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 86400 (seconds)
    TLS session ticket:
    0000 - 96 c5 94 12 1a 3c 93 27-05 cd a1 1a 9c 33 e6 c4   .....<.'.....3..
    0010 - b7 e8 63 75 02 0b da 63-41 32 fb 7d 29 59 94 97   ..cu...cA2.})Y..

    Start Time: 1705159932
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 1401EE2C36C7DEC521D8D04657226DD47C8D796AE882B5D2B53720B9E7CB8E13
    Session-ID-ctx: 
    Resumption PSK: 9B0E25B83F311053FF8C0323B01ED41F2856F368863A136AC4563CD909915058E72FCBE2685D1A3BE18CD962C0282A2E
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 86400 (seconds)
    TLS session ticket:
    0000 - 53 e3 b8 bb af a8 b2 15-d7 06 7f 73 b7 20 71 e0   S..........s. q.
    0010 - c1 d2 d5 44 4a e7 28 1f-56 82 fb 18 23 39 97 9c   ...DJ.(.V...#9..

    Start Time: 1705159932
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 13541FB7C6FC77AFFFF1C49B29CCB35AF67608A3CA19D01E1293D011DB290C1A
    Session-ID-ctx: 
    Resumption PSK: 662B7B9D335A67B8311C4FEDEA8D4003DBD76FFC1628B08AE2E461259DC59FC71D5D899308C80A98077B881DB917B928
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 86400 (seconds)
    TLS session ticket:
    0000 - c0 ef 37 7b 9d 93 fc 2b-fe 5b 9b 4f da fc cf cb   ..7{...+.[.O....
    0010 - f0 8d 2d fe 9f d2 f7 2d-d7 ae 0e 0e b0 63 51 5e   ..-....-.....cQ^

    Start Time: 1705159932
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
Please specify a server name
closed
```

из сертификата достаем названия серверов:

`openssl x509 -in cert.pem -text -noout`

```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            fd:39:7e:a5:66:2d:85:be:92:b3:ad:93:e2:63:75:fa:72:97:95:f8
        Signature Algorithm: ecdsa-with-SHA256
        Issuer: CN = rcgen self signed cert
        Validity
            Not Before: Jan  1 00:00:00 1975 GMT
            Not After : Jan  1 00:00:00 4096 GMT
        Subject: CN = rcgen self signed cert
        Subject Public Key Info:
            Public Key Algorithm: id-ecPublicKey
                Public-Key: (256 bit)
                pub:
                    04:5e:16:9e:7e:4f:66:16:3c:47:e8:7f:0e:4c:df:
                    7a:42:34:ce:ee:8b:6a:74:93:3e:d9:77:b4:17:cc:
                    af:e7:28:1c:c5:3f:22:ab:4f:31:7f:be:6d:71:00:
                    f6:c5:25:86:fc:c3:79:2b:2a:dd:f9:fc:0a:62:7b:
                    43:ed:d0:27:8e
                ASN1 OID: prime256v1
                NIST CURVE: P-256
        X509v3 extensions:
            X509v3 Subject Alternative Name: 
                DNS:nlqsvuyarcvsign.nup23.local, DNS:wsdsmimbagdauqz.nup23.local, DNS:rwoqroeqcyqieaw.nup23.local, DNS:fctchsivzjarnmp.nup23.local, DNS:kaxjqylqdsbrhpv.nup23.local
    Signature Algorithm: ecdsa-with-SHA256
    Signature Value:
        30:45:02:20:5e:71:3f:ad:99:c0:17:02:f6:17:d6:8a:b3:3e:
        66:b8:ed:32:e0:06:50:2e:72:dd:7b:fb:a6:c5:9e:ea:92:49:
        02:21:00:fc:77:ee:c3:18:8d:94:f3:e9:91:c2:06:f0:7a:30:
        89:27:fe:95:95:cd:a8:09:10:8f:a6:be:7f:53:81:c6:bd
```

P.S. надо получать имена серверов без выпендрежа через nmap:

`nmap -p 4888 --script ssl-cert 127.0.0.1`

подключаемся к серверу с указанием нужного нам сервера (конечно это последний)

`openssl s_client -connect 127.0.0.1:4888 -servername kaxjqylqdsbrhpv.nup23.local`

```
CONNECTED(00000003)

---

read R BLOCK
Fine, now send me the command
```

и здесь надо ввести `getflag`, но через echo

`echo -n "getflag" | openssl s_client -connect 127.0.0.1:4888 -servername kaxjqylqdsbrhpv.nup23.local`

```
CONNECTED(00000003)
depth=0 CN = rcgen self signed cert
verify error:num=18:self-signed certificate
verify return:1
depth=0 CN = rcgen self signed cert
verify return:1
---
Certificate chain
 0 s:CN = rcgen self signed cert
   i:CN = rcgen self signed cert
   a:PKEY: id-ecPublicKey, 256 (bit); sigalg: ecdsa-with-SHA256
   v:NotBefore: Jan  1 00:00:00 1975 GMT; NotAfter: Jan  1 00:00:00 4096 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIB6jCCAZCgAwIBAgIVAP05fqVmLYW+krOtk+Jjdfpyl5X4MAoGCCqGSM49BAMC
MCExHzAdBgNVBAMMFnJjZ2VuIHNlbGYgc2lnbmVkIGNlcnQwIBcNNzUwMTAxMDAw
MDAwWhgPNDA5NjAxMDEwMDAwMDBaMCExHzAdBgNVBAMMFnJjZ2VuIHNlbGYgc2ln
bmVkIGNlcnQwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAAReFp5+T2YWPEfofw5M
33pCNM7ui2p0kz7Zd7QXzK/nKBzFPyKrTzF/vm1xAPbFJYb8w3krKt35/Apie0Pt
0CeOo4GiMIGfMIGcBgNVHREEgZQwgZGCG25scXN2dXlhcmN2c2lnbi5udXAyMy5s
b2NhbIIbd3Nkc21pbWJhZ2RhdXF6Lm51cDIzLmxvY2Fsghtyd29xcm9lcWN5cWll
YXcubnVwMjMubG9jYWyCG2ZjdGNoc2l2emphcm5tcC5udXAyMy5sb2NhbIIba2F4
anF5bHFkc2JyaHB2Lm51cDIzLmxvY2FsMAoGCCqGSM49BAMCA0gAMEUCIF5xP62Z
wBcC9hfWirM+ZrjtMuAGUC5y3Xv7psWe6pJJAiEA/HfuwxiNlPPpkcIG8HowiSf+
lZXNqAkQj6a+f1OBxr0=
-----END CERTIFICATE-----
subject=CN = rcgen self signed cert
issuer=CN = rcgen self signed cert
---
No client certificate CA names sent
Peer signing digest: SHA256
Peer signature type: ECDSA
Server Temp Key: X25519, 253 bits
---
SSL handshake has read 869 bytes and written 343 bytes
Verification error: self-signed certificate
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Server public key is 256 bit
This TLS version forbids renegotiation.
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 18 (self-signed certificate)
---
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 8C7622817B4AE5EAD3A709C94C0A64C825FFB1DCFF31D70ACF44732E0CAF8439
    Session-ID-ctx: 
    Resumption PSK: B033BEBDA88833F6A326965D9B6C8978B1D19981D93747D081FA4769B604E85DE898ABA25F1F31F39BB2CD4E5B886CC0
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 86400 (seconds)
    TLS session ticket:
    0000 - 87 36 36 b5 39 6a 16 73-40 c2 1b ed fd 84 09 7e   .66.9j.s@......~
    0010 - 11 e6 e5 49 ce d4 1d f0-80 31 eb 8f 23 6d 7e e8   ...I.....1..#m~.

    Start Time: 1705162469
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 724A7393D120D923D6EE0A8F5388E323BD0E92F33D86C83FDA6B6238B92A6F19
    Session-ID-ctx: 
    Resumption PSK: EDCD0E252D80D57003948DECDC139C69C8448001A6B883F829F0B9D4B4D4DE50A8C85A5A7F497A2A660B756668042440
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 86400 (seconds)
    TLS session ticket:
    0000 - 4d be 27 34 5f 34 7c 08-e6 63 45 9b 31 52 af 7d   M.'4_4|..cE.1R.}
    0010 - 62 c2 98 45 da a5 14 49-68 73 6c 20 2c 3b d8 94   b..E...Ihsl ,;..

    Start Time: 1705162469
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 41B5F05D3556F5C89425098C6FB3FCD27131E1130E016BB2F48FFD50A12AAF52
    Session-ID-ctx: 
    Resumption PSK: 19FF7538E7378715B90DFDC8C1812DC566C428F30ACD100F881C9C4C761BE3E3167B888C150ACEFCD2997B138434F132
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 86400 (seconds)
    TLS session ticket:
    0000 - c5 94 d2 e9 78 20 75 cf-9c 76 1c b5 c4 11 98 62   ....x u..v.....b
    0010 - 80 de 70 2a c5 06 5e 43-28 d4 a9 97 e1 70 7e f7   ..p*..^C(....p~.

    Start Time: 1705162469
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 45E4D5A4ABCB44C44509346F91C3DA1914778BB2402C2CBD56531957F438C495
    Session-ID-ctx: 
    Resumption PSK: 0E6125753949F5831E021F1C9E78369C7BB8C3DA5EF8534B52F69B6A2DB4B1043B2B22D452AF62BA14A13FC7FDE580CB
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 86400 (seconds)
    TLS session ticket:
    0000 - dc 01 c8 b4 9a c4 88 3a-10 9c 9d 08 e6 4e b3 47   .......:.....N.G
    0010 - 05 3c 02 39 f5 cd 7f ac-cb 6f 22 55 97 90 54 4c   .<.9.....o"U..TL

    Start Time: 1705162469
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
Fine, now send me the command
getflag


NUP23{T3st_3x4m_t4sk_4}
```

отправлять нужно через ctrl+d а не Enter