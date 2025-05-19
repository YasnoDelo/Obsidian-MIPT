PC1
```
ip 10.10.1.2/24
```

PC2
```
ip 10.10.2.2/24
```

R1
```
conf t

int f1/0
no sh 
ip add 10.10.1.1 255.255.255.0

int se4/3
no sh
ip add 10.10.13.1 255.255.255.0

int tun0
ip add 192.168.14.1 255.255.255.0 
tunnel mode gre ip
tunnel source se4/3
tunnel destination 172.0.0.4

router ospf 1
net 192.168.14.0 0.0.0.255 a 0
red con sub

ip route 172.0.0.0 255.255.255.0 10.10.13.3

ip route 10.10.2.0 255.255.255.0 10.10.13.3 200
```

R2
```
conf t

int f1/0
no sh 
ip add 10.10.2.1 255.255.255.0

int se4/3
no sh
ip add 10.10.23.2 255.255.255.0

int tun1
ip add 192.168.24.2 255.255.255.0 
tunnel mode gre ip
tunnel source se4/3
tunnel destination 172.0.0.4

router ospf 1
net 192.168.24.0 0.0.0.255 a 0
red con sub

ip route 172.0.0.0 255.255.255.0 10.10.23.3
ip route 10.10.1.0 255.255.255.0 10.10.23.3 200
```

R3
```
conf t

int se4/1
no sh
ip add 10.10.13.3 255.255.255.0

int se4/2
no sh
ip add 10.10.23.3 255.255.255.0

int se4/4
no sh
ip add 172.0.0.3 255.255.255.0

ip route 10.10.2.0 255.255.255.0 10.10.23.2
ip route 10.10.1.0 255.255.255.0 10.10.13.1
```

R4
```
conf t

int se4/3
no sh
ip add 172.0.0.4 255.255.255.0

int tun0
ip add 192.168.14.4 255.255.255.0 
tunnel mode gre ip
tunnel source se4/3
tunnel destination 10.10.13.1

int tun1
ip add 192.168.24.4 255.255.255.0 
tunnel mode gre ip
tunnel source se4/3
tunnel destination 10.10.23.2

ip route 10.10.23.0 255.255.255.0 172.0.0.3
ip route 10.10.13.0 255.255.255.0 172.0.0.3

router ospf 1
network 192.168.14.0 0.0.0.255 a 0
network 192.168.24.0 0.0.0.255 a 0
```