
| command                            | discription                                         |
| ---------------------------------- | --------------------------------------------------- |
| `do show ip slb reals`             | Посмотреть реальные сервера, соединённые по SLB     |
| `do show ip slb vservers`          | Посмотреть информацию про то, как нас видят клиенты |
| `do show ip slb serverfarm detail` | Посмотреть дополнительные данные по серверам        |

### L3:

| command                                         | discription                                                                                                                   |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `ip slb serverfarm` + serv_farm_name            | создать набор серверов                                                                                                        |
| `nat server`                                    | сделать так, чтобы IP подменялся на виртуальный                                                                               |
| `real` + ip_num + port_num                      | инициализируем сервер и порт, который нужно будет обслуживать (один сервер может добавляться несколько раз с разными портами) |
| `maxconns` + num                                | заявить максимальную загрузку сервера                                                                                         |
| `weight` + num                                  | заявить, как много нагрузки помещать на сервере за один круг round-robin                                                      |
| `inservice`                                     | добавляем сервер в набор                                                                                                      |
|                                                 |                                                                                                                               |
| `ip slb vserver` virt_serv_name                 | создать виртуальный сервер                                                                                                    |
| `serverfarm` + serv_farm_name                   | инициализировать в виртуальном сервере набор из серверов                                                                      |
| `virtual` + virt_ip_num + `tcp`/`udp` +port_num | привязка виртуального ip и типа соединения к виртуальному серверу                                                             |
| `inservice`                                     | добавляем набор серверов в вирутальный сервер                                                                                 |
```
ip slb serverfarm sf1
nat server
real 192.168.1.2 23 -- заходим в сервер R2, 23 - это порт телнет
inservice -- добавить сервис в ферму
ip slb serverfarm sf1
real 192.168.1.3 23
inservice
exit

ip slb vserver SF1
serverfarm sf1
virtual 1.1.1.1 tcp 23
inservice
exit
```

### L2:
R1
```
ip slb serverfarm SF2
real 192.168.1.5
inservice
real 192.168.1.6
inservice

ip slb vserver VS1
virtual 1.1.1.1 tcp telnet
no inservice - пока перенастраиваем лучше выключить
serverfarm SF2
inservice
```

На серверах:
```
int lo0
ip add 1.1.1.1 255.255.255.255
```
