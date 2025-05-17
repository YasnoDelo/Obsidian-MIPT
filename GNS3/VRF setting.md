
| command                        | discription                                  |
| ------------------------------ | -------------------------------------------- |
| `do show ip vrf`               | показать инфу про VRF                        |
| `ip vrf` + vrf_name            | создать VRF                                  |
| `description` + text           | добавить описание                            |
|                                |                                              |
| `ip vrf forwarding` + vrf_name | определить интерфейс (или сабинтефейс) в VRF |
| `router ospf 1 vrf` + vrf_name | Запустить OSPF в VRF                         |

R1
```
ip vrf Cust1
description Customer 1 with OSPF
ip vrf Cust2
description Customer 2 with statics

int g2/0
ip vrf forwarding Cust1 -- если настраиваем врф после настройки адреса, то его
надо перенастроить
ip address 192.168.12.1 255.255.255.0
no sh

router ospf 1 vrf Cust1
net 192.168.12.0 0.0.0.255 area 0
red con sub
```