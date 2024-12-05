
| Comand                           | Descripsion                                  |
| -------------------------------- | -------------------------------------------- |
| `switchport`                     | Сконфигурировать интерфейс под L2            |
| `no switchport`                  | Сконфигурировать интерфейс под L3            |
| `switchport mode` + access/trunk | Настроить интерфейс по функции               |
| `vlan` + num                     | Создать VLAN                                 |
| `no vlan` + num                  | Удалить VLAN                                 |
| `show vlan`                      | Показать, какие порты к каким VLAN относятся |

### Like L2

| Comand                       | Descripsion                          |
| ---------------------------- | ------------------------------------ |
| `switchport access vlan 230` | Назначили интерфейсу конкретный VLAN |


### Like L3
| Comand                 | Descripsion                                                               |
| ---------------------- | ------------------------------------------------------------------------- |
| `interface vlan` + num | Зайти в настройку VLAN (после нужно настраивать как базовый subinterface) |
|                        |                                                                           |

## Cisco 3725
| Comand                              | Description                            |
| ----------------------------------- | -------------------------------------- |
| `sh spann`                          | Показать инфо про STP                  |
| `spanning-tree vlan 1 priority` + N | Поставить приоритет, равный N          |
| `spanning-tree vlan 1 root primary` | Сделать rootом                         |
| `spann port-priority` + N           | В интерфейсе выставить приоритет порта |
| `spann cost` + N                    | В интерфейсе выставить cost порта      |
|                                     |                                        |