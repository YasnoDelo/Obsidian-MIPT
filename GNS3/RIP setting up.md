R1

```
conf t
int e2/2
ip add 192.168.12.1 255.255.255.0
no sh


int e2/3
ip add 192.168.13.1 255.255.255.0
no sh

router rip
version 2
no auto-summary
network 192.168.12.0     ##--- interface in this subnet recives and sends                                 ##    RIP-requests
network 192.168.13.0

redistribute connected
passive-int lo0
```

network 192.168.12.0
network 192.168.13.0

R2

```
conf t
int e2/3
ip add 192.168.23.2 255.255.255.0
no sh


int e2/1
ip add 192.168.12.2 255.255.255.0
no sh

router rip
version 2
no auto-summary
network 192.168.23.0
network 192.168.12.0
```

R3

```
conf t
int e2/1
ip add 192.168.13.3 255.255.255.0
no sh


int e2/2
ip add 192.168.23.3 255.255.255.0
no sh

router rip
version 2
no auto-summary
network 192.168.23.0
network 192.168.13.0
```
