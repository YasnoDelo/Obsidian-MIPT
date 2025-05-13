![[Pasted image 20250310193850.png]]

SW1
![[Pasted image 20250310194455.png]]


FR SW 1
1 104 2 114
1 103 2 123
1 102 3 112

FR SW 2
1 101 3 112
1 104 2 124

FR SW 3
1 123 2 101
1 114 3 114

FR SW 4
3 114 2 101
1 124 2 101

![[Pasted image 20250310195406.png]]


R1
```
conf t
int se4/0
no sh

enc fr

int s4/0.104 point-to-point
frame-relay interface-dlci 104
exit
ip add 192.168.14.1 255.255.255.0
```

R2
```
conf t
int se4/0
no sh

enc fr

int s4/0.104 point-to-point
frame-relay interface-dlci 104
exit
ip add 192.168.24.2 255.255.255.0
```

R3
```
conf t
int se4/0
no sh

enc fr
```

R4
```
conf t
int se4/0
no sh

enc fr

int s4/0.102 point-to-point
frame-relay interface-dlci 102
exit
ip add 192.168.24.4 255.255.255.0

do sh frame pvc

int s4/0.101 point-to-point
frame-relay interface-dlci 101
exit
ip add 192.168.14.4 255.255.255.0
```