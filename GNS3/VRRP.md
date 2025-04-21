### Main router upstairs
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

### Main in 201 subn, backup in 202 subn
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
### Main in 202 subn, backup in 201 subn
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

### All daughter routers
```
ip route 0.0.0.0 0.0.0.0 192.168.201.1 - defaulf gateway to virtual router
```

Можно использовать `standby 1 track 1 decrement 20`, где [[Track|track]] это некоторое отслеживаемое условие