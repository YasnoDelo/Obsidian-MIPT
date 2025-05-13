### R1
```
 conf t
 int g2/0
  ip add 192.168.12.1 255.255.255.0
  no sh
  int g1/0
  ip add 192.168.13.1 255.255.255.0
  no sh
  do sh ip int br
  router ospf 1
  net 192.168.13.0 0.0.0.255 a 0
  red con subnets

int g2/0
 standby 1 ip 192.168.12.10
 standby 1 preempt
 do show history
 
track 1 ip route 3.3.3.3/21 reachability

int g2/0
standby 1 track 1 decrement 20

```

### R2
```
 conf t
  int g1/0
  ip add 192.168.12.2 255.255.255.0
  no sh
  int f0/0
  ip add 192.168.23.2 255.255.255.0
  no sh
  router ospf 1
    red con subnets
    do show history
    net 192.168.23.0 0.0.0.255 a 0
int g1/0
 standby 1 ip 192.168.12.10
 standby 1 preempt
 do show history

track 1 ip route 3.3.3.3/21 reachability

int g1/0
standby 1 track 1 decrement 20
  
```

### R3
```
 int f0/0
  ip add 192.168.13.3 255.255.255.0
  no sh
  int g1/0
  ip add 192.168.23.3 255.255.255.0
  no sh

int lo0
ip add 3.3.3.3 255.255.255.255
  
router ospf 1
red con subnets
    net 192.168.23.0 0.0.0.255 a 0
    net 192.168.13.0 0.0.0.255 a 0
```