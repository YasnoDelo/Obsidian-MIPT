
| command                                                                                                                             | discription                                                                                                                                                                                                      |
| ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `serial 0/1/1.1` +  `multipoint`/`point-to-point`                                                                                   | Переключиться на интерфейс (сабинтерфейс).<br>`multipoint` - если на него забинжены несколько dcli, то есть hub-and-spoke архитектура с одной подсетью на весь сегмент [[Frame Relay]]. Иначе - `point-to-point` |
| `enc frame-r`                                                                                                                       | Включить инкапсуляцию. Если связаны устройства cisco и не cisco, то в конце можно дописать `ietf`                                                                                                                |
| `frame-relay interface-dlci` + dlci_num                                                                                             | Настроить на интерфейсе (или сабинтерфейсе номер DLCI)                                                                                                                                                           |
| `do sh frame pvc`                                                                                                                   | посмотреть инфу про статистику и FR                                                                                                                                                                              |
| `do sh frame map`                                                                                                                   | посмотреть инфу про подключения                                                                                                                                                                                  |
| `frame-relay map ip` + ip_num + dcli_num + `broadcast`<br>ex:<br>`frame-relay map ip 199.1.1.1 51 broadcast`                        | Настроить статический маршрут до ip_num через некоторую линку с dlci_num<br>Нужно, если выключен inverse-ARP, который по DLCI узнаёт IP                                                                          |
| `debug frame-relay lmi`                                                                                                             | Посмотреть информацию по соединению линка                                                                                                                                                                        |
|                                                                                                                                     |                                                                                                                                                                                                                  |
| `frame-rel switching`                                                                                                               | включить режим FR-switch                                                                                                                                                                                         |
| `frame intf` + `dte`/`dce`                                                                                                          | DTE - клиент, DCE - провайдер. в GNS3 в сторону тглупого FR-Switch'a нужно всегда ставить dte                                                                                                                    |
| `frame-relay route ` + dlci_in_num + `interface `+ int_out_name + dlci_out_num<br>ex:<br>`frame-relay route 135 interface s4/1 101` | Настройка маршрута на входном интерфейсе роутера, настроенного под FR-switch. <br><br>Причём int_name может быть и туннелем!                                                                                     |
|                                                                                                                                     |                                                                                                                                                                                                                  |
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
Важно! Чтобы [[OSPF setting|OSPF]] работал корректно, включать нужно на каждом multicast интерфейсе прописать настройку: `ip ospf network point-to multipoint`. Подробнее в запись об [[OSPF setting|OSPF]]