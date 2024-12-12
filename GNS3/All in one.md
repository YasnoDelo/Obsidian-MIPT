In enable mode:
1) ```show hosts```
2) ```telnet name```
3) ```show ip int brief``` 

In conf_t mode:
1) ```interface fa1/0/7```
2) ```no shutdown```
3) ```show cdp neigh```

## Many Routers
#### R1 (usual)
```
conf t
int E2/0
ip add 192.168.0.1 255.255.255.0
no sh
```

#### R3 (+ telnet)
```
conf t
int E2/0
ip add 192.168.0.3 255.255.255.0
no sh

line vty 0 1869
login local
  
username usr secret pwd
username cisco secret cisco
enable secret cisco
```
 
### Настройка [[Telnet setting|Telnet]]
```
line vty 0 1869
login local
```
In [[Global config mode]] (not in config-line)
```
username usr secret pwd
username cisco secret cisco     //-инициализация пользователя
enable secret cisco             //-разрешения входа в привелегированный режим
```

### Настройка [[VLAN setting|VLAN]]
```
conf t
int fa0/0
no sh

int fa0/0.20
enc dot 20
ip add 192.168.20.1 255.255.255.0

int fa0/0.13
enc dot 13 nat
ip add 192.168.13.1 255.255.255.0
```

| Команда                             | Описание                                              |
| ----------------------------------- | ----------------------------------------------------- |
| `int fa0/0.13`                      | Переходим на виртуальный интерфейс                    |
| `enc dot 20`                        | Инкапсулируем в dot1q (т. е. превращаем в trunk)      |
| `enc dot 13 nat`                    | Инкапсулируем в dot1q и говорим, что native VLAN = 13 |
| `ip add 192.168.20.1 255.255.255.0` | Добавляем виртуальному интерфейсу ip-адресс           |
|                                     |                                                       |
### Настройка Роутера как хоста
```
conf t
int fa0/0
no sh

int fa0/0.20
ip add 192.168.20.2 255.255.255.0
ip route 0.0.0.0 0.0.0.0 192.168.20.1

```

### [[DHCP setting|DHCP]]
На сервере:
```
conf t
int fa0/0
ip add 192.168.0.1 255.255.255.0
no sh

ip dhcp pool Name
netw 192.168.0.0 /24
default-router 192.168.0.1
lease N N N

ip dhcp excl 192.168.0.1 192.168.0.15

```
На клиенте:
```
ip add dhcp
```

| Команда                                                                                                 | Описание                                                            |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `ip dhcp pool` + Name                                                                                   | Инициализируем пул                                                  |
| `netw 192.168.1.0 /24`                                                                                  | Задаём доступные адресса                                            |
| `default-router 192.168.0.1`                                                                            | Дефолт гейтвей                                                      |
| `lease N N N`                                                                                           | Настройка времени аренды                                            |
| `ip dhcp excl 192.168.0.1 192.168.0.15`                                                                 | Исключить адреса                                                    |
| `ip route` + адресс сети + маска сети + default gateway + индекс приоритетности (меньше - приоритетнее) | Настроить default gateway                                           |
| `ip route 0.0.0.0 0.0.0.0 192.168.20.1`                                                                 | Настроить так, чтобы все запросы перенаправлялись на `192.168.20.1` |

### [[Access Control List|ACL]] basic (составляем таблицу)
```
ip access-list standart 1
permit/deny + sourse_IP

int + int_name
ip access-group 1 out
```

### [[Access Control List|ACL]] extended (составляем таблицу)
```
ip access-list extended 100
permit/deny + TEG + sourse_IP + destination_IP + wildcard
exit

int + int_name
ip access-group 1 out
```
	
### Создание виртуальных соседей
```
int lo0
ip add 192.168.20.2 255.255.255.0
```


### [[IPv6 setting|IPv6]]

| Comand                                    | Description                                                                                                |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `ipv6 enable`                             | Запустить функции IPv6. На интерфейсе сразу выдаётся link local address. ==Не забыть включить интерфейс!== |
| `do sh ipv6 int br`                       | Показать краткую инфу про интерфейсы                                                                       |
| `do sh ipv6 route`                        | Показать таблицу маршрутизации                                                                             |
| `ipv6 unicast-routing`                    | Из [[Global config mode]] запускает маршрутизацию (по умолчанию машина - хост)                             |
| `ipv6 cef`                                | cef = Cisco Express Forvarding                                                                             |
| `ipv6 address fe80::2 link-local`         | Задаём локальный адресс                                                                                    |
| `ipv6 address` + prefix + mask + `eui-64` | Настроить адресс по EUI-64                                                                                 |
|                                           |                                                                                                            |
|                                           |                                                                                                            |
### DHCP IPv6
```
ipv6 dhcp pool Name
address prefix 2001:234::/64
dns-server 2001:234::1
domain-name cisco.com

##Далее на интерфейсе
ipv6 nd managed-config-flag
ipv6 nd other-config-flag
```
На клиенте:
```
ipv6 add dhcp
```
или для stateless dhcp:
```
ipv6 add autoconfig
```

