R1- host, R2 - client
#### CHAP setting:
R1:
```
username Cisco3 password Pwd3
int s3/3
enc ppp
no sh
ip add 192.168.13.1 255.255.255.254

ppp authe chap
ppp chap hostn Cisco1
ppp chap password Pwd3
```

R2:
```
conf t

int s3/1
enc ppp
no sh
ip add 192.168.13.0 255.255.255.254

ppp chap host Cisco3
ppp chap pass Pwd3
```
#### PAP setting
R1:
```
username Cisco2 password Pwd2
int s3/2
enc ppp
no sh
ip add 192.168.12.1 255.255.255.252
ppp authe pap
```
R2:
```
conf t

int s3/1
enc ppp
no sh
ip add 192.168.12.2 255.255.255.252

ppp pap sent Cisco2 pass Pwd2
```
#### Different networks
Разные подсети успешно подключаются:
R1:
```
int s3/4
enc ppp
no sh
ip add 192.168.14.1 255.255.255.252
```
R2:
```
conf t

int s3/1
enc ppp
no sh
ip add 192.168.41.1 255.255.255.252
```
#### Address assignment
R1:
```
int s3/5
enc ppp
no sh
ip add 192.168.15.1 255.255.255.254
peer default ip address 192.168.15.0
```
R2:
```
conf t

int s3/1
enc ppp
no sh
ip add negotiated
```
#### MLPPP
Как LAG, то есть повторное соединение
R1:
```
##Создаём новый логический интерфейс, с которого будем общаться
int multilink 1
enc ppp
ppp multilink group 1
ip add 192.168.21.1 255.255.255.252

int s3/1
enc ppp
ppp multilink group 1
no sh

int s3/0
enc ppp
ppp multilink group 1
no sh
```

R2
```
##Создаём новый логический интерфейс, с которого будем общаться
int multilink 1
enc ppp
ppp multilink group 1
ip add 192.168.21.2 255.255.255.252

int s3/1
enc ppp
ppp multilink group 1
no sh

int s3/0
enc ppp
ppp multilink group 1
no sh
```
#### PPP unnumbered
Создаём loopback и назначаем все интерфейсы на него (то есть с этого адреса будут слаться пакеты)
R1:
```
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
```
#### PPP neighbour route
Позволяет очистить таблицу маршрутизации, чтобы не было видно соседей. Лучше не делать, если подключён сосед из известной подсети, ведь иначе не сможет пройти ping.
```
no peer neig 
do sh ip route
do clear ip route *
do sh ip route
```