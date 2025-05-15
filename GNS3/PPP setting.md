R1- host, R2 - client


| command                         | description                                                                                                                          |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `ppp authe` + `chap`/`pap`      | Метод аутентификации - либо просто по паролю (pap), либо без передачи пароля по линии (по заранее известному паролю - chap)          |
| `username Cisco3 password Pwd3` | создать юзера с именем Cisco3, который сможет подключиться по паролю PWD3                                                            |
| `ppp chap hostn Cisco1`         | назвать себя `Cisco1`                                                                                                                |
| `ppp chap password Pwd3`        | задать пароль                                                                                                                        |
| `ppp pap sent Cisco2 pass Pwd2` | отправить сообщение по `pap`                                                                                                         |
| `interface multilink` + number  | Creates a multilink interface and moves the user to interface<br>configuration mode that that interface                              |
| `ppp multilink`                 | Interface subcommand that enables MLPPP features                                                                                     |
| `ppp multilink group` + number  | Interface subcommand that associates the interface with a<br>particular multilink interface and multilink group                      |
| `show ppp multilink`            | Lists detailed status information about each of the PPP<br>multilink groups configured on the router                                 |
| `show ppp all`                  | Lists one line of status information per PPP link on the router,<br>including the control protocol status and peer router IP address |
| `debug ppp authentication`      | Generates messages for each step in the PAP or CHAP<br>authentication process                                                        |
| `debug ppp negotiation`         | Generates debug messages for the LCP and NCP negotiation<br>messages sent between the devices                                        |


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