## Task 1 Solution

поебаться с настройками подсчета чексам для ipv4 и udp
    
`udp && ip.checksum_bad.expert && (eth.dst[0] & 1)`

win


## Task 2 Solution
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

## Task 3 Solution
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
# Define a hexadecimal string
hex_string = "4558414D7B3966356662363331396162303665653961373965303435 3535346230373166667D"

# Use bytes.fromhex() to convert the hexadecimal string to bytes
hex_bytes = bytes.fromhex(hex_string)

# Use decode("utf-8") to convert the bytes to a UTF-8 encoded string
ascii_string = hex_bytes.decode("utf-8")

# Print the result
print(ascii_string)
```

we get flag `EXAM{9f5fb6319ab06ee9a79e045554b071ff}`