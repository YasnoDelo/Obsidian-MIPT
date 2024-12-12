

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