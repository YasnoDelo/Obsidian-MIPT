![[Pasted image 20250515160700.png]]
R1
```
conf t

int g1/0
ip add 1.0.12.2 255.255.255.0
no sh

int g2/0
ip add 1.0.14.1 255.255.255.0
no sh

int f0/0
ip add 1.0.13.3 255.255.255.0
no sh

router ospf 1
net 1.0.13.0 0.0.0.255 a 0
net 1.0.12.0 0.0.0.255 a 0
red con sub

```

R2
```
conf t

int g1/0
ip add 1.0.12.1 255.255.255.0
no sh

int g2/0
ip add 1.0.23.3 255.255.255.0
no sh

router ospf 1
net 1.0.23.0 0.0.0.255 a 0
net 1.0.12.0 0.0.0.255 a 0
red con sub

```

R3
```
conf t

int g1/0
ip add 1.0.23.2 255.255.255.0
no sh

int g2/0
ip add 1.0.36.3 255.255.255.0
no sh

int f0/0
ip add 1.0.13.1 255.255.255.0
no sh

router ospf 1
net 1.0.13.0 0.0.0.255 a 0
net 1.0.23.0 0.0.0.255 a 0
red con sub

```


R4
```
conf t

int g2/0
ip add 1.0.14.4 255.255.255.0
no sh

ip route 0.0.0.0 0.0.0.0 1.0.14.1

int tun0
tunnel mode gre ip
tunnel source 1.0.14.4
tunnel destination 1.0.36.6
keepalive

int s3/5
no sh
enc frame-relay 
exit
frame-relay switching 
int s3/5
frame-relay intf-type dce
frame-relay route 57 interface tun0 157
exit
do sh frame-relay map

```

R5
```
conf t

interface Serial3/4
no sh
no ip address
encapsulation frame-relay
ipv6 address 2001:57::5/64
ipv6 enable
serial restart-delay 0
frame-relay map ipv6 2001:57::7 57 broadcast
frame-relay interface-dlci 57


```

R6
```
conf t

int g2/0
ip add 1.0.36.6 255.255.255.0
no sh

ip route 0.0.0.0 0.0.0.0 1.0.36.3

int tun0
tunnel mode gre ip
tunnel source 1.0.36.6
tunnel destination 1.0.14.4
keepalive

int s3/7
no sh
enc frame-relay 
exit
frame-relay switching 
int s3/7
frame-relay intf-type dce
frame-relay route 75 interface tun0 157
do sh frame-relay map
```

R7
```
conf t

interface Serial3/6
no sh
no ip address
encapsulation frame-relay
ipv6 address 2001:57::7/64
ipv6 enable
serial restart-delay 0
frame-relay map ipv6 2001:57::5 75 broadcast
frame-relay interface-dlci 75

int f0/0
no sh

int f0/0.10
ipv6 enable
ipv6 unicast-routing


```

R8
```
conf t

int f0/0
no sh
ipv6 add autoconfig
```

R9
```
conf t

int f0/0
no sh
ipv6 add autoconfig
```

R10
```
conf t

int f0/0
no sh
ipv6 add autoconfig
```

R11
```
conf t

int f0/0
no sh
ipv6 add autoconfig
```