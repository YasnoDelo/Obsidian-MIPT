### R1
```
conf t

int s3/2
enc ppp
no sh
ip add 192.168.12.1 255.255.255.252

int s3/3
enc ppp
no sh
ip add 192.168.13.1 255.255.255.254

int s3/4
enc ppp
no sh
ip add 192.168.14.1 255.255.255.252

int s3/5
enc ppp
no sh
ip add 192.168.15.1 255.255.255.254
peer default ip address 192.168.15.0

PAP:
username Cisco2 password Pwd2
username Cisco3 password Pwd3
int s3/2
ppp authe pap

CHAP:
int s3/3
ppp authe chap
ppp chap hostn Cisco1
ppp chap password Pwd3

### Делаем Unnumbered
int lo0
ip add 1.1.1.1 255.255.255.255

int s3/2
ip unnumbered lo0

int s3/3
ip unnumbered lo0

int s3/4
ip unnumbered lo0

int s3/5
ip unnumbered lo0

### OSPF
router ospf 1
netw 192.168.12.0 0.0.0.3 a 0
netw 192.168.13.0 0.0.0.1 a 0
netw 192.168.14.0 0.0.0.3 a 0
netw 192.168.15.0 0.0.0.1 a 0

### Multilink

int multilink 1
enc ppp
ppp multilink group 1
ip add 192.168.21.1 255.255.255.252

int s3/2
ppp multilink group 1

int s3/0
enc ppp
ppp multilink group 1
no sh
```


R2
```
conf t

int s3/1
enc ppp
no sh
ip add 192.168.12.2 255.255.255.252

ppp pap sent Cisco2 pass Pwd2

### PPP Neighbour route
no peer neig 
do sh ip route
do clear ip route *
do sh ip route

router ospf 1
netw 192.168.12.0 0.0.0.3 a 0

int multilink 1
enc ppp
ppp multilink group 1
ip add 192.168.21.2 255.255.255.252

int s3/1
ppp multilink group 1

int s3/0
enc ppp
ppp multilink group 1
no sh
```

R3
```
conf t

int s3/1
enc ppp
no sh
ip add 192.168.13.0 255.255.255.254

ppp chap host Cisco3
ppp chap pass Pwd3

router ospf 1
netw 192.168.13.0 0.0.0.1 a 0

```

R4
```
conf t

int s3/1
enc ppp
no sh
ip add 192.168.41.1 255.255.255.252

router ospf 1
netw 192.168.14.0 0.0.0.3 a 0

```

R5
```
conf t

int s3/1
enc ppp
no sh
ip add neg

router ospf 1
netw 192.168.15.0 0.0.0.1 a 0
```