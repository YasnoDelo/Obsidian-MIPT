R1
```
conf t
int f0/0
no sh

int f0/0.112
encapsulation dot1Q 11 second-dot1q 2
ip add 192.168.0.1 255.255.255.0

int f0/0.113
encapsulation dot1Q 11 second-dot1q 3
ip add 192.168.1.1 255.255.255.0

int f0/0.122
encapsulation dot1Q 12 second-dot1q 2
ip add 192.168.2.1 255.255.255.0

int f0/0.123
encapsulation dot1Q 12 second-dot1q 3
ip add 192.168.3.1 255.255.255.0
```
![[Pasted image 20250517194456.png]]
PC1
```
ip 192.168.0.2/24 192.168.0.1
```

PC2
```
ip 192.168.1.2/24 192.168.1.1
```
PC3
```
ip 192.168.2.2/24 192.168.2.1
```
PC4
```
ip 192.168.3.2/24 192.168.3.1
```
PC5
```
ip 192.168.0.3/24 192.168.0.1
```
PC6
```
ip 192.168.1.3/24 192.168.1.1
```
PC7
```
ip 192.168.2.3/24 192.168.2.1
```
PC8
```
ip 192.168.3.3/24 192.168.3.1
```

Теперь настроим безотказную систему с балансировкой по VLAN с помощью HSRP
R1:
```
int f0/0
no sh

int f0/0.112
encapsulation dot1Q 11 second-dot1q 2
ip add 192.168.0.11 255.255.255.0

standby 2 ip 192.168.0.1
standby 2 preempt
standby 2 timers 3 10
standby 2 prio 120

int f0/0.113
encapsulation dot1Q 11 second-dot1q 3
ip add 192.168.1.11 255.255.255.0

standby 2 ip 192.168.1.1
standby 2 preempt
standby 2 timers 3 10
standby 2 prio 120

int f0/0.122
encapsulation dot1Q 12 second-dot1q 2
ip add 192.168.2.11 255.255.255.0

standby 1 ip 192.168.2.1
standby 1 preempt
standby 1 timers 3 10
standby 1 prio 80

int f0/0.123
encapsulation dot1Q 12 second-dot1q 3
ip add 192.168.3.11 255.255.255.0

standby 1 ip 192.168.3.1
standby 1 preempt
standby 1 timers 3 10
standby 1 prio 80
```

R2:
```
int f0/0
no sh

int f0/0.112
encapsulation dot1Q 11 second-dot1q 2
ip add 192.168.0.12 255.255.255.0

standby 2 ip 192.168.0.1
standby 2 preempt
standby 2 timers 3 10

int f0/0.113
encapsulation dot1Q 11 second-dot1q 3
ip add 192.168.1.12 255.255.255.0

standby 2 ip 192.168.1.1
standby 2 preempt
standby 2 timers 3 10

int f0/0.122
encapsulation dot1Q 12 second-dot1q 2
ip add 192.168.2.12 255.255.255.0

standby 1 ip 192.168.2.1
standby 1 preempt
standby 1 timers 3 10

int f0/0.123
encapsulation dot1Q 12 second-dot1q 3
ip add 192.168.3.12 255.255.255.0

standby 1 ip 192.168.3.1
standby 1 preempt
standby 1 timers 3 10
```