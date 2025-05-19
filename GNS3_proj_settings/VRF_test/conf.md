R1
```
conf t

int f0/0
no sh
ip add 1.1.1.1 255.255.255.0

router ospf 2
net 1.1.1.0 0.0.0.255 a 0
```

R2
```
conf t

int f1/0
no sh
ip add 2.2.2.2 255.255.255.0

router ospf 3
net 2.2.2.0 0.0.0.255 a 0
```

R3
```
conf t

ip vrf A
description A subnet
rd 1:1
ip vrf B
description B subnet
rd 2:1

int f0/0
no sh
ip vrf forwarding A
ip add 1.1.1.3 255.255.255.0

int f1/0
no sh
ip vrf forwarding B
ip add 2.2.2.3 255.255.255.0

int f2/0
no sh
ip add 34.34.34.3 255.255.255.0

int lo0
ip address 1.1.3.1 255.255.255.252


int tun0
ip vrf forwarding A
ip add 35.35.0.3 255.255.255.0
tunnel mode gre ip
tunnel source lo0
tunnel destination 1.1.4.1
tunnel key 1


int tun1
ip vrf forwarding B
ip add 35.35.1.3 255.255.255.0
tunnel mode gre ip
tunnel source lo0
tunnel destination 1.1.4.1
tunnel key 2

router ospf 1
network 34.34.34.0 0.0.0.255 a 0
network 1.1.3.0 0.0.0.3 a 0

router ospf 2 vrf A 
network 1.1.1.0 0.0.0.255 area 0  
network 35.35.0.0 0.0.0.255 area 0

router ospf 3 vrf B
network 2.2.2.0 0.0.0.255 area 0  
network 35.35.1.0 0.0.0.255 area 0

```

R4
```
conf t

int f2/0
no sh
ip add 34.34.34.4 255.255.255.0

int f1/1
no sh
ip add 45.45.45.4 255.255.255.0

router ospf 1
network 34.34.34.0 0.0.0.255 a 0
network 45.45.45.0 0.0.0.255 a 0
```

R5
```
conf t

ip vrf A
description A subnet
rd 1:2
ip vrf B
description B subnet
rd 2:2

int f0/0
no sh
ip vrf forwarding A
ip add 3.3.3.5 255.255.255.0

int f1/0
no sh
ip vrf forwarding B
ip add 4.4.4.5 255.255.255.0

int f1/1
no sh
ip add 45.45.45.5 255.255.255.0

int lo1
ip address 1.1.4.1 255.255.255.252

int tun0
ip vrf forwarding A
ip add 35.35.0.5 255.255.255.0
tunnel mode gre ip
tunnel source lo1
tunnel destination 1.1.3.1
tunnel key 1

int tun1
ip vrf forwarding B
ip add 35.35.1.5 255.255.255.0
tunnel mode gre ip
tunnel source lo1
tunnel destination 1.1.3.1
tunnel key 2

router ospf 1
network 45.45.45.0 0.0.0.255 a 0
network 1.1.4.0 0.0.0.3 a 0

router ospf 2 vrf A 
network 3.3.3.0 0.0.0.255 area 0  
network 35.35.0.0 0.0.0.255 area 0

router ospf 3 vrf B
network 4.4.4.0 0.0.0.255 area 0  
network 35.35.1.0 0.0.0.255 area 0
```

R6
```
conf t

int f0/0
no sh
ip add 3.3.3.6 255.255.255.0

router ospf 2
net 3.3.3.0 0.0.0.255 a 0
```

R7
```
conf t

int f1/0
no sh
ip add 4.4.4.7 255.255.255.0

router ospf 3
net 4.4.4.0 0.0.0.255 a 0
```
