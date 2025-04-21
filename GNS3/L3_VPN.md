R1 PE
```
conf t

int f0/0
no sh 
ip add 10.0.12.1 255.255.255.0

router ospf 1
network 0.0.0.0 0.0.0.0 area 0

int l0
ip add 1.1.1.1 255.255.255.255

in Global
mpls ip
router ospf 1
mpls ldp auto

создаём VRF
vrf defin A
address-f ipv4
exit
rd 1:1
// 1 - номер роутера, 1 - номер клиента А
route-target both 1:1
//1 - номер клиента А
exit

vrf defin B
address-f ipv4
exit
rd 1:2
// 1 - номер роутера, 2 - номер клиента В
route-target both 2:2
// 2 - номер клиента В

int g1/0

vrf forwar A
ip add 10.0.14.1 255.255.255.0
no sh

router ospf 2 vrf A
net 0.0.0.0 0.0.0.0 a 0

// Поднимаем BGP между R1 и R3
router BGP 13
address-f vpnv4
exit
neigh 3.3.3.3 remote-as 13
neigh 3.3.3.3 update-source l0
// разрываем соседство в рамках ipv4
no bgp default ipv4-unicast

//поднимаем в vpnv4
address-family vpnv4 
neigh 3.3.3.3 send-comm both
neigh 3.3.3.3 ac

router bgp 13
address-f ipv4 vrf A
red ospf 2

do sh bgp vpnv4 uni all

// теперь добавляем bgp в ospf
router ospf 2
red bgp 13 sub

```
R2 P
```
conf t

int f0/0
no sh 
ip add 10.0.12.2 255.255.255.0

int g1/0
no sh 
ip add 10.0.23.2 255.255.255.0

int l0
ip add 2.2.2.2 255.255.255.255

in Global
mpls ip
router ospf 1
mpls ldp auto
```

R3 PE
```
conf t

int g1/0
no sh 
ip add 10.0.23.3 255.255.255.0

int l0
ip add 3.3.3.3 255.255.255.255

in Global
mpls ip
router ospf 1
mpls ldp auto

создаём VRF
vrf defin A
address-f ipv4
exit
rd 3:1
// 3 - номер роутера, 1 - номер клиента А
route-target both 1:1
//1 - номер клиента А

vrf defin B
address-f ipv4
exit
rd 3:2
// 3 - номер роутера, 2 - номер клиента В
route-target both 2:2
// 2 - номер клиента В

int g2/0

vrf forwar A
ip add 10.0.37.3 255.255.255.0
no sh

router ospf 2 vrf A
net 0.0.0.0 0.0.0.0 a 0

router BGP 13
address-f vpnv4
exit
neigh 1.1.1.1 remote-as 13
neigh 1.1.1.1 update-source l0

//теперь выключаем автоматически поднятое ipv4 соседство
address-family ipv4 unicast
neigh 1.1.1.1 sh

//поднимаем в vpnv4
address-family vpnv4 
neigh 1.1.1.1 ac
neigh 1.1.1.1 send-comm both

exit
no neighbor 1.1.1.1 shutdown

address-family ipv4
no neighbor 1.1.1.1 activate

exit
router bgp 13
address-f ipv4 vrf A
red ospf 2

do sh bgp vpnv4 uni all

// теперь добавляем bgp в ospf
router ospf 2
red bgp 13 sub

```

R4 CE
```
conf t
int g1/0
ip add 10.0.14.4 255.255.255.0
no sh

int l0
ip add 4.4.4.4 255.255.255.255

router ospf 2
net 0.0.0.0 0.0.0.0 a 0
```

R7 CE
```
conf t
int g2/0
ip add 10.0.37.7 255.255.255.0
no sh

int l0
ip add 7.7.7.7 255.255.255.255

// Поднимаем между CE и PE
router ospf 2
net 0.0.0.0 0.0.0.0 a 0
```