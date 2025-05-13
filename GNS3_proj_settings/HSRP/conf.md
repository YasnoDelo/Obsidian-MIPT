R1
```
conf t
int g1/0
ip add 192.168.14.1 255.255.255.0
no sh 

int f0/0
no sh

int f0/0.10
enc dot 10
ip add 192.168.10.1 255.255.255.0

int f0/0.20
enc dot 20
ip add 192.168.20.1 255.255.255.0

router ospf 1
net 192.168.14.0 0.0.0.255 a 0
red con subn



/// HSRP
int f0/0.10
standby 1 ip 192.168.10.123
standby 1 preempt
standby 1 timers 3 10

int f0/0.20
standby 2 ip 192.168.20.123
standby 2 preempt
standby 2 timers 3 10

```

R2
```
conf t
int g1/0
ip add 192.168.24.2 255.255.255.0
no sh 

int f0/0
no sh

int f0/0.10
enc dot 10
ip add 192.168.10.2 255.255.255.0

int f0/0.20
enc dot 20
ip add 192.168.20.2 255.255.255.0

router ospf 1
net 192.168.24.0 0.0.0.255 a 0
red con subn

int f0/0.10
standby 1 ip 192.168.10.123
standby 1 preempt
standby 1 timers 3 10

int f0/0.20
standby 2 ip 192.168.20.123
standby 2 preempt
standby 2 timers 3 10

```

R3
```
conf t
int g1/0
ip add 192.168.34.3 255.255.255.0
no sh 

int f0/0
no sh

int f0/0.10
enc dot 10
ip add 192.168.10.3 255.255.255.0

int f0/0.20
enc dot 20
ip add 192.168.20.3 255.255.255.0

router ospf 1
net 192.168.34.0 0.0.0.255 a 0
red con subn

int f0/0.10
standby 1 ip 192.168.10.123
standby 1 preempt
standby 1 timers 3 10

int f0/0.20
standby 2 ip 192.168.20.123
standby 2 preempt
standby 2 timers 3 10
```

R4
```
conf t
int f0/0
ip add 192.168.14.4 255.255.255.0
no sh 

int g1/0
ip add 192.168.24.4 255.255.255.0
no sh

int g2/0
ip add 192.168.34.4 255.255.255.0
no sh

int lo1
ip add 8.8.8.8 255.255.255.255
int lo0
ip add 4.4.4.4 255.255.255.255


router ospf 1
net 192.168.14.0 0.0.255.255 a 0
net 192.168.24.0 0.0.255.255 a 0
net 192.168.34.0 0.0.255.255 a 0

red con subn

```

PC1
```
ip 192.168.10.10/24 192.168.10.123
```

