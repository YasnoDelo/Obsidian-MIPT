### R1 //SLB
```
conf t

int f0/0
ip add 192.168.0.1 255.255.255.0
no sh

int g1/0
ip add 192.168.1.1 255.255.255.0
no sh

ip slb serverfarm sf1
nat server
real 192.168.1.5 23
inservice
real 192.168.1.6 23
inservice
exit

ip slb vserver SF1
serverfarm sf1
virtual 1.1.1.1 tcp 23
inservice
exit
```

### R2 // Client 1
```
conf t

int f0/0
ip add 192.168.0.2 255.255.255.0
no sh

ip route 1.1.1.1 255.255.255.255 192.168.0.1

```

### R3 // Client 2
```
conf t

int f0/0
ip add 192.168.0.3 255.255.255.0
no sh

ip route 1.1.1.1 255.255.255.255 192.168.0.1

```

### R4 // Inet
```
conf t

int f0/0
ip add 192.168.0.4 255.255.255.0
no sh
```

### R5 // Server 1
```
conf t

int g1/0
ip add 192.168.1.5 255.255.255.0
no sh

line vty 0 1869
pass cisco
enable secret cisco

ip route 0.0.0.0 0.0.0.0 192.168.1.1
```

### R6 // Server 2
```
conf t

int g1/0
ip add 192.168.1.6 255.255.255.0
no sh

line vty 0 1869
pass cisco
enable secret cisco

ip route 0.0.0.0 0.0.0.0 192.168.1.1
```