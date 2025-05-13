### 2620 - left
```
conf t
int f0/0
no sh

int fa0/0.204
enc dot 204
ip add 192.168.204.20 255.255.255.0

int fa0/0.203
enc dot 203
ip add 192.168.203.20 255.255.255.0

```

### 1921 - left
```
conf t
int fa0/0
no sh

int fa0/0.202
enc dot 202
ip add 192.168.202.21 255.255.255.0

int fa0/0.201
enc dot 201
ip add 192.168.201.21 255.255.255.0

int fa0/0.203
enc dot 203
ip add 192.168.203.21 255.255.255.0

int f0/0.201
vrrp 201 ip 192.168.201.1
vrrp 201 priority 200
vrrp 201 preempt 
int f0/0.202
vrrp 202 ip 192.168.202.1
vrrp 202 preempt 

```
### 1941  - left
```
conf t
int fa0/0
no sh

int fa0/0.202
enc dot 202
ip add 192.168.202.41 255.255.255.0

int fa0/0.201
enc dot 201
ip add 192.168.201.41 255.255.255.0

int fa0/0.204
enc dot 204
ip add 192.168.204.41 255.255.255.0

int f0/0.201
vrrp 201 ip 192.168.201.1
vrrp 201 preempt 
int f0/0.202
vrrp 202 ip 192.168.202.1
vrrp 202 priority 200
vrrp 202 preempt 
```
### 3750-4 - left
```
conf t
vlan 202
exit

int vlan 202
no sh
exit 

vlan 201
exit

int vlan 201
no sh
exit

vlan 203
exit

int vlan 203
no sh
exit 

vlan 204
exit

int vlan 204
no sh
exit

int f2/3
switchport trunk encapsulation dot1q
switchport mode trunk
no sh

int f2/2
switchport trunk encapsulation dot1q
switchport mode trunk
no sh

int f2/1
switchport trunk encapsulation dot1q
switchport mode trunk
no sh

int f2/0
switchport trunk encapsulation dot1q
switchport mode trunk
no sh
```
### 3750-2 - left
```
conf t
vlan 202 
exit

int vlan 202
no sh
exit 

vlan 201
exit

int vlan 201
no sh
exit

int f2/0
switchport trunk encapsulation dot1q
switchport mode trunk
no sh

int f2/1
switchport trunk encapsulation dot1q
switchport mode trunk
no sh
```

### 1941 - right
```
conf t
int f0/0
ip add 192.168.201.141 255.255.255.0
no sh

ip route 0.0.0.0 0.0.0.0 192.168.201.1
```

### 3750-1 - right (3640)
```
conf t
int f0/0
ip add 192.168.202.140 255.255.255.0
no sh

ip route 0.0.0.0 0.0.0.0 192.168.202.1
```

### 3750-3  - right
```
conf t
vlan 202 
exit

int vlan 202
no sh
exit 

vlan 201
exit

int vlan 201
no sh
exit

int f2/1
switchport trunk encapsulation dot1q
switchport mode trunk
no sh

int f2/2
switchport acc vlan 201
switchport mode acc
no sh

int f2/3
switchport acc vlan  202
switchport mode acc
no sh
```

