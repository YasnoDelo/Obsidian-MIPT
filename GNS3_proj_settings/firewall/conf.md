![[Pasted image 20250324192811.png]]

R1 (ZBF)
```
conf t
int f0/0
no sh
ip add 192.168.15.1 255.255.255.0

int g1/0
no sh
int g1/0.12
encap dot 12
ip add 192.168.12.1 255.255.255.0

int g1/0.13
encap dot 13
ip add 192.168.13.1 255.255.255.0

int g1/0.14
encap dot 14
ip add 192.168.14.1 255.255.255.0

router ospf 1
net 192.168.15.0 0.0.0.255 area 0
red con sub

int lo0
ip add 1.1.1.1 255.255.255.255

zone security IN
zone security OUT
zone security DMZ

exit

zone-pair secu IN2DMZ source IN dest DMZ
zone-pair secu OUT2DMZ source OUT dest DMZ
zone-pair secu IN2OUT source IN dest OUT

class-map type inspect Telnet11
match protocol telnet

exit

class-map type inspect Http11
match protocol http

exit

class-map type inspect Icmp11
match protocol icmp

policy-map type inspect IN2DMZ
class Telnet11
inspect
\\как pass, на туда и обратно гарантированно пройдёт, без проверки политики на пути обратно
class Http11
drop

policy-map type inspect IN2OUT
class Telnet11
inspect
class Icmp11
inspect

policy-map type inspect OUT2DMZ
class Telnet11
drop
class Http11
inspect

do sh policy-map type inspec //чтобы посмотреть, что наделали

zone-pair secu IN2DMZ
serv type inspect IN2DMZ
zone-pair secu OUT2DMZ 
serv type inspect OUT2DMZ 
zone-pair secu IN2OUT 
serv type inspect IN2OUT

int g1/0.12
zone-member sec IN
int g1/0.13
zone-member sec IN
int g1/0.14
zone-member sec DMZ
int f0/0
zone-member sec OUT

line vty 0 1869
pass cisco
login


```

R2
```
conf t
int f0/0
no sh
ip add 192.168.12.2 255.255.255.0
ip route 0.0.0.0 0.0.0.0 192.168.12.1
```

R3
```
conf t
int f0/0
no sh
ip add 192.168.13.3 255.255.255.0
ip route 0.0.0.0 0.0.0.0 192.168.13.1
```
R4
```
conf t
int f0/0
no sh
ip add 192.168.14.4 255.255.255.0
ip route 0.0.0.0 0.0.0.0 192.168.14.1

```

R5
```
conf t
int lo0
ip add 5.5.5.5 255.255.255.255

int f0/0
no sh
ip add 192.168.15.5 255.255.255.0
ip route 0.0.0.0 0.0.0.0 192.168.15.1

router ospf 1
net 0.0.0.0 0.0.0.0 area 0
```