| Команда                         | Описание                                             |
| ------------------------------- | ---------------------------------------------------- |
| `ipv4 dhcp pool` + Name         | Инициализируем пул                                   |
| `address prefix 2001:234:0 /64` | Настройка подсети, в которой работает сервер         |
| `ipv6 nd managed-config-flag`   | Поднять флаг о передаче адреса клиену (для stateful) |
| `ipv6 nd other-config-flag`     | Поднять флаг о передачи всей информации кроме адреса |



R4
```
conf t

ipv6 unicast-routing
int f0/0
ipv6 address 2001:14::4/64
no sh

do sh ipv6 int br 

ipv6 route ::/0 2001:14::1
```

R1
```
conf t
ipv6 unicast-routing

int f0/0
ipv6 address 2001:14::1/64
no sh


int f4/0
ipv6 address 2001:12::1/64
no sh

int g1/0
ipv6 address 2001:13::1/64
no sh
do sh ipv6 int br 

ipv6 route 2001:23::/64 2001:13::3
ipv6 route 2001:25::/64 2001:13::3
```

R2
```
conf t
ipv6 unicast-routing

int f0/0
ipv6 address 2001:25::2/64
no sh


int f4/0
ipv6 address 2001:12::2/64
no sh

int g1/0
ipv6 address 2001:23::2/64
no sh
do sh ipv6 int br 

ipv6 route 2001:13::/64 2001:13::3
ipv6 route 2001:14::/64 2001:13::3
```

R3
```
conf t
int g5/0
ipv6 address 2001:23::3/64
no sh

int g1/0
ipv6 address 2001:13::3/64
no sh
do sh ipv6 int br 

ipv6 route 2001:14::/64 2001:13::1
ipv6 route 2001:25::/64 2001:23::2
ipv6 route 2001:12::/64 2001:13::1
```

R5
```
conf t

ipv6 unicast-routing
int f0/0
ipv6 address 2001:15::5/64
no sh

do sh ipv6 int br 
ipv6 route ::/0 2001:25::2
```

### [[NAT,PAT settings|NAT/PAT]]

#### R1
```
ip access-list extended 100
permit ip 192.168.134.0 0.0.0.255 any
int g1/0
ip nat inside

int f0/0
ip nat outside

// Далее в priveleged mode
ip nat inside source list 100 interface f0/0 overload
do sh ip nat tra
do sh ip nat stat
```


| ПО ЧАСТЯМ         | ЗАЧЕМ                                             |
| ----------------- | ------------------------------------------------- |
| `ip nat`          | командуем для nat                                 |
| `inside`          | говорим, что начинаем разбирать логику трансляции |
| `source list 100` | Sourse, который проходит правила ACL 100          |
| `interface f0/0`  | Sourse выше заменяется на IP на интерфейсе `f0/0` |
| `overload`        | Указание, чтобы использовалось PAT                |

## PAT+NAT
```
\\ in global config
\\ инициализировали пул
ip nat pool CiscoPool 10.0.0.1 10.0.0.10 netmask 255.0.0.0
ip nat inside source list 100 pool CiscoPool overload
```

## NAT
Настраивается как PAT+NAT, но без ==overload==

### [[Tunnel setting]]

| Comand                            | Description                                            |
| --------------------------------- | ------------------------------------------------------ |
| `int tun0`                        | поднимаем интерфейс для туннеля                        |
| `tunnel mode` + mode_name         | Настраиваем туннель                                    |
| `tunnel mode gre ip`              | Настраиваем туннель IP через GRE                       |
| `tunnel source e2/3`              | Отправитель через физический интерфейс (плохой дизайн) |
| `tunnel destination 192.168.45.5` | Получатель через IP                                    |
| `keepalive`                       | Мониторинг состояния туннеля                           |
|                                   |                                                        |

```
int tun0
ip add 192.168.25.2 255.255.255.0  // логический адрес туннеля
tunnel mode gre ip
tunnel source Ethernet2/3
tunnel destination 192.168.45.5    // адрес физического интерфейса
keepalive
```

### [[OSPF setting]]

| Command                                  | Description                                            |
| ---------------------------------------- | ------------------------------------------------------ |
| `router ospf 1`                          | инициализируем процесс 1. каждый процесс - одно дерево |
| `router-id 3.3.3.3`                      | Ставим ID на роутере                                   |
| `network 0.0.0.0 255.255.255.255 area 0` | Ставим сети, участвующие в OSPF. Маска wildcart        |
| `sh ip ospf data`                        | Показать всю информацию по OSPF                        |
| `clear ip ospf process`                  | Очистить таблицу маршрутизации                         |


```
++++R2

router ospf 1
network 192.168.23.0 0.0.0.255 area 0
passive-int e2/1

  

++++R3

router ospf 1
network 0.0.0.0 255.255.255.255 area 0
router-id 3.3.3.3

  

++++R4

router ospf 1
network 0.0.0.0 255.255.255.255 area 0
int lo0
ip add 4.4.4.4 255.255.255.255
int lo1
ip add 44.44.44.44 255.255.255.255

  

++++R5

router ospf 1
network 192.168.45.0 0.0.0.255 area 0
```
