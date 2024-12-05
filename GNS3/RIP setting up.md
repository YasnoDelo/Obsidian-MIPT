
| Команда                  | Значение                                                                        |
| ------------------------ | ------------------------------------------------------------------------------- |
| `router rip`             | Зайти в настройки RIP                                                           |
| `version 2`              | Установить версию RIP (по умолчанию 1, которая работает с классами)             |
| `no auto-summary`        | Отключить автосуммаризацию                                                      |
| `network` + subnet_num   | interface in this subnet recives and sends RIP-requests                         |
| `redistribute connected` | отсылает directly connected подсети (но не слушает и ничего по ней не передаёт) |
| `passive-int` + int_name | Не отправляем и не слушаем int_name                                             |


R1

```
conf t
int e2/2
ip add 192.168.12.1 255.255.255.0
no sh


int f0/0
ip add 192.168.1.1 255.255.255.0
no sh

router rip
version 2
no auto-summary
network 192.168.12.0

redistribute connected
```

network 192.168.12.0
network 192.168.13.0

R2

```
conf t
int e2/3
ip add 192.168.23.2 255.255.255.0
no sh


int e2/1
ip add 192.168.12.2 255.255.255.0
no sh

router rip
version 2
no auto-summary
network 192.168.23.0
network 192.168.12.0
```

R3

```
conf t
int e2/1
ip add 192.168.13.3 255.255.255.0
no sh


int f0/
ip add 192.168.3.1 255.255.255.0
no sh

router rip
version 2
no auto-summary
network 192.168.23.0
redistribute connected

```

router rip
ver 2
netw 0.0.0.0


### Редистрибьюция
Несколько видов маршрутов: (Directly)Connected, Static, Protocols(RIP, OSPF)
И по RIP можно отправлять даже иначе (не по RIP) полученные подсети 
