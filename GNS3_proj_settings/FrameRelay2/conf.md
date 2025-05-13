FR SW 1
```
1 102 2 112
1 103 3 113
```
FR SW 2
```
2 101 1 112
```
FR SW 3
```
1 113 2 135
```

R5 (as a switch)
```
s3/0 135 s3/1 101

conf t
frame-rel switching
int s4/0
enc frame-r ietf
no sh
frame intf dte
frame-relay route 135 interface s4/1 101

int s4/1
enc frame-r ietf
no sh
frame intf dce
frame-relay route 101 interface s4/0 135
```

R1
```
conf t
int s4/0
no sh
enc frame ietf

int s4/0.123 multip
frame-relay interf 103 
frame-relay interf 102 
load-interval 30
exi
ip add 192.168.123.1 255.255.255.0

int lo0
ip add 1.1.1.1 255.255.255.255

router ospf 1
net 192.168.123.0 0.0.0.255 a 0
red con sub

ip ospf network point-to-m

```

R2
```
conf t
int s4/0
no sh
enc frame ietf

int s4/0.101 multip
frame-relay interf 101
load-interval 30
exi
ip add 192.168.123.2 255.255.255.0

int s4/1
no sh
enc frame-relay
ip add 192.168.24.2 255.255.255.0

frame-r intf-type dce
frame-r interf 24

int lo0
ip add 2.2.2.2 255.255.255.255

router ospf 1
net 192.168.123.0 0.0.0.255 a 0
net 192.168.24.0 0.0.0.255 a 0
red con sub

int s4/1
router ospf 1
nei 192.168.24.4

int 4/0.101
frame-relay map ip 192.168.123.3 101
```

R3
```
conf t
int s4/0
no sh
enc frame ietf

int s4/0.101 multip
frame-relay interf 101
load-interval 30
exi
ip add 192.168.123.3 255.255.255.0

int lo0
ip add 3.3.3.3 255.255.255.255

router ospf 1
net 192.168.123.0 0.0.0.255 a 0
red con sub

int 4/0.101
frame-relay map ip 192.168.123.2 101
```

R4
```
int s4/1
no sh
enc frame-relay
ip add 192.168.24.4 255.255.255.0

frame-r intf-type dte
frame-r interf 24

	router ospf 1

int lo0
ip add 4.4.4.4 255.255.255.255
```

