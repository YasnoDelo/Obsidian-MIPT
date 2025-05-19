R1
```
conf t

int f0/0
no sh
ip add 4.4.4.1 255.255.255.0

int f0/1
no sh

int f0/1.2
enc dot1q 2
ip add 10.10.12.1 255.255.255.0

int f0/1.3
enc dot1q 3
ip add 10.10.13.1 255.255.255.0

int f0/1.4
enc dot1q 4
ip add 10.10.14.1 255.255.255.0

zone security IN
zone security OUT
zone security DMZ

zone-pair sec DMZ2OUT sou DMZ dest OUT
zone-pair sec OUT2DMZ sou OUT dest DMZ
zone-pair sec IN2DMZ sou IN dest DMZ

ip access-list extended VLAN2
permit ip 10.10.12.0 0.0.0.255 any

ip access-list extended VLAN3
permit ip 10.10.13.0 0.0.0.255 any

ip access-list extended VLAN3
permit ip 10.10.12.0 0.0.0.255 any

class-map type ins ICMP_VLAN3
match prot icmp
match acc name VLAN3

class-map type ins HTTP_VLAN3
match prot http
match acc name VLAN3

class-map type ins DMZ2OUT
match prot http

class-map type ins TELNET_VLAN2
match prot telnet
match acc name VLAN2

class-map type ins HTTP_match
match prot http

policy-map type inspect DMZ2OUT
class HTTP_match
pass

policy-map type inspect OUT2DMZ
class HTTP_match
pass

zone-pair secu DMZ2OUT
serv type inspect DMZ2OUT
zone-pair sec OUT2DMZ
serv type inspect OUT2DMZ

int f0/1.4
zone-member sec DMZ

int f0/0
zone-member sec OUT

```

R2
```
conf t

int f0/0
no sh
ip add 10.10.12.2 255.255.255.0
```

R3
```
conf t

int f0/0
no sh
ip add 10.10.13.3 255.255.255.0
```

R4
```
conf t

int f0/0
no sh
ip add 10.10.14.4 255.255.255.0

ip route 0.0.0.0 0.0.0.0 10.10.14.1


line vty 0 1869
  password pass
  login
```

R5
```
conf t

int f0/0
no sh
ip add 4.4.4.4 255.255.255.0

ip route 0.0.0.0 0.0.0.0 4.4.4.1

```