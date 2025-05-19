R1
```
conf t

int se3/2
ip add 192.168.12.1 255.255.255.252
enc hdlc
no sh

router ospf 1
net 192.168.12.0 0.0.0.3 a 0
```

R2
```
conf t

int se3/1
ip add 192.168.12.2 255.255.255.252
enc hdlc
no sh

int se3/3
ip add 192.168.23.2 255.255.255.252
enc hdlc
no sh

router ospf 1
net 192.168.12.0 0.0.0.3 a 0
net 192.168.23.0 0.0.0.3 a 0
```

R3
```
conf t

int se3/2
ip add 192.168.23.1 255.255.255.252
enc hdlc
no sh

router ospf 1
net 192.168.23.0 0.0.0.3 a 0
```